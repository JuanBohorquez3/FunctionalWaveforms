# Descriptively named functions to operate HSDIO and AO channels
from numpy import *  # Totally redundant but helps IDE understand our scope

# utility functions
HSDIO = experiment.LabView.HSDIO.add_transition
AO = experiment.LabView.AnalogOutput.add_transition
label = experiment.functional_waveforms_graph.label
add_repeat = experiment.LabView.HSDIO.add_repeat


# Instrument Triggers ----------------------------------------------------------
def ni_scope_trigger(t, state):
    """Not set!"""
    return HSDIO(t, 2, state)


def z_stage_trigger(t, state):
    """Not set!"""
    return HSDIO(t, 2, state)


def andor_trigger(t, state):
    return HSDIO(t, 15, state)


def nidaq_trigger(t, state):
    """ Split off to both nidaq and monitoring scope"""
    return HSDIO(t, 14, state)


def hamamatsu_trigger(t, state):
    return HSDIO(t, 31, state)


def mot_coils_switch(t, state):
    return HSDIO(t, 17, not (state))


def counter_gate(t, state):
    """Not set!"""
    return HSDIO(t, 2, state)


def counter_clock(t, state):
    return HSDIO(t, 24, state)


instrument_triggers = [
    ni_scope_trigger,
    z_stage_trigger,
    andor_trigger,
    nidaq_trigger,
    hamamatsu_trigger,
    mot_coils_switch,
    counter_gate,
    counter_clock
]


# RF Switches ------------------------------------------------------------------
def microwave_switch(t, state):
    return HSDIO(t, 0, not state)


def repumper_switch(t, state):
    return HSDIO(t, 18, not state)


def d2_switch(t, state):
    return HSDIO(t, 19, not state)


def trap_switch(t, state):
    return HSDIO(t, 20, not state)


def ryd595_switch(t, state):
    return HSDIO(t, 21, state)


def ryd685_switch(t, state):
    return HSDIO(t, 22, state)


def optical_pumping_switch(t, state):
    return HSDIO(t, 23, state)


rf_switches = [
    d2_switch,
    repumper_switch,
    trap_switch,
    ryd685_switch,
    ryd595_switch,
    microwave_switch,
    optical_pumping_switch
]


# Shutter Switches -------------------------------------------------------------
def xz_shutter(t, state):
    return HSDIO(t, 25,state)


def x_shutter(t, state):
    return HSDIO(t, 13, not (state))


def y_shutter(t, state):
    return HSDIO(t, 11, state)


def y2_shutter(t, state):
    return HSDIO(t, 8, state)


def repumper_shutter(t, state):
    return HSDIO(t, 7, state)


def d2_shutter(t, state):
    return HSDIO(t, 12, state)


def optical_pumping_shutter(t, state):
    return HSDIO(t, 10, not state)


def op_repumper_shutter(t, state):
    return HSDIO(t, 6, state)


def blowaway_shutter(t, state):
    """
    Shutters blowaway path on D2 breadboard
    Not Set!
    """
    return HSDIO(t, 2, state)  #Not Set!


def ryd595_shutter(t, state):
    """Not Set!"""
    return HSDIO(t, 2, not (state))  #Not Set!


def collection_shutter(t, state):
    return HSDIO(t, 5, not state)


shutters = [
    xz_shutter,
    y_shutter,
    y2_shutter,
    x_shutter,
    repumper_shutter,
    d2_shutter,
    optical_pumping_shutter,
    op_repumper_shutter,
    blowaway_shutter,
    ryd595_shutter,
    collection_shutter
]

hsdio_channels = instrument_triggers + rf_switches + shutters


# AO functions
def quadrupole_current(t, v):
    return AO(t, 0, v)


# analog output voltages controlling instruments with analog inputs
analog_instruments = [quadrupole_current]


def repumper_amplitude(t, v):
    return AO(t, 3, v)


def trap_amplitude(t, v):
    """Currently not useful"""
    return AO(t, 7, v)


# analog output voltages controlling variable voltage attenuators
vvas = [repumper_amplitude, trap_amplitude]


def shim_x(t, v):
    return AO(t, 4, v)


def shim_y(t, v):
    return AO(t, 5, v)


def shim_z(t, v):
    return AO(t, 6, v)


# analog output voltages controlling magnetic bias/shim fields
magnetic_bias_shims = [shim_x, shim_y, shim_z]


ao_channels = analog_instruments + vvas + magnetic_bias_shims


