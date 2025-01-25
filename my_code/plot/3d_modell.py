import numpy as np
import matplotlib.pyplot as plt

coords = np.loadtxt("../data_topology_2/coords_tp2.csv", delimiter=",")

x = coords[:, 0]
y = coords[:, 1]
z = coords[:, 2]

cmap = plt.get_cmap()
norm = plt.Normalize(vmin=np.min(z), vmax=np.max(z))

plt.rcParams.update({'font.size': 16})

plt.figure(figsize=(7, 11))
sc1 = plt.scatter(x, y, c=z, cmap=cmap, norm=norm)
plt.xlabel("X-Coordinate in meters")
plt.ylabel("Y-Coordinate in meters")
plt.colorbar(sc1, label="Height of Z-Coordinate in meters")
plt.savefig("../data_topology_2/plots/top_down.svg")
plt.show()

plt.figure(figsize=(10, 5))
sc3 = plt.scatter(y, z, c=z, cmap=cmap, norm=norm)
plt.xlabel("Y-Coordinate in meters")
plt.ylabel("Z-Coordinate in meters")
plt.colorbar(sc3, label="Height of Z-Coordinate in meters")
plt.savefig("../data_topology_2/plots/side_view.svg")
plt.show()
