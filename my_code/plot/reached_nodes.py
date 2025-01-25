import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

arr = np.loadtxt("../data_topology_2/data_lille_cleaned.csv")

flat_array = arr
filtered_array = flat_array[~np.isnan(flat_array)]

unique_values, counts = np.unique(filtered_array, return_counts=True)

for i in range(1, len(counts)):
    counts[i] = counts[i - 1] + counts[i]

plt.figure(figsize=(8, 6))
plt.rcParams.update({'font.size': 16})
sns.regplot(x=unique_values, y=counts, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})

plt.xlabel("Antenna Transmission Power in dBm (decibel-milliwatts)")
plt.ylabel("Reached Nodes")
plt.grid(True)
plt.savefig("../data_topology_2/plots/reached_nodes.svg")
plt.show()
