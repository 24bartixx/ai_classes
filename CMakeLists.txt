cmake_minimum_required(VERSION 3.10)
project(AI_Laby_2_cpp)

set(CMAKE_CXX_STANDARD 17)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)

# Source files
file(GLOB SRC_FILES ${CMAKE_SOURCE_DIR}/src/*.cpp)

# Main executable (optional, if you have main.cpp)
add_executable(main ${SRC_FILES} ${CMAKE_SOURCE_DIR}/main.cpp)

# Find all test files in tests/*/*/*.cpp
file(GLOB_RECURSE TEST_FILES ${CMAKE_SOURCE_DIR}/tests/*/*.cpp)

foreach(test_file ${TEST_FILES})
    get_filename_component(test_name ${test_file} NAME_WE)
    add_executable(${test_name} ${SRC_FILES} ${test_file})
    target_include_directories(${test_name} PRIVATE ${CMAKE_SOURCE_DIR}/include)
endforeach()
