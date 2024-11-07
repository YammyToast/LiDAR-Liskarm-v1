import argparse
import os
import re
from datetime import datetime
import subprocess

# =======================================

cmake_cmd = r"cmake -DCMAKE_TOOLCHAIN_FILE=/home/yammy/Code/LiDAR-Liskarm-v1/toolchain-arm.cmake -DCMAKE_BUILD_TYPE=Release .."
make_cmd = r"make"
# scp_cmd = r"scp ./Liskarm james@raspberrypi.local:/home/james/"
ssh_cmd = r"sshpass -p"
scp_cmd = r"scp ./Liskarm"

# =======================================


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


# =======================================


def handle_local_build_dir():
    if not os.path.isdir("build"):
        write_log("/build directory does not exist, creating...")
        mk_result = subprocess.run(["mkdir", "build"], capture_output=True)
        if mk_result.returncode == 1:
            raise Exception(f"Could not create /build directory: {mk_result.stderr}")


def run_cmake():
    cmake_cmd_components = cmake_cmd.split(" ")
    write_log(f"Running CMake.\n\t{cmake_cmd_components}")
    cmake_result = subprocess.run(
        cmake_cmd_components, cwd="build", capture_output=True
    )
    if cmake_result.returncode != 0:
        raise Exception(
            f"CMake Failed: \n\tstderr - {cmake_result.stderr}, \n\tstdout - {cmake_result.stdout}"
        )


def run_make(__make_jobs):

    make_cmd_components = [*make_cmd.split(" "), f"-j{__make_jobs}"]
    write_log(f"Running Make.\n\t{make_cmd_components}")
    make_result = subprocess.run(make_cmd_components, cwd="build", capture_output=True)
    if make_result.returncode != 0:
        raise Exception(
            f"Make Failed: \n\tstderr - {make_result.stderr},\n\tstdout - {make_result.stdout}"
        )
    if hasattr(make_result, "stderr"):
        for item in (str(make_result.stderr)).split("\n"):
            # ughh
            if item == "b''":
                continue
            write_log(f"Warning: {item}")


def handle_target_project_directory(
    __ssh_cmd_components, __ssh_username, __target_ip, __target_dir
):
    target_dir_check_cmd_components = [
        *__ssh_cmd_components,
        "ssh",
        f"{__ssh_username}@{__target_ip}",
        f"[ -d {__target_dir} ] && echo 1 || echo 0",
    ]
    target_dir_result = subprocess.run(
        target_dir_check_cmd_components, capture_output=True, text=True
    )
    if "0" in target_dir_result.stdout:
        write_log("/Liskarm directory does not exist on host, creating...")
        target_dir_make_cmd_components = [
            *__ssh_cmd_components,
            "ssh",
            f"{__ssh_username}@{__target_ip}",
            "mkdir",
            f"{__target_dir}",
        ]
        res = subprocess.run(target_dir_make_cmd_components, capture_output=True)
        print(res)


def run_scp(__ssh_cmd_components, __ssh_username, __target_ip, __target_dir):
    scp_cmd_components = [
        *scp_cmd.split(" "),
        f"{__ssh_username}@{__target_ip}:{__target_dir}",
    ]
    copy_cmd = [*__ssh_cmd_components, *scp_cmd_components]
    write_log(
        f"Running SCP via SSHPass.\nTarget IP: {__target_ip}, User: {__ssh_username}"
    )
    scp_result = subprocess.run(copy_cmd, cwd="build", capture_output=True)
    if scp_result.returncode != 0:
        raise Exception(
            f"SCP Failed: \n\tstderr - {scp_result.stderr},\n\tstdout - {scp_result.stdout}"
        )


# =======================================


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
        target_dir = f"/home/{ssh_username}/Liskarm/"

        # BUILD START =================
        # Build Directory
        handle_local_build_dir()
        # CMake
        run_cmake()
        # Make
        run_make(make_jobs)
        # SSHPASS STEM
        ssh_cmd_components = [*ssh_cmd.split(" "), f"{ssh_password}"]
        # Make Project directory on target
        handle_target_project_directory(
            ssh_cmd_components, ssh_username, target_ip, target_dir
        )
        # SCP
        if no_copy == False:
            run_scp(ssh_cmd_components, ssh_username, target_ip, target_dir)
        write_log(f"Finished with main executable...")
    except Exception as e:
        raise (e)

    try:
        write_log(f"Compiling Web GUI")
    except Exception as e:
        raise (e)


# =======================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-nc",
        "--no-copy",
        action="store_true",
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
