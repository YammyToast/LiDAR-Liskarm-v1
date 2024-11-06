import argparse
import os
import re
from datetime import datetime
import subprocess

cmake_cmd = r"cmake -DCMAKE_TOOLCHAIN_FILE=/home/yammy/Code/LiDAR-Liskarm-v1/toolchain-arm.cmake -DCMAKE_BUILD_TYPE=Release .."
scp_cmd = r"scp ./Liskarm james@raspberrypi.local:/home/james/"


def write_log(__msg):
    try:
        fmt = f"[{datetime.now().strftime('%H:%M:%S')}] "
        fmt += str(__msg)
        print(fmt)
    except Exception as e:
        print(f"Could not log: {e}")


def read_username(__username_file_path):
    with open(__username_file_path, "r") as f:
        file_data = f.read()
        username_capture = re.search(r"USER=(.*)", file_data)
        if username_capture == None:
            raise Exception(
                f"Could not find USER key-pair in provided username file path: {__username_file_path}"
            )
        return __username_file_path.group().split("=")[-1]


def read_password(__password_file_path):
    with open(__password_file_path, "r") as f:
        file_data = f.read()
        password_capture = re.search(r"PASSWORD=(.*)", file_data)
        if password_capture == None:
            raise Exception(
                f"Could not find PASSWORD key-pair in provided password file path: {__password_file_path}"
            )
        return password_capture.group().split("=")[-1]


def main(__args_namespace):
    no_copy = __args_namespace.no_copy
    password_file_path = __args_namespace.password_file
    write_log(
        f"Building with: Password File Path=\"{password_file_path}\" | Copy To Target={'OFF' if no_copy else 'ON'}"
    )

    try:
        if os.path.isfile(password_file_path) == False:
            raise FileNotFoundError(
                f"could not find provided password file at path: {password_file_path}"
            )
        ssh_password = read_password(password_file_path)

        # BUILD START =================
        if not os.path.isdir("build"):
            write_log("/build directory does not exist, creating...")
            mk_result = subprocess.run(["mkdir", "build"], capture_output=True)
            if mk_result.returncode == 1:
                raise Exception(f"Could not create /build directory: {mk_result.stderr}")
        cmake_cmd_components = cmake_cmd.split(" ")
        cmake_result = subprocess.run(cmake_cmd_components, cwd="build", capture_output=True)
        if cmake_result.returncode != 0:
            raise Exception(f"CMake Failed: {cmake_result.stderr}, {cmake_result.stdout}") 

    except Exception as e:
        raise (e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-nc",
        "--no-copy",
        action="store_false",
        help="don't copy built program to target.",
    )
    parser.add_argument(
        "-u",
        "--target-user",
        action="store",
        default=".env",
        help="username to ssh into target as, file path. File must somewhere contain username in fmt: USER=...",
    )
    parser.add_argument(
        "-p",
        "--password-file",
        action="store",
        default=".env",
        help="target user's SSH password, file path. File must somewhere contain password in fmt: PASSWORD=...",
    )

    args = parser.parse_args()
    main(args)
