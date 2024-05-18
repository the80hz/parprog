#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>

void multiplyMatrices(const std::vector<std::vector<int>>& matrixA,
                      const std::vector<std::vector<int>>& matrixB,
                      std::vector<std::vector<int>>& resultMatrix, int size) {
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
    std::ofstream timingFile("timingResults.txt");

    for (int size : sizes) {
        std::vector<std::vector<int>> matrixA(size, std::vector<int>(size, 1)); // Example matrices
        std::vector<std::vector<int>> matrixB(size, std::vector<int>(size, 1)); // Fill with 1 for simplicity
        std::vector<std::vector<int>> resultMatrix(size, std::vector<int>(size));

        double totalDuration = 0.0;

        for (int run = 0; run < count; run++) {
            auto start = std::chrono::high_resolution_clock::now();

            multiplyMatrices(matrixA, matrixB, resultMatrix, size);

            auto end = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> duration = end - start;
            totalDuration += duration.count();
        }

        double averageDuration = totalDuration / double(count);
        timingFile << size << " " << averageDuration << "\n";
        std::cout << "Size: " << size << ", Average Time: " << averageDuration << " seconds" << std::endl;
    }

    timingFile.close();
    return 0;
}
