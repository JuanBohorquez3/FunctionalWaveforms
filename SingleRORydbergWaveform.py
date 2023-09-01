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


def ramp(t1, duration, v1, v2, channel):
    t2 = t1 + duration
    times = arange(t1, t1 + duration, .001)
    voltages = linspace(v1, v2, len(times))
    for t, v in zip(times, voltages):
        AO(t, channel, v)
    return t2


# RF Switches ------------------------------------------------------------------
ryd685_timing = 600e-6
ryd595_timing = 900e-6

D2_switch = lambda t, state: HSDIO(t, 19, not (state))
# D2_switch = lambda t, state: HSDIO(t, 19, 0)  # not (state))
HF_switch = lambda t, state: HSDIO(t, 18, not (state))
# HF_switch = lambda t, state: HSDIO(t, 18, 0)
vODT_switch = lambda t, state: HSDIO(t, 20, not (state))
# vODT_switch = lambda t, state: HSDIO(t, 20, 1)
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
Hamamatsu_Trig = lambda t, state: HSDIO(t, 31,state)
MOT_coils_switch = lambda t, state: HSDIO(t, 17, not (state))
SPCM_gate = lambda t, state: HSDIO(t, 26, state)
OP_DDS = lambda t, state: HSDIO(t, 27,state)
AO_start_trig = lambda t, state: HSDIO(t, 30,state)
RydRyd_switch = lambda t, state: HSDIO(t, 16, not(state))

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
vODT_power = lambda t, v: t  # useless, refactor to get rid of

def biasAO(t, shims):
    '''
    Takes in a time and a 3-element list of shim voltages (x,y,z)
    Holds level until next control
    '''

    AO(t, 4, shims[0])
    AO(t, 5, shims[1])
    AO(t, 6, shims[2])

    # correct for a finite switching time
    t += 2
    return t

def exp_biasAO(ti, tf, bias_i, bias_f, T, b, dt = .001):
    """
    switch bias fields from bias_i to bias_f with a low pass character. based on function a*(1-b*exp(-(t-ti)/T)) where a
    is set based on bias_i and bias_f for each coil.
    Args:
        ti: initial time (ms)
        tf: final time (ms)
        bias_i: initial bias field configuration [x,y,z] (V)
        bias_f: final bias field configuration [x,y,z] (V)
        T: characteristic decay time of low pass character (ms)
        b: b coefficient of low pass character (unitless)
        dt: rate at which function is sampled

    Returns:
        t after bias field sweep
    """
    avec = [bias_f[i] - bias_i[i] for i in range(3)]
    funcs = lambda x : [avec[i]*(1-b*exp(-(x-ti)/T))+bias_i[i] for i in range(3)]
    times =  arange(ti,tf,dt)
    for ts in times:
        biasAO(ts, funcs(ts))
    return tf

###SPCM Clocks on succsessive rising edges###

SPCM_clock = lambda t, state: HSDIO(t, 24, state)


###HSDIO control of DDS state for Double Pass D2 Laser###

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
    stage_dict = {'FORTLoading': (0), 'FORTRO': (1)}
    set = stage_dict[stage]
    HSDIO(t, 15, set)

    return t


### Experiment Functions ###

# ------------------------------------------------------------------------
#  initialize: Initializes all channels
#  Params: t: Starting time (ms)
#  Returns: t: Ending time (ms)
#  Sets all channels to their initial conditions
# ------------------------------------------------------------------------
def initialize(t):
    '''
    Sets Idle state of all HSDIO Channels to be zero with the exception of shutters
    '''
    shutters = (8,9,10,11,12,13)  # Shutters have idle state of 1
    for i in range(32):
        if i in shutters:
            HSDIO(t, i, 1)
        else:
            HSDIO(t, i, 0)
    vODT_switch(t, 1)
    vODT_power(t, vertTrapPower)
    Ryd685_switch(t, 0)
    Ryd595_switch(t, 0)
    RP_Shutter_switch_init(t, 1)
    Cooling_Shutter_switch_init(t, 1)
    OP_Shutter_switch_init(t, 0)
    OP_RP_Shutter_switch_init(t, 0)
    OP_switch(t, 0)
    Blowaway_Shutter_switch_init(t, 0)
    SPCM_gate(t, 0)
    FORT_DDS(t, 'FORTLoading')
    Collection_Shutter_switch_init(t, 0)

    uW_switch(t, 0)

    MOT_Andor_Trig(t, 0)
    Hamamatsu_Trig(t, 0)
    NIDAQ_Trig(t, 0)
    NIScope_Trig(t, 0)
    HF_switch(t, 1)
    D2_switch(t, 1)
    D2_DDS(t, 'MOT')
    biasAO(t, MOT_shim)
    switchcoils(t, True)

    AO_start_trig(t, 1)
    AO_start_trig(t+0.1,0)

    return t

# ------------------------------------------------------------------------
#  MOT_load: Load MOT
#  Params: t: Starting time (ms), duration: MOT load time in ms.
#  Returns: t: Ending time (ms)
#  Turns on MOT lasers, bias field, and gradient field for duration. Then turns off gradient field.
# ------------------------------------------------------------------------
def MOT_load(t, duration, trigger_andor = True,coils_on=False):
    ts = t
    HF_switch(t, 1)
    D2_switch(t, 1)
    # HF_switch(t,0)
    # D2_switch(t,0)
    D2_DDS(t, 'MOT')
    biasAO(t, MOT_shim)
    switchcoils(t, True)

    HF_amplitude(t, MOT_hyperfine_power)
    t += duration

    if not coils_on:
        switchcoils(t - .3, False)
    if trigger_andor:
        if t - AndorExpT < ts:
            tAnd = ts
        else:
            tAnd = t - AndorExpT
        MOT_Andor_Trig(tAnd, 1)
        MOT_Andor_Trig(tAnd + 1, 0)
    return t


# ------------------------------------------------------------------------
#  PGC1_and_TrapOn: Polarization Gradient Cooling and Trap On
#  Params: t: Starting time (ms), PGC_1_time: PGC time in ms. hODT_delay: Delay time in ms for turning on dipole trap
#  Optional Params: ODT_on: Trap on if true. chop: Chopped Loading if True.
#  Returns: t: Ending time (ms)
#  Runs PGC Sequence (detunes MOT laser and sets shims). Also triggers trap on.
# ------------------------------------------------------------------------
def PGC1_and_TrapOn(t, PGC_1_time, hODT_delay, ODT_on=True, chop=True,coils_on=False):
    D2_DDS(t, 'PGC1')
    biasAO(t, PGC1_shim)
    # vODT_switch(t+hODT_delay,ODT_on)
    HF_amplitude(t, PGC_1_hyperfine_power)
    vODT_power(t + hODT_delay, vertTrapPower)
    vODT_switch(t + hODT_delay, ODT_on)
    if chop:
        print "Chopped loading enabled"
        ChoppedRO(t, PGC_1_time, period=2.1e-3, RO_onoff=[.01, .5],
                  Trap_onoff=[0.27, .72])
    else:
        vODT_switch(t + hODT_delay, ODT_on)
    t += PGC_1_time
    if coils_on:
        switchcoils(t - .3, False)
    return t


