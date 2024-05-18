#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <omp.h>

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
                      std::vector<std::vector<int>>& resultMatrix, int size) {
    #pragma omp parallel for
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            resultMatrix[i][j] = 0;
            for (int k = 0; k < size; k++) {
                resultMatrix[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }
}

int main() {
    std::vector<int> sizes = {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024};
    int count = 100;
    std::string data_dir = "data";
    std::ofstream timingFile(data_dir + "/timingResults_omp.txt");

    for (int size : sizes) {
        std::vector<std::vector<int>> matrixA = readMatrix(data_dir + "/matrixA_" + std::to_string(size) + ".txt", size);
        std::vector<std::vector<int>> matrixB = readMatrix(data_dir + "/matrixB_" + std::to_string(size) + ".txt", size);
        std::vector<std::vector<int>> resultMatrix(size, std::vector<int>(size));

        for (int run = 0; run < count; run++) {
            auto start = std::chrono::high_resolution_clock::now();

            multiplyMatrices(matrixA, matrixB, resultMatrix, size);

            auto end = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> duration = end - start;
            timingFile << size << " " << duration.count() << "\n";
        }

        saveMatrix(resultMatrix, data_dir + "/resultMatrix_" + std::to_string(size) + ".txt");
    }

    timingFile.close();
    return 0;
}
