import argparse
import os
import re
from datetime import datetime
import subprocess

cmake_cmd = r"cmake -DCMAKE_TOOLCHAIN_FILE=/home/yammy/Code/LiDAR-Liskarm-v1/toolchain-arm.cmake -DCMAKE_BUILD_TYPE=Release .."
make_cmd = r"make"
# scp_cmd = r"scp ./Liskarm james@raspberrypi.local:/home/james/"
ssh_cmd = r"sshpass -p"
scp_cmd = r"scp ./Liskarm"


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
        return username_capture.group().split("=")[-1]


def read_password(__password_file_path):
    with open(__password_file_path, "r") as f:
        file_data = f.read()
        password_capture = re.search(r"SSHPASS=(.*)", file_data)
        if password_capture == None:
            raise Exception(
                f"Could not find PASSWORD key-pair in provided password file path: {__password_file_path}"
            )
        return password_capture.group().split("=")[-1]


def main(__args_namespace):
    write_log(f"Liskarm configure.py")
    no_copy = __args_namespace.no_copy
    username_file_path = __args_namespace.ssh_id_file
    password_file_path = __args_namespace.ssh_id_file
    make_jobs = __args_namespace.make_jobs
    target_ip = __args_namespace.target_ip
    write_log(
        f"Building with: Password File Path=\"{password_file_path}\" | Copy To Target={'OFF' if no_copy else 'ON'}"
    )

    try:
        if os.path.isfile(password_file_path) == False:
            raise FileNotFoundError(
                f"could not find provided password file at path: {password_file_path}"
            )
        ssh_username = read_username(username_file_path)
        ssh_password = read_password(password_file_path)

        # BUILD START =================
        # Build Directory
        if not os.path.isdir("build"):
            write_log("/build directory does not exist, creating...")
            mk_result = subprocess.run(["mkdir", "build"], capture_output=True)
            if mk_result.returncode == 1:
                raise Exception(
                    f"Could not create /build directory: {mk_result.stderr}"
                )
        # CMake
        cmake_cmd_components = cmake_cmd.split(" ")
        write_log(f"Running CMake.\n\t{cmake_cmd_components}")
        cmake_result = subprocess.run(
            cmake_cmd_components, cwd="build", capture_output=True
        )
        if cmake_result.returncode != 0:
            raise Exception(
                f"CMake Failed: \n\tstderr - {cmake_result.stderr}, \n\tstdout - {cmake_result.stdout}"
            )
        # Make 
        make_cmd_components = [*make_cmd.split(" "), f"-j{make_jobs}"]
        write_log(f"Running Make.\n\t{make_cmd_components}")
        make_result = subprocess.run(
            make_cmd_components, cwd="build", capture_output=True
        )
        if make_result.returncode != 0:
            raise Exception(
                f"Make Failed: \n\tstderr - {make_result.stderr},\n\tstdout - {make_result.stdout}"
            )
        if hasattr(make_result, "stderr"):
            for item in (str(make_result.stderr)).split("\n"):
                # ughh
                if item == "b\'\'": continue
                write_log(f"Warning: {item}")
        # SCP
        ssh_cmd_components = [*ssh_cmd.split(" "), f"{ssh_password}"]
        scp_cmd_components = [*scp_cmd.split(" "), f"{ssh_username}@{target_ip}:/home/{ssh_username}/"]
        copy_cmd = [*ssh_cmd_components, *scp_cmd_components]
        write_log(f"Running SCP via SSHPass.\nTarget IP: {target_ip}, User: {ssh_username}")
        scp_result = subprocess.run(
            copy_cmd, cwd="build", capture_output=True
        )
        if scp_result.returncode != 0:
            raise Exception(
                f"SCP Failed: \n\tstderr - {scp_result.stderr},\n\tstdout - {scp_result.stdout}"
            )
        write_log(f"Finished.")
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
        "-j",
        "--make-jobs",
        action="store",
        default=4,
        help="Jobs to use in the make process.",
    )
    parser.add_argument(
        "-f",
        "--ssh-id-file",
        action="store",
        default=".env",
        help="File path, contains SSH username and password. File must somewhere contain username in fmt: USER=... and password in fmt: PASSWORD=...",
    )
    parser.add_argument(
        "-i",
        "--target-ip",
        action="store",
        default="raspberrypi.local",
        help="Target Pi's IP address.",
    )


    args = parser.parse_args()
    main(args)
