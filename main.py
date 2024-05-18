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
    print("Creating build directory...")
    os.makedirs(build_dir, exist_ok=True)
    os.chdir(build_dir)
    
    print("Running cmake...")
    run_command(["cmake", "-DCMAKE_BUILD_TYPE=Release", ".."])
    
    print("Building the project...")
    run_command(["cmake", "--build", ".", "--config", "Release"])
    os.chdir("..")

def save_matrix(matrix, filename):
    print(f"Saving matrix to {filename}...")
    np.savetxt(filename, matrix, fmt='%d')

def read_matrix(filepath):
    print(f"Reading matrix from {filepath}...")
    return np.loadtxt(filepath, dtype=int)

def read_timing_results(filepath):
    print(f"Reading timing results from {filepath}...")
    results = {}
    with open(filepath, 'r') as file:
        for line in file:
            size, time = map(float, line.split())
            size = int(size)
            if size not in results:
                results[size] = []
            results[size].append(time)
    return results

def verify_results(matrix_a, matrix_b, result_matrix):
    print("Verifying results...")
    calculated_result = np.dot(matrix_a, matrix_b)
    return np.allclose(calculated_result, result_matrix)

def main():
    sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

    print("Starting build process...")
    cmake_build()

    data_dir = "build/data"
    print(f"Creating data directory at {data_dir}...")
    os.makedirs(data_dir, exist_ok=True)

    print("Generating and saving matrices...")
    for size in sizes:
        matrix_a = np.random.randint(0, 10, (size, size))
        matrix_b = np.random.randint(0, 10, (size, size))

        save_matrix(matrix_a, f"{data_dir}/matrixA_{size}.txt")
        save_matrix(matrix_b, f"{data_dir}/matrixB_{size}.txt")

    print("Running the C++ program...")
    os.chdir("build")
    run_command(["./single"])
    os.chdir("..")

    timing_results_file = f"{data_dir}/timingResults.txt"
    if not os.path.exists(timing_results_file):
        print("Timing results file not found. Please ensure the C++ program has been run successfully.")
        return

    print("Reading timing results...")
    timing_results = read_timing_results(timing_results_file)

    print("Verifying multiplication results...")
    correctness = []
    for size in sizes:
        matrix_a = read_matrix(f"{data_dir}/matrixA_{size}.txt")
        matrix_b = read_matrix(f"{data_dir}/matrixB_{size}.txt")
        result_matrix = read_matrix(f"{data_dir}/resultMatrix_{size}.txt")
        is_correct = verify_results(matrix_a, matrix_b, result_matrix)
        correctness.append(is_correct)
        print(f"Size: {size}, Correct: {is_correct}")

    print("Processing timing results...")
    results = []
    for size in sizes:
        times = timing_results[size]
        mean_time = np.mean(times)
        std_dev = np.std(times, ddof=1)
        conf_interval = t.interval(0.95, len(times)-1, loc=mean_time, scale=std_dev/np.sqrt(len(times)))
        results.append((size, mean_time, conf_interval[1] - mean_time))

    print("Plotting results...")
    sizes, means, errors = zip(*results)
    fig, ax = plt.subplots()
    ax.errorbar(sizes, means, yerr=errors, fmt='-o')
    ax.set_xlabel('Matrix Size')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Performance Analysis with Error Bars')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('single.png')
    plt.close()
    print("Plot saved as single.png")

if __name__ == "__main__":
    main()