# Complex Functions of HSDIO and AO
def bias_shims(t, shims):
    """
    Biases the MOT shim coils to 'shims'.

    Starts biasing the shims at time t, increments the time by the time needed for the voltage
        values to settle (slew rate) and to account for the jitter in the relative timing between
        the HSDIO and AO. Returned time is "t+buffer times"
    Args:
        t (float): Start time (ms)
        shims (list): length 3 list of floats. Values will be voltage across the bias shims (in
            volts).
            Order: [x_shim_voltage, y_shim_voltage, z_shim_voltage]
    Returns:
        time after which the biasing will be complete
            currently accounts for field relaxation time and jitter in the relative timing
            between the HSDIO and AO
    """
    assert len(shims) == 3, "shims must be a list of length 3"

    for i, shim in enumerate(magnetic_bias_shims):
        shim(t, shims[i])

    # correct for a finite switching time
    t += 2

    # correct for AO-HSDIO timing instability
    t += 2

    return t


def d2_dds(t, stage):
    """
    Uses the HSDIO channels controlling the DDS to set the DDS states to one of presets defined in 
        DDS module.

    Presets are labeled bellow as 'stage_dict'.

    Changes to the DDS stage should be made such that only one bit is changed at a time, otherwise a
        grey-coding issue occurs.
    Args:
        t (float): Start time (ms)
        stage (str): state DDS should be set to
    Returns:
        t (float): End time (ms)
    """
    stage_dict = {'MOT': (0, 0, 0), 'PGC1': (0, 0, 1), 'PGC2': (0, 1, 1),
                  'LAC': (0, 1, 0), 'Recool': (1, 1, 0), 'RO': (1, 0, 0),
                  'BA': (1, 0, 1), 'NA': (1, 1, 1)}

    try:
        state = stage_dict[stage]
    except KeyError:
        print("Error setting DDS. Stage must be in {}".format(stage_dict.keys()))
        raise

    HSDIO(t, 1, state[2])  # DDS bit 0
    HSDIO(t, 3, state[1])  # DDS bit 1
    HSDIO(t, 4, state[0])  # DDS bit 2

    return t


def pulse(t, duration, channel, inverted=False):
    """
    Pulses channel on for duration then turns it off.
    Args:
        t (float): Start time (ms)
        duration (float): duration of pulse (ms)
        channel : can be int or a function of 2 arguments. Channel to be toggled. If an int the
            HDSIO function is called for that channel (0-31), if a callable it should be an HSDIO
            type function which can be toggled on/off.
        inverted: bool, should the channel be pulsed off then on instead of on then off?
    Returns:
        t: time when pulse is over
    """
    if callable(channel):
        channel(t, not inverted)
        t += duration
        channel(t, inverted)
    else:
        HSDIO(t, channel, not inverted)
        t += duration
        HSDIO(t, channel, inverted)

    return t


def ramp(ti, duration, vi, vf, channel):
    """
    Ramp AO channel from vi to vf in duration
    Args:
        ti (float): Start time (ms)
        duration (float) : length of time over which to ramp (ms), function is precise to the us
        vi (float): initial voltage(s)
        vf (float): final voltage(s)
        channel : can be int or a function of 2 arguments. Channel to be toggled. If an int the
            AO function is called for that channel (0-7). If a callable it should be an AO
            type function which can be called with a time and a voltage value (floats).
    Returns:
        tf (float): time after which ramp is completed
    """
    if callable(channel):
        func = channel
    else:
        func = lambda time, voltage: AO(time, channel, voltage)

    ao_increment = 0.001  # Shortest allowed time between changes to AO waveform
    tf = ti + duration
    times = arange(ti, tf+ao_increment, ao_increment)
    voltages = linspace(vi, vf, len(times))
    for t, v in zip(times, voltages):
        func(t, v)
    return tf


def bias_ao_ramp(t, duration, start_v, end_v, steps=None):
    """
    Ramps shim coils from start condition to end condition
    Args:
        t (float): Start time (ms)
        duration (float): duration of ramp (ms)
        start_v (list): length 3 list of floats, initial voltages for shims to take (X,Y,Z)
        end_v (list): length 3 list of floats, final voltages for shims to take (X,Y,Z)
        steps (int): number of steps over which to complete the ramp. Default is None, if it's none
            number of steps taken is determined by shortest time allowed in between changes to the
            analog output waveform

    Returns:
        t (float): End time (ms)

    """
    '''
    # Old implementation
    ar = array([[linspace(start_v[0], end_v[0], steps)[i],
                 linspace(start_v[1], end_v[1], steps)[i],
                 linspace(start_v[2], end_v[2], steps)[i]] for i in arange(steps)])
    for i in arange(steps):
        biasAO(t, ar[i])
        t += duration / steps
    biasAO(t, end_v)
    return t
    '''
    ti = t
    ao_increment = 0.001
    tf = ti+duration
    if steps is None:
        times = append(arange(t, tf, ao_increment), tf)
    else:
        times = linspace(t, tf, steps)
    voltages = linspace(start_v, end_v, len(times))

    for t, v in zip(times, voltages):
        bias_shims(t, v)
    return tf