# ------------------------------------------------------------------------
#  PGC2: Secondary PGC
#  Params: t: Starting time (ms), PGC_2_time: PGC time in ms.
#  Returns: t: Ending time (ms)
# ------------------------------------------------------------------------
def PGC2(t, PGC_2_time):
    D2_DDS(t, 'PGC2')
    biasAO(t, PGC2_shim)
    HF_amplitude(t, PGC_1_hyperfine_power)
    t += PGC_2_time
    return t


# ------------------------------------------------------------------------
#  Recool: Recooling after Readout
#  Params: t: Starting time (ms), Recool_time: Recool time in ms.
#  Returns: t: Ending time (ms)
# ------------------------------------------------------------------------
def Recool(t, recool_time, shims):
    D2_DDS(t, 'Recool')
    t = biasAO(t, shims)

    # turn on the D2 and HF AOMs
    D2_switch(t, 1)
    HF_switch(t, 1)

    # open the X and Z shutters
    # closeShutters(t-8.5, False,False,False,delay=False)
    HF_amplitude(t-4, Recool_hyperfine_power)
    t += recool_time

    # set the shutters to the RO configuration
    # closeShutters(t, closeXShutter,closeYShutter,closeZShutter,delay=False)

    # turn off the D2 and HF AOMs
    D2_switch(t, 0)
    HF_switch(t, 0)
    t += 0.01

    # D2_DDS(t,'LAC')
    # D2_DDS(t+0.001,'RO')
    return t


# ------------------------------------------------------------------------
#  holdinDark: Turns off MOT beams and holds atoms in trap in dark
#  Params: t: Starting time (ms), Trap_Hold_time: Hold time in ms.
#  Returns: t: Ending time (ms)
#  Turns off MOT beams and holds atoms in dipole trap (assuming there are atoms and a dipole trap)
# ------------------------------------------------------------------------
def holdinDark(t, Trap_Hold_time):
    # vODT_switch(t+.001,TrapOn)
    D2_switch(t, 0)
    HF_switch(t, 0)
    t += Trap_Hold_time
    return t


# ------------------------------------------------------------------------
#  TriggerNIScope: Triggers NI Scope to take waveform
#  Params: t: Starting time (ms)
#  Returns: t: Ending time (ms)
#  Triggers NI Scope cards in PXI crate to take waveform.
# ------------------------------------------------------------------------
def triggerNIScope(t):
    NIScope_Trig(t, 1)
    NIScope_Trig(t + 1, 0)
    return t


# ------------------------------------------------------------------------
#  TrapPulseOff: Pulses off dipole trap
#  Params: t: Starting time (ms), TrapOffPeriod: Trap off time in ms.
#  Returns: t: Ending time (ms)
#  Turns off dipole trap for TrapOffPeriod, to allow atoms to fall away
# ------------------------------------------------------------------------
def TrapPulseOff(t, TrapOffPeriod, ODT_on=True):
    vODT_switch(t, 0)
    t += TrapOffPeriod
    vODT_switch(t, ODT_on)
    return t


# ------------------------------------------------------------------------
#  BlowawayPulse: Blow Away with Blowaway Path
#  Params: t: Starting time (ms), BAPeriod: Blow away time (ms).
#  Returns: t: Ending time (ms)
#  Blows away F=4 atoms using blowaway path (rather than MOT path)
# ------------------------------------------------------------------------
def BlowawayPulse(t, BAPeriod):
    # closeShutters(t-1,True,True,True,True)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 0)
    D2_switch(t, 1)
    HF_switch(t, 0)
    D2_DDS(t, 'BA')
    HF_amplitude(t, RO1_hyperfine_power)
    Blowaway_Shutter_switch(t, 1)
    t += BAPeriod
    Blowaway_Shutter_switch(t, 0)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_off, 1)
    # closeShutters(t,*shuttersclosed,delay=False)
    D2_switch(t, 0)
    HF_switch(t, 0)
    return t


# ------------------------------------------------------------------------
#  biasAORamp: Ramps magnetic field from start condition to end condition
#  Params: t: Starting time (ms), start: starting bias (X,Y,Z). end: final bias (X,Y,Z). length: duration of ramp (ms). steps: number of steps over which to complete ramp
#  Returns: t: Ending time (ms)
#  Ramps bias fields in steps.
# ------------------------------------------------------------------------
def biasAORamp(t, start, end, length, steps):
    ar = array([[linspace(start[0], end[0], steps)[i],
                 linspace(start[1], end[1], steps)[i],
                 linspace(start[2], end[2], steps)[i]] for i in arange(steps)])
    for i in arange(steps):
        biasAO(t, ar[i])
        t += length / steps
    biasAO(t, end)
    return t


# ------------------------------------------------------------------------
#  counterreadout: A Version of Trap Imaging/Readout that doesn't switch any lasers
#  Params: t: Starting time (ms), OnTime: Duration of imaging (ms),
#  Optional Params: SPCM (bool): Enable photon counter. RO_bins: number of readout bins. drops: number of dropped bins at beginning (to remove spurious counts).
#                              returnPower: Raise trap power back to normal at end if True. chop: Chop trap and RO beams if True. shuttersclosed: Close [X,Y,Z] shutters if true.
#                              ROPowerToggle: If true, lower trap power during imaging
#  Returns: t: Ending time (ms)
#  Trap readout. If SPCM enabled, it pulses the SPCM clock, which tells it when to read out. Also triggers Hamamatsu and Andor cameras.
# ------------------------------------------------------------------------
def counterreadout(t, OnTime, SPCM=True, RO_bins=30, drops=3, returnPower=True,
                   chop=True, shuttersclosed=[False, False, False, False],
                   ROPowerToggle=False):
    # time per bin
    if ROPowerToggle: vODT_power(t - vertTrapPowerROPret, vertTrapPowerRO)
    RO_bin_width = OnTime / float(RO_bins) / 2
    print RO_bins
    print drops

    # set up pre-pulse dump bins
    tt = t - 2 * RO_bin_width * (drops - 1)
    # t = SPCMPulse(t,drops,RO_bin_width*2)
    for i in range(drops):
        SPCM_clock(tt, 1)
        tt += RO_bin_width
        SPCM_clock(tt, 0)
        tt += RO_bin_width
    # t-=2*RO_bin_width

    if chop:
        tend = 0  # ChoppedRO(t,OnTime,period=2e-3,RO_onoff=[.01,.5],Trap_onoff=[0.25,.71])
    else:
        tend = 0

    # trigger cameras
    ChipAndorOffset = -0.2
    MOT_Andor_Trig(t, 1)
    MOT_Andor_Trig(t + 1, 0)
    Hamamatsu_Trig(t + Hamamatsu_Trig_Shim, 1)
    Hamamatsu_Trig(t + Hamamatsu_Trig_Shim + OnTime, 0)

    # counter bins
    t += 2 * RO_bin_width
    for i in range(RO_bins):
        SPCM_clock(t, 1)
        t += RO_bin_width
        SPCM_clock(t, 0)
        t += RO_bin_width
    t -= 2 * RO_bin_width
    # SPCMPulse(t,RO_bins,RO_bin_width*2)

    return max(t, tend)


