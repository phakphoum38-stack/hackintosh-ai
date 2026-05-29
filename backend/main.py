import platform
import subprocess
import os

def run(cmd):

    try:
        return subprocess.check_output(
            cmd,
            shell=True
        ).decode().strip()

    except:
        return "Unknown"

def scan_hardware():

    system = platform.system()

    if system == "Windows":

        gpu = run(
            "wmic path win32_VideoController get name"
        )

        ram = run(
            "wmic MemoryChip get Capacity"
        )

        disk = run(
            "wmic diskdrive get model"
        )

        wifi = run(
            "netsh wlan show drivers"
        )

    else:

        gpu = run("lspci | grep VGA")
        ram = run("free -h")
        disk = run("lsblk")
        wifi = run("iwconfig")

    return {

        "os": system,

        "cpu":
        platform.processor(),

        "gpu": gpu,

        "ram": ram,
