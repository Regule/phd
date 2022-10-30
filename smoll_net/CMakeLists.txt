# Works with 3.11 and tested through 3.23
cmake_minimum_required(VERSION 3.11...3.23)

# Project name and a few useful settings. Other commands can pick up the results
project(
  SmollNet 
  VERSION 0.1
  DESCRIPTION "A code for my PHD"
  LANGUAGES CXX)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

SET(CMAKE_CXX_FLAGS_DEBUG "-O0")
SET(CMAKE_C_FLAGS_DEBUG "-O0")

# Let's ensure -std=c++xx instead of -std=g++xx
set(CMAKE_CXX_EXTENSIONS OFF)



# Source files
file(GLOB_RECURSE SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_executable(run_evolution ${SRC_FILES})
target_include_directories(run_evolution PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
