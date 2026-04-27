import plistlib
import os
import uuid


def sort_kexts(kexts):
    priority = [
        "Lilu.kext",
        "VirtualSMC.kext",
        "SMCProcessor.kext",
        "SMCSuperIO.kext",
        "SMCBatteryManager.kext",
        "WhateverGreen.kext",
        "AppleALC.kext"
    ]

    ordered = []

    for p in priority:
        if p in kexts:
            ordered.append(p)

    for k in kexts:
        if k not in ordered:
            ordered.append(k)

    return ordered


def generate_config(config: dict, kexts: list):
    output_path = f"/tmp/config_{uuid.uuid4()}.plist"

    # =========================
    # 🧠 Sort kext (สำคัญมาก)
    # =========================
    kexts = sort_kexts(kexts)

    # =========================
    # 🔧 Kernel Add
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
    # 🧠 Boot args
    # =========================
    boot_args = "-v keepsyms=1 debug=0x100"

    # =========================
    # 🧠 SMBIOS auto
    # =========================
    cpu = config.get("cpu", "").lower()

    if "amd" in cpu:
        smbios = "MacPro7,1"
    else:
        smbios = "iMac19,1"

    # =========================
    # 🧱 FINAL CONFIG
    # =========================
    plist_data = {
        "ACPI": {
            "Add": [
                {"Path": "SSDT-EC.aml", "Enabled": True},
                {"Path": "SSDT-PLUG.aml", "Enabled": True},
                {"Path": "SSDT-USBX.aml", "Enabled": True}
            ],
            "Delete": [],
            "Patch": []
        },

        "Booter": {
            "Quirks": {
                "AvoidRuntimeDefrag": True,
                "EnableSafeModeSlide": True,
                "ProvideCustomSlide": True
            }
        },

        "DeviceProperties": {
            "Add": {},
            "Delete": {}
        },

        "Kernel": {
            "Add": kernel_add,
            "Block": [],
            "Force": [],
            "Patch": [],
            "Quirks": {
                "AppleCpuPmCfgLock": False,
                "AppleXcpmCfgLock": False,
                "DisableIoMapper": True,
                "PanicNoKextDump": True,
                "PowerTimeoutKernelPanic": True,
                "XhciPortLimit": True
            }
        },

        "Misc": {
            "Boot": {
                "Timeout": 5
            },
            "Debug": {
                "AppleDebug": True,
                "ApplePanic": True,
                "DisableWatchDog": True
            },
            "Security": {
                "AllowSetDefault": True,
                "ScanPolicy": 0
            }
        },

        "NVRAM": {
            "Add": {
                "7C436110-AB2A-4BBB-A880-FE41995C9F82": {
                    "boot-args": boot_args
                }
            },
            "Delete": {}
        },

        "PlatformInfo": {
            "Generic": {
                "SystemProductName": smbios,
                "SystemSerialNumber": str(uuid.uuid4())[:12],
                "MLB": str(uuid.uuid4())[:16],
                "ROM": "112233445566"
            }
        },

        "UEFI": {
            "Drivers": [
                "OpenRuntime.efi",
                "HfsPlus.efi"
            ],
            "Quirks": {
                "EnableVectorAcceleration": True
            }
        }
    }

    # =========================
    # 💾 SAVE
    # =========================
    os.makedirs("/tmp", exist_ok=True)

    with open(output_path, "wb") as f:
        plistlib.dump(plist_data, f)

    return output_path
