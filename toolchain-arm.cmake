# toolchain-arm.cmake

# Set the system name and processor
SET(CMAKE_SYSTEM_NAME Linux)
SET(CMAKE_SYSTEM_PROCESSOR arm)

# Define the location of the sysroot
SET(CMAKE_SYSROOT /home/yammy/Code/LiDAR-Liskarm-v1/sysroot)

# Define the cross-compiler
# SET(CMAKE_C_COMPILER /usr/bin/arm-linux-gnueabihf-gcc)
# SET(CMAKE_CXX_COMPILER /usr/bin/arm-linux-gnueabihf-g++)
SET(CMAKE_C_COMPILER /usr/bin/aarch64-linux-gnu-gcc)
SET(CMAKE_CXX_COMPILER /usr/bin/aarch64-linux-gnu-g++)

# Define the location of the C and C++ libraries in the sysroot
SET(CMAKE_FIND_ROOT_PATH /home/yammy/Code/LiDAR-Liskarm-v1/sysroot)

# Ensure CMake finds libraries and includes in the sysroot
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
