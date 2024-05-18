import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

def run_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Command succeeded: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.stderr}")
        exit(1)

def cmake_build():
    build_dir = "build"
    os.makedirs(build_dir, exist_ok=True)
    os.chdir(build_dir)
    
    run_command(["cmake", "-DCMAKE_BUILD_TYPE=Release", ".."])
    run_command(["cmake", "--build", ".", "--config", "Release"])
    os.chdir("..")

def read_matrix(filepath):
    with open(filepath, 'r') as file:
        matrix = [list(map(int, line.split())) for line in file]
    return np.array(matrix)

def read_timing_results(filepath):
    sizes = []
    times = []
    with open(filepath, 'r') as file:
        for line in file:
            size, time = map(float, line.split())
            sizes.append(int(size))
            times.append(time)
    return sizes, times

def verify_results(matrix_a, matrix_b, result_matrix):
    calculated_result = np.dot(matrix_a, matrix_b)
    return np.allclose(calculated_result, result_matrix)

def main():
    sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    results = []

    cmake_build()

    os.chdir("build")
    run_command(["./single"])
    os.chdir("..")

    timing_results_file = "build/timingResults.txt"
    if not os.path.exists(timing_results_file):
        print("Timing results file not found. Please ensure the C++ program has been run successfully.")
        return

    sizes, times = read_timing_results(timing_results_file)

    correctness = []
    for size in sizes:
        matrix_a = read_matrix(f"build/matrixA_{size}.txt")
        matrix_b = read_matrix(f"build/matrixB_{size}.txt")
        result_matrix = read_matrix(f"build/resultMatrix_{size}.txt")
        if verify_results(matrix_a, matrix_b, result_matrix):
            correctness.append(True)
        else:
            correctness.append(False)

    for size, time, correct in zip(sizes, times, correctness):
        print(f"Size: {size}, Time: {time:.4f}s, Correct: {correct}")

    plt.figure()
    plt.plot(sizes, times, 'o-', label='Measured Time')
    plt.xlabel('Matrix Size')
    plt.ylabel('Time (seconds)')
    plt.title('Matrix Multiplication Performance')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
