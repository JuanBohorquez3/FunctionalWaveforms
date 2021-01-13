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
    trap_switch(t, 1)
    d2_switch(t, 0)
    repumper_switch(t, 0)
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
    trap_switch(t, 0)
    t += duration
    trap_switch(t, trap_on)
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
    d2_shutter(t - Cooling_Shutter_delay_on, 0)
    blowaway_shutter(t, 1)

    d2_dds(t, 'BA')
    d2_switch(t, 1)
    repumper_switch(t, 0)
    repumper_amplitude(t, RO1_hyperfine_power)

    t += duration

    d2_switch(t, 0)
    repumper_switch(t, 0)
    blowaway_shutter(t, 0)
    d2_shutter(t - Cooling_Shutter_delay_off, 1)

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

    pulse(t, duration, microwave_switch)
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
        pulse(t, duration, ryd685_switch)
    if on_beams[1]:
        pulse(t, duration, ryd595_switch)

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
        if channel in shutters:
            channel(t, 1)
        else:
            channel(t, 0)

    trap_switch(t, 1)
    trap_amplitude(t, vertTrapPower)
    ryd685_switch(t, 0)
    ryd595_switch(t, 1)
    RP_Shutter_switch_init(t, 1)
    Cooling_Shutter_switch_init(t, 1)
    OP_Shutter_switch_init(t, 0)
    OP_RP_Shutter_switch_init(t, 0)
    optical_pumping_switch(t, 0)
    Blowaway_Shutter_switch_init(t, 0)
    counter_gate(t, 0)
    Collection_Shutter_switch_init(t, 0)
    microwave_switch(t, 0)
    andor_trigger(t, 0)
    hamamatsu_trigger(t, 0)
    nidaq_trigger(t, 0)
    ni_scope_trigger(t, 0)
    repumper_switch(t, 1)
    d2_switch(t, 1)
    d2_dds(t, 'MOT')
    bias_shims(t, MOT_shim)
    quadrupole_coil_switch(t, True)

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
    collection_shutter(t, 0)
    t += Collection_Shutter_delay_off

    # Turn on cooling beam
    d2_shutter(t, 1)
    d2_switch(t, 1)
    d2_dds(t, 'MOT')

    # turn off the Repumper
    repumper_switch(t, 0)
    repumper_amplitude(t, 0)

    # Open all switchyard shutters
    close_shutters(t, delay=False, xz_closed=0, y_closed=0, y2_closed=0,
                   x_closed=0)

    # pulse on rydberg beams
    rydberg_pulse(t, calibration_time)

    t += calibration_time/2
    # trigger the NIDAQ
    trigger_nidaq(t)
    t += calibration_time/2

    return t


# Loading Phases -----------------------------------------------------------------------------------
def mot_loading(
        t,
        duration,
        hf_power,
        shim_fields,
        mot_current,
        trigger_andor=True,
        exposure_time=50,
        keep_quadrupole=False):
    """
    MOT loading phase.

    Loads the MOT for 'duration' ms
    Args:
        t (float): Start time (ms)
        duration (float): duration of MOT loading phase (ms)
        hf_power (float): voltage to be applied to the repumper VVA (V)
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)
        mot_current (float): Desired current through the quadrupole coils during the MOT
            phase (A)
        trigger_andor (bool): If true Andor is triggered during the MOT phase
            If true the andor trigger will occur AndorExpT ms before the end of the MOT phase,
            unless that would occur before the start of the MOT phase. In that case the trigger
            occurs at the start of the MOT phase
        exposure_time (float): exposure time of the Andor camera. Does nothing if trigger_andor
            is False. (ms)
        keep_quadrupole (bool) : If true quadrupole field coils will be kept on at the end of this
            phase

    Returns:
        t: time after which the MOT phase will have been com
    """
    t_initial = t
    # Delay doesn't matter, don't update time to reduce cycle time
    bias_shims(t, shim_fields)
    quadrupole_coil_switch(t, True, mot_current)

    d2_dds(t, 'MOT')
    d2_switch(t, 1)

    repumper_switch(t, 1)
    repumper_amplitude(t, hf_power)

    t += duration

    # Turn off beams to leave AO timing shims in future phases
    d2_switch(t, 0)
    repumper_switch(t, 0)

    if not keep_quadrupole:
        quadrupole_coil_switch(t - .3, False, 0)

    if trigger_andor:
        trigger_time = t - exposure_time
        if trigger_time < t_initial:
            trigger_time = t_initial
        pulse(trigger_time, 1, andor_trigger)
    return t


