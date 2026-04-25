import os
import json
import shutil
import zipfile

from backend.builder.kext_resolver import resolve_kexts
from backend.builder.config_gen import generate_config


# =========================
# 📁 CREATE EFI STRUCTURE
# =========================
def create_structure(base_path):

    paths = [
        f"{base_path}/EFI/OC",
        f"{base_path}/EFI/OC/ACPI",
        f"{base_path}/EFI/OC/Kexts",
        f"{base_path}/EFI/OC/Drivers"
    ]

    for p in paths:
        os.makedirs(p, exist_ok=True)


# =========================
# 📦 ZIP EFI
# =========================
def zip_efi(base_path, output_zip):

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, base_path)
                zipf.write(full_path, arcname)


# =========================
# 🚀 BUILD EFI (MAIN)
# =========================
def build_efi(job_id: int, config: dict):

    try:
        print(f"🧠 Resolving kexts for job {job_id}...")
        kexts = resolve_kexts(config)

        print("⚙️ Generating config.plist...")
        plist = generate_config(config, kexts)

        # =========================
        # 📁 แยกโฟลเดอร์ต่อ job
        # =========================
        base_path = f"/tmp/efi_build_{job_id}"

        # ลบของเก่า (กันชน)
        if os.path.exists(base_path):
            shutil.rmtree(base_path)

        create_structure(base_path)

        # =========================
        # 📝 เขียน config.plist
        # =========================
        config_path = f"{base_path}/EFI/OC/config.plist"

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(str(plist))

        # =========================
        # 📦 zip output
        # =========================
        output_zip = f"/tmp/efi_{job_id}.zip"
        zip_efi(base_path, output_zip)

        print(f"[✓] EFI built: {output_zip}")

        return output_zip  # 🔥 สำคัญ (worker ใช้)

    except Exception as e:
        print(f"[ERROR] EFI build failed: {e}")
        raise e
