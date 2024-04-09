def fct_scale_pch_dict_dfs_with_MPE(dict_dfs, MPE_sine):

    from scipy import interpolate

    freqs = ["f_x", "f_y", "f_z"]
    accs = ["a_x", "a_y", "a_z"]

    pch_file_ids = list(dict_dfs.keys())

    # create dictionary for interpolated MPE
    # (interpolate at frequencies from .pch)
    MPE_interp = {}
    MPE_interp["f"] = dict_dfs[pch_file_ids[0]]["frequency"]

    for i, freq in enumerate(freqs):
        x, y = MPE_sine[freq], MPE_sine[accs[i]]
        fct_interpolate_MPE = interpolate.interp1d(x, y)
        MPE_interp[i] = fct_interpolate_MPE(MPE_interp["f"])

    # scale values of DataFrame Columns by multiplying it by MPE profile
    columns_to_scale = [
        "T1",
        "T2",
        "T3",
        "R1",
        "R2",
        "R3",
    ]

    for i in range(3):

        # rename locally
        df = dict_dfs[pch_file_ids[i]]

        # add MPE column to "i-th" DataFrame
        df["MPE"] = MPE_interp[i]

        # add new columns to DataFrame:
        # "_SC" = "SCALED"
        for key in columns_to_scale:
            df[key + "_SC"] = (df[key] * MPE_interp[i]) * 9.81
    dict_dfs["MPE_name"] = MPE_sine["name"]
    return dict_dfs
