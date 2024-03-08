import numpy as np


def read_matrix(file_path):
    with open(file_path) as file:
        next(file)
        matrix = [list(map(int, line.split())) for line in file]
    return np.array(matrix)


def read_results(file_path):
    with open(file_path) as file:
        matrix = [list(map(int, line.split())) for line in file]
    return np.array(matrix)


def compare_matrices(matrix1, matrix2):
    return np.allclose(matrix1, matrix2)


def main():
    matrix_a = read_matrix("matrixA.txt")
    matrix_b = read_matrix("matrixB.txt")
    result_matrix = read_results("resultMatrix.txt")

    calculated_result = np.dot(matrix_a, matrix_b)

    if compare_matrices(calculated_result, result_matrix):
        print("Result is correct.")
    else:
        print("Result is incorrect.")


if __name__ == "__main__":
    main()
