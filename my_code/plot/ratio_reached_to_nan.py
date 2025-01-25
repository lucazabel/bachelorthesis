import numpy as np

arr = np.loadtxt("../data_topology_2/data_lille_cleaned.csv")

nan_counts = []
non_nan_counts = []
max_nans_row_index = -1
max_non_nans_row_index = -1
max_nans_count = -1
max_non_nans_count = -1

# Iterate through the rows and columns
for i, row in enumerate(arr):
    nan_count = 0
    non_nan_count = 0

    for j, value in enumerate(row):
        if i != j:
            if np.isnan(value):
                nan_count += 1
            else:
                non_nan_count += 1

    nan_counts.append(nan_count)
    non_nan_counts.append(non_nan_count)

    if nan_count > max_nans_count:
        max_nans_count = nan_count
        max_nans_row_index = i

    if non_nan_count > max_non_nans_count:
        max_non_nans_count = non_nan_count
        max_non_nans_row_index = i

# Calculate the average number of NaN and non-NaN values
average_nans = np.mean(nan_counts)
average_non_nans = np.mean(non_nan_counts)

print(f"Average number of NaNs per row (excluding diagonal): {average_nans}")
print(f"Average number of non-NaN values per row (excluding diagonal): {average_non_nans}")
print(f"Row with most NaNs (excluding diagonal): {max_nans_row_index} (NaNs: {max_nans_count})")
print(f"Row with most non-NaNs (excluding diagonal): {max_non_nans_row_index} (Non-NaNs: {max_non_nans_count})")