# __author__ = 'Hybrid'

#
# Hybrid Calibration Waveform
#
# 2020/03/03
#


HSDIO = experiment.LabView.HSDIO.add_transition
AO = experiment.LabView.AnalogOutput.add_transition
label = experiment.functional_waveforms_graph.label
add_repeat = experiment.LabView.HSDIO.add_repeat


def pulse(t, duration, channel):
    HSDIO(t, channel, True)
    t += duration
    HSDIO(t, channel, False)
    return t


def ramp(t1, duration, v1, v2, channel,dt = 0.001):
    t2 = t1 + duration
    times = arange(t1, t1 + duration, dt)
    voltages = linspace(v1, v2, len(times))
    for t, v in zip(times, voltages):
        AO(t, channel, v)
    return t2


# RF Switches ------------------------------------------------------------------
ryd685_timing = 600e-6
ryd595_timing = 900e-6

D2_switch = lambda t, state: HSDIO(t, 19, not (state))
#D2_switch = lambda t, state: HSDIO(t, 19, 0)  # not (state))
HF_switch = lambda t, state: HSDIO(t, 18, not (state))
# HF_switch = lambda t, state: HSDIO(t, 18, 1)
vODT_switch = lambda t, state: HSDIO(t, 20, not (state))
#vODT_switch = lambda t, state: HSDIO(t, 20, 0)
Ryd685_switch = lambda t, state: HSDIO(t, 22, state)
Ryd595_switch = lambda t, state: HSDIO(t, 21, state)
chop = lambda t, state: HSDIO(t, 24, state)
uW_switch = lambda t, state: HSDIO(t, 0, not (state))
OP_switch = lambda t, state: HSDIO(t, 23, state)

# Instrument Triggers ----------------------------------------------------------

NIScope_Trig = lambda t, state: HSDIO(t, 2, state)  #Not Set!
Zstage_Trig = lambda t, state: HSDIO(t, 2, state)  #Not Set!
MOT_Andor_Trig = lambda t, state: HSDIO(t, 15, state)
NIDAQ_Trig = lambda t, state: HSDIO(t, 14, state)
Hamamatsu_Trig = lambda t, state: HSDIO(t, 2,state)
MOT_coils_switch = lambda t, state: HSDIO(t, 17, not (state))
SPCM_gate = lambda t, state: HSDIO(t, 26, state)
OP_DDS = lambda t, state: HSDIO(t, 27,state)
Aerotech_z_trig = lambda t, state: HSDIO(t, 28, state)
AO_start_trig = lambda t, state: HSDIO(t, 30,state)
timing_trig = lambda t, state: HSDIO(t, 29, state)

# Shutter Switches -------------------------------------------------------------
XZ_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 25, not state)
# XZ_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 25, state*0)
Y_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 11, state)
# Y_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 11, state*0+1)
Y2_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 8, state)
# Y2_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 8, 1)
X_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 13, not (state))
# X_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 13, 0)
RP_Shutter_switch_init = lambda t, state: HSDIO(t, 7,state)
# RP_Shutter_switch_init = lambda t, state: HSDIO(t, 7,1)
Cooling_Shutter_switch_init = lambda t, state: HSDIO(t, 12, not(state))
# Cooling_Shutter_switch_init = lambda t, state: HSDIO(t, 12, 0)
OP_Shutter_switch_init = lambda t, state: HSDIO(t, 10, not(not(state)))
# OP_Shutter_switch_init = lambda t, state: HSDIO(t, 10, 1)
OP_RP_Shutter_switch_init = lambda t, state: HSDIO(t, 6, state)
# OP_RP_Shutter_switch_init = lambda t, state: HSDIO(t, 6, 1)
Blowaway_Shutter_switch_init = lambda t, state: HSDIO(t, 2, state)  #Not Set!
Ryd595_Shutter_switch_init = lambda t, state: HSDIO(t, 2, not (state))  #Not Set!
Collection_Shutter_switch_init = lambda t, state: HSDIO(t, 5, state)
# Collection_Shutter_switch_init = lambda t, state: HSDIO(t, 5, 1)

if ShuttersOn:
    XZ_Only_Shutter_switch = XZ_Only_Shutter_switch_init  # Shutter on Z1 Chip Imaging Beam. Used to be HF Shutter
    Y_Only_Shutter_switch = Y_Only_Shutter_switch_init  # Shutter on Z1 Chip Imaging Beam. Used to be HF Shutter
    Y2_Only_Shutter_switch = Y2_Only_Shutter_switch_init  # Shutter on Z1 Chip Imaging Beam. Used to be HF Shutter
    X_Only_Shutter_switch = X_Only_Shutter_switch_init
    RP_Shutter_switch = RP_Shutter_switch_init  # Shutter in Repumper
    Cooling_Shutter_switch = Cooling_Shutter_switch_init  # Shutter in Cooling Laser
    OP_Shutter_switch = OP_Shutter_switch_init  # Shutter in Optical Pumping beam
    OP_RP_Shutter_switch = OP_RP_Shutter_switch_init  # Shutter in Optical Pumping Repumper beam
    Blowaway_Shutter_switch = Blowaway_Shutter_switch_init
    Ryd595_Shutter_switch = Ryd595_Shutter_switch_init
    Collection_Shutter_switch = Collection_Shutter_switch_init
