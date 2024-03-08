#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>


int main() {
    std::ifstream fileA("matrixA.txt"), fileB("matrixB.txt");
    std::ofstream fileC("resultMatrix.txt");
    if (!fileA.is_open() || !fileB.is_open()) {
        std::cout << "Could not open the file!" << std::endl;
        return 1;
    }

    int rowsA, colsA, rowsB, colsB;
    fileA >> rowsA >> colsA;
    fileB >> rowsB >> colsB;

    if (colsA != rowsB) {
        std::cout << "Matrix cannot be multiplied!" << std::endl;
        return 1;
    }

    std::vector<std::vector<int>> matrixA(rowsA, std::vector<int>(colsA));
    std::vector<std::vector<int>> matrixB(rowsB, std::vector<int>(colsB));
    std::vector<std::vector<int>> resultMatrix(rowsA, std::vector<int>(colsB, 0));

    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsA; j++) {
            fileA >> matrixA[i][j];
        }
    }

    for (int i = 0; i < rowsB; i++) {
        for (int j = 0; j < colsB; j++) {
            fileB >> matrixB[i][j];
        }
    }

    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsB; j++) {
            for (int k = 0; k < colsA; k++) {
                resultMatrix[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }

    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);

    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsB; j++) {
            fileC << resultMatrix[i][j] << " ";
        }
        fileC << "\n";
    }

    std::cout << "Execution time: " << duration.count() << " microseconds" << std::endl;

    fileA.close();
    fileB.close();
    fileC.close();

    return 0;
}