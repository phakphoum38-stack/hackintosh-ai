# =========================
# 🚀 BUILD EFI (FIXED)
# =========================
def build_efi(job_id: int, config: dict, user_id: int = None):

    base_path = f"/tmp/efi_build_{job_id}"
    output_zip = f"/tmp/efi_{job_id}.zip"

    try:
        print(f"🧠 Resolving kexts for job {job_id}...")
        kexts = resolve_kexts(config)

        print("⚙️ Generating config.plist...")
        config_path_tmp = generate_config(config, kexts)

        # =========================
        # 🧹 clean old build
        # =========================
        if os.path.exists(base_path):
            shutil.rmtree(base_path)

        create_structure(base_path)

        # =========================
        # 📝 copy config.plist (FIX)
        # =========================
        final_config_path = f"{base_path}/EFI/OC/config.plist"
        shutil.copy(config_path_tmp, final_config_path)

        # =========================
        # 📦 FAKE KEXT (กันพัง)
        # =========================
        kext_dir = f"{base_path}/EFI/OC/Kexts"

        for k in kexts:
            kext_path = os.path.join(kext_dir, k)
            os.makedirs(kext_path, exist_ok=True)

            # สร้าง Info.plist dummy
            info_path = os.path.join(kext_path, "Contents")
            os.makedirs(info_path, exist_ok=True)

            with open(os.path.join(info_path, "Info.plist"), "w") as f:
                f.write("<plist></plist>")

        # =========================
        # 📦 DRIVER placeholder
        # =========================
        drivers_dir = f"{base_path}/EFI/OC/Drivers"

        with open(os.path.join(drivers_dir, "OpenRuntime.efi"), "w") as f:
            f.write("DUMMY")

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
