cmake_minimum_required(VERSION 3.27)
project(parprog)

set(CMAKE_CXX_STANDARD 17)

find_package(MPI REQUIRED)
include_directories(${MPI_INCLUDE_PATH})

find_package(OpenMP REQUIRED)

add_executable(single single.cpp)

add_executable(mpi mpi.cpp)
target_link_libraries(mpi ${MPI_LIBRARIES})

add_executable(omp omp.cpp)
target_link_libraries(omp OpenMP::OpenMP_CXX)
