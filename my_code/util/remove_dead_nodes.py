import numpy as np

nodes_alive = [4,5,9,11,12,22,23,25,26,31,36,37,38,39,40,41,42,43,44,45,46,48,53,57,58,65,68,74,76,77,79,80,81,83,88,99,100,101,102,103,104,114,117,118,130,131,132,141,142,143,148,149,150,151,152,153,158,159,160,161,165,166,167,200,201,208,216,217,218,220,221,231,237,238,239,243,244,245,246,249,251,254,255,256]
nodes_alive_idx = [node - 1 for node in nodes_alive]

arr = np.loadtxt("../data_topology_2/data_lille.csv")

arr_cleaned = arr[nodes_alive_idx, :][:, nodes_alive_idx]

np.savetxt("../data_topology_2/data_lille_cleaned.csv", arr_cleaned, fmt="%.1f")
