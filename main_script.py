# --------------------------------------------
# Author :   J.G.Alvarez
# Date   :   19/02/2023
# Title  :   Notching for Sine Vibration MPE's
# --------------------------------------------

import glob
import os

import numpy as np
import pandas as pd
from scipy import interpolate

from src.fct_print_console import fct_print_console
from src.fct_notch_envelope_generator import fct_notch_envelope_generator
from src.fct_notch_inverse_envelope_generator import (
    fct_notch_inverse_envelope_generator,
)
from src.fct_parse_pch_data_SOL111 import fct_parse_pch_data_SOL111
from src.fct_scale_pch_dict_dfs_with_MPE import fct_scale_pch_dict_dfs_with_MPE
from src.fct_generate_notched_MPE_dict import fct_generate_notched_MPE_dict
from src.fct_calculate_qs_forces_falcon9_Oct2022 import (
    fct_calculate_qs_forces_falcon9_Oct2022,
)


from visualization.plot_MPE import plot_MPE
from visualization.plot import plot_pch

# current working directory
cwd = os.getcwd()

# folder with 'raw' FE data, in this case, in .pch format
folder_pch = os.path.join(cwd, "data", "input", "pch")

# delete old .csv files
files = glob.glob("./data/processed/csv/*")
for f in files:
    os.remove(f)

# folder for generated .csv data (processed .pch)
folder_csv = os.path.join(cwd, "data", "processed", "csv")

# folder for output pictures
folder_output = os.path.join(cwd, "output")

# -----------------------------------------------------
#  STEP 0
#  INPUT SECTION - B
# -----------------------------------------------------
#  ALL INPUT DATA ENCAPSULATED IN "./data/input/" FOLDER:
#
#  1  - satellite mass
#  2  - sine MPE (Maximum Predicted Environment):
#     (i) Quasi-Static + Static test factor
#     (ii)  Sine 50%;
#     (iii) Sine 100%
#
#  Current file should be "mostly" unmodified.
# -----------------------------------------------------
test_types = ["qualification", "acceptance"]

m_sat = 120
sat_model = "Gen3"
h_CoG = 300.07
d_IF = 15 * 25.4
test_type = test_types[1]

# Test factors
if test_type == "qualification":
    sine_vibe_factor = 1.25
elif test_type == "acceptance":
    sine_vibe_factor = 1.0
# MPE's
# From SpaceX RPUG October 2022
# 100% amplitude Sine MPE

MPE_sine_falcon9 = {
    "name": "SpaceX RPUG, October 2022, Sine MPE",
    "f_x": np.array([5, 48, 49, 61.5, 62, 58, 61, 2301.0]),
    "a_x": sine_vibe_factor * np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]),
    "f_y": np.array([5, 62, 63, 63.9, 76, 77, 65, 74, 76, 2301]),
    "a_y": sine_vibe_factor
    * np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]),
    "f_z": np.array([5, 45, 50, 100, 145, 2301]),
    "a_z": sine_vibe_factor * np.array([1.4, 1.4, 1.4, 1.4, 1.4, 1.4]),
}

MPE_sine_falcon9_50pct = {
    "name": "SpaceX RPUG, October 2022, Sine MPE 50%",
    "f_x": np.array([5, 45, 50, 100, 145, 2301.0]),
    "a_x": 0.5 * sine_vibe_factor * np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5]),
    "f_y": np.array([5, 45, 50, 100, 145, 2301]),
    "a_y": 0.5 * sine_vibe_factor * np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5]),
    "f_z": np.array([5, 45, 50, 100, 145, 2301]),
    "a_z": 0.5 * sine_vibe_factor * np.array([1.4, 1.4, 1.4, 1.4, 1.4, 1.4]),
}

# ------------------------------------------------
#  STEP 1
#  calculation of maximum MPE QS forces
# ------------------------------------------------

# calculate accs and forces in XYZ on base to qs MPE and S/C mass
a_qs, F_Limit_qs = fct_calculate_qs_forces_falcon9_Oct2022(
    test_type, m_sat,  h_CoG, d_IF
)
print(a_qs, F_Limit_qs)

# ------------------------------------------------
#  STEP 2
#  parse data from .pch and convert into .csv and convert it into pandas
#  DataFrames:
#
# dict_dfs = {
#        sine_x : "DataFramed sine_x.pch data",
#        sine_y : "DataFramed sine_y.pch data",
#        sine_z : "DataFramed sine_z.pch data",
#        }
# ------------------------------------------------

# parse file names of .pch files in folder

list_all_pch = ["sine_x.pch", "sine_y.pch","sine_z.pch"]
dict_dfs = {}

for file in list_all_pch:

    # absolute path for input file
    abspath_pch_file = os.path.join(folder_pch, file)

    # absolute path for output file
    key = file.split('.')[0]
    abspath_csv_file = os.path.join(folder_csv, key + ".csv")

    # parse data from .pch and convert into .csv
    fct_parse_pch_data_SOL111(abspath_pch_file, abspath_csv_file)

    # conversion of 
    dict_dfs[key] = pd.read_csv(abspath_csv_file)

# extract key names to a list
pch_file_ids = list(dict_dfs)

# ------------------------------------------------
#  STEP 4
#  Scale .pch FE output with the RPUG sine spectra
# ------------------------------------------------

