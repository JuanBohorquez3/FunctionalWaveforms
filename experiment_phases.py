# functions that serve as phases for the hybrid experiment

from hybrid_wave_functions import *


# ------------------------------------------------------------------------
#  initialize: Initializes all channels
#  Params: t: Starting time (ms)
#  Returns: t: Ending time (ms)
#  Sets all channels to their initial conditions
# ------------------------------------------------------------------------
def initialize(t):
    """
    Sets Idle state of all HSDIO Channels to be zero with the exception of shutters, then
    initializes all channels to a convenient initial state
    """
    for channel in hsdio_channels:
        if channel in shutter_switches:
            channel(t, 1)
        else:
            channel(t, 0)

    vODT_switch(t, 1)
    vODT_power(t, vertTrapPower)
    Ryd685_switch(t, 0)
    Ryd595_switch(t, 1)
    RP_Shutter_switch_init(t, 1)
    Cooling_Shutter_switch_init(t, 1)
    OP_Shutter_switch_init(t, 0)
    OP_RP_Shutter_switch_init(t, 0)
    OP_switch(t, 0)
    Blowaway_Shutter_switch_init(t, 0)
    SPCM_gate(t, 0)
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
def Recool(t, recool_time):
    D2_DDS(t, 'Recool')
    t = biasAO(t, Recool_shim)

    # turn on the D2 and HF AOMs
    D2_switch(t, 1)
    HF_switch(t, 1)

    # open the X and Z shutters
    # closeShutters(t-8.5, False,False,False,delay=False)
    HF_amplitude(t, Recool_hyperfine_power)
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
    print "RO_bins = {}".format(RO_bins)
    print "RO_bin_width = {}".format(RO_bin_width)
    print "SPCM_bins = {}".format(SPCM_bins)
    print "SPCM_bin_width = {}".format(SPCM_bin_width)
    print drops

    # set up pre-pulse dump bins
    tt = t - 2 * RO_bin_width * (drops)  # -1)
    # t = SPCMPulse(t,drops,RO_bin_width*2)
    # SPCM_gate(t,1)
    for i in range(drops):
        SPCM_clock(tt, 1)
        SPCM_gate(tt, 1)
        tt += RO_bin_width
        SPCM_clock(tt, 0)
        SPCM_gate(tt, 0)
        tt += RO_bin_width
    # t-=2*RO_bin_width

    # turn on pulse light
    # FORT_DDS(t,"FORTRO")
    Collection_Shutter_switch(t - Collection_Shutter_delay_on, 1)
    t = biasAO(t + ROShimTimeOffset, RO1_shim)
    t = closeShutters(t, shuttersclosed[0], shuttersclosed[1],
                      shuttersclosed[2], shuttersclosed[3])

    D2_switch(t, 1)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
    HF_switch(t, 1)
    D2_DDS(t, 'RO')

    HF_amplitude(t - 0.1, RO1_hyperfine_power)

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
    tt = t
    for i in range(SPCM_bins):
        SPCM_gate(tt, 1)
        tt += SPCM_bin_width
        tt += SPCM_bin_width
        SPCM_gate(tt - 0.01, 0)

    # Counter bins
    for i in range(RO_bins):
        SPCM_clock(t, 1)
        t += RO_bin_width
        SPCM_clock(t, 0)
        t += RO_bin_width
    t -= 2 * RO_bin_width
    # SPCMPulse(t,RO_bins,RO_bin_width*2)

    # turn off lasers, and done.
    # SPCM_gate(t,0)
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


def switchcoils(t, state):
    MOT_coils_switch(t, state)
    MOT_coilsAO(t, MOTAOVolt(MOT_Coil_Current) * state)


# ---------------------------------------------------------------------------------------------
# Calibration: creates a calibration pulse for easy readout of your relevant and/or sensitive powers
# params: t: Starting time(ms), calTime: Length of calibration pulse (ms)
# returns: t: Ending time(ms)
# ---------------------------------------------------------------------------------------------
def Calibration(t, calTime=3):
    # turn on the MOT Beams:
    Cooling_Shutter_switch(t, 1)
    closeShutters(t, 0, 0, 0, 0, delay=False)
    D2_switch(t, 1)
    D2_DDS(t, 'MOT')
    # turn off the Repumper
    HF_switch(t, 0)
    HF_amplitude(t, 0)
    Ryd595_switch(t, 1)

    t += calTime
    # trigger the NIDAQ
    trigNIDAQ(t)
    t += calTime

    Ryd595_switch(t, 0)
    Collection_Shutter_switch(t, 1)
    return t