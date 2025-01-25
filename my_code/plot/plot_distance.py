import numpy as np
import matplotlib.pyplot as plt

dist = np.loadtxt("../data_topology_2/dist_arr.csv", delimiter=",")

upper_triangle_indices = np.triu_indices_from(dist, k=1)
upper_triangle_distances = dist[upper_triangle_indices]

plt.rcParams.update({'font.size': 16})

plt.hist(upper_triangle_distances, bins=500, edgecolor='blue')
plt.xlabel("Distance in meters")
plt.ylabel("Number of node pairs")
plt.savefig("../data_topology_2/plots/hist_distance.svg")
plt.show()