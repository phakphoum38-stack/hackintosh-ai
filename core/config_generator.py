import plistlib
import os

def generate_config(hw,cpu,gpu):

    config = {

        "Booter": {},

        "DeviceProperties": {

            "Add": {

                "PciRoot(0x0)/Pci(0x2,0x0)":
                gpu

            }

        },

        "NVRAM": {

            "boot-args":
            cpu.get("boot_args","")

        },

        "PlatformInfo": {

            "Generic": {

                "SystemProductName":
                "MacBookPro16,3"

            }

        }

    }

    os.makedirs("output",exist_ok=True)

    with open(
        "output/config.plist",
        "wb"
    ) as f:

        plistlib.dump(config,f)

    return config
