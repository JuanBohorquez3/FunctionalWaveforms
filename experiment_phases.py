# Functions to produce useful experimental sequences

from hybrid_wave_functions import *


# FORT utility pulses ------------------------------------------------------------------------------
def trap_in_dark(t, duration):
    """
    Turns off MOT beams and holds atoms in FORT
    Args:
        t (float): Start time (ms)
        duration (float): how long trap is on in darkness (ms)

    Returns:
        t (float): End time (ms)
    """
    vODT_switch(t, 1)
    D2_switch(t, 0)
    HF_switch(t, 0)
    t += duration
    return t


def trap_pulse_off(t, duration, trap_on=True):
    """
    Switches off the FORT for duration
    Args:
        t (float): Start time (ms)
        duration (float): how long trap is off (ms)
        trap_on (bool): If true FORT is turned back on at the end of the phase

    Returns:
        t (float): End time (ms)
    """
    vODT_switch(t, 0)
    t += duration
    vODT_switch(t, trap_on)
    return t


# useful beam and rf pulses ------------------------------------------------------------------------
def blowaway_pulse(t, duration):
    """
    Pulse the beam at the output of the blowaway path
    Args:
        t (float): start time (ms)
        duration (float): duration of blowaway pulse (ms)

    Returns:
        t (float): end time (ms)
    """
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 0)
    Blowaway_Shutter_switch(t, 1)

    D2_DDS(t, 'BA')
    D2_switch(t, 1)
    HF_switch(t, 0)
    HF_amplitude(t, RO1_hyperfine_power)

    t += duration

    D2_switch(t, 0)
    HF_switch(t, 0)
    Blowaway_Shutter_switch(t, 0)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_off, 1)

    return t


def microwave_pulse(t, delay, duration, chop=False):
    """
    Pulses on 9GHz microwave for uW_time.
    Args:
        t (float): Start time (ms)
        delay (float): delay before beginning microwave pulses
        duration (float): duration of microwave pulse
        chop (bool): if true, trap is chopped during microwave pulse

    Returns:
        t (float): End time (ms)
    """

    t += delay
    if chop:
        # vODT_power(t,vertTrapPowerChop)
        chopped_trap(t, duration, period=1e-3, trap_duty_cycle=(0.2, 0.41))

    pulse(t, duration, uW_switch)
    return t


def rydberg_pulse(t, duration, on_beams=None):
    """
    Pulses on rydberg beams
    Args:
        t (float): Start time (ms)
        duration (float): pulse duration
        on_beams (tuple): tuple of 2 bools, determining which of the beams are on.
            [684nm, 595nm]. Default is [True, True] (both beams on)

    Returns:
        t (float): End time (ms)
    """
    on_beams = [True, True] if on_beams is None else on_beams
    if on_beams[0]:
        pulse(t, duration, Ryd685_switch)
    if on_beams[1]:
        pulse(t, duration, Ryd595_switch)

    t += duration

    return t