# ------------------------------------------------------------------------
#  TrapCenterFluorescence: Trap Imaging/Readout
#  Params: t: Starting time (ms), OnTime: Duration of imaging (ms),
#  Optional Params: SPCM (bool): Enable photon counter. RO_bins: number of readout bins. drops: number of dropped bins at beginning (to remove spurious counts).
#                              returnPower: Raise trap power back to normal at end if True. chop: Chop trap and RO beams if True. shuttersclosed: Close [X,Y,Z] shutters if true.
#                              ROPowerToggle: If true, lower trap power during imaging, recool: If true, enters Recool phase after RO
#  Returns: t: Ending time (ms)
#  Trap readout. If SPCM enabled, it pulses the SPCM clock, which tells it when to read out. Also triggers Hamamatsu and Andor cameras.
# ------------------------------------------------------------------------
def TrapCenterFluorescence(t, OnTime, SPCM=True, RO_bins=30, drops=3,
                           returnPower=True, chop=True,
                           shuttersclosed=[False, False, False, False],
                           ROPowerToggle=False, SPCM_bins=30, trigger_andor=False, trigger_hm=False):
    # time per bin
    if ROPowerToggle: vODT_power(t - vertTrapPowerROPret, vertTrapPowerRO)
    RO_bin_width = OnTime / float(RO_bins) / 2
    SPCM_bin_width = OnTime / float(SPCM_bins) / 2
    # print "RO_bins = {}".format(RO_bins)
    # print "RO_bin_width = {}".format(RO_bin_width)
    # print "SPCM_bins = {}".format(SPCM_bins)
    # print "SPCM_bin_width = {}".format(SPCM_bin_width)
    # print drops

    # Set up shutters and fields
    Collection_Shutter_switch(t - Collection_Shutter_delay_on, 1)
    t = biasAO(t, RO1_shim)
    closeShutters(t-4, shuttersclosed[0], shuttersclosed[1],
                      shuttersclosed[2], shuttersclosed[3])

    # set up pre-pulse dump bins
    tt = t - 2 * RO_bin_width * (drops)  # -1)
    # t = SPCMPulse(t,drops,RO_bin_width*2)
    # SPCM_gate(t,1)
    for i in range(drops):
        SPCM_clock(tt, 1)
        # SPCM_gate(tt, 1)
        tt += RO_bin_width
        SPCM_clock(tt, 0)
        # SPCM_gate(tt, 0)
        tt += RO_bin_width
    # t-=2*RO_bin_width

    # Collection_Shutter_switch(t - Collection_Shutter_delay_on, 1)
    # t = biasAO(t + ROShimTimeOffset, RO1_shim)
    # t = closeShutters(t, shuttersclosed[0], shuttersclosed[1],
    #                   shuttersclosed[2], shuttersclosed[3])
    SPCM_gate(t, 1)
    D2_switch(t, 1)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
    HF_switch(t, 1)
    D2_DDS(t, 'RO')

    HF_amplitude(t - 4, RO1_hyperfine_power)

    if chop:
        tend = 0  # ChoppedRO(t,OnTime,period=2e-3,RO_onoff=[.01,.5],Trap_onoff=[0.25,.71])
    else:
        tend = 0

    # trigger cameras
    ChipAndorOffset = -0.2
    if trigger_andor:
        MOT_Andor_Trig(t,1)
        MOT_Andor_Trig(t+1,0)
    if trigger_hm:
        Hamamatsu_Trig(t+Hamamatsu_Trig_Shim,1)
        Hamamatsu_Trig(t+Hamamatsu_Trig_Shim+OnTime,0)

    t += 2 * RO_bin_width

    # SPCM bins
    # tt = t
    # for i in range(SPCM_bins):
    #     # SPCM_gate(tt, 1)
    #     tt += SPCM_bin_width
    #     tt += SPCM_bin_width
    #     # SPCM_gate(tt - 0.01, 0)

    # Counter bins
    for i in range(RO_bins):
        SPCM_clock(t, 1)
        t += RO_bin_width
        SPCM_clock(t, 0)
        t += RO_bin_width
    t -= 2 * RO_bin_width
    # SPCMPulse(t,RO_bins,RO_bin_width*2)

    # turn off lasers, and done.
    SPCM_gate(t,0)
    D2_switch(t, 0)
    HF_switch(t, 0)
    # FORT_DDS(t,"FORTLoading")
    # D2_DDS(t,'PGC1')
    if returnPower:
        vODT_power(t, vertTrapPower)
    return max(t, tend)


# ------------------------------------------------------------------------
#  LightAssistedCollisions: Light Assisted Collisions
#  Params: t: Starting time (ms), shimFields (optional): If True, set shim fields. shuttersclosed (optional): calls closeShutters to set shutters to values specified in shuttersclosed
#  Implicit params: LAC_time: Light-assisted collision duration (ms), LAC_hyperfine_power: Repump power during LAC, LAC_shim
#  Returns: t: Ending time (ms)
#  Turns on MOT beams in LAC profile to kick atoms out of the trap to make it single-atom
# ------------------------------------------------------------------------
def LightAssistedCollisions(t, shimFields=True,
                            shuttersclosed=[False, False, False, False]):
    # start LAC at t
    # t = closeShutters(t, *shuttersclosed)
    if shimFields:
        t = biasAO(t, LAC_shim)
    D2_switch(t, 1)
    HF_amplitude(t, LAC_hyperfine_power)
    HF_switch(t, 1)
    D2_DDS(t, 'LAC')
    # end LAC/Cooling pulse after (time)
    t += LAC_Time
    D2_switch(t, 0)
    HF_switch(t, 0)
    return t


# ------------------------------------------------------------------------
#  trigZStage: Trigger Z Stage
#  Params: t: Starting time (ms)
#  Returns: t: Ending time (ms)
#  Sends a trigger to the Aerotech controller, telling the Z stage to move. This is necessary to move the Lux Mux up to the chip position.
#  It is also necessary to send a trigger even if you are not moving during measurements, so the program knows to read in the next iteration's parameters.
#   In those cases, simply set the initial and final positions to be equal.
# ------------------------------------------------------------------------
def trigZstage(t):
    Zstage_Trig(t, True)
    Zstage_Trig(t + 1, False)
    return t


