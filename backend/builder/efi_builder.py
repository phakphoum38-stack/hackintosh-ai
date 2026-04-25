import os
import json
import shutil
import zipfile

from backend.builder.kext_resolver import resolve_kexts
from backend.builder.config_gen import generate_config

# ☁️ S3
from backend.core.storage import upload_file


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
def build_efi(job_id: int, config: dict, user_id: int = None):

    base_path = f"/tmp/efi_build_{job_id}"
    output_zip = f"/tmp/efi_{job_id}.zip"

    try:
        print(f"🧠 Resolving kexts for job {job_id}...")
        kexts = resolve_kexts(config)

        print("⚙️ Generating config.plist...")
        plist = generate_config(config, kexts)

        # =========================
        # 🧹 clean old build
        # =========================
        if os.path.exists(base_path):
            shutil.rmtree(base_path)

        create_structure(base_path)

        # =========================
        # 📝 write config.plist
        # =========================
        config_path = f"{base_path}/EFI/OC/config.plist"

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(str(plist))

        # =========================
        # 📦 zip output
        # =========================
        zip_efi(base_path, output_zip)

        print(f"[✓] EFI built locally: {output_zip}")

        # =========================
        # ☁️ upload to S3
        # =========================
        if user_id:
            s3_key = f"efi/{user_id}/{job_id}.zip"
        else:
            s3_key = f"efi/{job_id}.zip"

        print("☁️ Uploading to S3...")
        s3_url = upload_file(output_zip, s3_key)

        print(f"[✓] Uploaded to S3: {s3_url}")

        return s3_url  # 🔥 ส่ง URL กลับ worker

    except Exception as e:
        print(f"[ERROR] EFI build failed: {e}")
        raise e

    finally:
        # =========================
        # 🧹 cleanup tmp
        # =========================
        try:
            if os.path.exists(base_path):
                shutil.rmtree(base_path)

            if os.path.exists(output_zip):
                os.remove(output_zip)

            print("🧹 Cleaned tmp files")

        except Exception as cleanup_error:
            print(f"[WARN] Cleanup failed: {cleanup_error}")
