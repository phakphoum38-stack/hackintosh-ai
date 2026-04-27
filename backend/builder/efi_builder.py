import os
import shutil

from backend.builder.kext_resolver import resolve_kexts
from backend.builder.config_gen import generate_config
from backend.builder.kext_downloader import install_kexts
from backend.builder.snapshot import snapshot_kexts_into_config
from backend.builder.hardware import normalize_hardware
from backend.builder.copy_base import copy_base_efi


def build_efi(job_id: int, config: dict, user_id: int = None):

    base_path = f"/tmp/efi_build_{job_id}"
    output_zip = f"/tmp/efi_{job_id}.zip"

    try:
        # =========================
        # 🧠 normalize hardware
        # =========================
        config = normalize_hardware(config)

        print(f"🧠 Resolving kexts for job {job_id}...")
        kexts = resolve_kexts(config)

        print("⚙️ Generating config.plist...")
        config_path_tmp = generate_config(config, kexts)

        # =========================
        # 🧹 clean old build
        # =========================
        if os.path.exists(base_path):
            shutil.rmtree(base_path)

        os.makedirs(base_path, exist_ok=True)

        # =========================
        # 🧱 COPY OpenCore base (สำคัญสุด)
        # =========================
        copy_base_efi(base_path)

        # =========================
        # 📦 INSTALL KEXT (REAL)
        # =========================
        kext_dir = install_kexts(base_path, kexts)

        # =========================
        # 📝 COPY config.plist
        # =========================
        final_config_path = f"{base_path}/EFI/OC/config.plist"
        shutil.copy(config_path_tmp, final_config_path)

        # =========================
        # ⚙️ SNAPSHOT (sync kext → config)
        # =========================
        snapshot_kexts_into_config(final_config_path, kext_dir)

        # =========================
        # 📦 ZIP
        # =========================
        zip_efi(base_path, output_zip)

        print(f"[✓] EFI built locally: {output_zip}")

        # =========================
        # ☁️ Upload to S3
        # =========================
        if user_id:
            s3_key = f"efi/{user_id}/{job_id}.zip"
        else:
            s3_key = f"efi/{job_id}.zip"

        print("☁️ Uploading to S3...")
        s3_url = upload_file(output_zip, s3_key)

        print(f"[✓] Uploaded to S3: {s3_url}")

        return s3_url

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