def OneChopCamTrig(t, period=2e-3, RO_onoff=[0, .5], Trap_onoff=[.5, .99]):
    '''

    period: time in ms
    RO_onoff: tuple containing [on,off] as a percentage of period
    Trap_onoff: tuple containing [on,off] as a percentage of period

    '''
    MOT_Andor_Trig(t, 0)
    MOT_Andor_Trig(t + RO_onoff[0] * period, 1)
    MOT_Andor_Trig(t + RO_onoff[1] * period, 0)
    return t + period


def OneChopRO(t, period=2e-3, RO_onoff=[.5, 1], Trap_onoff=[0, .5]):
    '''

    period: time in ms
    RO_onoff: tuple containing [on,off] as a percentage of period
    Trap_onoff: tuple containing [on,off] as a percentage of period

    '''
    D2_switch(t, 0)
    vODT_switch(t, 0)
    D2_switch(t + RO_onoff[0] * period, 1)
    D2_switch(t + RO_onoff[1] * period, 0)
    vODT_switch(t + Trap_onoff[0] * period, 1)
    vODT_switch(t + Trap_onoff[1] * period, 0)
    return t + period


def OneChopTrap(t, period=2e-3, Trap_onoff=[0, .5]):
    '''

    period: time in ms
    Trap_onoff: tuple containing [on,off] as a percentage of period

    '''
    vODT_switch(t, 1)
    vODT_switch(t + Trap_onoff[0] * period, 0)
    vODT_switch(t + Trap_onoff[1] * period, 1)
    return t + period


def OneChopOP(t, period=2e-3, Trap_onoff=[0, .5]):
    OP_switch(t, 0)
    OP_switch(t + Trap_onoff[0] * period, 1)
    OP_switch(t + Trap_onoff[1] * period, 0)
    return t + period


def EndChopOP(t, period=2e-3):
    print t
    t += period * 2
    OP_switch(t, 0)
    return t


def EndChopRO(t, period=2e-3):
    '''

    period: time in ms
    RO_onoff: tuple containing [on,off] as a percentage of period
    Trap_onoff: tuple containing [on,off] as a percentage of period

    '''
    print t
    t += period * 2
    D2_switch(t, 0)
    vODT_switch(t, 1)
    return t


def EndChopTrap(t, period=2e-3):
    '''

    period: time in ms
    RO_onoff: tuple containing [on,off] as a percentage of period
    Trap_onoff: tuple containing [on,off] as a percentage of period

    '''
    print t
    # vODT_switch(t,1)
    t += period * 2
    # vODT_switch(t,1)
    return t


# ------------------------------------------------------------------------
#  ChoppedRO: Chops dipole trap and imaging beams
#  Params: t: Starting time (ms), RO_time: Duration over which to chop (ms), period: Chopping period (ms), RO_onoff: 2-element array specifying duty cycle of readout beam, Trap_onoff: 2-element array specifying duty cycle of trap beam
#  Returns: t: Ending time (ms)
#  Chops dipole trap and imaging beams with duty cycle specified by Trap_onoff (1st element is start of on period, second is end, with 0 at beginning of cycle and 1 at end. Do not use 0.00 as beginning, since it causes issues...)
#  Individual cycles are set by OneChopRO and the final cycle is set by EndChopRO.
# ------------------------------------------------------------------------
def ChoppedRO(t, RO_time, period=2e-3, RO_onoff=[.5, 1], Trap_onoff=[0, .5]):
    repeats = int(RO_time / period) + 1
    funct = lambda t: OneChopRO(t, period, RO_onoff, Trap_onoff)
    t = add_repeat(t, funct, repeats)
    return EndChopRO(t, period)


# ------------------------------------------------------------------------
#  ChoppedTrap: Chops dipole trap
#  Params: t: Starting time (ms), RO_time: Duration over which to chop (ms), period: Chopping period (ms), Trap_onoff: 2-element array specifying duty cycle
#  Returns: t: Ending time (ms)
#  Chops dipole trap with duty cycle specified by Trap_onoff (1st element is start of on period, second is end, with 0 at beginning of cycle and 1 at end. Do not use 0.00 as beginning, since it causes issues...)
#  Individual cycles are set by OneChopTrap and the final cycle is set by EndChopTrap.
# ------------------------------------------------------------------------
def ChoppedTrap(t, RO_time, period=2e-3, Trap_onoff=[0.01, .501]):
    repeats = int(RO_time / period) + 1
    funct = lambda t: OneChopTrap(t, period, Trap_onoff)
    t = add_repeat(t, funct, repeats)
    return EndChopTrap(t, period)


# ------------------------------------------------------------------------
#  SPCMPulse: sets up pulse repetition for single photon counter bins
#  Params: t: Starting time (ms), pulses: number of pulses, period: bin time in ms
#  Returns: t: Ending time (ms)
#  Sets up pulse repetition for photon counter bins. OnePulseSPCM sets up a single repetition. Not currently used because it clashes with trap chopping during imaging (HSDIO does not allow more than one repeat at a time).
# ------------------------------------------------------------------------
def SPCMPulse(t, pulses, period):
    funct = lambda t: OnePulseSPCM(t, period)
    t = add_repeat(t, funct, pulses)
    return t


def OnePulseSPCM(t, period):
    SPCM_clock(t, 0)
    SPCM_clock(t + 0.25 * period, 1)
    SPCM_clock(t + 0.75 * period, 0)
    return t + period


# ------------------------------------------------------------------------
#  closeShutters: Sets MOT shutters based on input parameters
#  Params: t: Starting time (ms), close[XZ,Y,Y2,X]Shutter: True to close, False to open. delay: if True, insert delay. May need to be False in some cases when opening shutters for timing to work. ALWAYS CHECK, because shit goes wrong.
#  Returns: t: Ending time (ms)
#  Closes or opens shutters based on input parameters.
# ------------------------------------------------------------------------
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


# ------------------------------------------------------------------------
#  Blow_Away
#  Params: t: Starting time (ms)
#  Implicit Param: Blow_Away_time: Blow away time in ms
#  Returns: t: Ending time (ms)
#  Blows away F=4 atoms using MOT beams
# ------------------------------------------------------------------------
def Blow_Away(t, shuttersclosed=[False, False, False, False], chopTrap=False):
    D2_DDS(t, 'BA')
    biasAO(t, RO1_shim)
    D2_switch(t, 1)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on - 0.5, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_off, 0)

    # XZ_Only_Shutter_switch(t-XZ_Shutter_delay_off,0)
    # Y_Only_Shutter_switch(t,1)
    # Y2_Only_Shutter_switch(t-Y2_Shutter_delay_off,0)

    # closeShutters(t-1.5,*shuttersclosed)
    tp = t
    if chopTrap:
        tp = ChoppedTrap(tp, Blow_Away_time, period=0.005,
                         Trap_onoff=[0.15, 0.2])
    t += Blow_Away_time
    # closeShutters(t, not(shuttersclosed[0]), shuttersclosed[1], shuttersclosed[2],shuttersclosed[3]) # !!currently broken!!
    D2_switch(t, 0)
    RP_Shutter_switch(t - RP_Shutter_delay_off * 1, 1)
    return t + .001


