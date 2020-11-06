# Descriptively named functions to operate HSDIO and AO channels
from numpy import *  # Totally redundant but helps IDE understand our scope

# utility functions
HSDIO = experiment.LabView.HSDIO.add_transition
AO = experiment.LabView.AnalogOutput.add_transition
label = experiment.functional_waveforms_graph.label

# Instrument Triggers ----------------------------------------------------------
NIScope_Trig = lambda t, state: HSDIO(t, 2, state)  #Not Set!
Zstage_Trig = lambda t, state: HSDIO(t, 2, state)  #Not Set!
MOT_Andor_Trig = lambda t, state: HSDIO(t, 15, state)
NIDAQ_Trig = lambda t, state: HSDIO(t, 14, state)
Hamamatsu_Trig = lambda t, state: HSDIO(t, 31,state)
MOT_coils_switch = lambda t, state: HSDIO(t, 17, not (state))
SPCM_gate = lambda t, state: HSDIO(t, 2, state)  #Not Set!
###SPCM Clocks on succsessive rising edges
SPCM_clock = lambda t, state: HSDIO(t, 24, state)

instrument_triggers = [
    NIScope_Trig,
    Zstage_Trig,
    MOT_Andor_Trig,
    NIDAQ_Trig,
    Hamamatsu_Trig,
    MOT_coils_switch,
    SPCM_gate,
    SPCM_clock
]

# RF Switches ------------------------------------------------------------------
uW_switch = lambda t, state: HSDIO(t, 0, not state)
HF_switch = lambda t, state: HSDIO(t, 18, not state)
D2_switch = lambda t, state: HSDIO(t, 19, not state)
vODT_switch = lambda t, state: HSDIO(t, 20, not state)
Ryd595_switch = lambda t, state: HSDIO(t, 21, state)
Ryd685_switch = lambda t, state: HSDIO(t, 22, state)
OP_switch = lambda t, state: HSDIO(t, 23, state)
chop = lambda t, state: HSDIO(t, 24, state)


rf_switches = [
    D2_switch,
    HF_switch,
    vODT_switch,
    Ryd685_switch,
    Ryd595_switch,
    chop,
    uW_switch,
    OP_switch
]

# Shutter Switches -------------------------------------------------------------
XZ_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 25,state)
Y_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 11, state)
Y2_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 8, state)
X_Only_Shutter_switch_init = lambda t, state: HSDIO(t, 13, not (state))
RP_Shutter_switch_init = lambda t, state: HSDIO(t, 7,state)
Cooling_Shutter_switch_init = lambda t, state: HSDIO(t, 12, state)
OP_Shutter_switch_init = lambda t, state: HSDIO(t, 10, not(not(state)))
OP_RP_Shutter_switch_init = lambda t, state: HSDIO(t, 6, state)
Blowaway_Shutter_switch_init = lambda t, state: HSDIO(t, 2, state)  #Not Set!
Ryd595_Shutter_switch_init = lambda t, state: HSDIO(t, 2, not (state))  #Not Set!
Collection_Shutter_switch_init = lambda t, state: HSDIO(t, 5, not(state) )
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

shutter_switches = [
    XZ_Only_Shutter_switch,
    Y_Only_Shutter_switch,
    Y2_Only_Shutter_switch,
    X_Only_Shutter_switch,
    RP_Shutter_switch,
    Cooling_Shutter_switch,
    OP_Shutter_switch,
    OP_RP_Shutter_switch,
    Blowaway_Shutter_switch,
    Ryd595_Shutter_switch,
    Collection_Shutter_switch
]

hsdio_channels = instrument_triggers + rf_switches + shutter_switches

# AO functions

MOT_coilsAO = lambda t, v: AO(t, 0, v)
HF_amplitude = lambda t, v: AO(t, 3, v)
vODT_power = lambda t, v: AO(t, 7, v)  # Currently not useful
shim_x = lambda t, v: AO(t, 4, v)
shim_y = lambda t, v: AO(t, 5, v)
shim_z = lambda t, v: AO(t, 6, v)


