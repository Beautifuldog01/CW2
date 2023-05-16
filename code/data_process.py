import csv
import numpy as np

def read_and_process_csv(file_name):
    matrix = []

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            new_row = [np.nan if cell == '' else float(cell) for cell in row]
            matrix.append(new_row)

    matrix = np.array(matrix, dtype=float)
    n = matrix.shape[0]
    matrix[np.isnan(matrix)] = 2000000

    for i in range(n):
        for j in range(i+1, n):
            matrix[i, j] = matrix[j, i]
    matrix /= 1000

    return matrix
