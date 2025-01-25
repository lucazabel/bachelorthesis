import numpy as np

nodes_alive = [4,5,9,11,12,22,23,25,26,31,36,37,38,39,40,41,42,43,44,45,46,48,53,57,58,65,68,74,76,77,79,80,81,83,88,99,100,101,102,103,104,114,117,118,130,131,132,141,142,143,148,149,150,151,152,153,158,159,160,161,165,166,167,200,201,208,216,217,218,220,221,231,237,238,239,243,244,245,246,249,251,254,255,256]

with open("../data_topology_2/coords_tp2.csv", "r") as file:
    arr = np.zeros((84, 3))

    counter = 0
    for line in file:
        line = line.split(",")
        x = float(line[0])
        y = float(line[1])
        z = float(line[2])
        arr[counter] = [x, y, z]
        counter += 1

    dist_arr = np.zeros((84, 84))

    for i in range(84):
        for j in range(84):
            if i != j:
                dist_arr[i][j] = np.sqrt((arr[i][0] - arr[j][0])**2 + (arr[i][1] - arr[j][1])**2 + (arr[i][2] - arr[j][2])**2)

    np.savetxt("../data_topology_2/dist_arr.csv", dist_arr, fmt="%.3f", delimiter=",")