ao_channels = [
    MOT_coilsAO,
    HF_amplitude,
    vODT_power,
    shim_x,
    shim_y,
    shim_z
]


# Complex Functions of HSDIO and AO
def biasAO(t, shims):
    """
    Biases the MOT shim coils to 'shims'.

    Starts biasing the shims at time t, increments the time by the time needed for the voltage
        values to settle (slew rate) and to account for the jitter in the relative timing between
        the HSDIO and AO. Returned time is "t+buffer times"
    Args:
        t: time to start biasing the shims
        shims: length 3 array-like of floats. Values will be voltages the shims will take.
            Should be formatted: [x_shim_voltage, y_shim_voltage, z_shim_voltage]
    Returns:
        time after which the biasing will be complete
            currently accounts for slew time and jitter in the relative timing between the
            HSDIO and AO
    """
    assert len(shims) == 3, "shims must be a length 3 array-like"

    for i, shim in enumerate(["x", "y", "z"]):
        eval("shim_{}({},{})".format(shim, t, shims[i]))

    # correct for a finite switching time
    t += 2

    # correct for AO-HSDIO timing instability
    t += 2

    return t


def D2_DDS(t, stage):
    """
    Uses the HSDIO channels controlling the DDS to set the DDS states to one of presets defined in 
        DDS module.

    Presets are labeled bellow as 'stage_dict'.

    Changes to the DDS stage should be made such that only one bit is changed at a time, otherwise a
        grey-coding issue occurs.
    Args:
        t: time when DDS state is set
        stage: state DDS should be set to
    Returns:
        t: time when DDS switch is complete. Currently equal to the input time
    """
    stage_dict = {'MOT': (0, 0, 0), 'PGC1': (0, 0, 1), 'PGC2': (0, 1, 1),
                  'LAC': (0, 1, 0), 'Recool': (1, 1, 0), 'RO': (1, 0, 0),
                  'BA': (1, 0, 1), 'NA': (1, 1, 1)}

    state = stage_dict[stage]
    HSDIO(t, 1, state[2])  # DDS bit 0
    HSDIO(t, 3, state[1])  # DDS bit 1
    HSDIO(t, 4, state[0])  # DDS bit 2

    return t


def pulse(t, duration, channel, invert = False):
    """
    Pulses channel on for duration then turns it off.
    Args:
        t: time to start pulse
        duration: duration of pulse (ms)
        channel: int or callable, channel to be toggled. If an int the HDSIO function is called, if
            a callable it should be an HSDIO type function which can be toggled on/off
        invert: bool, should the channel be pulsed off then on instead of on then off?
    Returns:
        t: time when pulse is over
    """
    if callable(channel):
        func = channel
    else:
        func = lambda t0, state : HSDIO(t0, channel, state)

    func(t, not invert)
    t += duration
    func(t, invert)
    return t


def ramp(ti, duration, vi, vf, channel):
    """
    Ramp AO channel from vi to vf in duration
    Args:
        ti: start time for the ramp
        duration: length of time over which to ramp
        vi: initial voltage
        vf: final voltage
        channel: int or callable, AO channel to be ramped. If an int the AO function is called on
            for this channel, if it's a callable it should an AO function which can be set to a
            float value at a time t.
    Returns:
        tf: time after which ramp is completed
    """
    if callable(channel):
        func = channel
    else:
        func = lambda time, voltage: AO(time, channel, voltage)

    ao_increment = 0.001  # Shortest allowed time between changes to AO waveform
    tf = ti + duration
    times = arange(ti, tf, ao_increment)
    voltages = linspace(vi, vf, len(times))
    for t, v in zip(times, voltages):
        func(t, v)
    return tf


# Device specific functions
def trigNIDAQ(t):
    t = pulse(t, 1, NIDAQ_Trig)
    return t


def MOTAOVolt(current):
    return (current - 0.24) / 8.100


def switchcoils(t, state):
    MOT_coils_switch(t, state)
    MOT_coilsAO(t, MOTAOVolt(MOT_Coil_Current) * state)

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
