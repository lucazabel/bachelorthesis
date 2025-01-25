import csv
import matplotlib.pyplot as plt
import numpy as np
from gateway import max_dist_gateway
from collections import defaultdict
from itertools import islice
from scipy.io import savemat


######################################################################
############################## RECEIVER ##############################
######################################################################
def receiver(centered: bool):
    with open("omls/m3_25_receiver.oml", "r", encoding="utf-8") as file:
        receiver_content = list(csv.reader(file, delimiter='\t'))

        counter = 0
        receiver_list = []
        for line in receiver_content:
            if counter > 9 and float(line[0]) > 36.0:
                if float(line[5]) > 0.13:
                    receiver_list.append(line)
            counter += 1

        grouped_receiver_list = []
        i = 0
        while i < len(receiver_list)-1:
            temp_list = [[int(receiver_list[i][2]), float(receiver_list[i][5])]]
            timestamp_curr = float(receiver_list[i][0])
            for j in range(len(receiver_list)-i-1):
                timestamp_next = float(receiver_list[i+j+1][0])
                if timestamp_next < timestamp_curr + 2.5:
                    temp_list.append([int(receiver_list[i + j + 1][2]) ,float(receiver_list[i + j + 1][5])])
                else:
                    break
            grouped_receiver_list.append(temp_list)
            i+=len(temp_list)

        line_list = []
        for i in range(15):
            start_idx = grouped_receiver_list[i*30][0][0]-1
            stop_idx = grouped_receiver_list[(i+1)*30-1][0][0]+1
            line_list.append([start_idx, stop_idx])

        power_list = []
        average_consumption_receiver = []
        for start_idx, stop_idx in line_list:
            temp_list = []
            for idx, line in enumerate(receiver_content):
                if start_idx <= idx < stop_idx:
                    temp_list.append(float(line[5]))  # Collect lines in the range
            power_list.append(temp_list)
            average_consumption_receiver.append(np.average(temp_list))

        average_consumption_receiver = np.array([0.1059, 0.1054, 0.1063, 0.1061, 0.1059, 0.1057, 0.1062, 0.1058, 0.1061, 0.1057, 0.1056, 0.1057, 0.1058, 0.1057, 0.1053])

        if centered:
            average_consumption_receiver = average_consumption_receiver - np.mean(average_consumption_receiver)
            average_consumption_receiver += np.abs(np.min(average_consumption_receiver))

        average_consumption_receiver = np.multiply(average_consumption_receiver, 1000)
        return average_consumption_receiver


######################################################################
############################### SENDER ###############################
######################################################################
def sender(centered: bool):
    with open("omls/m3_24_sender.oml", "r", encoding="utf-8") as file:
        sender_content = csv.reader(file, delimiter='\t')

        counter = 0
        sender_list = []
        for line in sender_content:
            if counter > 9 and float(line[0])>36.0:
                if float(line[5]) > 0.07:
                    sender_list.append(line)
            counter += 1

        grouped_sender_list = []
        i = 0
        while i < len(sender_list) - 1:
            temp_list = [float(sender_list[i][5])]
            timestamp_curr = float(sender_list[i][0])
            for j in range(len(sender_list) - i - 1):
                timestamp_next = float(sender_list[i + j + 1][0])
                if timestamp_next < timestamp_curr + 2.5:
                    temp_list.append(float(sender_list[i + j + 1][5]))
                else:
                    break
            grouped_sender_list.append(temp_list)
            i += len(temp_list)

        filtered_list_sender = []
        for sublist in grouped_sender_list:
            if (sum(sublist) / len(sublist)) >= 0.08:
                filtered_list_sender.append(sublist)

        consumption_sender = []
        for i in range(15):
            temp = filtered_list_sender[i * 30:(i + 1) * 30]
            flat_list = []
            for sublist in temp:
                for item in sublist:
                    flat_list.append(item)
            consumption_sender.append(flat_list)


        average_consumption_sender = []
        for data in consumption_sender:
            average_consumption_sender.append(np.average(data))

        if centered:
            average_consumption_sender = average_consumption_sender - np.mean(average_consumption_sender)
            average_consumption_sender += np.abs(np.min(average_consumption_sender))

        average_consumption_sender = np.multiply(average_consumption_sender, 1000)
        return average_consumption_sender


######################################################################
################################ IDLE ################################
######################################################################
def idle(centered: bool):
    with open("omls/m3_24.oml", "r", encoding="utf-8") as file:
        idle_content = csv.reader(file, delimiter='\t')

        counter = 0
        idle_list = []
        for line in idle_content:
            if counter > 9 and float(line[0]) > 36.0:
                if float(line[5]) < 0.07:
                    idle_list.append(line)
            counter += 1

        grouped_idle_list = []
        i = 0
        while i < len(idle_list) - 1:
            temp_list = [float(idle_list[i][5])]
            timestamp_curr = float(idle_list[i][0])
            for j in range(len(idle_list) - i - 1):
                timestamp_next = float(idle_list[i + j + 1][0])
                if timestamp_next < timestamp_curr + 0.2:
                    temp_list.append(float(idle_list[i + j + 1][5]))
                else:
                    break
            grouped_idle_list.append(temp_list)
            i += len(temp_list)


        average_consumption_idle = []
        for i in range(int(len(grouped_idle_list)/89)):
            sum = 0.0
            for j in range(89):
                sum += float(np.average(grouped_idle_list[i+j]))
            average_consumption_idle.append(sum/89)

        if centered:
            average_consumption_idle = average_consumption_idle - np.mean(average_consumption_idle)
            average_consumption_idle += np.abs(np.min(average_consumption_idle))

        average_consumption_idle = np.multiply(average_consumption_idle, 1000)
        return average_consumption_idle


