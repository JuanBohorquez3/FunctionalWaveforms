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
#running = experiment.running
status = experiment.status

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
ryd685_timing = 200e-6
ryd595_timing = 50e-6

D2_switch = lambda t, state: HSDIO(t, 19, not (state))
#D2_switch = lambda t, state: HSDIO(t, 19, 0)  # not (state))
HF_switch = lambda t, state: HSDIO(t, 18, not (state))
#HF_switch = lambda t, state: HSDIO(t, 18, 0)
vODT_switch = lambda t, state: HSDIO(t, 20, not (state))
#vODT_switch = lambda t, state: HSDIO(t, 20, 1)
vODT_source_switch = lambda t, state: HSDIO(t,16,state)
vODT_source_switch = lambda t, state: HSDIO(t,16,1)
Ryd685_switch = lambda t, state: HSDIO(t, 22, state)
#Ryd685_switch = lambda t, state: HSDIO(t, 22, 0)
Ryd595_switch = lambda t, state: HSDIO(t, 21, state)
#Ryd595_switch = lambda t, state: HSDIO(t, 21, 0)   # COMMENT ME OUT -----------
chop = lambda t, state: HSDIO(t, 24, state)
uW_switch = lambda t, state: HSDIO(t, 0, not (state))
OP_switch = lambda t, state: HSDIO(t, 23, state)
HF_freq = lambda t, state: HSDIO(t, 2, not state)  # NC

# Instrument Triggers ----------------------------------------------------------

NIScope_Trig = lambda t, state: HSDIO(t, 2, state)  #Not Set!
Zstage_Trig = lambda t, state: HSDIO(t, 2, state)  #Not Set!
MOT_Andor_Trig = lambda t, state: HSDIO(t, 2, state)  # Not Set!
Blackfly_Trig = lambda t, state: HSDIO(t, 15, state)
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
#XZ_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 25, 0)
Y_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 11, state)
# Y_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 11, state*0+1)
Y2_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 8, state)
# Y2_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 8, 1)
X_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 13, not (state))
# X_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 13, 0)
RP_Shutter_switch_init = lambda t, state: HSDIO(t, 7,state)
RP_Shutter_switch_init = lambda t, state: HSDIO(t, 7,1)
Cooling_Shutter_switch_init = lambda t, state: HSDIO(t, 12, not(state))
# Cooling_Shutter_switch_init = lambda t, state: HSDIO(t, 12, 0)
OP_Shutter_switch_init = lambda t, state: HSDIO(t, 10, not(not(state)))
# OP_Shutter_switch_init = lambda t, state: HSDIO(t, 10, 1)
OP_RP_Shutter_switch_init = lambda t, state: HSDIO(t, 6, state)
#OP_RP_Shutter_switch_init = lambda t, state: HSDIO(t, 6, 1)
Blowaway_Shutter_switch_init = lambda t, state: HSDIO(t, 2, state)  #Not Set!
Ryd595_Shutter_switch_init = lambda t, state: HSDIO(t, 2, not (state))  #Not Set!
Collection_Shutter_switch_init = lambda t, state: HSDIO(t, 5, state)
# Collection_Shutter_switch_init = lambda t, state: HSDIO(t, 5, 1)
RydRyd_switch = lambda t, state: HSDIO(t, 16, not state)

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
TestA0 = lambda t: AO(t, 1, 0.5)
MOT_coilsAO = lambda t, v: AO(t, 0, v)
HF_amplitude = lambda t, v: AO(t, 3, v)
#HF_amplitude = lambda t, v: AO(t, 3, 2.6)
vODT_power = lambda t, v: AO(t, 2, v)
r684_vva = lambda t, v: AO(t,7,v)

# FORT VVA -------------------------------------------------------------------------------------------------------------

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

def ramp_FORT(t,duration,pi,pf,dt=0.001):
    """
    Create a ramp of FORT power
    Args:
        t: start time (ms)
        duration: duration (ms)
        pi: initial power (fraction of max FORT power)
        pf: final power (fraction of max FORT power)
        dt: size of time steps (ms)

    Returns:

    """
    vi = FORT_cal(pi)
    vf = FORT_cal(pf)

    return  ramp(t, duration, vi, vf, 2, dt)


def ramp_ODTVVA(t,duration,vi,vf,dt=0.05):
    """
    Create a ramp of FORT power using the VVA control voltage directly
    Args:
        t: start time (ms)
        duration: duration of ramp (ms)
        vi: initial control voltage (V)
        vf: final control voltage (V)
        dt: size of time steps (ms)

    Returns:
        t: time after ramp
    """
    return ramp(t,duration,vi,vf,2,dt)

# FORT VVA 2 ---------------------------------------------------------------------------------------------------------------

def FORT2_cal(p):
    """
    uses Second FORT VVA calibration parameters to return voltage to D2 VVA that results in
    desired D2 output power (as a fraction of max power)
    Currently useless
    Args:
        p: desired D2 output power as a fraction of max power

    Returns:
        v_set: VVA set voltage that results in desired p
    """
    a = -3e-2
    b = 1.35e-2
    vt = 0

    v_set = vt+1/(2*b)*(-a+sqrt(a**2+4*b*p))
    return v_set

FORT_power2 = lambda t, p: vODT_power2(t,FORT2_cal(p*0+1))


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

def exp_biasAO(ti, duration, bias_i, bias_f, T, b, dt = .01):
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
    tf = ti+duration
    avec = [bias_f[i] - bias_i[i] for i in range(3)]
    funcs = lambda x : [avec[i]*(1-b*exp(-(x-ti)/T))+bias_i[i] for i in range(3)]
    times =  arange(ti,tf,dt)
    #print(times)
    for ts in times:
        biasAO(ts, funcs(ts))
        # print(funcs(ts))
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
    stage_dict = {'FORTLoading': (0,0), 'FORTLAC': (0,1), 'FORTRO': (1,1)}
    set = stage_dict[stage]

    # HSDIO(t, 16, set[0]) #DDS bit 0
    HSDIO(t, 31, set[1]) #DDS bit 1

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
    FORT_power(t,1)
    Ryd685_switch(t, 0)
    Ryd595_switch(t, 0)
    RP_Shutter_switch_init(t, 1)
    Cooling_Shutter_switch_init(t, 1)
    OP_Shutter_switch_init(t, 0)
    OP_RP_Shutter_switch_init(t, 0)
    OP_switch(t, 0)
    Blowaway_Shutter_switch_init(t, 0)
    SPCM_gate(t, 0)
    FORT_DDS(t,"FORTLoading")
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

