#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int main() {
    FILE *fileA = fopen("matrixA.txt", "r"), *fileB = fopen("matrixB.txt", "r"),
         *fileC = fopen("resultMatrix.txt", "w");
    if (!fileA || !fileB) {
        printf("Could not open the file!\n");
        return 1;
    }

    int rowsA, colsA, rowsB, colsB;
    fscanf(fileA, "%d %d", &rowsA, &colsA);
    fscanf(fileB, "%d %d", &rowsB, &colsB);

    if (colsA != rowsB) {
        printf("Matrices cannot be multiplied!\n");
        return 1;
    }

    int **matrixA = (int **)malloc(rowsA * sizeof(int *));
    int **matrixB = (int **)malloc(rowsB * sizeof(int *));
    int **resultMatrix = (int **)malloc(rowsA * sizeof(int *));
    for (int i = 0; i < rowsA; i++) {
        matrixA[i] = (int *)malloc(colsA * sizeof(int));
        resultMatrix[i] = (int *)calloc(colsB, sizeof(int));
    }
    for (int i = 0; i < rowsB; i++) {
        matrixB[i] = (int *)malloc(colsB * sizeof(int));
    }

    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsA; j++) {
            fscanf(fileA, "%d", &matrixA[i][j]);
        }
    }

    for (int i = 0; i < rowsB; i++) {
        for (int j = 0; j < colsB; j++) {
            fscanf(fileB, "%d", &matrixB[i][j]);
        }
    }

    clock_t start = clock();
    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsB; j++) {
            for (int k = 0; k < colsA; k++) {
                resultMatrix[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }
    clock_t stop = clock();

    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsB; j++) {
            fprintf(fileC, "%d ", resultMatrix[i][j]);
        }
        fprintf(fileC, "\n");
    }

    double duration = (double)(stop - start) * 1000.0 / CLOCKS_PER_SEC;
    printf("Execution time: %f milliseconds\n", duration);

    for (int i = 0; i < rowsA; i++) {
        free(matrixA[i]);
        free(resultMatrix[i]);
    }
    for (int i = 0; i < rowsB; i++) {
        free(matrixB[i]);
    }
    free(matrixA);
    free(matrixB);
    free(resultMatrix);

    fclose(fileA);
    fclose(fileB);
    fclose(fileC);

    return 0;
}
