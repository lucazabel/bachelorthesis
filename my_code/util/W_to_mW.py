import numpy as np
from scipy.io import savemat

arr = np.loadtxt("../data_topology_2/energy_consumption_tp2_including_receiver.csv", delimiter=",")

arr_mW = arr * 1000

np.savetxt("../data_topology_2/energy_consumption_tp2_mW_including_receiver.csv", arr_mW, fmt="%.1f", delimiter=",")
savemat("../data_topology_2/fit_energy_tp2_mW_including_receiver.mat", {"fit_energy_tp2_mW": arr_mW})