def PGC1_and_TrapOn(t, PGC_1_time, hODT_delay, ODT_on=True, chop=True,coils_on=False, ramp_p = False):
    '''
    PGC1_and_TrapOn: Polarization Gradient Cooling and Trap On
    Runs PGC Sequence (detunes MOT laser and sets shims). Also triggers trap on.
    Args:
       t: Starting time (ms),
       PGC_1_time: PGC time in ms.
       hODT_delay: Delay time in ms for turning on dipole trap.
       ODT_on: Trap on if true.
       chop: Chopped Loading if True.
       coils_on:
       ramp_p: deprecated. Does nothing
    Returns:
        t: Ending time (ms)
    '''
    PGC_ramp_t = 2
    PGC_D2_p = 0.5

    D2_DDS(t, 'PGC1')
    biasAO(t, PGC1_shim)
    switch_T = 0.83
    #exp_biasAO(t,max(PGC_1_time,5*switch_T),MOT_shim,PGC1_shim,0.83,1,0.01)
    # vODT_switch(t+hODT_delay,ODT_on)
    HF_amplitude(t, PGC_1_hyperfine_power)
    vODT_switch(t + hODT_delay, ODT_on)
    if chop:
        print "Chopped loading enabled"
        ChoppedRO(t, PGC_1_time, period=2.1e-3, RO_onoff=[.01, .5],
                  Trap_onoff=[0.27, .72])
    else:
        vODT_switch(t + hODT_delay, ODT_on)
    t += PGC_1_time
    if coils_on:
        switchcoils(t - .2, False)

    return t

def PGC2(t, PGC_2_time,shim=PGC2_shim):
    '''
    PGC2: Secondary PGC
    Args:
        t: Starting time (ms)
        PGC_2_time: PGC time in ms.
    Returns:
         t: Ending time (ms)
    '''
    D2_DDS(t, 'PGC2')
    biasAO(t-1.5, shim)
    D2_switch(t,1)
    HF_switch(t,1)
    HF_amplitude(t, PGC_1_hyperfine_power)
    t += PGC_2_time
    D2_switch(t,0)
    HF_switch(t,0)
    return t

def Recool(t, recool_time, shims, chop=False):
    '''
    Recool: Recooling after Readout
    Args:
        t: Starting time (ms)
        recool_time: Recool time in ms.
        shims:
        chop:
    Returns:
        t: Ending time (ms)
    '''
    D2_DDS(t, 'Recool')
    t = biasAO(t, shims)

    # turn on the D2 and HF AOMs
    D2_switch(t, 1)
    HF_switch(t, 1)

    # open the X and Z shutters
    # closeShutters(t-8.5, False,False,False,delay=False)
    HF_amplitude(t-4, Recool_hyperfine_power)
    if chop:
        #t = ChoppedRO(t, recool_time, 2, RO_onoff=[0.1,0.5],Trap_onoff=[0.01,1.0])
        t = ChoppedRO_dcp(t, recool_time, 1e-3, ROdc = 0.35, Trapdc=0.5, phase=Recool_phi)
    else:
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
                           ROPowerToggle=False, SPCM_bins=30, trigger_andor=False, trigger_hm=False,
                           repump_power=None,shim=None,preshelve=False):
    """
    Readout phase.
    Args:
        t: start time (ms)
        OnTime: duration (ms)
        SPCM: If true, waveform made to accomodate readout with SPCM
        RO_bins: number of time bins to sub-divide counter data. Only useful if SPCM is True
        drops: number of fake bins before RO phase where accumulated counter counts are dumped (not real data)
        returnPower: Not in use
        chop: If true, D2 and FORT beams are chopped out of phase
        shuttersclosed: MOT beam shutter configuration during RO [XZ,Y,Y2,X]
        ROPowerToggle: No in use
        SPCM_bins: number of times to pulse the SPCM gate during RO. Usually SPCM_bins=RO_bins, choose different
            settings when debugging SPCM response
        trigger_andor: If true, andor is sent trigger during RO
        trigger_hm: If true, hammamatsu is sent trigger during RO
        repump_power: repumper power during RO (V). Default is "RO1_hyperfine_power" independent variable
        shim: shim settings during RO [X,Y,Z] (V)
        preshelve: If true, flash repumper on for 2ms before start of RO phase
    """
    # time per bin
    RO_bin_width = OnTime / float(RO_bins) / 2
    SPCM_bin_width = OnTime / float(SPCM_bins) / 2
    # print "RO_bins = {}".format(RO_bins)
    # print "RO_bin_width = {}".format(RO_bin_width)
    # print "SPCM_bins = {}".format(SPCM_bins)
    # print "SPCM_bin_width = {}".format(SPCM_bin_width)
    # print drops

    # Set up shutters and fields
    Collection_Shutter_switch(t - Collection_Shutter_delay_on, 1)
    if shim == None:
        t = biasAO(t, RO1_shim)
    else:
        t = biasAO(t, shim)
    closeShutters(t-4, shuttersclosed[0], shuttersclosed[1],
                      shuttersclosed[2], shuttersclosed[3])

    # set up pre-pulse dump bins
    tt = t - 2 * RO_bin_width * (drops)  # -1)
    # t = SPCMPulse(t,drops,RO_bin_width*2)
    # SPCM_gate(t,1)
    if SPCM:
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
    if preshelve:
        HF_switch(t,1)
        t+=2
    SPCM_gate(t, 1)
    D2_switch(t, 1)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
    HF_switch(t, 1)
#    D2_DDS(t, 'RO')

    if repump_power is None:
        HF_amplitude(t-2, RO1_hyperfine_power)
    else:
        HF_amplitude(t-4, repump_power)

    if chop:
        #ChoppedRO(t,OnTime,period=2e-3,RO_onoff=[0.01,.43+.05-0.20],Trap_onoff=[0.5,.99])
        tt=ChoppedRO(t,OnTime,period=0.5e-3,RO_onoff=[0.35,0.75],Trap_onoff=[0.05,.7])

        #ChoppedTrap(t,OnTime,period=2e-3,Trap_onoff=[0.5,.99])
        tend = 0
    else:
        tt=t+OnTime
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

    if SPCM:
        # Counter bins
        for i in range(RO_bins):
            SPCM_clock(t, 1)
            t += RO_bin_width
            SPCM_clock(t, 0)
            t += RO_bin_width
        t -= 2 * RO_bin_width
    else:
        t = tt
    # SPCMPulse(t,RO_bins,RO_bin_width*2)

    # turn off lasers, and done.
    SPCM_gate(t,0)
    D2_switch(t, 0)
    HF_switch(t, 0)
    # D2_DDS(t,'PGC1')
    return max(t, tend)


