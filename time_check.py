import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import time

from utils import generate_matrices_and_empty_result_file, compare_matrices, read_matrix, read_results


def main():
    sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    results = []
    confidence_intervals = []

    for size in sizes:
        times = []
        correctness = []
        print(size)
        for _ in range(100):
            generate_matrices_and_empty_result_file(size, size, size, size)
            os.chdir("cmake-build-release")
            start = time.time()
            os.system("./parprog_lab1")
            elapsed = time.time() - start
            times.append(elapsed)
            os.chdir("..")

            matrix_a = read_matrix("cmake-build-release/matrixA.txt")
            matrix_b = read_matrix("cmake-build-release/matrixB.txt")
            result_matrix = read_results("cmake-build-release/resultMatrix.txt")
            calculated_result = np.dot(matrix_a, matrix_b)

            if compare_matrices(calculated_result, result_matrix):
                correctness.append(True)
            else:
                correctness.append(False)

        mean_time = np.mean(times)
        std_dev = np.std(times, ddof=1)
        conf_interval = t.interval(0.95, len(times)-1, loc=mean_time, scale=std_dev/np.sqrt(len(times)))
        confidence_intervals.append((size, conf_interval))
        results.append((size, mean_time, std_dev, all(correctness)))

        print(f"Mean time: {mean_time:.4f}s, Std Dev: {std_dev:.4f}s, Correctness: {all(correctness)}")

    sizes, means, errors = zip(*[(r[0], r[1], r[2]) for r in results])
    fig, ax = plt.subplots()
    ax.errorbar(sizes, means, yerr=errors, fmt='-o')
    ax.set_xlabel('Matrix Size')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Performance Analysis with Error Bars')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()


if __name__ == "__main__":
    main()
