import os
import shutil

ASSETS_DIR = "assets/opencore/EFI"

def copy_base_efi(base_path):
    src = ASSETS_DIR
    dst = os.path.join(base_path, "EFI")

    if not os.path.exists(src):
        raise Exception("❌ OpenCore base not found in assets/opencore")

    shutil.copytree(src, dst, dirs_exist_ok=True)

    print("[✓] OpenCore base copied")
