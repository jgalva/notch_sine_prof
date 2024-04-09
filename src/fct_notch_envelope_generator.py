def fct_notch_envelope_generator(x_array, y_array, x1, m1, x2, m2, ymin):
    import numpy as np

    x1_idx = np.where(abs(x_array - x1) < 0.1)[0][0]
    x2_idx = np.where(abs(x_array - x2) < 0.1)[0][0]

    y1, y2 = y_array[x1_idx], y_array[x2_idx]
    n1 = y1 - m1 * x1
    n2 = y2 - m2 * x2

    x_vertex = (n2 - n1) / (m1 - m2)

    # important! np.copy of C array.
    # never make: "y_array_return = y_array", since modifications
    # in one array would change both arrays
    y_array_return = np.copy(y_array)

    if x1 <= x_vertex and x_vertex <= x2:
        print("Generating envelope for notched MPE...")
        x_vertex_idx = np.where(abs(x_array - x_vertex) <= 1.0)[0][0]

        for i in range(x1_idx, x_vertex_idx):
            y_array_return[i] = m1 * x_array[i] + n1

        for i in range(x_vertex_idx, x2_idx):
            y_array_return[i] = m2 * x_array[i] + n2

        for i in range(x1_idx, x2_idx):
            if y_array_return[i] < ymin:
                y_array_return[i] = ymin

        if ymin is not None:
            x_cap_left_idx = np.where(abs(y_array_return[x1_idx:x2_idx] - ymin) < 0.01)[
                0
            ][0]
            x_cap_right_idx = np.where(
                abs(y_array_return[x1_idx:x2_idx] - ymin) < 0.01
            )[0][-1]
            x_cap_left = round(x_array[x1_idx + x_cap_left_idx], 2)
            x_cap_right = round(x_array[x1_idx + x_cap_right_idx], 2)
            y_cap_left = round(y_array_return[x1_idx + x_cap_left_idx], 2)
            y_cap_right = round(y_array_return[x1_idx + x_cap_right_idx], 2)

        else:
            x_cap_left, x_cap_right = [None, None]

    else:
        raise Exception(
            "Error!! Intersection of the two lines is not within the interval [x1,x2]"
        )

    print("new points in MPE Table : ")
    print("X", "Y")
    print(x1, y1)
    print(x_cap_left, y_cap_left)
    print(x_cap_right, y_cap_right)
    print(x2, y2)
    print("")

    return y_array_return
