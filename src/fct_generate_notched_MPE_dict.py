def fct_generate_notched_MPE_dict(dict_dfs, F_Limit_qs):

    pch_file_ids = list(dict_dfs.keys())
    translations = ["T1_SC", "T2_SC", "T3_SC"]

    if "MPE_name" not in pch_file_ids:
        raise Exception("FE data not MPE-factorized!")

    for i, TR in enumerate(translations):

        # local renaming for shorter code lines
        df = dict_dfs[pch_file_ids[i]]

        # cap forces i.e. trim with max QS value on that axis
        df[TR + "_cap"] = df[TR].clip(upper=F_Limit_qs[i])

        # NF = capped max forces / uncapped max forces. NF <= 1.0
        df["NF"] = df[TR + "_cap"] / df[TR]

        if df["NF"].max() > 1.00:
            raise Exception("ERROR : Notching factor is larger than 1.0")

        # apply NF + Generation of columns for notched profile
        df["MPE_notched"] = df["MPE"] * df["NF"]

    # generate new MPE dictionary for notched profile
    MPE_notched = {
        "name": dict_dfs["MPE_name"] + " NOTCHED",
        "f_x": dict_dfs[pch_file_ids[0]]["frequency"],
        "a_x": dict_dfs[pch_file_ids[0]]["MPE_notched"],
        "f_y": dict_dfs[pch_file_ids[1]]["frequency"],
        "a_y": dict_dfs[pch_file_ids[1]]["MPE_notched"],
        "f_z": dict_dfs[pch_file_ids[2]]["frequency"],
        "a_z": dict_dfs[pch_file_ids[2]]["MPE_notched"],
    }

    return MPE_notched
