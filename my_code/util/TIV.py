import itertools
import numpy as np


def calculate_triangle_inequality_error(matrix, node_ids):
    """
    Calculates the triangle inequality error for a given latency matrix and maps errors to node IDs.

    Parameters:
    matrix (np.array): A 2D numpy array where matrix[i][j] represents the latency
                       from node i to node j.
    node_ids (list): A list of node IDs corresponding to the indices of the matrix.

    Returns:
    dict: A dictionary containing summary statistics of triangle inequality errors.
    """
    errors = []
    num_nodes = matrix.shape[0]

    # Iterate through all triplets of nodes
    for i, j, k in itertools.combinations(range(num_nodes), 3):
        # Distances
        dist_ij = matrix[i, j]
        dist_jk = matrix[j, k]
        dist_ik = matrix[i, k]

        # Check triangle inequality and record errors
        if dist_ik > dist_ij + dist_jk:
            error = dist_ik - (dist_ij + dist_jk)
            errors.append((node_ids[i], node_ids[j], node_ids[k], error))

        if dist_ij > dist_ik + dist_jk:
            error = dist_ij - (dist_ik + dist_jk)
            errors.append((node_ids[i], node_ids[k], node_ids[j], error))

        if dist_jk > dist_ij + dist_ik:
            error = dist_jk - (dist_ij + dist_ik)
            errors.append((node_ids[j], node_ids[i], node_ids[k], error))

    # Calculate summary statistics
    if errors:
        total_errors = len(errors)
        average_error = np.mean([error[3] for error in errors])
        max_error = max(errors, key=lambda x: x[3])
        summary = {
            'total_errors': total_errors,
            'average_error': average_error,
            'max_error': max_error,
            'errors': errors[:5]  # Return top 5 errors for detailed view
        }
    else:
        summary = {
            'total_errors': 0,
            'average_error': 0,
            'max_error': None,
            'errors': []
        }

    return summary


# Example matrix: Replace this with your actual 84x84 latency matrix
matrix = np.loadtxt("../data_topology_2/energy_consumption_tp2_mW_rec.csv", delimiter=",")

# List of node IDs
node_ids = [4, 5, 9, 11, 12, 22, 23, 25, 26, 31, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48,
            53, 57, 58, 65, 68, 74, 76, 77, 79, 80, 81, 83, 88, 99, 100, 101, 102, 103, 104, 114,
            117, 118, 130, 131, 132, 141, 142, 143, 148, 149, 150, 151, 152, 153, 158, 159, 160,
            161, 165, 166, 167, 200, 201, 208, 216, 217, 218, 220, 221, 231, 237, 238, 239, 243,
            244, 245, 246, 249, 251, 254, 255, 256]

# Calculate and print triangle inequality errors
summary = calculate_triangle_inequality_error(matrix, node_ids)

print("Triangle Inequality Error Summary:")
print(f"Total Errors: {summary['total_errors']}")
print(f"Average Error Magnitude: {summary['average_error']:.2f}")
if summary['max_error']:
    max_err = summary['max_error']
    print(f"Maximum Error: Nodes {max_err[0]}, {max_err[1]}, {max_err[2]} | Magnitude: {max_err[3]:.2f}")
else:
    print("No triangle inequality violations found.")
print("\nSample Errors:")
for error in summary['errors']:
    print(f"Nodes: {error[0]}, {error[1]}, {error[2]} | Error Magnitude: {error[3]:.2f}")
