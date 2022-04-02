# Works with 3.11 and tested through 3.23
cmake_minimum_required(VERSION 3.11...3.23)

# Project name and a few useful settings. Other commands can pick up the results
project(
  Neat23 
  VERSION 0.1
  DESCRIPTION "A code for my PHD"
  LANGUAGES CXX)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# Let's ensure -std=c++xx instead of -std=g++xx
set(CMAKE_CXX_EXTENSIONS OFF)


# Docs only available if this is the main app
find_package(Doxygen)



if(Doxygen_FOUND)
	set(DOXYGEN_IN ${CMAKE_CURRENT_SOURCE_DIR}/docs/Doxyfile.in)
    set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)

    # request to configure the file
    configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
    message("Doxygen build started")

    # note the option ALL which allows to build the docs together with the application
    add_custom_target( doc_doxygen ALL
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating API documentation with Doxygen"
        VERBATIM )
else()
  message(STATUS "Doxygen not found, not building docs")
endif()

# Source files
file(GLOB_RECURSE SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_executable(Neat23 ${SRC_FILES})
target_include_directories(Neat23 PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
