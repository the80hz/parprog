import numpy as np


def generate_matrices_and_empty_result_file(rows_a, cols_a, rows_b, cols_b, value_range=(0, 10)):
    matrix_a = np.random.randint(value_range[0], value_range[1], (rows_a, cols_a))
    matrix_b = np.random.randint(value_range[0], value_range[1], (rows_b, cols_b))

    np.savetxt("matrixA.txt", matrix_a, fmt="%d")
    np.savetxt("matrixB.txt", matrix_b, fmt="%d")

    open("resultMatrix.txt", 'w').close()

    print("Files generated.")


generate_matrices_and_empty_result_file(3, 4, 4, 3)