def plot_power(avg_r, avg_s, avg_i):
    power_levels = [-17, -12, -10, -7, -5, -4, -3, -2, -1, 0.7, 1.3, 1.8, 2.3, 2.8, 3]

    plt.figure(figsize=(8, 6))

    plt.plot(power_levels, avg_r, marker="o", linestyle="-", color="blue", label="Receiver Power Consumption")
    plt.plot(power_levels, avg_s, marker="o", linestyle="-", color="orange", label="Sender Power Consumption")
    plt.plot(power_levels, avg_i, marker="o", linestyle="-", color="green", label="Idle Power Consumption")

    plt.xlabel("Antenna Power in dBm (decibel-milliwatts)")
    plt.ylabel("Power consumption in Milliwatts (mW)")
    plt.legend(loc="upper left", bbox_to_anchor=(0, 0.9, 0, 0))
    plt.grid(True)
    plt.savefig("plots/consumption_r_s_i.svg")
    # plt.savefig("plots/consumption_s.svg")
    plt.show()


def plot_dist_pow(data):
    filtered_data = {k: v for k, v in data.items() if k != 0}

    # Plot the filtered data
    plt.plot(filtered_data.keys(), filtered_data.values())
    plt.xlabel("Distance in Meters")
    plt.ylabel("Power Consumption in Watts")
    plt.grid(True)
    plt.savefig("plots/dist_to_pow.svg")
    plt.show()


def flatten(lst):   # https://chatgpt.com/c/675847a4-dd20-8013-9093-488667577d9f
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))  # Recursively flatten if it's a list
        else:
            flat_list.append(item)  # Add the element if it's not a list
    return flat_list


if __name__ == "__main__":
    centered = False
    average_consumption_receiver = receiver(centered)
    average_consumption_sender = sender(centered)
    average_consumption_idle = idle(centered)

    plot_power(average_consumption_receiver, average_consumption_sender, average_consumption_idle)

    input_arr = np.loadtxt("output_array.txt")
    dead_nodes = [1, 17, 19, 35, 45, 50]
    rows, cols = input_arr.shape

    max_dist_arr = max_dist_gateway(rows, cols, dead_nodes, input_arr)
    max_dist_arr = max_dist_gateway(rows, cols, dead_nodes, max_dist_arr)  # run it a second time to reach all values

    avg_receiver = np.average(average_consumption_receiver)
    avg_idle = np.average(average_consumption_idle)

    power_arr = np.zeros((rows, cols))
    power_levels = [-17.0, -12.0, -10.0, -7.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.7, 1.3, 1.8, 2.3, 2.8, 3.0]

    for i in range(rows):
        for j in range(cols):
            if i != j and i+1 not in dead_nodes and j+1 not in dead_nodes:
                flat = flatten(max_dist_arr[i, j])
                total = 0
                for val in flat:
                    if val in power_levels:
                        total += average_consumption_sender[power_levels.index(val)]
                power_arr[i, j] = total

    distance_arr = np.loadtxt("dist_array.txt")
    distance_to_power = defaultdict(list)

    dead_nodes_idx = [node - 1 for node in dead_nodes]
    power_arr_filtered = np.delete(power_arr, dead_nodes_idx, axis=0)
    power_arr_filtered = np.delete(power_arr_filtered, dead_nodes_idx, axis=1)
    distance_arr_filtered = np.delete(distance_arr, dead_nodes_idx, axis=0)
    distance_arr_filtered = np.delete(distance_arr_filtered, dead_nodes_idx, axis=1)

    rows, cols = power_arr_filtered.shape
    with open("energy_consumption_header.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(power_arr_filtered)
    # np.savetxt("energy_consumption.csv", power_arr_filtered, fmt="%.10f")

    # float_power_list = []
    # for i in range(rows):
    #     r = []
    #     for j in range(cols):
    #         r.append(float(power_arr_filtered[i, j]))
    #     float_power_list.append(r)

    for i in range(rows):
        for j in range(cols):
            distance = distance_arr_filtered[i][j]
            power = power_arr_filtered[i][j]
            if not np.isnan(power):
                distance_to_power[distance].append(power)

    distance_to_avg_power = {dist: np.mean(powers) for dist, powers in distance_to_power.items()}

    sorted_distance_to_avg_power = dict(sorted(distance_to_avg_power.items()))

    s_keys = list(sorted_distance_to_avg_power.keys())

    filtered_sorted_distance_to_avg_power = defaultdict(list)

    i = 0
    while i < len(s_keys) - 1:
        current_key = s_keys[i]
        next_key = s_keys[i+1]
        current_val = sorted_distance_to_avg_power[current_key]
        next_val = sorted_distance_to_avg_power[next_key]
        if next_key - current_key <= 0.25:
            k = np.average([current_key, next_key])
            v = np.average([current_val, next_val])
            filtered_sorted_distance_to_avg_power[k].append(v)
            i += 2
        else:
            filtered_sorted_distance_to_avg_power[current_key].append(current_val)
            i += 1

    plot_dist_pow(filtered_sorted_distance_to_avg_power)


