import uuid
import os
import shutil
from backend.builder.kext_resolver import resolve_kexts
from backend.builder.config_gen import generate_config
from backend.builder.efi_builder import build_efi_structure
from backend.core.job_manager import update_job

OUTPUT_DIR = "/app/output"

def run_pipeline(job_id: str, spec: dict):
    job_path = os.path.join(OUTPUT_DIR, job_id)
    os.makedirs(job_path, exist_ok=True)

    # 1. resolve kexts
    update_job(job_id, status="building", progress=10)
    kexts = resolve_kexts(spec)

    # 2. config
    update_job(job_id, progress=40)
    config_path = os.path.join(job_path, "config.plist")
    generate_config(spec, kexts, config_path)

    # 3. EFI
    update_job(job_id, progress=70)
    efi_path = os.path.join(job_path, "EFI")
    build_efi_structure(efi_path, kexts, config_path)

    # 4. zip
    update_job(job_id, progress=90)
    zip_path = os.path.join(job_path, "efi.zip")
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', efi_path)

    update_job(job_id, status="done", progress=100, result=zip_path)
