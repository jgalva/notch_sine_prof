"""
SpaceX Rideshare Payload User Guide, March 2022, 
page 9 , table 3-3.
Sinusoidal Vibration MPE, Dispenser Ring 

 - frequencies given in Hz 
 - accelerations given in g's

IMPORTANT!!!
MPE's converted to ICEYE payload axis system

i.e. Z_iceye = X_SpaceX
"""
import numpy as np

# Quasi-Static MPE (before static test factor)
# QS accelerations dependent on satellite mass
# acceleration units : [g]  ; mass units : [kg]
MPE_QS_falcon9 = {
    "name": "SpaceX RPUG, March 2022, QS MPE",
    "mass": np.array([1, 30, 100, 225, 400, 600, 900]),
    "a_x": np.array([7.4, 7.4, 6.4, 5.5, 5.1, 5.1, 5.1]),
    "a_y": np.array([12.9, 12.9, 12.0, 11.1, 10.3, 9.4, 8.1]),
    "a_z": np.array([12.9, 12.9, 12.0, 11.1, 10.3, 9.4, 8.1]),

    # static test factor
    # RPUG Falcon9, 03.2022, sec 3.4.3 "Payload Unit Test Levels"
    "static_test_factor" : 1.1,
}

# 50% amplitude Sine MPE
MPE_sine_falcon9_50pct = {
    "name": "SpaceX RPUG, March 2022, Sine MPE, 50% amplitude",
    "f_x": np.array(0,5, 45, 50, 100, 145, 2001.0]),
    "a_x": 0.5 * np.array([1.4, 1.4, 3.0, 3.0, 3.0, 3.0]),
    "f_y": np.array([0,5, 45, 50, 100, 145, 2001]),
    "a_y": 0.5 * np.array([1.5, 1.5, 2.0, 2.0, 2.0, 2.0]),
    "f_z": np.array([0,5, 45, 50, 100, 145, 2001]),
    "a_z": 0.5 * np.array([1.5, 1.5, 2.0, 2.0, 2.0, 2.0]),
}

# 100% amplitude Sine MPE
MPE_sine_falcon9 = {
    "name": "SpaceX RPUG, March 2022, Sine MPE",
    "f_x": np.array([5, 45, 50, 100, 145, 2001.0]),
    "a_x": np.array([1.4, 1.4, 3.0, 3.0, 3.0, 3.0]),
    "f_y": np.array([5, 45, 50, 100, 145, 2001]),
    "a_y": np.array([1.5, 1.5, 2.0, 2.0, 2.0, 2.0]),
    "f_z": np.array([5, 45, 50, 100, 145, 2001]),
    "a_z": np.array([1.5, 1.5, 2.0, 2.0, 2.0, 2.0]),
}



# -------------------------------------------------------------
""" 
from presentation about EXOport Neptune: Clocking concept

"""
MPE_sine_neptune_exolaunch = {
    "name": "Exolaunch MPE sine vibe (Neptune adaptor) ",
    "f_x": [0.0, 5.0, 30, 32, 35, 36, 43, 48, 82, 100, 2001],
    "a_x": [1.5, 1.5, 1.5, 2.4, 2.4, 2, 2, 2.6, 2.6, 2.2, 2.2],
    "f_y": [0.0, 5.0, 20, 22, 43, 47, 100, 2001],
    "a_y": [1.5, 1.5, 1.5, 1.8, 1.8, 2.3, 2.3, 2.3],
    "f_z": [0.0, 5.0, 20, 22, 26, 27, 45, 51, 100, 2001],
    "a_z": [1.4, 1.4, 2, 4, 4, 2, 2, 4, 4, 4],
}
# -------------------------------------------------------------
