

# --------------------------------------------
# Author :   J.G.Alvarez
# Date   :   19/02/2023
# Title  :   Notching for Sine Vibration MPE's
# --------------------------------------------


# -----------------------------------------------------
#  STEP 0
#  INPUT SECTION - B
# -----------------------------------------------------
#  1  - satellite mass
#  2  - Sine vibe security factor
#  3  - sine MPE (Maximum Predicted Environment):
#     (i) Quasi-Static; (ii)  Sine 50%; (iii) Sine 100%
# -----------------------------------------------------
# ------------------------------------------------
#  STEP 1
#  calculation of maximum MPE QS forces
# ------------------------------------------------

# ------------------------------------------------
# STEP 2
# conversion of all .csv in to pandas Dataframes.
# ------------------------------------------------
# dictionary structure for DataFrame storage:
#
# dict_dfs = {
#        key1 : "DataFramed file1.pch",
#        key2 : "DataFramed file2.pch",
#        ...
#        }
# ------------------------------------------------

# -------------------------------------------------------
#  STEP 3
#  Scale .pch FE output with the sine spectra from Exolauch
# -------------------------------------------------------

# ---------------------------------------------------------
# STEP 4 - OVERVIEW CONSOLE RESULT DISPLAY MODULE
# ---------------------------------------------------------

# ------------------------------------------------
#  STEP 5
#  Notching of results on base to max QS forces
# ------------------------------------------------

NASTRAN SOL111 are run with a given acceleration amplitude.
usually 1 g, i.e. 9.81 m/s**2 at all frequencies.
.pch results are to be factorized according to
the corresponding RPUG spectrum.

1 - the SPCFORCES in the .pch are the response of an enforced
sinus vibration of amplitude 1 g, where g = 9.81 m/s^2

The applied NASTRAN force function is specified with the RLOAD1 NASTRAN command,
which takes as an input the values specified in the TABLED1.

In order to calculate the quasi-static total force specified in
the RPUG, one needs to apply the following formula:

    F_t = m * n_g * g  

F_t  : Total force
m    : payload mass
n_g  : number of g's in RPUG spectrum
g    : gravity acceleration

# Update of "dict_dfs" storage dictionary:
# add new column to X, Y and Z DataFrames
# then, we take the T1, T2 and T3 columns from sine_x, sine_y and sine_z
# dataframes and cap or clip the values
# larger than the QS at the corresponding axis

# ------------------------------------------------
#  STEP 6
#  Generate envelope/notch curves for MPE's
# ------------------------------------------------
# -----------------------------------------------------
#  STEP 7
#  plot generation
# -----------------------------------------------------
#  7.1
#  plot Max force vs. frequency, X Y Z
# -----------------------------------------------------
# -----------------------------------------------------
#  7.2
#  plot final delivery MPE's for X Y Z
# -----------------------------------------------------