# ------------------------------------------------------------------------
#  OpticalPumping: Optical Pumping and (Optional) Shelving
#  Params: t: Starting time (ms), OP_time: optical pumping time (ms), shelve_time: shelving time (ms) (Repump if -, OP if +), chop (bool): Chops dipole trap
#  Returns: t: Ending time (ms)
#  Runs Optical Pumping sequence (turn on OP beams and open shutters), then shelving if enabled (close OP or repumper shutter before other)
# ------------------------------------------------------------------------
def OpticalPumping(t, OP_time, shelve_time=0, chop=True):
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_off * 3, 0)
    closeShutters(t - 2, 1, 1, 1, 1)
    OP_Shutter_switch(t - OP_Shutter_delay_on, 1)
    OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_on, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_on, 1)

    if chop:
        # vODT_power(t,vertTrapPowerChop)
        ChoppedTrap(t, OP_time + abs(shelve_time), period=1e-3,
                    Trap_onoff=[0.2, 0.41])

    # Chip_Andor_Trig(t,1)
    HF_switch(t, 1)
    OP_switch(t, 1)
    D2_switch(t, 0)
    HF_amplitude(t, OP_HF_amplitude)
    biasAO(t, OP_shim)
    t += OP_time
    print OP_time
    HF_off_delay = 0.027
    if shelve_time >= 0:
        if shelve_time > 0:
            RP_Shutter_switch(t - RP_Shutter_delay_off, 0)
        OP_RP_Shutter_switch(t, 0)
        HF_switch(t, 0)
        HF_amplitude(t + HF_off_delay, 0)
    else:
        OP_Shutter_switch(t, 0)
        OP_switch(t, 0)

    t += abs(shelve_time)

    if shelve_time >= 0:
        OP_Shutter_switch(t, 0)
        OP_switch(t, 0)
    else:
        RP_Shutter_switch(t - RP_Shutter_delay_off, 0)
        OP_RP_Shutter_switch(t, 0)
        HF_switch(t, 0)
        HF_amplitude(t + HF_off_delay, 0)
    # Chip_Andor_Trig(t,0)
    # biasAO(t,RO1_shim)
    vODT_power(t, vertTrapPower)
    return t


# ------------------------------------------------------------------------
#  Depump: Runs depumping experiment
#  Params: t: Starting time (ms), shelve_time: depumping time (ms), chop (bool): Chops dipole trap if True
#  Returns: t: Ending time (ms)
#  Turns on Repumper (neg. depump time) or optical pumping beam (pos. depump time) on OP path
# ------------------------------------------------------------------------
def Depump(t, shelve_time=0, chop=True):
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_off, 0)
    closeShutters(t, 1, 1, 1, 1)
    D2_switch(t, 0)
    biasAO(t, OP_shim)

    if chop:
        vODT_power(t, vertTrapPowerChop)
        ChoppedTrap(t, OP_time + abs(shelve_time), period=1e-3)

    if shelve_time < 0:
        RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
        OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_on, 1)
        HF_switch(t, 1)
        HF_amplitude(t, OP_HF_amplitude)
    else:
        OP_Shutter_switch(t - OP_Shutter_delay_on, 1)
        OP_switch(t, 1)

    t += abs(shelve_time)

    if shelve_time >= 0:
        OP_Shutter_switch(t, 0)
        OP_switch(t, 0)
    else:
        RP_Shutter_switch(t, 0)
        OP_RP_Shutter_switch(t, 0)
        HF_switch(t, 0)
        HF_amplitude(t, 0)
    # Chip_Andor_Trig(t,0)
    biasAO(t, RO1_shim)
    vODT_power(t, vertTrapPower)
    return t


# ------------------------------------------------------------------------
#  MicrowavePulse: Microwave Pulse
#  Params: t: Starting time (ms), pre_uW_time: Delay before microwaves (ms), uW_time: microwave time (ms)
#  Returns: t: Ending time (ms)
#  Triggers microwave pulse of length uW_time
# ------------------------------------------------------------------------
def MicrowavePulse(t, pre_uW_time, uW_time, chop):
    t += pre_uW_time

    if chop:
        # vODT_power(t,vertTrapPowerChop)
        ChoppedTrap(t, uW_time, period=1e-3, Trap_onoff=[0.2, 0.41])

    uW_switch(t, 1)
    t += uW_time
    uW_switch(t, 0)
    return t


# ------------------------------------------------------------------------
# RydPulse: Rydberg Pulse
# Params: t: Starting Time (ms), RydTime: Rydberg Pulse Length(ms),RydOn : Which of the two rydberg beams are on format is : [685nm Bool,595nm Bool]
# Returns: t: Ending time(ms)
# Triggers a Rydberg pulse of length RydTime
# ------------------------------------------------------------------------
def RydPulse(t, RydTime, RydOn=[True, True]):
    if RydOn[0]:
        Ryd685_Shutter_switch(t - Ryd685_Shutter_delay_on, 1)
        Ryd685_switch(t, 1)
    if RydOn[1]:
        Ryd595_Shutter_switch(t - Ryd595_Shutter_delay_on, 1)
        Ryd595_switch(t, 1)

    t += RydTime

    if RydOn[0]:
        Ryd685_Shutter_switch(t - Ryd685_Shutter_delay_off, 0)
        Ryd685_switch(t, 0)
    if RydOn[1]:
        Ryd595_Shutter_switch(t - Ryd595_Shutter_delay_off, 0)
        Ryd595_switch(t, 0)

    return t


# ------------------------------------------------------------------------
#  shelve_and_blowaway: Shelving and Blowaway
#  Params: t: Starting time (ms), shelve_time: microwave time (ms),
#                    shelve_state: F level to shelve into (if shelve_time is negative, the opposite state will be shelved into),
#                    blowaway (bool): if True, blowaway is done, if False, it is skipped.
#  Returns: t: Ending time (ms)
#  Runs Optical Pumping sequence, then microwaves, then blowaway.
# ------------------------------------------------------------------------
def shelve_and_blowaway(t, sTime, sState, blowaway=True, toRO=True):
    D2_DDS(t, 'Recool')
    closeShutters(t, 0, 0, 0, 0, delay=True)
    t += 1
    tt = t + 10
    assert sState == 3 or sState == 4
    if sTime < 0:
        sTime = abs(sTime)
        if sState == 4:
            sState = 3
        else:
            sState = 4

    if sState == 4:
        HF_switch(t, 1)
        t += sTime
        HF_switch(t, 0)
    else:
        biasAO(t, Recool_shim)
        D2_switch(t, 1)
        t += abs(sTime)
        D2_switch(t, 0)

    if t < tt:
        t = tt

    t += RP_Shutter_delay_off + 1
    if blowaway:
        closeShutters(t, 1, 0, 1, 0, delay=True)
        t += 1
        RP_Shutter_switch(t - RP_Shutter_delay_off, 0)
        biasAO(t, RO1_shim)
        D2_DDS(t - 0.01, 'RO')
        D2_DDS(t, 'BA')
        D2_switch(t, 1)
        Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 1)
        t += Blow_Away_time
        D2_switch(t, 0)
        t += RP_Shutter_delay_on
        RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
    if toRO:
        t = holdinDark(t, 4)
        closeShutters(t, *closetheshutters, delay=True)
    return t


