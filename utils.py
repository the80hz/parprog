import numpy as np


def generate_matrices(rows, cols, value_range=(0, 100)):
    return np.random.randint(value_range[0], value_range[1], (rows, cols))


def save_matrix(matrix, filename):
    with open(filename, 'w') as file:
        rows, cols = matrix.shape
        file.write(f"{rows} {cols}\n")
        np.savetxt(file, matrix, fmt="%d")


def read_matrix(filename):
    with open(filename, 'r') as file:
        if 'result' not in filename:
            next(file)
        matrix = [list(map(int, line.split())) for line in file]
    return np.array(matrix)


def compare_matrices(matrix1, matrix2):
    return np.array_equal(matrix1, matrix2)
