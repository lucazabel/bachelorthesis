import numpy as np
import matplotlib.pyplot as plt

arr0 = np.loadtxt("../data_topology_2/energy_consumption_tp2_mW.csv", delimiter=",")
arr1 = np.loadtxt("../data_topology_2/energy_consumption_tp2_mW_gate_rec.csv", delimiter=",")
arr2 = np.loadtxt("../data_topology_2/energy_consumption_tp2_mW_rec.csv", delimiter=",")

plt.rcParams.update({'font.size': 16})

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

axes[0].hist(arr0, bins=10, edgecolor="blue")
axes[0].set_xlabel("power consumption in mW")
axes[0].set_ylabel("number of nodes")

axes[1].hist(arr1, bins=10, edgecolor="blue")
axes[1].set_xlabel("power consumption in mW")

axes[2].hist(arr2, bins=10, edgecolor="blue")
axes[2].set_xlabel("power consumption in mW")

plt.tight_layout()
plt.savefig("../data_topology_2/plots/hist_mW_comparison.svg")
plt.show()