# ------------------------------------------------------------------------
#  RFE: Rabi Flopping Experiment
#  Params: t: Starting time (ms), uW_time: microwave time (ms)
#  Returns: t: Ending time (ms)
#  Runs Optical Pumping sequence, then microwaves, then blowaway.
# ------------------------------------------------------------------------
def RFE(t, uW_time):
    t = OpticalPumping(t, OP_time)
    t = MicrowavePulse(t, pre_uW_time, uW_time)
    stray_time = 10 - OP_time - pre_uW_time - uW_time - Blow_Away_time
    if stray_time > 2.8:
        t += stray_time
    else:
        print "Experiment longer than 10 ms."
        t += 2.8
    t = Blow_Away(t)
    D2_switch(t, 0)
    D2_DDS(t, 'RO')
    return t + .01


# ---------------------------------------------------------------------------
# ShimSweep: Adiabatically sweeps magnetic shim fields from initial values to final values adiabatically
# Params: t: Starting time (ms), sweep_time: time to sweep, init_v: initial bias voltages, fin_v: final bias voltages
# returns: t: Ending time (ms)
# ---------------------------------------------------------------------------
def ShimSweep(t, sweep_time, init_v, fin_v):
    # empirically discovered minimum time step between sweep steps
    dt = 0.1
    steps = int(sweep_time / dt)
    dv = zeros(len(init_v))
    set_v = zeros((len(init_v), steps), dtype=float)
    for n in range(len(init_v)):
        set_v[n, :] = linspace(init_v[n], fin_v[n], steps)
    for i in range(steps):
        biasAO(t, set_v[:, i])
        t += dt
        # set_v = set_v + dv
    return t


def trigNIDAQ(t):
    NIDAQ_Trig(t, 1)
    NIDAQ_Trig(t + 1, 0)
    return t


def MOTAOVolt(current):
    return (current - 0.24) / 8.100


def switchcoils(t, stat):
    MOT_coils_switch(t, stat)
    MOT_coilsAO(t, MOTAOVolt(MOT_Coil_Current) * stat)


def OnePulseRyd(t, pulse_time, trap_time, uW_enhance):
    """
    Args:
        t: start time
        pulse_time: length of rydberg pulse
        duty_cycle: duty cycle of rydberg beams during the chop
    """
    t0 = t
    t = t+max(ryd685_timing, ryd595_timing)
    vODT_switch(t0, 0)
    Ryd685_switch(t-ryd685_timing, 1)
    Ryd595_switch(t-ryd595_timing, 1)
    Ryd685_switch(t-ryd685_timing+pulse_time, 0)
    Ryd595_switch(t-ryd595_timing+pulse_time, 0)
    t = t0 + pulse_time
    vODT_switch(t, 1)
    if uW_enhance:
        uW_switch(t,1)
        uW_switch(t+trap_time-1e-3,0)
    return t+trap_time

def EndChopRyd(t, pulse_time):
    """
    Args:
        t: start time
        pulse_time: length of rydberg pulse
    """
    t+=pulse_time*2
    Ryd685_switch(t,0)
    Ryd595_switch(t,0)
    vODT_switch(t,1)
    # t0 = t
    # t = t+max(ryd685_timing, ryd595_timing)
    # vODT_switch(t0, 0)
    # Ryd685_switch(t-ryd685_timing, 1)
    # Ryd595_switch(t-ryd595_timing, 1)
    # Ryd685_switch(t-ryd685_timing+pulse_time, 0)
    # Ryd595_switch(t-ryd595_timing+pulse_time, 0)
    # t = t+pulse_time
    # vODT_switch(t, 1)
    return t

def ChoppedRyd(t, pulse_time, repeats, uW_enhance=False):
    funct = lambda t: OnePulseRyd(t, pulse_time, 3e-3,uW_enhance)
    t = add_repeat(t, funct, repeats)
    return EndChopRyd(t, pulse_time)
# ---------------------------------------------------------------------------------------------
# Calibration: creates a calibration pulse for easy readout of your relevant and/or sensitive powers
# params: t: Starting time(ms), calTime: Length of calibration pulse (ms)
# returns: t: Ending time(ms)
def Calibration(t, calTime=3):
    # turn on the MOT Beams:
    trigNIDAQ(t)
    measured_switches = [Ryd595_switch, Ryd685_switch, OP_switch, OP_DDS]
    # measured_switches = [OP_switch, OP_DDS]
    Cooling_Shutter_switch(t, 1)
    closeShutters(t, 0, 0, 0, 0, delay=False)
    D2_switch(t, 1)
    D2_DDS(t, 'MOT')
    # turn off the Repumper
    HF_switch(t, 0)
    HF_amplitude(t, 0)
    for sw in measured_switches:
        sw(t, 1)

    # HSDIO(t, 20, 0)
    t += calTime
    # trigger the NIDAQ
    #trigNIDAQ(t)
    t += calTime
    # HSDIO(t, 20, 1)

    for sw in measured_switches:
        sw(t, 0)
    # Collection_Shutter_switch(t, 0)
    return t
# ---------------------------------------------------------------------------------------------


TrapOn = True
ROPowerToggle = False
# DoChop=False

XZJitter = .7

gradient_during_pgc = True

t = 0
initialize(t)
Collection_Shutter_switch(t,0)
# t0 = OP_RP_Shutter_switch(t,0)
trigZstage(t)
tp = t
# Blowaway_Shutter_switch(t,1)
t = Calibration(t)
# t += 1
rydberg_MOT_dep = False
if rydberg_MOT_dep:
    Ryd685_switch(t, 1)
    Ryd595_switch(t, 1)
t = MOT_load(t, MOT_loading_time,trigger_andor=True,coils_on=gradient_during_pgc)  # DDS: MOT (0,0,0)
if rydberg_MOT_dep:
    Ryd685_switch(t-5, 0)
    Ryd595_switch(t-5, 0)
# MOT_Andor_Trig(tp+80,1)
# MOT_Andor_Trig(tp+81,0)

Blowaway_Shutter_switch(t - BA_Shutter_delay_off, 0)
# counterreadout(t-MOT_loading_time/4,RO_Time,chop=DoChop,RO_bins=RO1_bins,drops=RO1_drops,shuttersclosed=[0,0,0,0],ROPowerToggle=ROPowerToggle)

