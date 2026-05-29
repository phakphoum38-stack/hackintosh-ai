import os
import shutil

def build_efi(config):

    base = "output/EFI/OC"

    os.makedirs(base+"/Kexts",exist_ok=True)
    os.makedirs(base+"/Drivers",exist_ok=True)
    os.makedirs(base+"/ACPI",exist_ok=True)

    shutil.copy(
        "output/config.plist",
        base+"/config.plist"
    )
