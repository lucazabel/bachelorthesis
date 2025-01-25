import numpy as np


##########################
######## MAX_DIST ########
##########################
# max dist wird immer am besten sein, weil empfänger verbrauch > senden bei max power
def max_dist_gateway(rows, cols, dead_nodes, input_arr):
    max_dist_arr = np.full(input_arr.shape, np.nan, dtype=object)

    for i in range(rows):
        for j in range(cols):
            if i + 1 not in dead_nodes and j + 1 not in dead_nodes:
                if i == j:
                    max_dist_arr[i, j] = [np.nan]
                elif i > j:  # left side
                    if not np.isnan(input_arr[i, j]).all():  # already reached
                        max_dist_arr[i, j] = [input_arr[i, j]]
                    elif np.isnan(input_arr[i, j]).any():
                        for k in range(cols - j):
                            if not np.isnan(input_arr[i, j + k]).all() and not np.isnan(input_arr[j+k, j]).all():
                                max_dist_arr[i, j] = [input_arr[i, j + k], input_arr[j+k, j]]
                                break
                elif i < j:  # right side
                    if not np.isnan(input_arr[i, j]).all():  # already reached
                        max_dist_arr[i, j] = [input_arr[i, j]]
                    elif np.isnan(input_arr[i, j]).any():
                        for k in range(j, 0, -1):  # Note corrected range
                            if not np.isnan(input_arr[i, k]).all() and not np.isnan(input_arr[k, j]).all():
                                max_dist_arr[i, j] = [input_arr[i, k], input_arr[k, j]]
                                break

    return max_dist_arr


if __name__ == "__main__":
    input_arr = np.loadtxt("output_array.txt")

    example = np.array([[np.nan, -17, -7, -1, 3, np.nan, np.nan, np.nan],
                          [-12, np.nan, -17, -1, 2.8, 3, np.nan, np.nan],
                          [-17, -17, np.nan, -12, -1, 1.3, 2.3, 3],
                          [-1, -7, -12, np.nan, 3, np.nan, 3, np.nan],
                          [3, np.nan, -5, -12, np.nan, -12, 2.3, 3],
                          [np.nan, np.nan, 2.8, -4, -12, np.nan, np.nan, np.nan],
                          [np.nan, 3, np.nan, -3, -12, -17, np.nan, -12],
                          [np.nan, np.nan, 3, 2.8, -17, -17, -17, np.nan]])

    np.savetxt("example_matrix.txt", example, fmt="%.1f")

    dead_nodes = [1, 17, 19, 35, 45, 50]
    # dead_nodes = []

    rows, cols = input_arr.shape

    max_dist_arr = max_dist_gateway(rows, cols, dead_nodes, input_arr)
    max_dist_arr = max_dist_gateway(rows, cols, dead_nodes, max_dist_arr)   # run it a second time to reach all values