t = PGC1_and_TrapOn(t, PGC_1_time, hODT_delay, ODT_on=TrapOn,
                    chop=DoChop,coils_on=gradient_during_pgc)  # DDS: PGC1 (0,0,1)
# t = PGC2(t, PGC_2_time)
D2_DDS(t+0.1,'PGC2')

closetheshutters = [closeXZShutter, closeYShutter, closeY2Shutter,
                    closeXShutter]
print closetheshutters

# ---------------------------------------------------------
'''
# MOT Temperature
t = holdinDark(t,Drop_Time)


#Grey Coding
t += 0.03
D2_DDS(t-.04,'PGC2')
D2_DDS(t-0.03,'LAC')
D2_DDS(t-0.02,'Recool')
D2_DDS(t-0.01,'RO')

#Trigger andor
MOT_Andor_Trig(t,1)
MOT_Andor_Trig(t+1,0)

#On and off the RO lights
D2_switch(t, 1)
Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 1)
RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
HF_switch(t, 1)
HF_amplitude(t - 0.1, RO1_hyperfine_power)
t += RO_Time
D2_switch(t,0)
HF_switch(t,0)
HF_amplitude(t,0)
D2_DDS(t,'Recool')
'''
# ----------------------------------------------------------

t = holdinDark(t, 1)

D2_DDS(t, 'LAC')

t = LightAssistedCollisions(t, shuttersclosed=[0, 0, 0, 0])

# t = t + 2
D2_DDS(t, 'Recool')
Collection_Shutter_switch(t,1)
t = Recool(t, Recool_time, Recool_shim)  # TODO Uncouple the length of this recool phase from the one between RO
t = closeShutters(t-4, *closetheshutters, delay=False)
t = holdinDark(t,Trap_Hold_time/2)

t += XZJitter

t = holdinDark(t, Trap_Hold_time/2)

D2_DDS(t,'Recool')
t+=0.01

#Post-RO Recool
Collection_Shutter_switch(t, 0)
recool2_time = 0
if recool2_time > 0:
    closeShutters(t, 0, 0, 0, 0, delay=False)
    t=holdinDark(t,6)
    # t=holdinDark(t,X_Shutter_delay_on+5)
    t0 = t
    t = Recool(t+0.1, recool2_time,Recool_shim)
    # closeShutters(t+5,*closetheshutters,delay=False)
else:
    t += 5

# drop recapture
if DropTime > 0:
    t = holdinDark(t,1)
    t = TrapPulseOff(t,DropTime/1000, ODT_on=TrapOn) #comment out
    t = holdinDark(t,1)

# t = holdinDark(t, GapTime)						# Retention

