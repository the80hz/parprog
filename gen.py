import numpy as np


def generate_matrices_and_empty_result_file(rows_a, cols_a, rows_b, cols_b, value_range=(0, 100)):
    if cols_a != rows_b:
        print("Matrix dimensions do not allow for multiplication. Adjusting dimensions.")
        cols_a = rows_b
    matrix_a = np.random.randint(value_range[0], value_range[1], (rows_a, cols_a))
    matrix_b = np.random.randint(value_range[0], value_range[1], (rows_b, cols_b))

    with open("cmake-build-release/matrixA.txt", 'w') as file:
        file.write(f"{rows_a} {cols_a}\n")
        np.savetxt(file, matrix_a, fmt="%d")

    with open("cmake-build-release/matrixB.txt", 'w') as file:
        file.write(f"{rows_b} {cols_b}\n")
        np.savetxt(file, matrix_b, fmt="%d")

    open("cmake-build-release/resultMatrix.txt", 'w').close()

    print("Files generated with correct dimensions for multiplication.")


generate_matrices_and_empty_result_file(100, 100, 100, 100)
