import platform
import subprocess

def run(cmd):

    try:
        return subprocess.check_output(
            cmd,
            shell=True
        ).decode()

    except:
        return "Unknown"

def scan_hardware():

    return {

        "cpu":
        platform.processor(),

        "gpu":
        run("wmic path win32_VideoController get name"),

        "ram":
        run("wmic MemoryChip get Capacity"),

        "disk":
        run("wmic diskdrive get model"),

        "wifi":
        run("netsh wlan show drivers")

    }
