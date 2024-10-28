cd build
cmake -DCMAKE_TOOLCHAIN_FILE=../home/yammy/Code/LiDAR-Liskarm-v1/toolchain-arm.cmake -DCMAKE_BUILD_TYPE=Release ..
make -j4
scp ./Liskarm james@raspberrypi.local:/home/james/