ba_delay = 15
if not BL:

    # Shelve into hyperfine levels ------------------------------------------------------------ Shelving
    if abs(shelve_time) > 0:
        t += 1
        D2_DDS(t, 'Recool')
        biasAO(t - 4, Recool_shim)
        if shelve_state not in [3, 4]:
            raise ValueError("shelve_state must be 3 or 4. There are no other HF Levels!")
        st = shelve_state == 3
        if shelve_time < 0:
            st = not st
            shelve_time = abs(shelve_time)
        [cool_delay, hf_delay] = [Cooling_Shutter_delay_on, RP_Shutter_delay_off] if st else [Cooling_Shutter_delay_off, RP_Shutter_delay_on]
        Cooling_Shutter_switch(t - cool_delay, st)
        RP_Shutter_switch(t - hf_delay, not st)
        D2_switch(t, st)
        HF_switch(t, not st)
        HF_amplitude(t, (not st)*2.6)
        t += shelve_time
        [cool_delay, hf_delay] = [Cooling_Shutter_delay_on, RP_Shutter_delay_on]
        #Cooling_Shutter_switch(t, 1)
        # if Blow_Away_time == 0:
        RP_Shutter_switch(t - hf_delay, 1)
        D2_switch(t, 0)
        HF_switch(t, 0)
        t0 = t
        # OPRP from MOT paths
        # if OP_Time == 0 and OP_shelve_time == 0 and uW_time ==0:
        #   closeShutters(t, *[1, 0, 1, 1], delay=False)
        # OPRP from MuxJr path
        closeShutters(t, *[1, 0, 1, 1], delay=False)
        # D2_switch(t, 1)


    # OP pulse -------------------------------------------------------------------------------------- OP
    if OP_Time > 0:
        # AO(t-4, 3, 0)
        t = holdinDark(t, 1)
        Cooling_Shutter_switch(t, 0)
        # OPRP from MuxJr path
        # closeShutters(t, *[1, 1, 1, 1], delay=False)
        t = ShimSweep(t, 1, Recool_shim, OP_shim)
        t = holdinDark(t, 6)
        OP_switch(t, 1)
        # HF_switch(t, 0)
        HF_switch(t, 1)
        # HF_amplitude(t-4, OP_HF_amplitude)
        # OPRP from MuxJr path
        OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_on, 1)
        t += OP_Time
        OP_switch(t, 0)
        HF_switch(t, 0)
        if abs(OP_shelve_time) == 0 and uW_time == 0:
            # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
            # OPRP from MuxJr path
            OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_off+6, 0)
            t = ShimSweep(t, 1, OP_shim, RO1_shim)
            t0 = t

    # print("abs(OP_shelve_time) = {}".format(abs(OP_shelve_time)))
    # print("RO1 Shim = {}".format(RO1_shim))
    # OP shelve ------------------------------------------------------------------------------ OP shelve
    OP_shelve_init = OP_shelve_time
    if abs(OP_shelve_time) > 0:
        # print("abs(OP_shelve_time) = {}".format(abs(OP_shelve_time)))
        if OP_Time == 0:
            # print("optiem".format(abs(OP_shelve_time)))
            t = holdinDark(t, 1)
            Cooling_Shutter_switch(t, 0)
            # closeShutters(t, *[1] * 4, delay=False)
            t = ShimSweep(t, 1, Recool_shim, OP_shim)
            OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_on, 1)
            t = holdinDark(t, 6)
        if shelve_state not in [3,4]:
            raise ValueError("shelve_state must be 3 or 4. There are no other HF Levels!")
        st = shelve_state == 3
        if OP_shelve_time < 0:
            st = not st
            OP_shelve_time = abs(OP_shelve_time)
        print(st)
        OP_switch(t, st)
        HF_switch(t, not st)
        # HF_switch(t, 0)
        OPRP_delay = OP_RP_Shutter_delay_on if not st else OP_RP_Shutter_delay_off - 6
        # OP_RP_Shutter_switch(t - OPRP_delay, not st)
        # RP_Shutter_switch(t-RP_Shutter_delay_on, not st)
        t += OP_shelve_time
        OP_switch(t, 0)
        HF_switch(t, 0)
        # OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_off + 6, 0)
        RP_Shutter_switch(t, 0)
        if uW_time == 0 and ryd_time == 0:
            # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
            t = ShimSweep(t, 1, OP_shim, RO1_shim)
            t0 = t

    # OP shelve ------------------------------------------------------------------------------ OP shelve
    # Shelve into F=4 state no matter what
    if OP_shelve_init > 0:
        OP_shelve_time_p = -0.5
        # print("abs(OP_shelve_time) = {}".format(abs(OP_shelve_time)))
        if OP_Time == 0:
            # print("optiem".format(abs(OP_shelve_time)))
            t = holdinDark(t, 1)
            Cooling_Shutter_switch(t, 0)
            # closeShutters(t, *[1] * 4, delay=False)
            t = ShimSweep(t, 1, Recool_shim, OP_shim)
            OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_on, 1)
            t = holdinDark(t, 6)
        if shelve_state not in [3,4]:
            raise ValueError("shelve_state must be 3 or 4. There are no other HF Levels!")
        st = shelve_state == 3
        if OP_shelve_time_p < 0:
            st = not st
            OP_shelve_time_p = abs(OP_shelve_time_p)
        print(st)
        OP_switch(t, st)
        # HF_switch(t, 0)
        HF_switch(t, not st)
        OPRP_delay = OP_RP_Shutter_delay_on if not st else OP_RP_Shutter_delay_off - 6
        OP_RP_Shutter_switch(t - OPRP_delay, not st)
        # RP_Shutter_switch(t-RP_Shutter_delay_on, not st)
        t += OP_shelve_time_p
        OP_switch(t, 0)
        HF_switch(t, 0)
        OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_off + 6, 0)
        RP_Shutter_switch(t, 0)
        if uW_time == 0 and ryd_time == 0:
            # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
            t = ShimSweep(t, 1, OP_shim, RO1_shim)
            t0 = t

    if uW_time > 0:
        t = ShimSweep(t-1, 1, OP_shim, uW_shim)
        t = holdinDark(t,3)
        uW_switch(t, 1)
        t+= uW_time
        uW_switch(t, 0)
        # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
        OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_off+6, 0)
        if ryd_time == 0:
            t = ShimSweep(t, 1, uW_shim, RO1_shim)
        t0 = t

    if ryd_time > 0:
        if uW_time == 0:
            t += 4
            t = ShimSweep(t - 1, 1, OP_shim, uW_shim)
            t += 4
        else:
            t += 1
        chop_ryd = ryd_chops > 1
        if chop_ryd:
            ChoppedRyd(t, ryd_time*1e-3, int(ryd_chops), uW_enhance=False)
        else:
            ryd_time = ryd_time*1e-3
            Ryd685_switch(t-ryd685_timing,1)
            Ryd595_switch(t-ryd595_timing,1)
            Ryd685_switch(t-ryd685_timing+ryd_time,0)
            Ryd595_switch(t-ryd595_timing+ryd_time,0)
            t = TrapPulseOff(t-1e-3, ryd_time + 1.0e-3, ODT_on=True)
            # Pulse on uW field to expedite photoionization
            # uW_switch(t+1e-3,1)
            # uW_switch(t+3e-3,0)
            t = holdinDark(t, 5e-3)
        if Blow_Away_time == 0:
            t = ShimSweep(t+1, 1, uW_shim, RO1_shim)
        else:
            t = ShimSweep(t+1, 1, uW_shim, BA_shim)

    # Blow Away ------------------------------------------------------------------------------ Blow Away
    if Blow_Away_time > 0:
        # Blow Away Pulse
        t = ShimSweep(t, 1,RO1_shim, BA_shim)
        t += 1
        Cooling_Shutter_switch(t, 1)
        RP_Shutter_switch(t, 0)
        # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
        t0 += 0.5
        # RP_Shutter_switch(t0, 0)
        t0 = holdinDark(t0, 7)
        # t0 +=5.5
        t = t0  # max(t0, t)
        D2_DDS(t-0.001, "RO")
        # AO(t, 3, 2.6)
        D2_DDS(t, "BA")
        D2_switch(t, 1)
        HF_switch(t, 0)
        t += Blow_Away_time
        # drop recapture
        #t = holdinDark(t,1)
        TrapPulseOff(t - Blow_Away_time, DropTime/1000, ODT_on=TrapOn) #comment out
        #t = holdinDark(t,1)
        D2_switch(t, 0)
        RP_Shutter_switch(t, 1)
        t = ShimSweep(t+1, 1, BA_shim, RO1_shim)
        t += 1
        Cooling_Shutter_switch(t, 1)
        closeShutters(t+3, *closetheshutters, delay=False)
        t = holdinDark(t, ba_delay)
    else:
        Cooling_Shutter_switch(t, 1)
        closeShutters(t+3, *closetheshutters, delay=False)
        t = holdinDark(t, ba_delay+1)

else:
    closeShutters(t + 3, *closetheshutters, delay=False)
    Cooling_Shutter_switch(t,1)
    t = holdinDark(t, ba_delay + 1)
# t = max(t, t0)

#closeShutters(t, *closetheshutters)
#t = holdinDark(t,X_Shutter_delay_off+11)
#t = trigZstage(t)
# t = holdinDark(t,25)
HF_amplitude(t, 2.6)
closeShutters(t-ba_delay/2, *closetheshutters, delay=False)
t+=3
OP_RP_Shutter_switch(t - Collection_Shutter_delay_on - 5, 0)
Collection_Shutter_switch(t - Collection_Shutter_delay_on, 1)
Hamamatsu_Trig(t + Hamamatsu_Trig_Shim + 10.85, 1)
Hamamatsu_Trig(t + Hamamatsu_Trig_Shim + 10.85 + RO_Time, 0)
# TrapPulseOff(t, RO_Time, ODT_on=TrapOn)     #FORT Off/On
t = TrapCenterFluorescence(t, RO_Time, chop=DoChop, RO_bins=RO1_bins,
    drops=RO1_drops, shuttersclosed=closetheshutters,
    ROPowerToggle=ROPowerToggle, SPCM_bins=SPCM_gates)
Collection_Shutter_switch(t, 0)
switchcoils(t, True)
closeShutters(t+10, False, False, False, False, delay=False)
t = holdinDark(t, 25*1.0)
#t += 20
t = TrapPulseOff(t, 2, ODT_on=TrapOn)

#initialize(t)

# OP_DDS(t, 1)
# t = MOT_load(t, 1, False, coils_on=True)
# t = Calibration(t)
t = MOT_load(t, 5, False, coils_on=True)
# Ryd595_switch(t,1)
# Ryd685_switch(t,1)
# HF_switch(t, 1)
# OP_switch(t, 1)
OP_DDS(t, 1)
# t = Calibration(t)
# t = MOT_load(t, 1, False, coils_on=True)