# ------------------------------------------------------------------------
#  LightAssistedCollisions: Light Assisted Collisions
#  Params: t: Starting time (ms), shimFields (optional): If True, set shim fields. shuttersclosed (optional): calls closeShutters to set shutters to values specified in shuttersclosed
#  Implicit params: LAC_time: Light-assisted collision duration (ms), LAC_hyperfine_power: Repump power during LAC, LAC_shim
#  Returns: t: Ending time (ms)
#  Turns on MOT beams in LAC profile to kick atoms out of the trap to make it single-atom
# ------------------------------------------------------------------------
def LightAssistedCollisions(t, shimFields=True, chop=False,
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
    if chop:
        ChoppedRO(t,LAC_Time,2e-3,RO_onoff=[.15,.43],Trap_onoff=[0.5,.99])
        t += LAC_Time
    else:
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
    #HF_switch(t, 0)
    vODT_switch(t, 0)
    D2_switch(t + RO_onoff[0] * period, 1)
    D2_switch(t + RO_onoff[1] * period, 0)
    #HF_switch(t + RO_onoff[0] * period, 1)
    #HF_switch(t + RO_onoff[1] * period, 0)
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

def OneChopTrap2(t, period, Trap_onoff, ch2, ch2_onoff, invert=False):
    vODT_switch(t, 1)
    vODT_switch(t + Trap_onoff[0] * period, 0)
    vODT_switch(t + Trap_onoff[1] * period, 1)

    HSDIO(t, ch2, not invert)
    HSDIO(t+ch2_onoff[0]*period,ch2, invert)
    HSDIO(t+ch2_onoff[1]*period,ch2, not invert)
    #HSDIO(t+period-.00001,ch2,invert)
    return t+period


def OneChopGen(t,  channel, period=2e-3, Trap_onoff=[0,0.5], invert=False):
    """
    Generic single chop for given HSDIO channel
    Args:
        t: float, start time of chop
        channel: int, channel that is chopped on and off
        period: float, chop period
        Trap_onoff: tuple[float,float], [0] start of on time, [1] end of on time (as fraction of period)

    Returns:
        end time
    """
    if invert:
        HSDIO(t, channel, 0)
        HSDIO(t+Trap_onoff[0]*period, channel, 1)
        HSDIO(t+Trap_onoff[1]*period, channel, 0)
    else:
        HSDIO(t, channel, 1)
        HSDIO(t+Trap_onoff[0]*period, channel, 0)
        HSDIO(t+Trap_onoff[1]*period, channel, 1)
    return t+period

def EndChopGen(t, channel, period=2e-3,invert=False):
    """
    Generic End chop for given HSDIO channel
    Args:
        t: float, start time for end chop
        channel: int, HSDIO channel being chopped
        period: float,  chopping period
        invert: Tuple[float,float], if true, chopping is inverted
    Returns:
        end time
    """
    t += period*2
    HSDIO(t,channel, 0+invert)
    return t

def OneChopOP(t, period=2e-3, Trap_onoff=[0, .5]):
    OP_switch(t, 0)
    OP_switch(t + Trap_onoff[0] * period, 1)
    OP_switch(t + Trap_onoff[1] * period, 0)
    return t + period


def EndChopOP(t, period=2e-3):
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
#    vODT_switch(t, 1)
    t += period
    vODT_switch(t, 1)
    t += period
    D2_switch(t, 0)
    HF_switch(t,0)
#    vODT_switch(t, 1)
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

def EndChopTrap2(t, period, Trap_onoff, ch2, ch2_onoff, invert):
    #vODT_switch(t+0.0001, 1)
    vODT_switch(t + Trap_onoff[0] * period+.0001, 0)
    vODT_switch(t + Trap_onoff[1] * period, 1)

    #HSDIO(t+.0001, ch2, not invert)
    HSDIO(t+ch2_onoff[0]*period,ch2, invert)
    #HSDIO(t+ch2_onoff[1]*period,ch2, not invert)
    #HSDIO(t+0.0001,ch2,invert)
    t += period*2
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

def ChoppedRO_dcp(t, RO_time, period, ROdc, Trapdc, phase):
    """
    Wrapper for Chopped RO that re-parameterizes it based on the Trap and RO duty cycles (dc)
    and the relative phase between them (trap_phase).
    Args:
        t: start time
        RO_time: duration of chopped RO phase
        period: chopping period
        ROdc: duty cycle of RO beams
        Trapdc: duty cycle of Trap beam
        phase: relative phase between trap and RO chops. When 0, RO and trap turn on at the same time.

    """
    start_eps = 0.005
    RO_start = max(1-ROdc,start_eps)
    RO_end = 1
    if RO_start-phase < 0:
        if ROdc+Trapdc < 1:
            ODT_start = 1-Trapdc
            ODT_end = 1
            RO_start = ODT_start-1+phase
            RO_end = RO_start+ROdc
        else:
            print("this is not a good waveform.")
    else:
        ODT_start = max(RO_start-phase,start_eps)
        ODT_end = min(ODT_start+Trapdc,1)


    print("ROdc {}; ODTdc {}".format(ROdc,Trapdc))
    print("phi = 2pi*{}".format(phase))
    print("RO_start {}; RO_end = {}; ODT_start {}; ODT_end {}".format(RO_start, RO_end, ODT_start,ODT_end))
    return ChoppedRO(
        t, 
        RO_time, 
        period, 
        RO_onoff=[RO_start,RO_end],
        Trap_onoff=[ODT_start,ODT_end]
    )
    pass

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

def ChoppedTrap2(t, RO_time, period=2e-3, Trap_onoff=[0.01,0.501], ch2=None, ch2_onoff=[0.01,0.501],invert=False):
    """

    Args:
        t: start time
        RO_time: total chopping time
        period: chopping period
        Trap_onoff: [start of on period, end of on period] normalized to period
        ch2: HSDIO channel to chop alongside FORT
        ch2_onoff: same as Trap_onoff for ch2

    Returns:
        t + RO_time
    """
    if ch2 is None:
        return ChoppedTrap(t, RO_time, period, Trap_onoff)
    else:
        repeats = int(RO_time/ period) + 1
        funct = lambda t: OneChopTrap2(t, period, Trap_onoff, ch2, ch2_onoff,invert)
        t = add_repeat(t, funct, repeats)
        return EndChopTrap2(t, period, Trap_onoff,ch2,ch2_onoff,invert)

def ChoppedFORTDDS(t, duration, period=2e-3, Trap_onoff=[0.01, .501]):
    repeats = int(duration / period) + 1
    funct = lambda t: OneChopGen(t, 31, period, Trap_onoff,invert=True)
    t = add_repeat(t, funct, repeats)
    return EndChopGen(t, 31, period, invert=False)

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
    # AO clock dt
    if init_v == fin_v:
        return t
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


def OnePulseRyd(t, pulse_time, trap_time, uW_enhance, ryd_595_on = True):
    """
    Args:
        t1: start time
        pulse_time: length of rydberg pulse
        trap_time: how long trap stays on between Rydberg pulses
    """
    t0 = t
    vODT_switch(t, 0)
    print("start time " + str(t))
    t1 = t + max(ryd685_timing, ryd595_timing)
    print("t1 " + str(t1))
    vODT_switch(t1, 0)
    Ryd685_switch(t1 + ryd685_timing, 1)
    Ryd595_switch(t1 + ryd595_timing, ryd_595_on)
    Ryd685_switch(t1 + ryd685_timing + pulse_time, 0)
    Ryd595_switch(t1 + ryd595_timing + pulse_time, 0)
    FORTshim = 350e-6
    t1 = t1 + pulse_time + FORTshim
    print("FORT on Time " + str(t1))
    vODT_switch(t1, 1)
    if uW_enhance:
        uW_switch(t1, 1)
        uW_switch(t1 + trap_time - 1e-3, 0)
    print("Return time " + str(t1+trap_time))
    vODT_switch(t1+trap_time,0)
    #Ryd595_switch(t1+trap_time, 1)
    return t1 + trap_time+.0001

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

def ChoppedRyd(t, pulse_time, repeats, uW_enhance=False, ryd_595_on = True):
    print("cycle time = {}".format(pulse_time+max(3e-3, pulse_time+0.5e-3)))
    funct = lambda t: OnePulseRyd(t, pulse_time, max(3e-3, pulse_time+0.5e-3), uW_enhance, ryd_595_on = ryd_595_on)
    t = add_repeat(t, funct, repeats)
    return EndChopRyd(t, pulse_time)
# ---------------------------------------------------------------------------------------------
# Calibration: creates a calibration pulse for easy readout of your relevant and/or sensitive powers
# params: t: Starting time(ms), calTime: Length of calibration pulse (ms)
# returns: t: Ending time(ms)
# ---------------------------------------------------------------------------------------------
def Calibration(t, calTime=3):
    # turn on the MOT Beams:
    trigNIDAQ(t)
    Blackfly_Trig(t, 1)
    Blackfly_Trig(t+1, 0)
    vODT_source_switch(t-1,1)
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

    t += calTime
    # trigger the NIDAQ
    #trigNIDAQ(t)
    t += calTime

    for sw in measured_switches:
        sw(t, 0)
    # Collection_Shutter_switch(t, 0)
    return t


TrapOn = True
ROPowerToggle = False
# DoChop=False

XZJitter = .7

gradient_during_pgc = True

ToF =False

RO_trap_depth = 1.3+1.0*0  # mK
Loading_trap_depth = 0.6 # mK
rel_power = Loading_trap_depth/RO_trap_depth
LAC_ODT_rel = LAC_ODTDepth/RO_trap_depth
ba_p = BA_FORT_Power/RO_trap_depth

# ----------------------------------------------------------------------------------------------------------------------
# START EXPERIMENT -----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
t = 0

print("MOT: " + str(MOT_shim))
print("PGC: " + str(PGC1_shim))
print("LAC: " + str(LAC_shim))
print("RO: " + str(RO1_shim))
print("Recool: " + str(Recool_shim))
print("OP: " + str(OP_shim))
print("Rydberg: " + str(ryd_shim))
print("uW: " + str(uW_shim))

if status=="idle" or BL or ryd_time == 0:
    # set Electrodes to be grounded
    print("Ground Electrodes")
else:
    print("Charge Electrodes")

TestA0(t)

FORT_power(t,1)
r684_vva(t,4.5*0+9)

initialize(t)
Collection_Shutter_switch(t,0)
# t0 = OP_RP_Shutter_switch(t,0)
trigZstage(t)
tp = t
t+=1
# Blowaway_Shutter_switch(t,1)
t = Calibration(t)
HF_freq(t,0)
vODT_source_switch(t,1)

t+=0.02

t += 1
FORT_power(t,rel_power)  #------------------------------------------------------------------------------------FORT power

rydberg_MOT_dep = False
if rydberg_MOT_dep:
    Ryd685_switch(t, 1)
    Ryd595_switch(t, 1)
vODT_switch(t+1,0)
t = MOT_load(t, MOT_loading_time,trigger_andor=not ToF,coils_on=gradient_during_pgc or ToF)  # DDS: MOT (0,0,0)
if rydberg_MOT_dep:
    Ryd685_switch(t-5, 0)
    Ryd595_switch(t-5, 0)
# MOT_Andor_Trig(tp+80,1)
# MOT_Andor_Trig(tp+81,0)

Blowaway_Shutter_switch(t - BA_Shutter_delay_off, 0)
# counterreadout(t-MOT_loading_time/4,RO_Time,chop=DoChop,RO_bins=RO1_bins,drops=RO1_drops,shuttersclosed=[0,0,0,0],ROPowerToggle=ROPowerToggle)

#ramp_FORT(t,PGC_1_time,0,1,dt=0.1)
vODT_switch(t,1)
t = PGC1_and_TrapOn(t, PGC_1_time, hODT_delay, ODT_on=TrapOn,
                    chop=False,coils_on= (not ToF) and gradient_during_pgc, ramp_p = False)  # DDS: PGC1 (0,0,1)


#t = PGC2(t, PGC_2_time)
D2_DDS(t+0.01,'PGC2')

closetheshutters = [closeXZShutter, closeYShutter, closeY2Shutter,
                    closeXShutter]
print closetheshutters

# ---------------------------------------------------------
# TO measure MOT Temp: set ToF to true, vary Drop_Time (not DropTime), increase MOT loading time
# MOT Temperature
if ToF:
    biasAO(t,PGC1_shim)
    t = holdinDark(t,Drop_Time)


    #Grey Coding
    D2_DDS(t+0.01,"MOT")
    t+=0.01
    # t += 0.05
    # D2_DDS(t-.04,'PGC2')
    # D2_DDS(t-0.03,'LAC')
    # D2_DDS(t-0.02,'Recool')
    # D2_DDS(t-0.01,'RO')

    #Trigger andor
    MOT_Andor_Trig(t,1)
    MOT_Andor_Trig(t+1,0)

    #On and off the RO lights
    D2_switch(t, 1)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
    HF_switch(t, 1)
    HF_amplitude(t - 0.1, RO1_hyperfine_power)
    t += AndorExpT
    D2_switch(t,0)
    HF_switch(t,0)
    HF_amplitude(t,0)
    #D2_DDS(t,'Recool')
    switchcoils(t, False)
# ----------------------------------------------------------

t = holdinDark(t,10)

if False and DropTime > 0:
    t = holdinDark(t, 1)
    t = TrapPulseOff(t, DropTime / 1000, ODT_on=TrapOn)  # comment out
    t = holdinDark(t, 1)
#switchcoils(t,0)

#t = PGC2(t, PGC_2_time=PGC_2_time, shim=PGC2_shim)
# D2_DDS(t-0.01, "LAC")
# D2_DDS(t-0.005, "Recool")
# t = Recool(t, recool_time=PGC_2_time, shims=Recool_shim)

biasAO(t+1,LAC_shim)
t = holdinDark(t, 3)

D2_DDS(t, 'LAC')
LAC_RO = True
#t = closeShutters(t-4*0, *closetheshutters, delay=False)
t = holdinDark(t,1)

#FORT(t,
# t=ramp_FORT(t,5,0,0.5,0.1)
if not LAC_RO:
    if LAC_Time > 0:
        #t=ramp_FORT(t, 14, 0.5, 1, 0.1)
        #ramp_FORT(t-1,4,0.5,0.4*0.5,0.1)
        t += 1.5
        print("time before LAC = {}. Expected time after LAC = {}".format(t, t + LAC_Time + 2))
        t = LightAssistedCollisions(t, chop=False, shuttersclosed=[0,0,0,0])
    else:
        t+=1.5
    #t = LightAssistedCollisions(t, chop=True,shuttersclosed=[0, 0, 0, 0])
    t=holdinDark(t,1)
    if LAC_Time > 0:
        pass
        #ramp_FORT(t, 14, 0.4*0.5, 1, 0.1)
    else:
        pass
        # ramp_FORT(t, 14, 0.5, 1, 0.1)
else:
    pass
    #ramp_FORT(t, 14, 0.5, 1, 0.1)




D2_DDS(t-0.1, 'Recool')
Collection_Shutter_switch(t,1)
biasAO(t, RO1_shim)
D2_DDS(t-0.05,"LAC")
D2_DDS(t,"PGC2")
t = PGC2(t, PGC_2_time, PGC2_shim)
#t = Recool(t, PGC_2_time, PGC2_shim)  # TODO Uncouple the length of this recool phase from the one between RO
t = closeShutters(t-4*0, *closetheshutters, delay=False)
t = holdinDark(t,Trap_Hold_time/2)

t += XZJitter

t = holdinDark(t, Trap_Hold_time/2)

t+=1
D2_DDS(t,'Recool')
t+=0.01

# t= BlowawayPulse(t,50)
# t+=10

# Blowaway_Shutter_switch(t-2,0)

# t = triggerNIScope(t)
# t0 = t

# t = holdinDark(t,5)
# t = BlowawayPulse(t,20)
# t = holdinDark(t,5)

#t = TrapPulseOff(t,10,ODT_on=TrapOn)

# Ryd595_Shutter_switch(t-Ryd595_Shutter_delay_on,1)
# t = holdinDark(t,25)
#t = TrapCenterFluorescence(t, LAC_Time, chop=DoChop, RO_bins=RO1_bins,
#                           drops=RO1_drops, shuttersclosed=closetheshutters,
#                           ROPowerToggle=ROPowerToggle, SPCM_bins=SPCM_gates)


if LAC_RO and LAC_Time > 0:
    ramp_FORT(t-5,5,rel_power,LAC_ODT_rel,dt=0.01)
    print("LAC_see")
    print(LAC_Time)
    D2_DDS(t,"LAC")
    t += 1
    t = TrapCenterFluorescence(t, LAC_Time, SPCM=False, chop=DoChop, RO_bins=RO1_bins,
                               drops=RO1_drops, shuttersclosed=closetheshutters,
                               ROPowerToggle=ROPowerToggle, SPCM_bins=SPCM_gates,
                               repump_power=LAC_hyperfine_power,shim=LAC_shim)
    D2_DDS(t,"Recool")
    ramp_FORT(t,5,LAC_ODT_rel,rel_power,dt=0.01)
t=holdinDark(t,10)

# adiabatic boiling
boiling = False
if boiling:
    t = ramp_ODTVVA(t,5,10,zzz,dt=0.01)
    t = holdinDark(t,3)
    t = ramp_ODTVVA(t,5,zzz,10,dt=0.01)

t = ramp_FORT(t,5,rel_power,1,dt=0.1) #-------------------------------------------------------------------------------
#t = ramp_FORT(t,5,rel_power,zzz,dt=0.1)
# vODT_switch(t,0)
HF_freq(t,1)
D2_DDS(t,"RO")
Collection_Shutter_switch(t-Collection_Shutter_delay_on-1, 1)
Hamamatsu_Trig(t + Hamamatsu_Trig_Shim + 10.85, 1)
Hamamatsu_Trig(t + Hamamatsu_Trig_Shim + 10.85 + RO_Time, 0)
t = TrapCenterFluorescence(t, RO_Time, chop=DoChop, RO_bins=RO1_bins,
    drops=RO1_drops, shuttersclosed=closetheshutters,
    ROPowerToggle=ROPowerToggle, SPCM_bins=SPCM_gates)
t = ramp_FORT(t,5,1,rel_power,dt=0.1) #-------------------------------------------------------------------------------
#t = ramp_FORT(t,5,zzz,rel_power,dt=0.1)

#Post-RO Recool
Collection_Shutter_switch(t, 0)
recool2_time = Recool_time
if recool2_time > 0:
    biasAO(t-1,Recool_shim)
    X_Only_Shutter_switch(t-3,1)
    closeShutters(t-2.5, 0, 0, 0, 0, delay=False)
    # ramp_FORT(t+5, 5, rel_power, zzz, dt=0.01)
    t=holdinDark(t,7.5)
    # t=holdinDark(t,X_Shutter_delay_on+5)
    t0 = t
    t = Recool(t+0.1, recool2_time,Recool_shim,chop=True*0)
    # ramp_FORT(t, 5, zzz, rel_power, dt=0.01)
    if BL:
        if recool2_time > 3:
            closeShutters(t+1,*closetheshutters,delay=False)
        else:
            closeShutters(t+4,*closetheshutters,delay=False)
else:
    t += 5
t += 5
# t=holdinDark(t,uW_time)
# Ryd595_Shutter_switch(t-Ryd595_Shutter_delay_off,0)
# t0 = TrapPulseOff(t0,RO_Time,ODT_on=TrapOn)

t = holdinDark(t,GapTime) # --- retention
#t = TrapPulseOff(t,GapTime) # --- SNR
# # drop recapture
trap_osc = False  # if true, measure transverse trap frequency using French Method, else drop-recapture
if trap_osc:
    t= holdinDark(t,1)
    t = TrapPulseOff(t,Drop1_Time/1000,ODT_on=TrapOn)
    t += osc_time/1000
    t = TrapPulseOff(t,DropTime/1000,ODT_on=TrapOn)
else:
    if DropTime > 0 and False:
        t = holdinDark(t,1)
        t = TrapPulseOff(t,DropTime/1000, ODT_on=TrapOn) #comment out
        t = holdinDark(t,1)

# parametric heating
if ChopTime > 0:
    chop_period = 1.0/Chop_freq
    off_time = 4.0e-3  #ms
    if off_time < chop_period/2:
        onoff=[1-off_time/chop_period,0.99]
    else:
        onoff=[0.5,0.99]
    onoff=[0.5,0.9]
#    print(off_time,chop_period,onoff)
    t = ChoppedFORTDDS(t, ChopTime, chop_period, Trap_onoff=onoff)
    #t = ChoppedTrap(t, ChopTime, chop_period, Trap_onoff=onoff)


# closeShutters(t,1,1,1,1)
# Ryd595_Shutter_switch(t,1)
# closeShutters(t,*closetheshutters,delay=False)

#t = holdinDark(t, GapTime)						# Retention
#t = TrapPulseOff(t, GapTime, ODT_on=TrapOn) 					# SNR

# MicrowavePulse(t-.01,0,0.01,uWchop)
# RydPulse(t,RamseyTime,[False,True])
# MicrowavePulse(t+RamseyTime,0,0.01,uWchop)

# Shelve and Blowaway experiment
# D2_DDS(t-0.01,'RO')
# t = shelve_and_blowaway(t,sTime=15,sState=3,blowaway=False)
# t = shelve_and_blowaway(t, sTime=shelve_time, sState = shelve_state, blowaway=True)

# OP BlowAway Experiment
# t = holdinDark(t,4)
# t = shelve_and_blowaway(t,shelve_time,shelve_state,blowaway=False,toRO=False)
# t = holdinDark(t,1)#+OP_shelve_time)
# t = ShimSweep(t,1,RO1_shim,OP_shim)
# t = holdinDark(t,2.0)
# t = OpticalPumping(t, OP_Time, shelve_time=OP_shelve_time,chop=OP_chop) #uncomment
# closeShutters(t,*closetheshutters,delay=False)
# Cooling_Shutter_switch(t,1)
# RP_Shutter_switch(t,1)
# t = holdinDark(t,GapTime)
# t=holdinDark(t,1.0)
# t = ShimSweep(t,1,OP_shim,RO1_shim)

# UWRabiExperiment
# t = holdinDark(t,4)
# t = shelve_and_blowaway(t,shelve_time,shelve_state,blowaway=False,toRO=False)
# t = holdinDark(t,1)#+OP_shelve_time)
# t = ShimSweep(t,1,RO1_shim,OP_shim)
# t = holdinDark(t,2.0)
# t = OpticalPumping(t, OP_Time, shelve_time=OP_shelve_time,chop=OP_chop) #uncomment
# closeShutters(t,1,0,1,0,delay=False)
# t = MicrowavePulse(t, pre_uW_time, uW_time,uWchop)
# t = holdinDark(t,GapTime)
# t=holdinDark(t,1.0)
# t = ShimSweep(t,1,OP_shim,RO1_shim)
# t=holdinDark(t,6)
# D2_DDS(t-0.01,'RO')
# t = Blow_Away(t, [True,False,False],BAChop)
# t = holdinDark(t,RP_Shutter_delay_on)#+Blow_Away_time)
# RP_Shutter_switch(t-RP_Shutter_delay_on,1)
# Cooling_Shutter_switch(t,1)
# t = holdinDark(t,15)

##UWRamseyExperiment
# This Block of code is useful for aligning the 595nm beam to the trap.
# t = holdinDark(t,4)
# t = shelve_and_blowaway(t,shelve_time,shelve_state,blowaway=False)
# t = holdinDark(t,5)#+OP_shelve_time)
# t = ShimSweep(t,1,RO1_shim,OP_shim)
# t = holdinDark(t,2.0)
# t = OpticalPumping(t, OP_Time, shelve_time=OP_shelve_time,chop=OP_chop) #uncomment
# t= holdinDark(t,0.5)
# t = MicrowavePulse(t,0, uWPiTime/2,uWchop)
# t = RydPulse(t,RamseyTime,RydOn=[False,True])##for AC Stark shift
# t = holdinDark(t,RamseyTime)##for Dark Ramsey
# t = MicrowavePulse(t,0, uWPiTime/2,uWchop)
# t=holdinDark(t,4.0)
# t = ShimSweep(t,1,OP_shim,RO1_shim)
# t=holdinDark(t,6)
# D2_DDS(t-0.01,'RO')
# t = Blow_Away(t, [True,False,False],BAChop)
# t = holdinDark(t,RP_Shutter_delay_on)#+Blow_Away_time)
# RP_Shutter_switch(t-RP_Shutter_delay_on,1)
# Cooling_Shutter_switch(t,1)
# t = holdinDark(t,15)

# t = Depump(t, shelve_time=OP_shelve_time,chop=OP_chop)
# t = holdinDark(t,0.5)
# t = MicrowavePulse(t, pre_uW_time, uW_time)
# t=holdinDark(t,4.0)
# t = holdinDark(t,3.5)

ba_delay = 15
current_shim = Recool_shim
if BL:
    bad_op = False
    if OP_Time > 0 and bad_op:
        closeShutters(t,*[1,1,0,1],delay=False)
        OP_RP_Shutter_switch(t-1,1)
        OP_DDS(t,0)
        t+= RP_Shutter_delay_off
        OP_switch(t,1)
        HF_switch(t,1)
        HF_amplitude(t,OP_HF_amplitude)
        t+= OP_Time
        OP_switch(t,0)
        HF_switch(t,0)
        OP_RP_Shutter_switch(t,1)
        RP_Shutter_switch(t,1)

    closeShutters(t + 3, *closetheshutters, delay=False)
    Cooling_Shutter_switch(t, 1)
    t = holdinDark(t, ba_delay + 1)

    # Rough Rydberg
    bad_ryd = False

    if bad_ryd and ryd_time > 0:
        if ryd_chops > 1:
            print(ryd_chops)
            HF_switch(t, 1)
            HF_amplitude(t, 4)
            t += 4
            HF_switch(t, 0)
            HF_amplitude(t, 0)
            t = ChoppedRyd(t, ryd_time * 1e-3, int(ryd_chops), uW_enhance=False)
        else:
            ryd_time = ryd_time * 1e-3
            Ryd595_switch(t - ryd595_timing, 1)
            Ryd685_switch(t - ryd685_timing + ryd_time, 0)
            Ryd595_switch(t - ryd595_timing + ryd_time, 0)
            t = TrapPulseOff(t - 1e-3, ryd_time + 1.0e-3, ODT_on=True)
            t = holdinDark(t, 5e-3)
    t = ramp_FORT(t,5,rel_power,1,dt=0.1)
else:
    # Shelve into hyperfine levels ------------------------------------------------------------ Shelving
    if abs(shelve_time) > 0:
        t += 1
        D2_DDS(t-0.03, 'Recool')
        #D2_DDS(t-0.02, 'RO')
        #D2_DDS(t-0.01, "BA")
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
        #t = holdinDark(t,5)
        t0 = t
        # OPRP from MOT paths
        # if OP_Time == 0 and OP_shelve_time == 0 and uW_time ==0:
        #   closeShutters(t, *[1, 0, 1, 1], delay=False)
        # OPRP from MuxJr path
        closeShutters(t-1, *[1, 0, 1, 1], delay=False)
        # D2_switch(t, 1)

    if AerotechTrigger:
        Aerotech_z_trig(t,1)
        t += 5
        Aerotech_z_trig(t,0)
        t += aerotech_rise_time
        timing_trig(t, 1)
        timing_trig(t+1, 0)

    # OP pulse -------------------------------------------------------------------------------------- OP
    if OP_Time > 0:
        # AO(t-4, 3, 0)
        Cooling_Shutter_switch(t, 0)
        # OPRP from MuxJr path
        # closeShutters(t, *[1, 1, 1, 1], delay=False)
        t = max(ShimSweep(t, 5, current_shim, OP_shim),holdinDark(t, 4))
        t += 5  # let low BW shims settle
        current_shim=OP_shim
        OP_switch(t, 1)
        # HF_switch(t, 0)
        HF_switch(t, 1)
        HF_amplitude(t-4, OP_HF_amplitude)
        # OPRP from MuxJr path
        OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_on, 1)
        t += OP_Time
        OP_switch(t, 0)
        HF_switch(t, 0)
        t = holdinDark(t, 1)
        RP_Shutter_switch(t,0)

        OPdrc = True# drop recapture after OP phase
        if OPdrc:
            if DropTime > 0:
                t = holdinDark(t, 1)
                t = TrapPulseOff(t, DropTime / 1000, ODT_on=TrapOn)  # comment out
                t = holdinDark(t, 1)

        if abs(OP_shelve_time) == 0:
            OP_switch(t, 0)
            HF_switch(t, 0)
            t = holdinDark(t, 1)
        if abs(OP_shelve_time) > 0 or (uW_time == 0 and ryd_time > 0):
            pass
        elif uW_time>0 :
            print("UW")
            t0=t
        elif Blow_Away_time>0:
            print("BA")
            OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_off+6, 0)
            t0 = t
        else:
            print("RO")
            OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_off+6, 0)
            t0 = t

    # print("abs(OP_shelve_time) = {}".format(abs(OP_shelve_time)))
    # print("RO1 Shim = {}".format(RO1_shim))
    # OP shelve ------------------------------------------------------------------------------ OP shelve
    OP_shelve_init = OP_shelve_time*0
    if abs(OP_shelve_time) > 0:
        # print("abs(OP_shelve_time) = {}".format(abs(OP_shelve_time)))
        if OP_Time == 0:
            # print("optiem".format(abs(OP_shelve_time)))
            t = holdinDark(t, 1)
            Cooling_Shutter_switch(t, 0)
            # closeShutters(t, *[1] * 4, delay=False)
            t = ShimSweep(t, 5, current_shim, OP_shim)
            current_shim = OP_shim
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
        #RP_Shutter_switch(t, 0)
        if Blow_Away_time > 0:

            # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
            t0 = t

    # OP shelve ------------------------------------------------------------------------------ OP shelve
    # Shelve into F=4 state no matter what
    if OP_shelve_init > 0:
        OP_shelve_time_p = -5
        # print("abs(OP_shelve_time) = {}".format(abs(OP_shelve_time)))
        if OP_Time == 0:
            # print("optiem".format(abs(OP_shelve_time)))
            t = holdinDark(t, 1)
            Cooling_Shutter_switch(t, 0)
            # closeShutters(t, *[1] * 4, delay=False)
            t = ShimSweep(t, 5, current_shim, OP_shim)
            current_shim = OP_shim
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
        if uW_time == 0:
            # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
            t0 = t

    if ryd_time > 0:
        t = ShimSweep(t,5,current_shim,ryd_shim)
        current_shim = ryd_shim
        t+=3
        chop_ryd = ryd_chops > 1
        q_depump=False
        if chop_ryd:
            t = ChoppedRyd(t, ryd_time*1e-3, int(ryd_chops), uW_enhance=False)
            t+=3

        elif q_depump:
            pulse_time = 3e-3
            comp_chops = (1e-3*ryd_time)//pulse_time
            print(comp_chops, pulse_time)
            t = ChoppedRyd(t, pulse_time, int(comp_chops), uW_enhance=False,ryd_595_on=False)
        else:
            print("No chops")
            ryd_time = ryd_time*1e-3
            Ryd685_switch(t-ryd685_timing+.5e-3,1)
            Ryd595_switch(t-ryd595_timing+.5e-3,1)
            Ryd685_switch(t-ryd685_timing+ryd_time+.5e-3,0)
            Ryd595_switch(t-ryd595_timing+ryd_time+.5e-3,0)
            RydDRC = False
            if RydDRC:
                t = TrapPulseOff(t-1e-3, ryd_time + 1.5e-3 + DropTime/1000, ODT_on=True)
            else:
                t = TrapPulseOff(t - 1e-3, ryd_time + 1.5e-3, ODT_on=True)
            # Pulse on uW field to expedite photoionization
            uW_switch(t,1)
            uW_switch(t+2e-3,0)
            t = t +ryd_time
            t = holdinDark(t, 5e-3)
        if Blow_Away_time == 0:
            pass
        else:
            t0=t

    if uW_time > 0:
        ryd_uw = False
        if ryd_uw:
            if current_shim != ryd_shim:
                t = ShimSweep(t, 5, current_shim, ryd_shim)
                current_shim = ryd_shim
        else:
            t = ShimSweep(t, 5, current_shim, uW_shim)
            current_shim = uW_shim
        t += 5

    if uW_time > 0 and RamseyTime == 0:

        print("Here")
        t = holdinDark(t,3)
        uW_switch(t, 1)
        t+= uW_time
        uW_switch(t, 0)

        uWdrc = True # drop recapture during uW phase
        if uWdrc:
            if DropTime > 0:
                t = holdinDark(t, 1)
                t = TrapPulseOff(t, DropTime / 1000, ODT_on=TrapOn)  # comment out
                t = holdinDark(t, 1)
        # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open
        OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_off+6, 0)
        t0 = t

    if RamseyTime > 0:
        #print("Here")
        t = holdinDark(t,13)
        uW_switch(t,1)
        t += uW_time/2  # make your pulse length a pi pulse
        uW_switch(t,0)

        ramsey_chop=False
        q_ramsey=True
        ramsey_drc = False
        if ramsey_drc:
            if DropTime > 0:
               t = TrapPulseOff(t+0.05,DropTime/1000, ODT_on=TrapOn) #comment out

        if ramsey_chop:
            dc = 0.5  # fraction of chop time where FORT is OFF
            t=ChoppedTrap(t,RamseyTime/dc,period=1e-3,Trap_onoff=[0.01,dc+0.01])
        elif q_ramsey:
            t += RamseyTime / 2
            t0=t+3e-3  # add a 1 us shim
            #t = TrapPulseOff(t, 21e-3)  # turn FORT off for 11us
            t = t+21e-3
            Ryd685_switch(t0 + ryd685_timing, 1)
            Ryd685_switch(t0 + ryd685_timing + q_ramsey_t, 0)
            t += 14e-3
            t += RamseyTime / 2
        else:
            t+= RamseyTime
        uW_switch(t,1)
        t += uW_time/2  # make your pulse length a pi pulse
        uW_switch(t,0)
        t += 2

        t0=t

    if AerotechTrigger:
        timing_trig(t, 1)
        timing_trig(t+1, 0)
        t += aerotech_fall_time
        timing_trig(t, 1)
        timing_trig(t+1, 0)

    # Blow Away ------------------------------------------------------------------------------ Blow Away
    if Blow_Away_time > 0:
        RP_Shutter_switch(t,0)
        # Blow Away Pulse
        try:
            closeShutters(t, *[1, 0, 1, 1], delay=False)
            t0 += 0.5
        except NameError:
            closeShutters(t, *[1, 0, 1, 1], delay=False)
            t0 = t + 0.5
        Cooling_Shutter_switch(t, 1)
        t0 = max(ramp_FORT(t,5,rel_power,ba_p,dt=0.01),ShimSweep(t,5,current_shim,BA_shim))
        Cooling_Shutter_switch(t,1)
        current_shim = BA_shim

        #if not zzz:
        # closeShutters(t, *[1, 0, 1, 1], delay=False)  # Leave just Y1 open

        # RP_Shutter_switch(t0, 0)
        t = t0  # max(t0, t)
        t = holdinDark(t,0.5)
        D2_DDS(t-0.001, "RO")
        D2_DDS(t, "BA")
        D2_switch(t, 1)
        HF_switch(t, 0)
        #HF_switch(t, zzz)
        # HF_amplitude(t,4.0)
        t += Blow_Away_time
        D2_switch(t, 0)
        Cooling_Shutter_switch(t,0)
        # if not zzz:
        # RP_Shutter_switch(t, 1)
        closeShutters(t+3, *closetheshutters, delay=False)
        t = holdinDark(t, 1)
        t = max(ShimSweep(t+1, 3, current_shim, RO1_shim), ramp_FORT(t, 5, ba_p, 1, dt=0.01))
        t += 1
        t = holdinDark(t, ba_delay)
    else:
        t+=0.5
        D2_DDS(t+.01,"BA")
        D2_DDS(t+0.02,"RO")
        Cooling_Shutter_switch(t, 1)
        if current_shim == RO1_shim:
            t = ramp_FORT(t, 5, rel_power, 1,dt=0.1)  # -------------------------------------------------------------------------------
        else:
            t = max(ramp_FORT(t, 5, rel_power, 1, dt=0.1), ShimSweep(t, 3, current_shim, RO1_shim))
        closeShutters(t+4, *closetheshutters, delay=False)
        t = holdinDark(t, ba_delay+1)

