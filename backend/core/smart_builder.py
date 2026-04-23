# backend/core/smart_builder.py

from core.infer import predict
from builder.efi_builder import build_efi
from core.dataset import save_sample

def smart_build(config):

    # 🧠 ML prediction
    prediction = predict(config)

    # ⚙️ tuning decision
    if prediction["boot_success_probability"] < 50:
        config["mode"] = "safe_mode"
        config["acpi_tuning"] = "aggressive_patch"
    else:
        config["mode"] = "optimized"
        config["acpi_tuning"] = "native"

    # 🖥️ build EFI
    efi = build_efi(config)

    # 📊 IMPORTANT: write back to dataset (THIS WAS MISSING)
    save_sample(
        features=[
            config.get("acpi_score", 50) / 100,
            config.get("gpu_score", 50) / 100,
            config.get("usb_score", 50) / 100
        ],
        label=1 if prediction["boot_success_probability"] > 50 else 0
    )

    return {
        "efi": efi,
        "prediction": prediction
    }
