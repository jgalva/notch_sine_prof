def plot_pch(
    dict_dfs, pch_id, keys_to_plot, freq_range, cap_value, output_fig_abspath, test_type
):

    import matplotlib.pyplot as plt

    df1 = dict_dfs[pch_id]
    df1_keys = list(df1)

    # figure plotting
    fig, ax = plt.subplots(figsize=(9, 6))
    plt.grid(
        visible=True,
        which="major",
        color="#999999",
        linestyle="-",
        linewidth=0.5,
        alpha=0.8,
    )
    plt.grid(
        visible=True,
        which="minor",
        color="#999999",
        linestyle="-",
        linewidth=0.5,
        alpha=0.8,
    )
    plt.minorticks_on()

    plt.xlabel("Freq. $[Hz]$", fontsize=20)
    plt.ylabel("Force $[N]$", fontsize=20)

    # plot line with cap value
    for key in keys_to_plot:
        ax.plot(
            df1[df1_keys[1]],
            df1[key],
            # color=color[i],
            linestyle="-",
            linewidth=2.0,
            label=key,
        )

    plt.xlim([freq_range[0], freq_range[1]])
    fsize = 10
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)
    ax.plot(
        freq_range,
        [cap_value, cap_value],
        color="r",
        linestyle="--",
        linewidth=1.0,
        label="QS RPUG force limit",
    )
    ax.text(
        0.09,
        0.95,
        f"{pch_id}" + ".pch",
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax.transAxes,
        fontsize=16,
    )
    ax.text(
        0.09,
        0.90,
        test_type,
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax.transAxes,
        fontsize=12,
    )
    plt.title(keys_to_plot[0])
    plt.legend()
    plt.savefig(output_fig_abspath, bbox_inches="tight")
    plt.close()