# Device specific functions ------------------------------------------------------------------------

# pulsing triggers
def trigger_nidaq(t):
    t = pulse(t, 1, nidaq_trigger)
    return t


def trigger_ni_scope(t):
    t = pulse(t, 1, ni_scope_trigger)
    return t


def trigger_z_stage(t):
    t = pulse(t, 1, z_stage_trigger)
    return t


# MOT Coil controls
def quadrupole_current_to_voltage(current):
    """
    Function that returns the necessary Analog Out voltage needed to provide the desired MOT coil
        current
    Args:
        current (float): current, in amps, on the quadrupole field coils

    Returns:
        ao_voltage (float): the voltage to be output by the Analog Output device needed to run
            current in the quadrupole coils
    """
    return (current - 0.24) / 8.100


def quadrupole_coil_switch(t, state, current):
    """
    Switches the MOT coils on or off making use of both the HSDIO function and the AO function.
    Args:
        t (float): the time to start the switching the coils on or off
        state (bool): Desired end state of the coils
        current (float): Desired current in the quadrupole coils
    Returns:
        t (float): time after coils are switched. Currently equal to start time t
    """
    mot_coils_switch(t, state)
    quadrupole_current(t, quadrupole_current_to_voltage(current) * state)
    return t


def close_shutters(t, delay=True, xz_closed=0, y_closed=0, y2_closed=0,
                   x_closed=0):
    """
    close switchyard shutters
    Args:
        t (float): Start time (ms)
        delay (bool): if true, return time is time when all shutters have reached their final state
        xz_closed (bool): if true, XZ shutter is closed
        y_closed (bool): if true, Y shutter is closed
        y2_closed (bool): if true, Y2 shutter is closed
        x_closed (bool): if true, X shutter is closed

    Returns:
        t (float): End time. = t + max(shutter_delays)*delay
    """
    # TODO : Refactor this
    if not delay:
        delay_xz_off = 0
        delay_xz_on = 0
        delay_y_off = 0
        delay_y_on = 0
        delay_y2_on = 0
        delay_y2_off = 0
        delay_x_on = 0
        delay_x_off = 0

    else:
        delay_xz_off = XZ_Shutter_delay_off
        delay_xz_on = XZ_Shutter_delay_on
        delay_y_on = Y1_Shutter_delay_on
        delay_y_off = Y1_Shutter_delay_off
        delay_y2_on = Y2_Shutter_delay_on
        delay_y2_off = Y2_Shutter_delay_off
        delay_x_on = X_Shutter_delay_on
        delay_x_off = X_Shutter_delay_off

    dly = 0
    if xz_closed:
        xz_shutter(t - delay_xz_off, False)
        dly = max(dly, delay_xz_off)
    else:
        xz_shutter(t - delay_xz_on, True)
        dly = max(dly, delay_xz_on)
    if y_closed:
        y_shutter(t - delay_y_off, False)
        dly = max(dly, delay_y_off)
    else:
        y_shutter(t - delay_y_on, True)
        dly = max(dly, delay_y_on)
    if y2_closed:
        y2_shutter(t - delay_y2_off, False)
        dly = max(dly, delay_y2_off)
    else:
        y2_shutter(t - delay_y2_on, True)
        dly = max(dly, delay_y2_on)
    if x_closed:
        x_shutter(t - delay_x_off, False)
        dly = max(dly, delay_x_off)
    else:
        x_shutter(t - delay_x_on, True)
        dly = max(dly, delay_x_on)

    return t + dly


# Shutter timing calibrations
RP_Shutter_delay_off = 3.1
RP_Shutter_delay_on = .8

Cooling_Shutter_delay_on = 2.9
Cooling_Shutter_delay_off = 1.8

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

Collection_Shutter_delay_on = 10
Collection_Shutter_delay_off = 3

BA_Shutter_delay_on = 2.4
BA_Shutter_delay_off = 1.9