# t = max(t, t0)

#closeShutters(t, *closetheshutters)
#t = holdinDark(t,X_Shutter_delay_off+11)
#t = trigZstage(t)
# t = holdinDark(t,25)
HF_amplitude(t, 2.6)
# closeShutters(t-ba_delay/2, *closetheshutters, delay=False)
t+=3
RP_Shutter_switch(t,1)
Collection_Shutter_switch(t - Collection_Shutter_delay_on, 1)
#t = ramp_FORT(t,5,rel_power,zzz,dt=0.1)

D2_DDS(t,"RO")
Hamamatsu_Trig(t + Hamamatsu_Trig_Shim + 10.85, 1)
Hamamatsu_Trig(t + Hamamatsu_Trig_Shim + 10.85 + RO_Time, 0)
# TrapPulseOff(t, RO_Time, ODT_on=TrapOn)     #FORT Off/On
Cooling_Shutter_switch(t-3,1)
t = TrapCenterFluorescence(t, RO_Time, chop=DoChop, RO_bins=RO1_bins,
    drops=RO1_drops, shuttersclosed=closetheshutters,
    ROPowerToggle=ROPowerToggle, SPCM_bins=SPCM_gates,preshelve=True)
Collection_Shutter_switch(t, 0)
t = ramp_FORT(t,5,1,rel_power,dt=0.1) #--------------------------------------------------------------------------------
#t = ramp_FORT(t,5,zzz,rel_power,dt=0.1)
switchcoils(t, True)
closeShutters(t+10, False, False, False, False, delay=False)
t = holdinDark(t, 25*1.0)
#t += 20
t = TrapPulseOff(t, 2, ODT_on=TrapOn)

#initialize(t)
FORT_power(t,1)
t = MOT_load(t, 1, False, coils_on=True)
Ryd595_switch(t,0)
Ryd685_switch(t,0)
HF_switch(t, 0)
#OP_switch(t, 1)
#OP_DDS(t, 1)