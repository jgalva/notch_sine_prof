def fct_parse_pch_data_SOL111(
    abspath_pch_input_file,
    abspath_csv_output_file,
):
    import os
    from pathlib import Path

    """
    Description:
    -----------

    This function takes a single .pch as an input, 
    parses the data and formats it into
    a .csv readable file. Valid for Nastran SOL111 nodal output.
    rIinput and output files need to be passed as absolute
    path.


    :abspath_pch_input_file:  .pch Nastran file, absol. path required.
    :abspath_csv_output_file  .csv output file, absol.  path required.

    """

    with open(abspath_pch_input_file, "r") as file:
        lines = [line.rstrip() for line in file]

    # ------------------------------------------------------------------
    # .pch file check
    if len(lines) % 11 > 0:
        raise Exception("FATAL ERROR : .pch file has an invalid number of lines!")
    # ------------------------------------------------------------------

    # check if path for output file exists, otherwise create
    Path(os.path.dirname(abspath_csv_output_file)).mkdir(parents=True, exist_ok=True)
    # ------------------------------------------------------------------

    print("")
    print("# File reading successful!")
    print(".pch file name               :  ", abspath_pch_input_file.split("/")[-1])
    print("Total amount of lines        :  ", str(len(lines)))
    print("Total amount of punch cards  :  ", str(len(lines) / 11))

    # ------------------------------------------------------------------
    # total number of cards in .pch file
    n_cards = int(len(lines) / 11)
    with open(abspath_csv_output_file, "w") as f:

        # pandas df header
        # left out : 'title,subtitle,label,subcase_id,
        csv_header = "node,frequency,T1,T2,T3,R1,R2,R3,val7,val8,val9,val10,val11,val12"

        f.write(csv_header + "\n")  # python will convert \n to os.linesep

        for j in range(n_cards):
            new_csv_line = []

            # each punch card has 11 lines
            # see https://femci.gsfc.nasa.gov/sine_vib/ for explanation of
            # fields in punch format
            i = j * 11

            title = lines[i].split("=")[-1][:50].strip()
            subtitle = lines[i + 1].split("=")[-1][:50].strip()
            label = lines[i + 2].split("=")[-1][:50].strip()
            subcase_id = lines[i + 4].split("=")[-1][:50].strip()
            frequency = float(lines[i + 6].split()[-2])
            node = int(lines[i + 7].split()[0])
            T1 = float(lines[i + 7].split()[2])
            T2 = float(lines[i + 7].split()[3])
            T3 = float(lines[i + 7].split()[4])
            R1 = float(lines[i + 8].split()[1])
            R2 = float(lines[i + 8].split()[2])
            R3 = float(lines[i + 8].split()[3])
            val7 = float(lines[i + 9].split()[1])
            val8 = float(lines[i + 9].split()[2])
            val9 = float(lines[i + 9].split()[3])
            val10 = float(lines[i + 10].split()[1])
            val11 = float(lines[i + 10].split()[2])
            val12 = float(lines[i + 10].split()[3])

            # assemble row to be appended to .csv output file
            csv_list = [
                # title,subtitle,label,subcase_id,
                node,
                frequency,
                T1,
                T2,
                T3,
                R1,
                R2,
                R3,
                val7,
                val8,
                val9,
                val10,
                val11,
                val12,
            ]

            # format row string
            csv_line = str(csv_list).replace("[", "")
            csv_line2 = csv_line.replace("]", "")
            csv_line3 = csv_line2.replace(" ", "")

            # write row as a single line
            f.write(csv_line3 + "\n")  # python will convert \n to os.linesep

    print("Output file generated : " + abspath_csv_output_file.split("/")[-1])

    return None
