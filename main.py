# PYTHON 3.x
import itertools
CONF_FNAME  = "conf.txt"
CONF_COMMENT_PREFIX = "#"
CONF_CORES      , N_CORES       = "cores",      4
CONF_WBASE      , WBASE         = "wbase",      20
CONF_WINACTIVE  , WINACTIVE     = "winactivo",  1.2 
CONF_C          , C             = "c",          2.5
CONF_N_PSTATES  , N_PSTATES     = "pstates",    6
CONF_P_VOLTAGES , P_VOLTAGES    = "voltages",   [1.056, 1.080, 1.104, 1.16, 1.224, 1.28] # V
CONF_P_FREQS    , P_FREQS       = "freqs",      [1.776, 1.888, 2.004, 2.338, 2.672, 3.006] # GHz
CONF_SEQ_TIME   , SEQ_TIME      = "seq_time",   2300 # seconds
CONF_N_PARALEL  , N_PARALEL     = "grado_paralelizacion",   4
CONF_WORK_DISTR , WORK_DISTR    = "division_trabajo",       [15, 25, 25, 35]

def MAX_VOLTAGE():
    return P_VOLTAGES[N_PSTATES-1]

def MIN_VOLTAGE():
    return P_VOLTAGES[0]

def MAX_FREQ():
    return P_FREQS[N_PSTATES-1]

def MIN_FREQ():
    return P_FREQS[0]

def dynamic_energy(voltage, freq):
    return C * pow(voltage, 2) * freq

# PARSE CONFIG FILE
try:
    file = open("conf.txt")
except Exception:
    pass
else:
    for line in file:
        line = line.strip()
        if line.startswith("#") or line == "":
            continue 
        temp = line.split("=")
        if len(temp) > 2:
            raise Exception("Error while parsing: multiple '=' symbols")
        attribute, value = temp
        attribute = attribute.strip()
        if attribute == CONF_CORES:
            N_CORES = int(value)
        elif attribute == CONF_WBASE:
            WBASE = float(value)
        elif attribute == CONF_WINACTIVE:
            WINACTIVE = float(value)
        elif attribute == CONF_C:
            C = float(value)
        elif attribute == CONF_N_PSTATES:
            N_PSTATES = int(value)
        elif attribute == CONF_P_VOLTAGES:
            P_VOLTAGES = list(map(float,value.split(";")))
        elif attribute == CONF_P_FREQS:
            P_FREQS = list(map(float,value.split(";")))
        elif attribute == CONF_SEQ_TIME:
            SEQ_TIME = int(value)
        elif attribute == CONF_N_PARALEL:
            N_PARALEL = int(value)
        elif attribute == CONF_WORK_DISTR:
            WORK_DISTR = list(map(int,value.split(";")))

# CHECK
if sum(WORK_DISTR) != 100:
    raise ValueError("The sum of WORK_DISTR is not equal to 100%")

if N_PARALEL > N_CORES:
    raise ValueError("N_PARALEL > N_CORES")

# BEGIN
for combination in itertools.product(range(N_PSTATES), repeat=N_PARALEL):
    pstates = list(combination)
    for pstate_number in range(len(pstates)):
        print("P{} ".format(pstates[pstate_number]), end="")
    print(" :", end="")
    cores = [0.0] * N_CORES # for storing consumption for each core
    active_times = [0] * N_PARALEL
    total_sum = 0.0
    
    for i in range(N_PARALEL):
        active_times[i] = int(SEQ_TIME * WORK_DISTR[i]/100.0 \
                                * MAX_FREQ() / P_FREQS[pstates[i]])

    MAX_TIME = max(active_times)
    
    for i in range(N_PARALEL):
        active_time = active_times[i]/3600.0 # in hours
        print ("{:>6.0f}".format(active_times[i]), end="")
        # active energy
        cores[i] = dynamic_energy(P_VOLTAGES[pstates[i]], P_FREQS[pstates[i]]) \
                    * active_time 

        # inactive energy
        cores[i] += WINACTIVE * (MAX_TIME/3600.0 - active_time)

    # inactive energy for idle cores
    for i in range(N_PARALEL, N_CORES):
        cores[i] += WINACTIVE * MAX_TIME/3600.0

    total_sum = sum(cores) + WBASE * MAX_TIME/3600.0 # + static energy

    print ("  tmax = {:>5.0f}".format(MAX_TIME), end="")
    # for i in range(N_CORES):
    #    print ("CORE #{} {:>8.3f} Wh".format(i, cores[i]))
    print ("  Energia= {:.6f} KWh".format(total_sum/1000.0))
    
