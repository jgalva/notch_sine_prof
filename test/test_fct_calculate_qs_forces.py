import sys
import os

sys.path.append("..")

from src.fct_calculate_qs_forces import fct_calculate_qs_forces

cfd = os.path.dirname(os.path.abspath(__file__))


def test_fct_calc_qs_forces_static_factor():
    from data.input.MPEs.MPEs import MPE_QS_falcon9
    from data.input.MPEs.MPEs import MPE_sine_falcon9_50pct
    from data.input.MPEs.MPEs import MPE_sine_falcon9
    from data.input.satellite_props.satellite_props import m_sat
    from data.input.satellite_props.satellite_props import g

    test_factor = MPE_QS_falcon9["static_test_factor"]

    a_qs, F_Limit_qs = fct_calculate_qs_forces(
        m_sat,
        g,
        MPE_QS_falcon9,
    )

    tol = 0.001
    assert (a_qs[0] - F_Limit_qs[0] * (1 / test_factor)) < tol
    assert (a_qs[1] - F_Limit_qs[1] * (1 / test_factor)) < tol
    assert (a_qs[2] - F_Limit_qs[2] * (1 / test_factor)) < tol


# to do


def test_compare_max_capped_vs_max_uncapped_equal_min_NF():
    pass


def test_ratio_between_SC_and_pch_output_equals_MPE():
    pass
