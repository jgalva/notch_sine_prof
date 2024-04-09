def fct_print_console(dict_dfs, pch_file_ids, a_qs, F_Limit_qs, m_sat):

    """
    This function only takes values an prints them a bit nicely
    in the bash console. Good for data check but still messy to have
    among the other code.
    Also practical to comment/uncomment
    unclear
    """

    pch_x_maxval = dict_dfs[pch_file_ids[0]]["T1"].abs().max()
    pch_x_maxval_idx = dict_dfs[pch_file_ids[0]]["T1"].abs().idxmax()
    pch_x_maxval_FC = dict_dfs[pch_file_ids[0]]["T1_SC"].abs().max()

    pch_y_maxval = dict_dfs[pch_file_ids[1]]["T2"].abs().max()
    pch_y_maxval_idx = dict_dfs[pch_file_ids[1]]["T2"].abs().idxmax()
    pch_y_maxval_FC = dict_dfs[pch_file_ids[1]]["T2_SC"].abs().max()

    pch_z_maxval = dict_dfs[pch_file_ids[2]]["T3"].abs().max()
    pch_z_maxval_idx = dict_dfs[pch_file_ids[2]]["T3"].abs().idxmax()
    pch_z_maxval_FC = dict_dfs[pch_file_ids[2]]["T3_SC"].abs().max()

    print("---------------------------------")
    print("keys in dict_dfs : ")
    for key in pch_file_ids:
        print(key)
    print("---------------------------------")
    print("---------------------------------")
    print("MAXIMUM QUASI-SATIC LOADS")
    print("")
    print("Qasi-static load values extracted from the corresponding RPUG. ")
    print("Max QS values are used to cap the maximum Nastran FE forces obtained ")
    print("and apply notch to RPUG sine vibration MPE")
    print("")
    print("Satellite mass : ", m_sat, " kg")
    print("")
    print("RPUG deduced QS accelerations")
    print("")
    print("a_x_qs : ", round(a_qs[0], 2), "  g")
    print("a_y_qs : ", round(a_qs[1], 2), "  g")
    print("a_z_qs : ", round(a_qs[2], 2), "  g")
    print("")
    print("RPUG deduced total QS forces ( m_sat * a_xyz_qs)")
    print("F_x_qs : ", round(F_Limit_qs[0], 2), " N ")
    print("F_y_qs : ", round(F_Limit_qs[1], 2), " N ")
    print("F_z_qs : ", round(F_Limit_qs[2], 2), " N ")
    print("")
    print("---------------------------------")
    print("")
    print("SOL111 FINITE ELEMENT MODEL FORCES")
    print("Max force values from Nastran Finite Element Model (.pch file):")
    print(" ")
    print("Maximum Force in X (.pch file)")
    print(
        "Frequency           : ",
        round(dict_dfs[pch_file_ids[0]]["frequency"][pch_x_maxval_idx], 2),
        " Hz",
    )
    print("non-factorized (1g) : ", round(pch_x_maxval, 2), " N")
    print("MPE factorized      : ", round(pch_x_maxval_FC, 2), " N")
    print("Equivalence in Gs   : ", round(pch_x_maxval_FC / (9.81 * m_sat), 2), " g")
    print("RPUG QS a_x         : ", round(a_qs[0], 2), "  g")
    print(" ")
    print("Maximum Force in Y (.pch file)")
    print(
        "Frequency           : ",
        round(dict_dfs[pch_file_ids[1]]["frequency"][pch_y_maxval_idx], 2),
        " Hz",
    )
    print("non-factorized (1g) : ", round(pch_y_maxval, 2), " N")
    print("MPE factorized      : ", round(pch_y_maxval_FC, 2), " N")
    print("Equivalence in Gs   : ", round(pch_y_maxval_FC / (9.81 * m_sat), 2), " g")
    print("RPUG QS a_y         : ", round(a_qs[1], 2), "  g")
    print(" ")
    print("Maximum Force in Z (.pch file)")
    print(
        "Frequency           : ",
        round(dict_dfs[pch_file_ids[2]]["frequency"][pch_z_maxval_idx], 2),
        " Hz",
    )
    print("non-factorized (1g) : ", round(pch_z_maxval, 2), " N")
    print("MPE factorized      : ", round(pch_z_maxval_FC, 2), " N")
    print("Equivalence in Gs   : ", round(pch_z_maxval_FC / (9.81 * m_sat), 2), " g")
    print("RPUG QS a_z         : ", round(a_qs[2], 2), "  g")
    print(" ")
    print("---------------------------------")
    print(" ")
