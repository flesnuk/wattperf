
CONF_FNAME  = "conf.txt"
CONF_COMMENT_PREFIX = "#"
CONF_CORES      , N_CORES       = "cores",      4
CONF_WBASE      , WBASE         = "wbase",      1.2
CONF_STATIC_ENER, STATIC_ENER   = "static",     10 
CONF_C          , C             = "c",          2.5
CONF_N_PSTATES  , N_PSTATES     = "pstates",    7
CONF_P_VOLTAGES , P_VOLTAGES    = "voltages",   [1.056, 1.080, 1.104, 1.16, 1.224, 1.28, 1.5] # V
CONF_P_FREQS    , P_FREQS       = "freqs",      [1.776, 1.888, 2.004, 2.338, 2.672, 3.006, 4.5] # GHz
CONF_SEQ_TIME   , SEQ_TIME      = "seq_time",   3600 # seconds
CONF_N_PARALEL  , N_PARALEL     = "grado_paralelizacion",   3
CONF_WORK_DISTR , WORK_DISTR    = "division_trabajo",       [50, 30, 20]

def MAX_VOLTAGE():
    return P_VOLTAGES[N_PSTATES-1]

def MIN_VOLTAGE():
    return P_VOLTAGES[0]

def MAX_FREQ():
    return P_FREQS[N_PSTATES-1]

def MIN_FREQ():
    return P_FREQS[0]

cores = [0.0] * N_CORES # for storing consumption for each core

def dynamic_energy(c, voltage, freq):
    return c * pow(voltage, 2) * freq

# PARSE CONFIG FILE
def parse_cores():
    pass

# CHECK
if sum(WORK_DISTR) != 100:
    raise ValueError("The sum of WORK_DISTR is not equal to 100%")

if N_PARALEL > N_CORES:
    raise ValueError("N_PARALEL > N_CORES")

# BEGIN
MAX_WORK = max(WORK_DISTR)
MAX_TIME = MAX_WORK/100 * SEQ_TIME
for i in range(N_PARALEL):
    # active energy
    cores[i] = dynamic_energy(C, MAX_VOLTAGE(), MAX_FREQ()) \
                * SEQ_TIME/3600 \
                * WORK_DISTR[i]/100 

    # inactive energy
    cores[i] += WBASE \
                * SEQ_TIME/3600 \
                * (1 - WORK_DISTR[i]/100)

    # static energy
    cores[i] += STATIC_ENER * MAX_TIME/3600

# inactive energy for idle core
for i in range(N_PARALEL, N_CORES):
    cores[i] += (STATIC_ENER + WBASE) \
                * MAX_TIME/3600

print (MAX_TIME)
print (cores)
print ("sum " + str(sum(cores)))