else:
    XZ_Only_Shutter_switch = lambda t, state: 0
    Y_Only_Shutter_switch = lambda t, state: 0
    Y2_Only_Shutter_switch = lambda t, state: 0
    X_Only_Shutter_switch = lambda t, state: 0
    RP_Shutter_switch = lambda t, state: 0
    Cooling_Shutter_switch = lambda t, state: 0
    OP_Shutter_switch = lambda t, state: 0
    OP_RP_Shutter_switch = lambda t, state: 0
    Blowaway_Shutter_switch = lambda t, state: 0
    Ryd595_Shutter_switch = lambda t, state: 0
    Collection_Shutter_switch = lambda t, state: 0

RP_Shutter_delay_off = 3.1
RP_Shutter_delay_on = .8
Cooling_Shutter_delay_on = 4
Cooling_Shutter_delay_off = 2.8
OP_Shutter_delay_on = 5.20
OP_Shutter_delay_off = 1.80
OP_RP_Shutter_delay_on = 5.1
OP_RP_Shutter_delay_off = 1.8

XZ_Shutter_delay_off = 6.7
XZ_Shutter_delay_on = 0

Z1_Shutter_delay_on = 9.2
Z1_Shutter_delay_off = 5
Y1_Shutter_delay_on = 6.3
Y1_Shutter_delay_off = 3.75
Y2_Shutter_delay_on = 2.8
Y2_Shutter_delay_off = 7
X_Shutter_delay_on = 8.1
X_Shutter_delay_off = 8.1

Ryd595_Shutter_delay_on = 0.85
Ryd595_Shutter_delay_off = 3.45

Collection_Shutter_delay_on = 5
Collection_Shutter_delay_off = 0

BA_Shutter_delay_on = 2.4
BA_Shutter_delay_off = 1.9


###AO Controls###

MOT_coilsAO = lambda t, v: AO(t, 0, v)
HF_amplitude = lambda t, v: AO(t, 3, v)
# HF_amplitude = lambda t, v: AO(t, 3, 2.6)
vODT_power = lambda t, v: AO(t, 2, v)

def FORT_cal(p):
    """
    uses FORT calibration parameters to return voltage to FORT VVA that results in
    desired FORT output power (as a fraction of max power)
    Args:
        p: desired FORT output power as a fraction of max power

    Returns:
        v_set: VVA set voltage that results in desired p
    """
    a = 7.62e-2
    b = 5.56e-3
    vt = 1.79

    v_set = vt+1/(2*b)*(-a+sqrt(a**2+4*b*p))
    return v_set

FORT_power = lambda t, p: vODT_power(t, FORT_cal(p))

def biasAO(t, shims):
    '''
    Takes in a time and a 3-element list of shim voltages (x,y,z)
    Holds level until next control
    '''

    AO(t, 4, shims[0])
    AO(t, 5, shims[1])
    AO(t, 6, shims[2])

    # correct for a finite switching time
    t += 2+2
    return t

###SPCM Clocks on succsessive rising edges###

SPCM_clock = lambda t, state: HSDIO(t, 24, state)

def D2_DDS(t, stage):
    '''
    Takes in a time and stage and sets the HSDIO channels accordingly.
    Will eventually incorporate Gray Coding.
    Holds level until next control.
    '''
    stage_dict = {'MOT': (0, 0, 0), 'PGC1': (0, 0, 1), 'PGC2': (0, 1, 1),
                  'LAC': (0, 1, 0), 'Recool': (1, 1, 0), 'RO': (1, 0, 0),
                  'BA': (1, 0, 1), 'NA': (1, 1, 1)}
    # print("Setting DDS to state {} = {}. At t = {}".format(stage,stage_dict[stage],t))  # Use to Debug Grey Coding
    set = stage_dict[stage]
    HSDIO(t, 1, set[2])  # DDS bit 0
    HSDIO(t, 3, set[1])  # DDS bit 1
    HSDIO(t, 4, set[0])  # DDS bit 2

    return t

def FORT_DDS(t, stage):
    stage_dict = {'FORTLoading': (0,0), 'FORTLAC': (0,1), 'FORTRO': (1,1)}
    set = stage_dict[stage]

    HSDIO(t, 16, set[0]) #DDS bit 0
    HSDIO(t, 31, set[1]) #DDS bit 1

    return t

def MOTAOVolt(current):
    return (current - 0.24) / 8.100