dict_dfs_scaled = fct_scale_pch_dict_dfs_with_MPE(
        dict_dfs, 
        MPE_sine_falcon9
        )

# ------------------------------------------------
#  STEP 5
#  Notching of results on base to max QS forces
# ------------------------------------------------

# input : dictionary, MPE-Scaled (dict_dfs)  ; Quasi-static forces
# output: Notched MPE
# modifications:
#  - add new column with capped values (idx: ".._cap") using max QS forces
#  - add new column with notching factor (idx: "NF")
#  - add new column = MPE * NF

MPE_notched = fct_generate_notched_MPE_dict(
        dict_dfs_scaled, 
        F_Limit_qs
        )

# ---------------------------------------------------------
# STEP 6 - OVERVIEW CONSOLE RESULT DISPLAY MODULE
# ---------------------------------------------------------

# all console print statements
fct_print_console(
    dict_dfs,
    pch_file_ids,
    a_qs,
    F_Limit_qs,
    m_sat,
)
# ------------------------------------------------
#  STEP 7
#  Generate envelope/notch curves for MPE's
# ------------------------------------------------

# generate notch envelope curve in Y and Z

# when no notching is needed, take the acc_?_final column, for example:
# acc_z_final = dict_dfs[pch_file_ids[2]]["MPE_notched"]


# X
acc_x_final = dict_dfs[pch_file_ids[0]]["MPE_notched"]
#   acc_x_final = fct_notch_inverse_envelope_generator(
#       dict_dfs[pch_file_ids[0]]["frequency"],
#       dict_dfs[pch_file_ids[0]]["MPE_notched"],
#       48,  # x1
#       0.1,  # slope
#       62,  # x2
#       -0.1,  # slope
#       1.6,  # bottom y value
#   )


acc_y_final = dict_dfs[pch_file_ids[1]]["MPE_notched"]

# Y
#   acc_y_final = fct_notch_inverse_envelope_generator(
#       dict_dfs[pch_file_ids[1]]["frequency"],
#       dict_dfs[pch_file_ids[1]]["MPE_notched"],
#       63.0,  # x1
#       0.1,  # slope
#       77,  # x2
#       -0.1,  # slope
#       1.55,  # bottom y value
#   )

# Z
# in this case, no notch in Z is needed, thus commented out
acc_z_final = dict_dfs[pch_file_ids[2]]["MPE_notched"]

#   acc_z_final = fct_notch_envelope_generator(
#       dict_dfs[pch_file_ids[2]]["frequency"],
#       dict_dfs[pch_file_ids[2]]["MPE_notched"],
#       43,
#       -0.12,
#       54,
#       0.2,
#       1.1,
#   )


# -----------------------------------------------------
# Final delivery MPE
# -----------------------------------------------------

MPE_sine_falcon9_delivery = {
    "name": "SpaceX RPUG, October 2022, Sine MPE (FINAL)",
    "f_x": dict_dfs[pch_file_ids[0]]["frequency"],
    "a_x": acc_x_final,
    "f_y": dict_dfs[pch_file_ids[1]]["frequency"],
    "a_y": acc_y_final,
    "f_z": dict_dfs[pch_file_ids[2]]["frequency"],
    "a_z": acc_z_final,
}

# -----------------------------------------------------
#  STEP 8
#  plot generation
# -----------------------------------------------------

#  plot Max force vs. frequency, X Y Z

TR_to_plot = ["T1", "T2", "T3"]
for i, TR in enumerate(TR_to_plot):
    output_fig_abspath = os.path.join(folder_output, test_type + "_" + TR + ".png")
    df_keys_to_plot = [TR, TR + "_SC", TR + "_SC_cap"]
    freq_range = [0, 100.0]
    plot_pch(
        dict_dfs,
        pch_file_ids[i],
        df_keys_to_plot,
        freq_range,
        F_Limit_qs[i],
        output_fig_abspath,
        test_type,
    )

#  plot final delivery MPE's for X Y Z
freq_range_MPE_x = [0, 100]
freq_range_MPE_y = [0.5, 3.5]

DOFs = ["x", "y", "z"]
for DOF in DOFs:

    # absolute paths for output figures
    output_fig_MPE_abspath = os.path.join(
        folder_output, test_type + "_MPE_" + DOF + ".png"
    )
    output_fig_MPE_50pct_abspath = os.path.join(
        folder_output, test_type + "_MPE_50pct_" + DOF + ".png"
    )

    # plot 50% amplitude MPE's
    plot_MPE(
        MPE_sine_falcon9_50pct,
        DOF=DOF,
        freq_range_x=freq_range_MPE_x,
        freq_range_y=freq_range_MPE_y,
        output_fig_abspath=output_fig_MPE_50pct_abspath,
        test_type=test_type,
        m_sat=m_sat,
        sat_model=sat_model,
    )

    # plot 100% amplitude MPE's, NOTCHED
    plot_MPE(
        MPE_sine_falcon9,
        # MPE_notched,
        # MPE_sine_falcon9_delivery,
        DOF=DOF,
        freq_range_x=freq_range_MPE_x,
        freq_range_y=freq_range_MPE_y,
        output_fig_abspath=output_fig_MPE_abspath,
        test_type=test_type,
        m_sat=m_sat,
        sat_model=sat_model,
    )
