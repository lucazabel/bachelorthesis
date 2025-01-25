import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data0 = np.loadtxt("dimension_data/data.csv", delimiter=",")
data1 = np.loadtxt("dimension_data/data1.csv", delimiter=",")
data2 = np.loadtxt("dimension_data/data2.csv", delimiter=",")
data3 = np.loadtxt("dimension_data/data3.csv", delimiter=",")
data4 = np.loadtxt("dimension_data/data4.csv", delimiter=",")

data = (data0+data1+data2+data3+data4)/5

npre_data = data[:, 0]
mre_data = data[:, 1]

num_chunks = len(data) // 1

def average_every_x(arr):
    return np.array([np.mean(arr[i*1:(i+1)*1]) for i in range(num_chunks)])

averaged_npre_data = average_every_x(npre_data)
averaged_mre_data = average_every_x(mre_data)

averaged_dimensions = np.arange(2, 2 + 1*num_chunks, 1)

plt.rcParams.update({'font.size': 16})

sns.regplot(x=averaged_dimensions, y=averaged_mre_data, color="blue")
plt.xlabel("Dimension")
plt.ylabel("Mean Error in mW")
plt.grid(True)
plt.savefig("../../data_topology_2/plots/mre_scatter_regression.svg")
plt.show()

sns.regplot(x=averaged_dimensions, y=averaged_npre_data, color="green")
plt.xlabel("Dimension")
plt.ylabel("90th Percentile Error in mW")
plt.grid(True)
plt.savefig("../../data_topology_2/plots/npre_scatter_regression.svg")
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.regplot(x=averaged_dimensions, y=averaged_mre_data, color="blue", ax=axes[0])
axes[0].set_xlabel("Dimension")
axes[0].set_ylabel("Mean Error in mW")

axes[0].grid(True)

sns.regplot(x=averaged_dimensions, y=averaged_npre_data, color="green", ax=axes[1])
axes[1].set_xlabel("Dimension")
axes[1].set_ylabel("90th Percentile Error in mW")
axes[1].grid(True)

plt.tight_layout()
plt.savefig("../../data_topology_2/plots/npre_mre_scatter_regression.svg")
plt.show()