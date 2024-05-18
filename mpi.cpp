#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <mpi.h>

std::vector<std::vector<int>> readMatrix(const std::string& filename, int size) {
    std::ifstream file(filename);
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size));
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            file >> matrix[i][j];
        }
    }
    file.close();
    return matrix;
}

void saveMatrix(const std::vector<std::vector<int>>& matrix, const std::string& filename) {
    std::ofstream file(filename);
    for (const auto& row : matrix) {
        for (const auto& elem : row) {
            file << elem << " ";
        }
        file << "\n";
    }
    file.close();
}

void multiplyMatrices(const std::vector<std::vector<int>>& matrixA,
                      const std::vector<std::vector<int>>& matrixB,
                      std::vector<std::vector<int>>& resultMatrix, int size, int rank, int numProcs) {
    int rowsPerProc = size / numProcs;
    int startRow = rank * rowsPerProc;
    int endRow = (rank + 1) * rowsPerProc;

    for (int i = startRow; i < endRow; i++) {
        for (int j = 0; j < size; j++) {
            resultMatrix[i][j] = 0;
            for (int k = 0; k < size; k++) {
                resultMatrix[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, numProcs;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &numProcs);

    std::vector<int> sizes = {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024};
    int count = 100;
    std::string data_dir = "data";
    std::ofstream timingFile;

    if (rank == 0) {
        timingFile.open(data_dir + "/timingResults_mpi.txt");
    }

    for (int size : sizes) {
        std::vector<std::vector<int>> matrixA = readMatrix(data_dir + "/matrixA_" + std::to_string(size) + ".txt", size);
        std::vector<std::vector<int>> matrixB = readMatrix(data_dir + "/matrixB_" + std::to_string(size) + ".txt", size);
        std::vector<std::vector<int>> resultMatrix(size, std::vector<int>(size));

        for (int run = 0; run < count; run++) {
            auto start = std::chrono::high_resolution_clock::now();

            // Broadcast matrices to all processes
            for (int i = 0; i < size; i++) {
                MPI_Bcast(matrixA[i].data(), size, MPI_INT, 0, MPI_COMM_WORLD);
                MPI_Bcast(matrixB[i].data(), size, MPI_INT, 0, MPI_COMM_WORLD);
            }

            // Multiply matrices in parallel
            multiplyMatrices(matrixA, matrixB, resultMatrix, size, rank, numProcs);

            // Gather results from all processes
            for (int i = 0; i < size; i++) {
                MPI_Gather(MPI_IN_PLACE, size / numProcs, MPI_INT, resultMatrix[i].data(), size / numProcs, MPI_INT, 0, MPI_COMM_WORLD);
            }

            auto end = std::chrono::high_resolution_clock::now();
            if (rank == 0) {
                std::chrono::duration<double> duration = end - start;
                timingFile << size << " " << duration.count() << "\n";
            }
        }

        if (rank == 0) {
            saveMatrix(resultMatrix, data_dir + "/resultMatrix_" + std::to_string(size) + ".txt");
        }
    }

    if (rank == 0) {
        timingFile.close();
    }

    MPI_Finalize();
    return 0;
}
