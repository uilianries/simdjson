cmake_minimum_required(VERSION 3.1.3)
project(test_package CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

option(SIMDJSON_HEADER_ONLY "Build with somdjson header-only" OFF)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} CONAN_PKG::simdjson)
set_target_properties(${PROJECT_NAME} PROPERTIES CXX_STANDARD 17)
if (SIMDJSON_HEADER_ONLY)
    target_compile_definitions(${PROJECT_NAME} PRIVATE SIMDJSON_HEADER_ONLY=1)
endif()