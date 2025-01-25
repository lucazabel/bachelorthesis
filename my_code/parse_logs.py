import numpy as np
import os

source = ""
source_idx = 256
with open(f"data_topology_2/logs/output{source}.log", "r") as file:
    log_file = file.read()

arr = np.zeros((300,300))

file_path = "data_topology_2/data.csv"
file_path_lille = "data_topology_2/data_lille.csv"

if os.path.exists(file_path_lille):
    arr = np.loadtxt(file_path_lille)


def power_converter(power):
    if power[0] == "m":
        return float(power[1:-3])*-1
    elif power[1] == "_":
        return float(int(power[0]) + int(power[2])*0.1)
    else:
        return float(power[0])


def pars():
    for line in log_file.splitlines():
        parts = line.split(";")
        if len(parts) >= 7:
            receiver = int(parts[1].split("-")[1])
            # source = int(parts[2].split()[2].split("-")[1][:-1])
            # rssi = float(parts[4].split()[1])
            power = power_converter(parts[5].split()[1])
            arr[source_idx-1][receiver-1] = power

pars()
arr[arr == 0.0] = np.nan
np.savetxt(file_path_lille, arr, fmt="%.2f")
os.rename(f"data_topology_2/logs/output.log", f"data_topology_2/logs/output{source_idx}.log")

