# backend/builder/config_gen.py

import plistlib
import os


def generate_config(config: dict, kexts: list):
    output_path = "/tmp/config.plist"

    # =========================
    # 🔧 convert kext → OpenCore format
    # =========================
    kernel_add = []

    for k in kexts:
        name = k.replace(".kext", "")

        kernel_add.append({
            "BundlePath": k,
            "Enabled": True,
            "ExecutablePath": f"Contents/MacOS/{name}",
            "PlistPath": "Contents/Info.plist"
        })

    # =========================
    # 🧠 CONFIG STRUCTURE (minimal bootable)
    # =========================
    plist_data = {
        "ACPI": {
            "Add": [],
            "Delete": [],
            "Patch": []
        },
        "Booter": {
            "Quirks": {}
        },
        "DeviceProperties": {
            "Add": {},
            "Delete": {}
        },
        "Kernel": {
            "Add": kernel_add,
            "Block": [],
            "Force": [],
            "Patch": []
        },
        "Misc": {
            "Boot": {},
            "Debug": {},
            "Security": {}
        },
        "NVRAM": {
            "Add": {},
            "Delete": {}
        },
        "PlatformInfo": {
            "Generic": {
                "SystemProductName": "iMacPro1,1",
                "SystemSerialNumber": "AI123456789",
                "MLB": "AI000000000000000",
                "ROM": "112233445566"
            }
        },
        "UEFI": {
            "Drivers": [],
            "Quirks": {}
        }
    }

    # =========================
    # 💾 write plist
    # =========================
    os.makedirs("/tmp", exist_ok=True)

    with open(output_path, "wb") as f:
        plistlib.dump(plist_data, f)

    return output_path
