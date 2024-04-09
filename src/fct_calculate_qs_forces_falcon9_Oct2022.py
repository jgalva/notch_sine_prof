import os
from scipy import interpolate
import numpy as np


def fct_calculate_qs_forces_falcon9_Oct2022(
    test_type,m_sat,  h_CoG, d_IF
    ):
    
    g = 9.81

    if test_type == "qualification":
        qs_factor = 1.25
    elif test_type == "acceptance":
        qs_factor = 1.1




    factor = qs_factor
    print("")
    print("Load Spec for :  " + test_type)
    print("")
    a_qs, F_Limit_qs = np.empty(3), np.empty(3)
    accs = ["a_x", "a_y", "a_z"]

    if 61.0 <= m_sat <= 150.0:
        print("Mass within [61.0 , 150.] kg range")
        LCs = [
            [5, 10],
            [5, -10],
            [-5, 10],
            [-5, -10],
            [13, 3.5],
            [13, -3.5],
            [-13, 3.5],
            [-13, -3.5],
        ]
    if 251.0 <= m_sat <= 450.0:
        print("Mass within [251.0 ,  450.0] kg range")
        LCs = [
            [2, 5],
            [2, -5],
            [-2, 5],
            [-2, -5],
            [11, 2.5],
            [11, -2.5],
            [-11, 2.5],
            [-11, -2.5],
        ]

    # Max line loads calculated according to:
    # "ECSS-E-HB-32-26A, 19 February 2013
    # section6.2.6.2. page 143

    f_envelope = 0
    acc_axial_envelope = 0
    for LC in LCs:
        acc_lateral = LC[0] * factor
        acc_axial = LC[1] * factor

        N = m_sat * g * acc_axial
        M_lat = m_sat * g * acc_lateral * h_CoG
        f_N = N / (np.pi * d_IF)
        f_M = 4 * M_lat / (np.pi * d_IF**2)

        f = abs(round(f_N + f_M, 1))
        if f_envelope < abs(round(f_N + f_M, 1)):
            f_envelope = abs(round(f_N + f_M, 1))

        if acc_axial_envelope < abs(round(acc_axial, 2)):
            acc_axial_envelope = abs(round(acc_axial, 2))

    acc_lat_eq = round(f_envelope * np.pi * d_IF**2 / (4 * m_sat * h_CoG * g), 2)
    # print(acc_lat_eq)
    a_qs = [acc_lat_eq, acc_lat_eq, acc_axial_envelope]
    F_qs = [
        round(acc_lat_eq * g * m_sat, 2),
        round(acc_lat_eq * g * m_sat, 2),
        round(acc_axial_envelope * g * m_sat, 2),
    ]
    return a_qs, F_qs