def pgc1(
        t,
        duration,
        hf_power,
        shim_fields,
        trap_delay,
        trap_on=True,
        chop=True):
    """
    PGC1 phase to achieve quick, sub-doppler cooling
    Args:
        t (float): Start time (ms)
        duration (float): Duration of PGC1 phase (ms)
        hf_power (float): voltage to be applied to the repumper VVA (V)
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)
        trap_delay (float): Delay time for turning on the FORT (ms)
        trap_on (bool): If true, FORT is on during PGC phase
        chop (bool): If true, FORT and D2 laser are chopped during PGC phase

    Returns:
        t (float): End time (ms)
    """
    t = bias_shims(t, shim_fields)
    d2_dds(t, 'PGC1')
    d2_switch(t, 1)
    repumper_switch(t, 1)
    repumper_amplitude(t, hf_power)

    trap_switch(t + trap_delay, trap_on)
    if chop:
        print "Chopped loading enabled"
        t = chopped_d2_trap(
            t,
            duration,
            period=2.1e-3,
            d2_duty_cycle=(.01, .5),
            trap_duty_cycle=(0.27, .72))
    else:
        t += duration

    # Turn off beams to leave AO timing shims in future phases
    d2_switch(t, 0)
    repumper_switch(t, 0)

    # If coils were on, they're switched off, otherwise just a redundant command, for free.
    quadrupole_coil_switch(t - .3, False, 0)
    return t


def pgc2(t, duration, hf_power, shim_fields):
    """
    Secondary PGC phase to further reduce atom cloud temperature, albeit more slowly
    Args:
        t (float): Start time (ms)
        duration (float): duration of PGC2 phase (ms)
        hf_power (float): voltage to be applied to the repumper VVA (V)
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)

    Returns:
        t (float): End time (ms)
    """
    t = bias_shims(t, shim_fields)
    d2_dds(t, 'PGC2')
    d2_switch(t, 1)
    repumper_switch(t, 1)
    repumper_amplitude(t, hf_power)
    t += duration

    # Turn off beams to leave AO timing shims in future phases
    d2_switch(t, 0)
    repumper_switch(t, 0)

    return t


# in-trap d2 phases --------------------------------------------------------------------------------
def light_assisted_collisions(t, duration, hf_power, shim_fields):
    """
    Light Assisted Collision Phase
    Args:
        t (float): Start time (ms)
        duration (float): Duration of LAC phase (ms)
        hf_power (float): voltage to be applied to the repumper VVA (V)
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)

    Returns:
        t (float): End time (ms)
    """

    # start LAC at t
    t = bias_shims(t, shim_fields)
    d2_dds(t, 'LAC')
    d2_switch(t, 1)
    repumper_switch(t, 1)
    repumper_amplitude(t, hf_power)

    t += duration

    # Turn off beams to leave AO timing shims in future phases
    d2_switch(t, 0)
    repumper_switch(t, 0)

    return t


def recool(t, duration, hf_power, shim_fields):
    """
    Phase to cool atoms in the trap
    Args:
        t (float): start time (ms)
        duration (float): duration (ms)
        hf_power (float): voltage to be applied to the repumper VVA (V)
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)

    Returns:
        t (float): end time (ms)
    """
    t_shutters = close_shutters(t)  # Open all the shutters, delay experiment until all are open
    t_shim = bias_shims(t, shim_fields)
    t = max(t_shim, t_shutters)

    d2_dds(t, 'Recool')
    d2_switch(t, 1)
    repumper_switch(t, 1)
    repumper_amplitude(t, hf_power)

    t += duration

    # turn off the D2 and HF AOMs
    d2_switch(t, 0)
    repumper_switch(t, 0)

    return t


