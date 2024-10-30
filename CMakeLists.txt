#toolchain-arm.cmake

# =======================================
# Identity
# =======================================


cmake_minimum_required(VERSION 3.12)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


project(
    Liskarm
    VERSION 0.0.1
    DESCRIPTION "LISKARM PROJECT"
    LANGUAGES CXX
)





# =======================================
# Fetch Content
# =======================================
include(FetchContent)

# =======================================
# Subdirectories
# =======================================

add_subdirectory(src)

# =======================================
# Libs
# =======================================


include_directories(${CMAKE_SOURCE_DIR}/include)
link_directories(${CMAKE_SOURCE_DIR}/lib)

find_library(PIGPIO_LIB pigpio PATHS ${CMAKE_SYSROOT}/usr/lib NO_DEFAULT_PATH)
# find_library(WIRINGPI_LIB wiringPi PATHS ${CMAKE_SYSROOT}/usr/lib NO_DEFAULT_PATH)
# message(STATUS "WiringPi Path: ${WIRINGPI_LIB}")
# message(STATUS "SYSROOT: ${CMAKE_SYSROOT}/usr/lib")
message(STATUS "PIGPIO PATH: ${PIGPIO_LIB}")

# =======================================
# Links
# =======================================

add_executable(${PROJECT_NAME} src/main.cpp)

target_link_libraries(${PROJECT_NAME} PRIVATE spdlog)
# target_link_libraries(${PROJECT_NAME} PRIVATE ${WIRINGPI_LIB})
target_link_libraries(${PROJECT_NAME} PRIVATE ${PIGPIO_LIB})