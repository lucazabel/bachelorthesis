import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat
from collections import defaultdict


def gateway(data_arr, dist_arr):
    output_arr = np.zeros_like(data_arr, dtype=object)
    dist_arr_2 = np.zeros_like(dist_arr)

    # find the closest gateway
    for i in range(data_arr.shape[0]):
        for j in range(data_arr.shape[1]):
            if i != j:
                if np.isnan(data_arr[i, j]).any():
                    power, dist = find_gateway(data_arr, dist_arr, i, j)
                    output_arr[i, j] = power
                    dist_arr_2[i, j] = dist
                else:
                    output_arr[i, j] = data_arr[i, j]
                    dist_arr_2[i, j] = dist_arr[i, j]
            else:
                output_arr[i, j] = data_arr[i, j]
                dist_arr_2[i, j] = dist_arr[i, j]

    return output_arr, dist_arr_2


# row and col are the coordinates of the node which received nothing from the source
# therefore I swap row and col in merged array to find the node closest to the node (which wasn't reached)
# which is reached
def find_gateway(data_arr, dist_arr, row, col):
    min_dist = 9999.9
    prospect = np.nan
    for i in range(data_arr.shape[0]):
        if i != col and i != row:
            if not np.isnan(data_arr[row, i]).any():
                if not np.isnan(data_arr[i, col]).any():
                    dist_source_gateway = dist_arr[row, i]
                    dist_gateway_target = dist_arr[i, col]
                    dist = dist_source_gateway + dist_gateway_target
                    if dist < min_dist:
                        power_source_gateway = data_arr[row, i]
                        power_gateway_target = data_arr[i, col]
                        prospect = [power_source_gateway, power_gateway_target]
                        min_dist = dist
    if min_dist == 9999.9:
        min_dist = dist_arr[row, col]
    return prospect, min_dist


def flatten(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten(item))
        else:
            flattened.append(item)
    return flattened


def flatten_array(input_arr):
    for i in range(input_arr.shape[0]):
        for j in range(input_arr.shape[1]):
            if isinstance(input_arr[i, j], list):
                input_arr[i, j] = flatten(input_arr[i, j])
    return input_arr


def add_power(data_arr):
    antenna_power = [-17, -12, -10, -7, -5, -4, -3, -2, -1, 0.7, 1.3, 1.8, 2.3, 2.8, 3]
    consumption_per_tx_power = [0.08908089510489511, 0.08961525352112677, 0.09095223571428568, 0.09201991304347826, 0.09304200729927009,
                          0.09373911510791368, 0.09373911510791368, 0.0943576382978724, 0.09562398561151074, 0.0967082158273381, 0.09816119858156029,
                          0.09939540714285719, 0.09994109154929587, 0.10061198591549304, 0.10149526950354609, 0.10262283333333332]

    power_rx = 0.1055

    power_to_consumption = dict(zip(antenna_power, consumption_per_tx_power))
    added_power_arr = np.zeros_like(data_arr, np.float64)

    for i in range(data_arr.shape[0]):
        for j in range(data_arr.shape[1]):
            if i == j:
                added_power_arr[i, j] = 0
            else:
                if isinstance(data_arr[i, j], list):
                    power_list = data_arr[i, j]
                    sum = 0
                    for power in power_list:
                        sum += power_to_consumption.get(power)
                        # sum += power_rx
                    # sum -= power_rx
                    total_consumption = sum
                elif isinstance(data_arr[i, j], np.float64):
                    total_consumption = power_to_consumption.get(data_arr[i, j])
                added_power_arr[i, j] = total_consumption

    min = added_power_arr[added_power_arr > 0].min()

    return added_power_arr


if __name__ == "__main__":
    data_arr = np.loadtxt("../data_topology_2/data_lille_cleaned.csv")
    dist_arr = np.loadtxt("../data_topology_2/dist_arr.csv", delimiter=",")

    gateway_arr1, dist_arr1 = gateway(data_arr, dist_arr)
    gateway_arr2 = flatten_array(gateway_arr1)
    gateway_arr3, dist_arr2 = gateway(gateway_arr2, dist_arr1)
    gateway_arr4 = flatten_array(gateway_arr3)

    added_arr = add_power(gateway_arr4)

    np.savetxt("../data_topology_2/energy_consumption_tp2_rec.csv", added_arr, delimiter=",")

    savemat("../data_topology_2/fit_energy_tp2_including_rec.mat", {"fit_energy_tp2": added_arr})

    print("end")