def fluorescence_readout(
        t,
        duration,
        hf_power,
        shim_fields,
        counter_bins=30,
        drop_bins=3,
        spcm_bins=30,
        chop=True,
        shutter_states=None,
        trigger_andor=False,
        trigger_hm=False
):
    """
    Trap centered fluorescence readout
    Args:
        t (float): start time (ms)
        duration (float): duration of readout phase (ms)
        hf_power (float): voltage to be applied to the repumper VVA (V)
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)
        counter_bins (int): number of Readout bins on the SPCM
        drop_bins (int): number of Readout bins to drop at the start of readout (additional to RO_bins)
        spcm_bins (int): SPCM binning. Only use case is if time-dependent behavior for SPCM
            gating is being debugged
        chop (bool): chop the trap during readout
        shutter_states (list): length 4 list of bools, closes shutters if true [XZ, Y, Y2, X].
            default is to have all shutters open
        trigger_andor (bool): if true, Andor camera is sent a trigger during readout (1ms pulse)
        trigger_hm (bool): if true, Hamamatsu camera is send a trigger during readout (OnTime
            level trigger)

    Returns:
        t (float): end time
    """
    
    # time per bin - Counter and SPCM are gated individually
    ro_bin_width = duration / float(counter_bins) / 2
    spcm_bin_width = duration / float(spcm_bins) / 2

    tt = t - 2 * ro_bin_width * (drop_bins)
    # BiasAO and Set shutters to desired state all at once to minimize delays
    bias_shims(t, shim_fields)
    collection_shutter(t - Collection_Shutter_delay_on, 1)
    if shutter_states is None:
        shutter_states = [True] * 4
    t = close_shutters(t, xz_closed=shutter_states[0], y_closed=shutter_states[1],
                       y2_closed=shutter_states[2], x_closed=shutter_states[3])

    # set up pre-pulse dump bins
    for i in range(drop_bins):
        counter_clock(tt, 1)
        counter_gate(tt, 1)
        tt += ro_bin_width
        counter_clock(tt, 0)
        counter_gate(tt, 0)
        tt += ro_bin_width
    # t-=2*RO_bin_width

    # Turn on lasers
    d2_dds(t, 'RO')
    d2_switch(t, 1)
    d2_shutter(t - Cooling_Shutter_delay_on, 1)
    repumper_shutter(t - RP_Shutter_delay_on, 1)
    repumper_switch(t, 1)
    repumper_amplitude(t - 0.1, hf_power)

    if chop:
        # TODO : Check out behavior of chopping phase
        tend = 0 # ChoppedRO(t,OnTime,period=2e-3,RO_onoff=[.01,.5],Trap_onoff=[0.25,.71])
    else:
        tend = 0

    andor_trigger(t, trigger_andor)
    andor_trigger(t + 1, 0)
    hamamatsu_trigger(t + Hamamatsu_Trig_Shim, trigger_hm)
    hamamatsu_trigger(t + Hamamatsu_Trig_Shim + duration, 0)

    t += 2 * ro_bin_width

    # SPCM bins
    tt = t
    for i in range(spcm_bins):
        counter_gate(tt, 1)
        tt += spcm_bin_width
        tt += spcm_bin_width
        counter_gate(tt - 0.01, 0)

    # Counter bins
    for i in range(counter_bins):
        counter_clock(t, 1)
        t += ro_bin_width
        counter_clock(t, 0)
        t += ro_bin_width
    t -= 2 * ro_bin_width


    # turn off lasers, and done.
    d2_switch(t, 0)
    repumper_switch(t, 0)

    return max(t, tend)


def blowaway(t, duration, shim_fields, shutter_states=None, chop_trap=False):
    """
    Switchyard based blowaway phase. Blows away atoms in F=4 ground state manifold

    Currently dependent on outside functions to properly set shutter states before and after phase
    Args:
        t (float): Start time (ms)
        duration (float): Duration of blow away phase (ms)
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)
        shutter_states (list): list of booleans, which shutters should be closed. [XZ, Y, Y2, X]
        chop_trap (bool): if true, the trap is chopped during the blow away

    Returns:
        t (float): End time (ms)
    """
    shutter_states = [False] * 4 if shutter_states is None else shutter_states
    close_shutters(t, delay=True, *shutter_states)
    d2_dds(t, 'BA')
    bias_shims(t, shim_fields)
    d2_switch(t, 1)
    d2_shutter(t - Cooling_Shutter_delay_on - 0.5, 1)
    repumper_shutter(t - RP_Shutter_delay_off, 0)

    # closeShutters(t-1.5,*shuttersclosed)
    tp = t
    if chop_trap:
        tp = chopped_trap(tp, duration, period=0.005,
                          trap_duty_cycle=(0.15, 0.2))
    t += duration
    d2_switch(t, 0)
    repumper_shutter(t - RP_Shutter_delay_off * 1, 1)
    return t + .001


