import plistlib
import os

def snapshot_kexts_into_config(config_path, kext_dir):

    with open(config_path, "rb") as f:
        plist_data = plistlib.load(f)

    kernel_add = []

    for kext in os.listdir(kext_dir):
        if not kext.endswith(".kext"):
            continue

        name = kext.replace(".kext", "")

        kernel_add.append({
            "BundlePath": kext,
            "Enabled": True,
            "ExecutablePath": f"Contents/MacOS/{name}",
            "PlistPath": "Contents/Info.plist"
        })

    plist_data["Kernel"]["Add"] = kernel_add

    with open(config_path, "wb") as f:
        plistlib.dump(plist_data, f)
