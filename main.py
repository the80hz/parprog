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

def run_program(program_name):
    print(f"Running the {program_name} program...")
    os.chdir("build")
    run_command([f"./{program_name}"])
    os.chdir("..")

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

    # Run single executable
    run_program("single")

    # Verify results for single
    print("Verifying results for single...")
    correctness_single = []
    for size in sizes:
        matrix_a = read_matrix(f"{data_dir}/matrixA_{size}.txt")
        matrix_b = read_matrix(f"{data_dir}/matrixB_{size}.txt")
        result_matrix = read_matrix(f"{data_dir}/resultMatrix_{size}.txt")
        is_correct = verify_results(matrix_a, matrix_b, result_matrix)
        correctness_single.append(is_correct)
        print(f"Size: {size}, Correct (single): {is_correct}")

    # Run mpi executable
    run_program("mpi")

    # Verify results for mpi
    print("Verifying results for mpi...")
    correctness_mpi = []
    for size in sizes:
        matrix_a = read_matrix(f"{data_dir}/matrixA_{size}.txt")
        matrix_b = read_matrix(f"{data_dir}/matrixB_{size}.txt")
        result_matrix = read_matrix(f"{data_dir}/resultMatrix_{size}.txt")
        is_correct = verify_results(matrix_a, matrix_b, result_matrix)
        correctness_mpi.append(is_correct)
        print(f"Size: {size}, Correct (mpi): {is_correct}")

    # Run omp executable
    run_program("omp")

    # Verify results for omp
    print("Verifying results for omp...")
    correctness_omp = []
    for size in sizes:
        matrix_a = read_matrix(f"{data_dir}/matrixA_{size}.txt")
        matrix_b = read_matrix(f"{data_dir}/matrixB_{size}.txt")
        result_matrix = read_matrix(f"{data_dir}/resultMatrix_{size}.txt")
        is_correct = verify_results(matrix_a, matrix_b, result_matrix)
        correctness_omp.append(is_correct)
        print(f"Size: {size}, Correct (omp): {is_correct}")

    # Read and process timing results for single, mpi, and omp
    print("Processing timing results...")
    timing_results_single = read_timing_results(f"{data_dir}/timingResults_single.txt")
    timing_results_mpi = read_timing_results(f"{data_dir}/timingResults_mpi.txt")
    timing_results_omp = read_timing_results(f"{data_dir}/timingResults_omp.txt")

    results_single = []
    results_mpi = []
    results_omp = []
    for size in sizes:
        times_single = timing_results_single[size]
        times_mpi = timing_results_mpi[size]
        times_omp = timing_results_omp[size]
        
        mean_time_single = np.mean(times_single)
        std_dev_single = np.std(times_single, ddof=1)
        conf_interval_single = t.interval(0.95, len(times_single)-1, loc=mean_time_single, scale=std_dev_single/np.sqrt(len(times_single)))
        results_single.append((size, mean_time_single, conf_interval_single[1] - mean_time_single))
        
        mean_time_mpi = np.mean(times_mpi)
        std_dev_mpi = np.std(times_mpi, ddof=1)
        conf_interval_mpi = t.interval(0.95, len(times_mpi)-1, loc=mean_time_mpi, scale=std_dev_mpi/np.sqrt(len(times_mpi)))
        results_mpi.append((size, mean_time_mpi, conf_interval_mpi[1] - mean_time_mpi))
        
        mean_time_omp = np.mean(times_omp)
        std_dev_omp = np.std(times_omp, ddof=1)
        conf_interval_omp = t.interval(0.95, len(times_omp)-1, loc=mean_time_omp, scale=std_dev_omp/np.sqrt(len(times_omp)))
        results_omp.append((size, mean_time_omp, conf_interval_omp[1] - mean_time_omp))

    # Plotting results
    print("Plotting results...")
    sizes_single, means_single, errors_single = zip(*results_single)
    sizes_mpi, means_mpi, errors_mpi = zip(*results_mpi)
    sizes_omp, means_omp, errors_omp = zip(*results_omp)
    
    fig, ax = plt.subplots()
    ax.errorbar(sizes_single, means_single, yerr=errors_single, fmt='-o', label='Single')
    ax.errorbar(sizes_mpi, means_mpi, yerr=errors_mpi, fmt='-o', label='MPI')
    ax.errorbar(sizes_omp, means_omp, yerr=errors_omp, fmt='-o', label='OpenMP')
    ax.set_xlabel('Matrix Size')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Performance Analysis with Error Bars')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.savefig('single_mpi_omp_comparison.png')
    plt.close()
    print("Plot saved as single_mpi_omp_comparison.png")

if __name__ == "__main__":
    main()
