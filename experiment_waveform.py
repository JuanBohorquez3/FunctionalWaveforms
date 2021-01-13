from hybrid_wave_functions import *
from experiment_phases import *

ro_shutters = [closeXZShutter, closeYShutter, closeY2Shutter, closeXShutter]

t = 0
t = initialize(t)
t = calibration(t)
t = mot_loading(
    t,
    MOT_loading_time,
    MOT_hyperfine_power,
    MOT_shim,
    MOT_Coil_Current,
    trigger_andor=True,
    exposure_time=AndorExpT,
    keep_quadrupole=True
)

t = pgc1(
    t,
    PGC_1_time,
    PGC_1_hyperfine_power,
    PGC1_shim,
    hODT_delay,
    trap_on=True,
    chop=False
)

t = pgc2(
    t,
    PGC_2_time,
    PGC_2_hyperfine_power,
    PGC2_shim
)

t = light_assisted_collisions(
    t,
    LAC_Time,
    LAC_hyperfine_power,
    LAC_shim
)

t = recool(
    t,
    Recool_time,
    Recool_hyperfine_power,
    Recool_shim
)

t = trap_in_dark(t, Trap_Hold_time)
# Set shutters to RO configuration. Make sure shutters are settled before RO starts
t = max(t, close_shutters(t - Trap_Hold_time/2, delay=True, *ro_shutters))

t = fluorescence_readout(
    t,
    RO_Time,
    RO1_hyperfine_power,
    RO1_shim,
    RO1_bins,
    RO1_drops,
    SPCM_gates,
    chop=DoChop,
    shutter_states=ro_shutters,
    trigger_andor=False,
    trigger_hm=True
)

t = close_shutters(t, delay=True)
t = recool(
    t,
    Recool2_time,
    Recool_hypoerfine_power,
    Recool_shim
)


t = trap_in_dark(t, GapTime)  # -------------------------------------------------- Retention
t = pulse(t, GapTime, trap_switch, inverted=True)  # ---------------------------- SNR
t = max(t, close_shutters(t - GapTime/2, delay=True, *ro_shutters))

t = fluorescence_readout(
    t,
    RO_Time,
    RO1_hyperfine_power,
    RO1_shim,
    RO1_bins,
    RO1_drops,
    SPCM_gates,
    chop=DoChop,
    shutter_states=ro_shutters,
    trigger_andor=False,
    trigger_hm=True
)

close_shutters(t,delay=False)
t = trap_in_dark(t, GapTime*1.8)
t = pulse(t, 2, trap_switch, inverted=True)

t = mot_loading(
    t,
    MOT_loading_time,
    MOT_hyperfine_power,
    MOT_shim,
    MOT_Coil_Current,
    trigger_andor=True,
    exposure_time=AndorExpT,
    keep_quadrupole=True
)

repumper_switch(t, 0)
