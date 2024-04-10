import os

from gen import generate_matrices_and_empty_result_file


def main():
    sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        print(size)
        generate_matrices_and_empty_result_file(size, size, size, size)
        os.chdir("cmake-build-release")
        os.system("./parprog_lab1")
        os.chdir("..")


if __name__ == "__main__":
    main()