def switchcoils(t, stat):
    MOT_coils_switch(t, stat)
    MOT_coilsAO(t, MOTAOVolt(MOT_Coil_Current) * stat)

def closeShutters(t, closeXZShutter, closeYShutter, closeY2Shutter,
                  closeXShutter, delay=True):
    if not delay:
        delay_XZ_off = 0
        delay_XZ_on = 0
        delay_y_off = 0
        delay_y_on = 0
        delay_y2_on = 0
        delay_y2_off = 0
        delay_x_on = 0
        delay_x_off = 0

    else:
        delay_XZ_off = XZ_Shutter_delay_off
        delay_XZ_on = XZ_Shutter_delay_on
        delay_y_on = Y1_Shutter_delay_on
        delay_y_off = Y1_Shutter_delay_off
        delay_y2_on = Y2_Shutter_delay_on
        delay_y2_off = Y2_Shutter_delay_off
        delay_x_on = X_Shutter_delay_on
        delay_x_off = X_Shutter_delay_off

    dly = 0
    if closeXZShutter:
        XZ_Only_Shutter_switch(t - delay_XZ_off, False)
        dly = max(dly, delay_XZ_off)
    else:
        XZ_Only_Shutter_switch(t - delay_XZ_on, True)
        dly = max(dly, delay_XZ_on)
    if closeYShutter:
        Y_Only_Shutter_switch(t - delay_y_off, False)
        dly = max(dly, delay_y_off)
    else:
        Y_Only_Shutter_switch(t - delay_y_on, True)
        dly = max(dly, delay_y_on)
    if closeY2Shutter:
        Y2_Only_Shutter_switch(t - delay_y2_off, False)
        dly = max(dly, delay_y2_off)
    else:
        Y2_Only_Shutter_switch(t - delay_y2_on, True)
        dly = max(dly, delay_y2_on)
    if closeXShutter:
        X_Only_Shutter_switch(t - delay_x_off, False)
        dly = max(dly, delay_x_off)
    else:
        X_Only_Shutter_switch(t - delay_x_on, True)
        dly = max(dly, delay_x_on)

    return t + dly


def trigNIDAQ(t):
    NIDAQ_Trig(t, 1)
    NIDAQ_Trig(t + 1, 0)
    return t


t = 0
FORT_DDS(t,'FORTLoading')
FORT_power(t,1)
vODT_switch(t,1)
# initialize HSDIO and AO channels to create a MOT
closeShutters(t, 0, 0, 0, 0, False)
uW_switch(t,0)
HF_switch(t, 1)
D2_switch(t, 1)
# HF_switch(t,0)
# D2_switch(t,0)
D2_DDS(t, 'MOT')
biasAO(t, MOT_shim)
HF_amplitude(t, MOT_hyperfine_power)
switchcoils(t, True)
HF_amplitude(t, MOT_hyperfine_power)
# Initialize Rydberg Lasers to be On
Ryd685_switch(t, 1)  # To 1
Ryd595_switch(t, 1)
#calibrate
cal_time = 3.0
vODT_switch(t, 1)  # To 0
HF_switch(t, 0)
trigNIDAQ(t)
t += cal_time
vODT_switch(t, 1)  # To 0
HF_switch(t, 1)
Ryd685_switch(t, 1)  # To 1
Ryd595_switch(t, 1)

# Dummy AO transition
AO(t,1,0)
AO(t+2,1,1)

RO_bin_width = RO_Time / float(RO1_bins) / 2
# set up pre-pulse dump bins
tt = t
# t = SPCMPulse(t,drops,RO_bin_width*2)
# SPCM_gate(t,1)
# for i in range(RO1_drops):
#     SPCM_clock(tt, 1)
#     # SPCM_gate(tt, 1)
#     tt += RO_bin_width
#     SPCM_clock(tt, 0)
#     # SPCM_gate(tt, 0)
#     tt += RO_bin_width
#
# for i in range(RO1_bins):
#     SPCM_clock(t, 1)
#     tt += RO_bin_width
#     SPCM_clock(t, 0)
#     tt += RO_bin_width

print("tt = " + str(tt))

t += MOT_loading_time
MOT_Andor_Trig(t, 1)
MOT_Andor_Trig(t + 1, 0)

t += AndorExpT

tt = t

# for i in range(RO1_bins):
#     SPCM_clock(tt, 0)
#     # SPCM_gate(tt, 1)
#     tt -= RO_bin_width
#     SPCM_clock(tt, 1)
#     # SPCM_gate(tt, 0)
#     tt -= RO_bin_width

for i in range(2):
    SPCM_clock(tt, 0)
    # SPCM_gate(tt, 1)
    tt -= RO_bin_width
    SPCM_clock(tt, 1)
    # SPCM_gate(tt, 0)
    tt -= RO_bin_width


print("MOT depletion waveform loaded. Duration = {}".format(t))