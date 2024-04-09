def plot_MPE(
    *my_dicts,
    DOF,
    freq_range_x,
    freq_range_y,
    output_fig_abspath,
    test_type,
    m_sat,
    sat_model
):

    import matplotlib.pyplot as plt

    """
    Note asterisk left from *my_dicts, meaning that 
    multiple dictionaries can be passed as input.
    output_fig_abspath acts as a keyword.
    """

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

    plt.xlabel("Freq. [Hz]", fontsize=20)
    plt.ylabel("$Acc. [g]$", fontsize=20)

    for dct in my_dicts:
        ax.plot(
            dct["f_" + DOF],
            dct["a_" + DOF],
            # color=color[i],
            linestyle="-",
            linewidth=2.0,
            label=dct["name"],
        )
    plt.xlim(
        [
            freq_range_x[0],
            freq_range_x[1],
        ]
    )
    plt.ylim(
        [
            freq_range_y[0],
            freq_range_y[1],
        ]
    )

    ax.text(
        0.09,
        0.95,
        "AXIS : " + DOF,
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

    ax.text(
        0.1,
        0.85,
        sat_model + ", " + str(m_sat) + " Kg",
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax.transAxes,
        fontsize=11,
    )

    fsize = 12
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)
    plt.title(" Maximum Predicted Environments (MPE's)")
    plt.legend()
    plt.savefig(output_fig_abspath, bbox_inches="tight")
    plt.close()
