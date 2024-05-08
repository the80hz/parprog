#include <iostream>
#include <fstream>
#include <vector>
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::ifstream fileA, fileB;
    std::ofstream fileC;
    int rowsA, colsA, rowsB, colsB;

    // Обработка файлов и чтение размеров только в процессе 0
    if (rank == 0) {
        fileA.open("matrixA.txt");
        fileB.open("matrixB.txt");
        fileC.open("resultMatrix.txt");

        if (!fileA.is_open() || !fileB.is_open()) {
            std::cout << "Could not open the file!" << std::endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        fileA >> rowsA >> colsA;
        fileB >> rowsB >> colsB;

        if (colsA != rowsB) {
            std::cout << "Matrix cannot be multiplied!" << std::endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
    }

    // Рассылка размеров матриц всем процессам
    MPI_Bcast(&rowsA, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&colsA, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&rowsB, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&colsB, 1, MPI_INT, 0, MPI_COMM_WORLD);

    std::vector<int> subA(rowsA * colsA / size); // Локальный фрагмент матрицы A
    std::vector<int> fullB(rowsB * colsB);       // Полная матрица B
    std::vector<int> subC(rowsA * colsB / size, 0); // Локальный фрагмент результата

    if (rank == 0) {
        std::vector<int> fullA(rowsA * colsA);
        for (int i = 0; i < rowsA * colsA; ++i) {
            fileA >> fullA[i];
        }
        for (int i = 0; i < rowsB * colsB; ++i) {
            fileB >> fullB[i];
        }

        MPI_Scatter(fullA.data(), rowsA * colsA / size, MPI_INT, subA.data(), rowsA * colsA / size, MPI_INT, 0, MPI_COMM_WORLD);
    } else {
        MPI_Scatter(nullptr, rowsA * colsA / size, MPI_INT, subA.data(), rowsA * colsA / size, MPI_INT, 0, MPI_COMM_WORLD);
    }

    MPI_Bcast(fullB.data(), rowsB * colsB, MPI_INT, 0, MPI_COMM_WORLD);

    // Выполнение умножения
    int local_rows = rowsA / size;
    for (int i = 0; i < local_rows; ++i) {
        for (int j = 0; j < colsB; ++j) {
            for (int k = 0; k < colsA; ++k) {
                subC[i * colsB + j] += subA[i * colsA + k] * fullB[k * colsB + j];
            }
        }
    }

    if (rank == 0) {
        MPI_Gather(MPI_IN_PLACE, rowsA * colsB / size, MPI_INT, subC.data(), rowsA * colsB / size, MPI_INT, 0, MPI_COMM_WORLD);
    } else {
        MPI_Gather(subC.data(), rowsA * colsB / size, MPI_INT, nullptr, 0, MPI_INT, 0, MPI_COMM_WORLD);
    }

    if (rank == 0) {
        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                fileC << subC[i * colsB + j] << " ";
            }
            fileC << "\n";
        }

        fileA.close();
        fileB.close();
        fileC.close();
    }

    MPI_Finalize();
    return 0;
}
