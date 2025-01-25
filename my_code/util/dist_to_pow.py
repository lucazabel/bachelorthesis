import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

dist = np.loadtxt("../data_topology_2/dist_arr.csv", delimiter=",")
power = np.loadtxt("../data_topology_2/energy_consumption_tp2_mW_rec.csv", delimiter=",")

dist_flat = dist.flatten()
power_flat = power.flatten()

rounded_distances = np.round(dist_flat / 2) * 2

power_by_binned_distance = {}

for d, p in zip(rounded_distances, power_flat):
    if d not in power_by_binned_distance:
        power_by_binned_distance[d] = []
    power_by_binned_distance[d].append(p)

binned_distances = np.array(list(power_by_binned_distance.keys()))
average_power_consumption = np.array([np.mean(values) for values in power_by_binned_distance.values()])

mask = binned_distances != 0
binned_distances = binned_distances[mask]
average_power_consumption = average_power_consumption[mask]

sorted_indices = np.argsort(binned_distances)
sorted_binned_distances = binned_distances[sorted_indices]
sorted_average_power = average_power_consumption[sorted_indices]

plt.rcParams.update({'font.size': 16})

plt.plot(sorted_binned_distances, sorted_average_power, color="blue")
plt.xlabel("Distance in Meter")
plt.ylabel("Power Consumption in mW")
plt.grid(True)
plt.savefig("../data_topology_2/plots/dist_to_pow.svg")
plt.show()

sns.regplot(x=binned_distances, y=average_power_consumption, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
plt.xlabel("Distance in Meter")
plt.ylabel("Power Consumption in mW")
plt.grid(True)
plt.savefig("../data_topology_2/plots/dist_to_pow_scatter_regression.svg")
plt.show()