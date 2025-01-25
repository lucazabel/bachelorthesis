import csv

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


with open("omls/m3_47.oml", "r", encoding="utf-8") as file:
    content = list(csv.reader(file, delimiter='\t'))

    counter = 0
    energy_list = []
    for line in content:
        if counter > 9 and float(line[0])>36.0:
            if float(line[5]) > 0.07:
                energy_list.append(line)
        counter += 1

    output_list = []
    i = 0
    while i < len(energy_list) - 1:
        temp_list = [float(energy_list[i][5])]
        # temp_list = [[int(energy_list[i][2]), float(energy_list[i][5])]]
        timestamp_curr = float(energy_list[i][3]) + (float(energy_list[i][4]) / 1000000)
        for j in range(len(energy_list) - i - 1):
            timestamp_next = float(energy_list[i + j + 1][3]) + (float(energy_list[i + j + 1][4]) / 1000000)
            if timestamp_next < timestamp_curr + 0.2:
                temp_list.append(float(energy_list[i + j + 1][5]))
                # temp_list.append([int(energy_list[i + j + 1][2]) ,float(energy_list[i + j + 1][5])])
            else:
                break
        output_list.append(temp_list)
        i += len(temp_list)

    filtered_list = []
    for sublist in output_list:
        if (sum(sublist) / len(sublist)) >= 0.08:
            filtered_list.append(sublist)

    # line_list = []
    # for i in range(15):
    #     start_idx = output_list[i*30][0][0]-1
    #     stop_idx = output_list[(i+1)*30-1][0][0]+1
    #     line_list.append([start_idx, stop_idx])
    #
    # power_list = []
    # average_list = []
    # for start_idx, stop_idx in line_list:
    #     temp_list = []
    #     for idx, line in enumerate(content):
    #         if start_idx <= idx < stop_idx:
    #             temp_list.append(float(line[5]))  # Collect lines in the range
    #     power_list.append(temp_list)
    #     average_list.append(np.average(temp_list))
    #
    # power_levels = [-17, -12, -10, -7, -5, -4, -3, -2, -1, 0.7, 1.3, 1.8, 2.3, 2.8, 3]
    # plt.plot(power_levels, average_list, marker='o', linestyle='-')
    # plt.xlabel("Power Levels")
    # plt.ylabel("Average")
    # plt.title("Average Values by Power Levels")
    # plt.grid(True)
    # plt.show()

    # print("stop")

    #########################################
    #### dBm measurements per powerlevel ####
    #########################################

    # data = filtered_list[420:450]
    #
    # plt.figure(figsize=(12, 10))
    #
    # # Swarm Plot with Boxplot
    # sns.boxplot(data=data, whis=[0, 100], width=.6, showcaps=True)
    # sns.swarmplot(data=data, size=4, color="0", alpha=0.8)
    # plt.title("3 decibel-milliwatts Measurement")
    # plt.xlabel("Each sending of the data")
    # plt.ylabel("Power in Watts")
    # plt.xticks(ticks=range(len(data)), labels=range(1, len(data) + 1))


    ######################################
    #### powerlevel vs consumed power ####
    ######################################

    power_levels = [-17, -12, -10, -7, -5, -4, -3, -2, -1, 0.7, 1.3, 1.8, 2.3, 2.8, 3]
    consumption_per_power = [] #consumption per powerlevel
    for i in range(15):
        temp = filtered_list[i * 30:(i + 1) * 30]
        consumption_per_power.append([item for sublist in temp for item in sublist])

    average_consumption_per_power = [sum(data)*1000 / len(data) for data in consumption_per_power]

    print(average_consumption_per_power)

    plt.plot(power_levels, average_consumption_per_power, marker="o", linestyle="-", color="orange")
    # Customize the plot
    plt.xlabel("Antenna power in dBm (decibel-milliwatts)")
    plt.ylabel("Power in Watts")
    plt.grid(True)

    # for i, d in enumerate(consumption_per_power):
    #     total_consumption = sum(d)
    #     plt.text(i-0.3, max(d)+0.001, f"{round(total_consumption, 2)}")


    ####################################
    #### power_level to distance ####
    ####################################

    # distance = np.loadtxt("dist_array.txt")
    # energy = np.loadtxt("output_array.txt")
    # energy_to_distances = {}
    #
    # data = []
    # energy_levels = []
    #
    # n = distance.shape[0]
    # for i in range(n):
    #     for j in range(n):
    #         if i != j and not np.isnan(energy[i][j]):
    #             data.append(distance[i][j])
    #             energy_levels.append(energy[i][j])
    #
    # # Create a DataFrame
    # df = pd.DataFrame({"Distance": data, "EnergyLevel": energy_levels})
    #
    # # Plot
    # plt.figure(figsize=(12, 10))
    #
    # # Boxplot
    # sns.boxplot(x="EnergyLevel", y="Distance", data=df, whis=[0, 100], width=0.6)
    #
    # # Customization
    # plt.title("Distance to Energy Levels")
    # plt.xlabel("powerlevel (dBm)")
    # plt.ylabel("Distance (m)")
    #
    #
    #
    # # Save the plot as a .png file
    # #plt.savefig("plots/Distance_to_Energy_Levels.png")
    #
    # # Show the plot
    # plt.show()
    #
    # distance = np.loadtxt("dist_array.txt")
    # energy = np.loadtxt("output_array.txt")
    #
    # data = []
    # energy_levels = []
    #
    # n = distance.shape[0]
    # for i in range(n):
    #     for j in range(n):
    #         if i != j and not np.isnan(energy[i][j]):
    #             data.append(distance[i][j])
    #             energy_levels.append(energy[i][j])
    #
    # # Create a DataFrame
    # df = pd.DataFrame({"Distance": data, "EnergyLevel": energy_levels})
    #
    # # Define bins for linear energy levels
    # bins = np.arange(-17, 4, 1)  # Create bins from -17 to 3 (inclusive)
    # labels = bins[:-1]  # Labels for the bins
    #
    # # Add a new column for binned energy levels
    # df["BinnedEnergyLevel"] = pd.cut(df["EnergyLevel"], bins=bins, labels=labels, include_lowest=True)
    #
    # # Plot
    # plt.figure(figsize=(12, 10))
    #
    # # Boxplot
    # sns.boxplot(x="BinnedEnergyLevel", y="Distance", data=df, whis=[0, 100], width=0.6)
    #
    # # Customization
    # plt.title("Distance to Energy Levels")
    # plt.xlabel("Power Level (dBm)")
    # plt.ylabel("Distance (m)")
    #
    # # Save the plot as a .png file
    # plt.savefig("plots/node_24_power_levels_vs_watts.png")
    #
    # Show the plot
    plt.savefig("plots/consumption_s.svg")
    plt.show()


