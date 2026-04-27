import requests
import zipfile
import io
import os

KEXT_SOURCES = {
    "Lilu.kext": "https://github.com/acidanthera/Lilu/releases/latest/download/Lilu.zip",
    "VirtualSMC.kext": "https://github.com/acidanthera/VirtualSMC/releases/latest/download/VirtualSMC.zip",
    "WhateverGreen.kext": "https://github.com/acidanthera/WhateverGreen/releases/latest/download/WhateverGreen.zip",
    "AppleALC.kext": "https://github.com/acidanthera/AppleALC/releases/latest/download/AppleALC.zip"
}


def download_and_extract_kext(kext_name, dest_dir):
    url = KEXT_SOURCES.get(kext_name)

    if not url:
        print(f"[WARN] No source for {kext_name}")
        return

    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))

    for file in z.namelist():
        if ".kext/" in file:
            z.extract(file, dest_dir)


def install_kexts(base_path, kexts):
    kext_dir = os.path.join(base_path, "EFI/OC/Kexts")

    for k in kexts:
        download_and_extract_kext(k, kext_dir)

    return kext_dir