def hf_shelving(t, duration, shim_fields, shelve_state):
    """
    Shelves into either the F=3 or F=4 ground state levels using the D2 and HF lasers (through
        the MOT switchyard) then blows away the atoms in the F=4 level

    Args:
        t (float): Start time (ms)
        duration (float): duration of shelving pulse. If negative, sState is switched, from 4 to 3
        or 3 to 4
        shim_fields (list): length 3 list of voltages to be applied to magnetic bias shim
            controllers. Order [shim_x, shim_y, shim_z]. (V)
        shelve_state (int): either 3 or 4. Hyperfine level to shelve into. If 3, D2 beam is pulsed
            using the readout parameters, if 4 Repumper  beam is pulsed using the readout parametes

    Returns:
        t (float): End time (ms)
    """
    d2_dds(t, 'Recool')
    close_shutters(t, delay=True, *[False]*4)
    t += 1
    tt = t + 10
    assert shelve_state == 3 or shelve_state == 4
    if duration < 0:
        duration = abs(duration)
        if shelve_state == 4:
            shelve_state = 3
        else:
            shelve_state = 4

    if shelve_state == 4:
        repumper_switch(t, 1)
        t += duration
        repumper_switch(t, 0)
    else:
        bias_shims(t, shim_fields)
        d2_switch(t, 1)
        t += abs(duration)
        d2_switch(t, 0)

    if t < tt:
        t = tt

    t += RP_Shutter_delay_off + 1
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
    d2_shutter(t - Cooling_Shutter_delay_off * 3, 0)
    close_shutters(t - 2, xz_closed=1, y_closed=1, y2_closed=1, x_closed=1)
    optical_pumping_shutter(t - OP_Shutter_delay_on, 1)
    op_repumper_shutter(t - OP_RP_Shutter_delay_on, 1)
    repumper_shutter(t - RP_Shutter_delay_on, 1)

    if chop:
        # vODT_power(t,vertTrapPowerChop)
        chopped_trap(t, duration + abs(shelve_time), period=1e-3,
                     trap_duty_cycle=(0.2, 0.41))

    # Chip_Andor_Trig(t,1)
    repumper_switch(t, 1)
    optical_pumping_switch(t, 1)
    d2_switch(t, 0)
    repumper_amplitude(t, OP_HF_amplitude)
    bias_shims(t, OP_shim)

    t += duration
    print duration

    HF_off_delay = 0.027
    if shelve_time >= 0:
        if shelve_time > 0:
            repumper_shutter(t - RP_Shutter_delay_off, 0)
        op_repumper_shutter(t, 0)
        repumper_switch(t, 0)
        repumper_amplitude(t + HF_off_delay, 0)
    else:
        optical_pumping_shutter(t, 0)
        optical_pumping_switch(t, 0)

    t += abs(shelve_time)

    if shelve_time >= 0:
        optical_pumping_shutter(t, 0)
        optical_pumping_switch(t, 0)
    else:
        repumper_shutter(t - RP_Shutter_delay_off, 0)
        op_repumper_shutter(t, 0)
        repumper_switch(t, 0)
        repumper_amplitude(t + HF_off_delay, 0)
    # Chip_Andor_Trig(t,0)
    # biasAO(t,RO1_shim)
    trap_amplitude(t, vertTrapPower)
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
    d2_shutter(t - Cooling_Shutter_delay_off, 0)
    close_shutters(t, xz_closed=1, y_closed=1, y2_closed=1, x_closed=1)
    d2_switch(t, 0)
    bias_shims(t, OP_shim)

    if chop:
        trap_amplitude(t, vertTrapPowerChop)
        chopped_trap(t, OP_time + abs(shelve_time), period=1e-3)

    if shelve_time < 0:
        repumper_shutter(t - RP_Shutter_delay_on, 1)
        op_repumper_shutter(t - OP_RP_Shutter_delay_on, 1)
        repumper_switch(t, 1)
        repumper_amplitude(t, OP_HF_amplitude)
    else:
        optical_pumping_shutter(t - OP_Shutter_delay_on, 1)
        optical_pumping_switch(t, 1)

    t += abs(shelve_time)

    if shelve_time >= 0:
        optical_pumping_shutter(t, 0)
        optical_pumping_switch(t, 0)
    else:
        repumper_shutter(t, 0)
        op_repumper_shutter(t, 0)
        repumper_switch(t, 0)
        repumper_amplitude(t, 0)
    # Chip_Andor_Trig(t,0)
    bias_shims(t, RO1_shim)
    trap_amplitude(t, vertTrapPower)
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
    d2_switch(t, 0)
    d2_dds(t, 'RO')
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
        counter_clock(tt, 1)
        tt += RO_bin_width
        counter_clock(tt, 0)
        tt += RO_bin_width
    # t-=2*RO_bin_width

    # counter bins
    t += 2 * RO_bin_width
    for i in range(RO_bins):
        counter_clock(t, 1)
        t += RO_bin_width
        counter_clock(t, 0)
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
    andor_trigger(t, 0)
    andor_trigger(t + duty_cycle[0] * period, 1)
    andor_trigger(t + duty_cycle[1] * period, 0)
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
    d2_switch(t, 0)
    trap_switch(t, 0)
    d2_switch(t + d2_duty_cycle[0] * period, 1)
    d2_switch(t + d2_duty_cycle[1] * period, 0)
    trap_switch(t + trap_duty_cycle[0] * period, 1)
    trap_switch(t + trap_duty_cycle[1] * period, 0)
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
    trap_switch(t, 1)
    trap_switch(t + trap_duty_cycle[0] * period, 0)
    trap_switch(t + trap_duty_cycle[1] * period, 1)
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
    optical_pumping_switch(t, 0)
    optical_pumping_switch(t + op_duty_cycle[0] * period, 1)
    optical_pumping_switch(t + op_duty_cycle[1] * period, 0)
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

    counter_clock(t, 0)
    counter_clock(t + 0.25 * period, 1)
    counter_clock(t + 0.75 * period, 0)
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
    optical_pumping_switch(t, 0)
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
    d2_switch(t, 0)
    trap_switch(t, 1)
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
    trap_switch(t, 1)
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