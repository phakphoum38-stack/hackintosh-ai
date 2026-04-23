import os
import json
from builder.kext_resolver import resolve_kexts
from builder.config_gen import generate_config

def create_structure():

    paths = [
        "EFI/OC",
        "EFI/OC/ACPI",
        "EFI/OC/Kexts",
        "EFI/OC/Drivers"
    ]

    for p in paths:
        os.makedirs(p, exist_ok=True)

def build_efi(config):

    print("🧠 Resolving kexts...")
    kexts = resolve_kexts(config)

    print("⚙️ Generating config.plist...")
    plist = generate_config(config, kexts)

    create_structure()

    with open("EFI/OC/config.plist", "w") as f:
        f.write(str(plist))

    return {
        "status": "EFI_CREATED",
        "kexts": kexts
    }
