import os
import shutil
import zipfile
from datetime import datetime

from backend.core.db import SessionLocal
from backend.models.efi_job import EFIJob

# 🔥 ของที่คุณมีอยู่แล้ว
from backend.builder.efi_builder import build_efi_structure
from backend.builder.kext_resolver import resolve_kexts
from backend.builder.config_gen import generate_config

OUTPUT_DIR = "/app/output"


def build_efi_task(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(EFIJob).get(job_id)
        if not job:
            return

        job.status = "running"
        job.progress = 5
        db.commit()

        # =========================
        # 🧠 STEP 1: resolve kexts
        # =========================
        kexts = resolve_kexts({
            "cpu": "intel",
            "gpu": "amd",
            "wifi": "intel"
        })

        job.progress = 25
        db.commit()

        # =========================
        # ⚙️ STEP 2: generate config.plist
        # =========================
        config_path = generate_config(kexts)

        job.progress = 50
        db.commit()

        # =========================
        # 🧱 STEP 3: build EFI structure
        # =========================
        build_dir = f"/tmp/efi_{job_id}"
        os.makedirs(build_dir, exist_ok=True)

        build_efi_structure(
            output_dir=build_dir,
            kexts=kexts,
            config_path=config_path
        )

        job.progress = 75
        db.commit()

        # =========================
        # 📦 STEP 4: ZIP
        # =========================
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        zip_path = os.path.join(
            OUTPUT_DIR,
            f"efi_{job_id}.zip"
        )

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, build_dir)
                    zipf.write(full_path, rel_path)

        job.progress = 100
        job.status = "completed"
        job.result_path = zip_path
        db.commit()

        # cleanup
        shutil.rmtree(build_dir, ignore_errors=True)

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()

    finally:
        db.close()
