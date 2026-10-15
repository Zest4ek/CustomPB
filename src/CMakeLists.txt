cmake_minimum_required(VERSION 3.30)

project(CUSTOM_PB LANGUAGES C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_executable(custom_pb custom_pb.c example.c)