# Initialization an calibration --------------------------------------------------------------------
def initialize(t):
    """
    Sets Idle state of all HSDIO Channels to be zero with the exception of shutters, then
    initializes all channels to a convenient initial state
    Args:
        t (float): Start time

    Returns:
        t (float): End time, equal to start time
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


def calibration(t, calibration_time=6):
    """
    Calibration sequence to allow hybrid monitor chance to measure powers of beams and fields.
    Args:
        t (float): Start time (ms)
        calibration_time (float): duration of calibration sequence

    Returns:
        t (float): End time (ms)
    """
    # Ensure collection shutter is off
    Collection_Shutter_switch(t, 0)
    t += Collection_Shutter_delay_off

    # Turn on cooling beam
    Cooling_Shutter_switch(t, 1)
    D2_switch(t, 1)
    D2_DDS(t, 'MOT')

    # turn off the Repumper
    HF_switch(t, 0)
    HF_amplitude(t, 0)

    # Open all switchyard shutters
    close_shutters(t, delay=False, closeXZShutter=0, closeYShutter=0, closeY2Shutter=0,
                   closeXShutter=0)

    # pulse on rydberg beams
    rydberg_pulse(t, calibration_time)

    t += calibration_time/2
    # trigger the NIDAQ
    trigger_nidaq(t)
    t += calibration_time/2

    return t


# Loading Phases -----------------------------------------------------------------------------------
def mot_loading(t, duration, trigger_andor=True, keep_quadrupole=False):
    """
    MOT loading phase.

    Loads the MOT for 'duration' ms
    Args:
        t (float): Start time (ms)
        duration (float): duration of MOT loading phase (ms)
        trigger_andor (bool): If true Andor is triggered during the MOT phase
            If true the andor trigger will occur AndorExpT ms before the end of the MOT phase,
            unless that would occur before the start of the MOT phase. In that case the trigger
            occurs at the start of the MOT phase
        keep_quadrupole (bool) : If true quadrupole field coils will be kept on at the end of this
            phase

    Returns:
        t: time after which the MOT phase will have been com
    """
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

    if not keep_quadrupole:
        switchcoils(t - .3, False)
    if trigger_andor:
        if t - AndorExpT < ts:
            tAnd = ts
        else:
            tAnd = t - AndorExpT
        MOT_Andor_Trig(tAnd, 1)
        MOT_Andor_Trig(tAnd + 1, 0)
    return t


def pgc1(t, duration, trap_delay, trap_on=True, chop=True):
    """
    PGC1 phase to achieve quick, sub-doppler cooling
    Args:
        t (float): Start time (ms)
        duration (float): Duration of PGC1 phase (ms)
        trap_delay (float): Delay time for turning on the FORT (ms)
        trap_on (bool): If true, FORT is on during PGC phase
        chop (bool): If true, FORT and D2 laser are chopped during PGC phase
        coils_on (bool): If true, MOT quadrupole field is kept on during PGC1 phase

    Returns:
        t (float): End time (ms)
    """
    t = biasAO(t, PGC1_shim)
    D2_DDS(t, 'PGC1')
    HF_amplitude(t, PGC_1_hyperfine_power)
    vODT_power(t + trap_delay, vertTrapPower)

    vODT_switch(t + trap_delay, trap_on)
    if chop:
        print "Chopped loading enabled"
        t = chopped_d2_trap(t, duration, period=2.1e-3, d2_duty_cycle=(.01, .5),
                        trap_duty_cycle=(0.27, .72))
    else:
        t += duration

    # If coils were on, they're switched off, otherwise just a redundant command, for free.
    switchcoils(t - .3, False)
    return t


def pgc2(t, duration):
    """
    Secondary PGC phase to further reduce atom cloud temperature, albeit more slowly
    Args:
        t (float): Start time (ms)
        duration (float): duration of PGC2 phase (ms)

    Returns:
        t (float): End time (ms)
    """
    t = biasAO(t, PGC2_shim)
    D2_DDS(t, 'PGC2')
    D2_switch(t, 1)
    HF_switch(t, 1)
    RP_Shutter_switch(t-RP_Shutter_delay_on, 1)
    HF_amplitude(t, PGC_1_hyperfine_power)
    t += duration
    return t


# in-trap d2 phases --------------------------------------------------------------------------------
def light_assisted_collisions(t, duration):
    """
    Light Assisted Collision Phase
    Args:
        t (float): Start time (ms)
        duration (float): Duration of LAC phase (ms)

    Returns:
        t (float): End time (ms)
    """

    # start LAC at t
    t = biasAO(t, LAC_shim)
    D2_DDS(t, 'LAC')
    D2_switch(t, 1)
    HF_amplitude(t, LAC_hyperfine_power)
    HF_switch(t, 1)

    t += duration
    return t


def recool(t, recool_time):
    """
    Phase to cool atoms in the trap
    Args:
        t (float): start time (ms)
        recool_time (float): duration (ms)

    Returns:
        t (float): end time (ms)
    """
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

    return t


def fluorescence_readout(
        t,
        OnTime,
        RO_bins=30,
        drops=3,
        returnPower=True,
        chop=True,
        shuttersclosed=None,
        ROPowerToggle=False,
        SPCM_bins=30,
        trigger_andor=False,
        trigger_hm=False
):
    """
    Trap centered fluorescence readout
    Args:
        t (float): start time (ms)
        OnTime (float): duration of readout phase (ms)
        RO_bins (int): number of Readout bins on the SPCM
        drops (int): number of Readout bins to drop at the start of readout (additional to RO_bins)
        returnPower (bool): should trap power be returned to inital power at the end of RO
            (redundant if ROPowerToggle is false)
        chop (bool): chop the trap during readout
        shuttersclosed (list): length 4 list of bools, closes shutters if true [XZ, Y, Y2, X].
            default is to have all shutters open
        ROPowerToggle (bool): if true, trap power is reduced during readout
        SPCM_bins (int): SPCM binning. Only use case is if time-dependent behavior for SPCM
            gating is being debugged
        trigger_andor (bool): if true, Andor camera is sent a trigger during readout (1ms pulse)
        trigger_hm (bool): if true, Hamamatsu camera is send a trigger during readout (OnTime
            level trigger)

    Returns:
        t (float): end time
    """
    if ROPowerToggle:
        vODT_power(t - vertTrapPowerROPret, vertTrapPowerRO)

    # time per bin - Counter and SPCM are gated individually
    RO_bin_width = OnTime / float(RO_bins) / 2
    SPCM_bin_width = OnTime / float(SPCM_bins) / 2
    print "RO_bins = {}".format(RO_bins)
    print "RO_bin_width = {}".format(RO_bin_width)
    print "SPCM_bins = {}".format(SPCM_bins)
    print "SPCM_bin_width = {}".format(SPCM_bin_width)
    print drops

    # set up pre-pulse dump bins
    tt = t - 2 * RO_bin_width * (drops)  # -1)
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
    # BiasAO and Set shutters to desired state all at once to minimize delays
    biasAO(t + ROShimTimeOffset, RO1_shim)
    Collection_Shutter_switch(t - Collection_Shutter_delay_on, 1)
    if shuttersclosed is None:
        shuttersclosed = [1]*4
    t = close_shutters(t, closeXZShutter=shuttersclosed[0], closeYShutter=shuttersclosed[1],
                       closeY2Shutter=shuttersclosed[2], closeXShutter=shuttersclosed[3])

    # Turn on lasers
    D2_DDS(t, 'RO')
    D2_switch(t, 1)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_on, 1)
    HF_switch(t, 1)
    HF_amplitude(t - 0.1, RO1_hyperfine_power)

    if chop:
        # TODO : Check out behavior of chopping phase
        tend = 0 # ChoppedRO(t,OnTime,period=2e-3,RO_onoff=[.01,.5],Trap_onoff=[0.25,.71])
    else:
        tend = 0

    # trigger cameras
    ChipAndorOffset = -0.2

    MOT_Andor_Trig(t,trigger_andor)
    MOT_Andor_Trig(t+1,0)
    Hamamatsu_Trig(t+Hamamatsu_Trig_Shim, trigger_hm)
    Hamamatsu_Trig(t+Hamamatsu_Trig_Shim+OnTime, 0)

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


    # turn off lasers, and done.
    D2_switch(t, 0)
    HF_switch(t, 0)
    if returnPower:
        vODT_power(t, vertTrapPower)

    return max(t, tend)


def blowaway(t, duration, shutter_states=None, chopTrap=False):
    """
    Switchyard based blowaway phase. Blows away atoms in F=4 ground state manifold

    Currently dependent on outside functions to properly set shutter states before and after phase
    Args:
        t (float): Start time (ms)
        duration (float): Duration of blow away phase (ms)
        shutter_states (list): list of booleans, which shutters should be closed. [XZ, Y, Y2, X]
        chopTrap (bool): if true, the trap is chopped during the blow away

    Returns:
        t (float): End time (ms)
    """
    shutter_states = [False] * 4 if shutter_states is None else shutter_states
    D2_DDS(t, 'BA')
    biasAO(t, RO1_shim)
    D2_switch(t, 1)
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_on - 0.5, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_off, 0)

    # closeShutters(t-1.5,*shuttersclosed)
    tp = t
    if chopTrap:
        tp = chopped_trap(tp, duration, period=0.005,
                          trap_duty_cycle=(0.15, 0.2))
    t += duration
    D2_switch(t, 0)
    RP_Shutter_switch(t - RP_Shutter_delay_off * 1, 1)
    return t + .001


def shelve_and_blowaway(t, sTime, sState, blowaway=True, toRO=True):
    """
    Shelves into either the F=3 or F=4 ground state levels using the D2 and HF lasers (through
        the MOT switchyard) then blows away the atoms in the F=4 level

    Args:
        t (float): Start time (ms)
        sTime (float): duration of shelving pulse. If negative, sState is switched, from 4 to 3
        or 3 to 4
        sState (int): either 3 or 4. Hyperfine level to shelve into. If 3, D2 beam is pulsed
            using the readout parameters, if 4 Repumper  beam is pulsed using the readout parametes
        blowaway (bool): if true, atoms in the F=4 level are blown away using the switchyard beams
        toRO (bool): if true, 4ms delay is added, and all shutters are opened
            # TODO: Make this make sense

    Returns:
        t (float): End time (ms)
    """
    D2_DDS(t, 'Recool')
    close_shutters(t, delay=True, closeXZShutter=0, closeYShutter=0, closeY2Shutter=0,
                   closeXShutter=0)
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
        close_shutters(t, delay=True, closeXZShutter=1, closeYShutter=0, closeY2Shutter=1,
                       closeXShutter=0)
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
        t = trap_in_dark(t, 4)
        close_shutters(t, delay=True)
    return t


# Pumping Phases -----------------------------------------------------------------------------------
def optical_pumping(t, duration, shelve_time=0, chop=True):
    """
    Optical pumping and, optionally, shelving phase
    Args:
        t (float): Start time (ms)
        duration (float): duration of OP phase (ms)
        shelve_time (float): duration of shelving phase (ms). If shelve time > 0, atoms are
            shelved into F=3 manifold by using OP light in absence of repumper. If shelve_time < 0
            atoms are shelved into F=4 manifold by using repumper light in absence of OP light.
        chop (bool): if true, trap is chopped during OP phase

    Returns:
        t (float): End time (ms)
    """
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_off * 3, 0)
    close_shutters(t - 2, closeXZShutter=1, closeYShutter=1, closeY2Shutter=1, closeXShutter=1)
    OP_Shutter_switch(t - OP_Shutter_delay_on, 1)
    OP_RP_Shutter_switch(t - OP_RP_Shutter_delay_on, 1)
    RP_Shutter_switch(t - RP_Shutter_delay_on, 1)

    if chop:
        # vODT_power(t,vertTrapPowerChop)
        chopped_trap(t, duration + abs(shelve_time), period=1e-3,
                     trap_duty_cycle=(0.2, 0.41))

    # Chip_Andor_Trig(t,1)
    HF_switch(t, 1)
    OP_switch(t, 1)
    D2_switch(t, 0)
    HF_amplitude(t, OP_HF_amplitude)
    biasAO(t, OP_shim)

    t += duration
    print duration

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


def op_shelve(t, shelve_time=0, chop=True):
    """
    Runs a shelving phase using beams in OP path. If shelve_time > 0, optical pumping beam is
    turned on without repumper
        If shelve_time < 0 repumper is turned on without optical pumping beam.
    Args:
        t (float): Start time (ms)
        shelve_time (float): duration of phase (ms). Positive shelve times shelve into F=3,
            negative shelve times shelve into F=4
        chop (bool): if true, trap is chopped during this phase

    Returns:
        t (float): End time (ms)
    """
    Cooling_Shutter_switch(t - Cooling_Shutter_delay_off, 0)
    close_shutters(t, closeXZShutter=1, closeYShutter=1, closeY2Shutter=1, closeXShutter=1)
    D2_switch(t, 0)
    biasAO(t, OP_shim)

    if chop:
        vODT_power(t, vertTrapPowerChop)
        chopped_trap(t, OP_time + abs(shelve_time), period=1e-3)

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


def rabi_flopping_experiment(t, pumping_time, clock_time, blowaway_time, clock_delay=0):
    """
    Rabi flopping experiment. Runs optical pumping sequence, then induces rabi oscillation along
    the Cs clock transition, then blows away atoms in the F=4 hyperfine ground level

    Args:
        t (float): Start time (ms)
        pumping_time (float): duration of the optical pumping pulse (ms)
        clock_time (float): duration of the microwave pulse (ms)
        blowaway_time (float): duration of the blowaway pulse (ms)
        clock_delay (float): delay before the microwave pulse, after optical pumping pulse (ms)

    Returns:
        t (float): End time (ms)
    """
    t = optical_pumping(t, pumping_time)
    t = microwave_pulse(t, clock_delay, clock_time)
    stray_time = 10 - pumping_time - clock_delay - clock_time - blowaway_time
    if stray_time > 2.8:  # TODO: What is this 2.8 and why is it hard coded?
        t += stray_time
    else:
        print "Experiment longer than 10 ms."
        t += 2.8
    t = blowaway(t, blowaway_time)
    D2_switch(t, 0)
    D2_DDS(t, 'RO')
    return t + .01


# Counter utility phases ---------------------------------------------------------------------------
def counterreadout(
        t,
        OnTime,
        RO_bins=30,
        drops=3,
        chop=True,
        ROPowerToggle=False
):
    """
    Reads out data from the counters without changing the experiment state, i.e. all switches,
    shutters, triggers and AO channels remain in their state as this readout occurs
    Args:
        t (float): start time (ms)
        OnTime (float): duration of collection (ms)
        RO_bins (int): number of readout bins
        drops (int): number of bins to drop
        chop (bool): chop trap and RO beams if true
    Returns:
        t (float): ending time (ms)
    """
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

    # counter bins
    t += 2 * RO_bin_width
    for i in range(RO_bins):
        SPCM_clock(t, 1)
        t += RO_bin_width
        SPCM_clock(t, 0)
        t += RO_bin_width
    t -= 2 * RO_bin_width
    # SPCMPulse(t,RO_bins,RO_bin_width*2)

    return t


# repeat cycle based functions----------------------------------------------------------------------
def one_chop_andor(t, period=2e-3, duty_cycle=None):
    """
    One cycle of turning the MOT_Andor_Trig, off, then on, then back off
    Args:
        t (float): Start time (ms)
        period(float): cycle period (ms)
        duty_cycle(tuple): containing [on,off] time of andor trigger as a fraction of period
            default is [0,.5]
    Returns:
        t (float): end time (ms)
    """
    duty_cycle = [0, .5] if duty_cycle is None else duty_cycle
    MOT_Andor_Trig(t, 0)
    MOT_Andor_Trig(t + duty_cycle[0] * period, 1)
    MOT_Andor_Trig(t + duty_cycle[1] * period, 0)
    return t + period


def one_chop_readout(t, period=2e-3, d2_duty_cycle=None, trap_duty_cycle=None):
    """
    One cycle of chopping D2_switch and vODT_switch off, then on, then off again according to
    duty_cycle arguments
    Args:
        period: time in ms
        d2_duty_cycle: tuple containing [on,off] as a percentage of period
            default is [0,.5]
        trap_duty_cycle: tuple containing [on,off] as a percentage of period
            default is [0,.5]

    Returns:
        t (float): end time (ms)
    """
    d2_duty_cycle = [0, .5] if d2_duty_cycle is None else d2_duty_cycle
    trap_duty_cycle = [0, .5] if trap_duty_cycle is None else trap_duty_cycle
    D2_switch(t, 0)
    vODT_switch(t, 0)
    D2_switch(t + d2_duty_cycle[0] * period, 1)
    D2_switch(t + d2_duty_cycle[1] * period, 0)
    vODT_switch(t + trap_duty_cycle[0] * period, 1)
    vODT_switch(t + trap_duty_cycle[1] * period, 0)
    return t + period


def one_chop_trap(t, period=2e-3, trap_duty_cycle=None):
    """
    One cycle of turning the FORT off then on then off again
    Args:
        t (float): start time (ms)
        period (float): chop cycle period (ms)
        trap_duty_cycle (tuple): tuple containing [on, off] as a fraction of the period
            default is [0,.5]

    Returns:
        t (float): end time (ms)
    """
    trap_duty_cycle = [0., 0.5] if trap_duty_cycle is None else trap_duty_cycle
    vODT_switch(t, 1)
    vODT_switch(t + trap_duty_cycle[0] * period, 0)
    vODT_switch(t + trap_duty_cycle[1] * period, 1)
    return t + period


def one_chop_op(t, period=2e-3, op_duty_cycle=None):
    """
    One cycle of turning the OP_switch off then on then off again
    Args:
        t (float): start time (ms)
        period (float): chop cycle time (ms)
        op_duty_cycle (tuple): tuple containing [on, off] as a fraction of the period

    Returns:
        t (float): end time (ms)
    """
    op_duty_cycle = [0, .5] if op_duty_cycle is None else op_duty_cycle
    OP_switch(t, 0)
    OP_switch(t + op_duty_cycle[0] * period, 1)
    OP_switch(t + op_duty_cycle[1] * period, 0)
    return t + period


def one_pulse_counter_bin(t, period):
    """
    One cycle of setting up a 50% duty cycle binning pulse
    Args:
        t (float): Start time (ms)
        period (float): bin cycle period (ms)

    Returns:
        t (float): End time (ms)
    """

    SPCM_clock(t, 0)
    SPCM_clock(t + 0.25 * period, 1)
    SPCM_clock(t + 0.75 * period, 0)
    return t + period


def end_chop_op(t, period=2e-3):
    """
    Final chop to end chop cycle
    Args:
        t (float): start time (ms)
        period (float): cycle time (ms)

    Returns:
        t (float): end time (ms)
    """
    print t  # TODO : logging
    t += period * 2
    OP_switch(t, 0)
    return t


def end_chop_ro(t, period=2e-3):
    """
    Final chop to end chop cycle
    Args:
        t (float): start time (ms)
        period (float): cycle time (ms)

    Returns:
        t (float): end time (ms)
    """
    print t  # TODO : logging
    t += period * 2
    D2_switch(t, 0)
    vODT_switch(t, 1)
    return t


def end_chop_trap(t, period=2e-3):
    """
    Final chop to end chop cycle
    Args:
        t (float): start time (ms)
        period (float): cycle time (ms)

    Returns:
        t (float): end time (ms)
    """
    print t  # TODO : logging
    t += period * 2
    vODT_switch(t, 1)
    return t


def chopped_d2_trap(t, duration, period=2e-3, d2_duty_cycle=None, trap_duty_cycle=None):
    """
    Chops D2_switch and vODT_switch for chopped readout

    Individual cycles are set by OneChopRO and the final cycle is set by EndChopRO
    Args:
        t (float): Start time (ms)
        duration (float): duration of Readout Phase (ms)
        period (float): cycle period (ms)
        d2_duty_cycle (tuple): tuple containing [on, off] of D2_switch as a fraction of the period
            default is set in one_chop_readout
        trap_duty_cycle (tuple): tuple containing [on, off] of vODT_switch as a fraction of the
            period
            default is set in one_chop_readout
    Returns:
        t (float): End time (ms)
    """
    repeats = int(duration / period) + 1
    funct = lambda t: one_chop_readout(t, period, d2_duty_cycle, trap_duty_cycle)
    t = add_repeat(t, funct, repeats)
    return end_chop_ro(t, period)


def chopped_trap(t, duration, period=2e-3, trap_duty_cycle=None):
    """
    Chops vODT_switch

    Individual cycles are set by one_chop_trap and the final cycle is set by EndChopRO
    Args:
        t (float): Start time (ms)
        duration (float): duration of Readout Phase (ms)
        period (float): cycle period (ms)
        trap_duty_cycle (tuple): tuple containing [on, off] of vODT_switch as a fraction of the
            period
            default = [0.01, .501]
    Returns:
        t (float): End time (ms)
    """
    trap_duty_cycle = [0.01, .501] if trap_duty_cycle is None else trap_duty_cycle
    repeats = int(duration / period) + 1
    funct = lambda t: one_chop_trap(t, period, trap_duty_cycle)
    t = add_repeat(t, funct, repeats)
    return end_chop_trap(t, period)


def counter_bin_pulses(t, pulses, period):
    """
    Creates pulse repetition for single photon counter bins. IE binning on the NI frequency counter
    Args:
        t (float): Start time (ms)
        pulses (int): Number of pulses
        period (float): bin cycle period (ms)

    Returns:
        t (float): End time (ms)
    """
    funct = lambda t: one_pulse_counter_bin(t, period)
    t = add_repeat(t, funct, pulses)
    return t