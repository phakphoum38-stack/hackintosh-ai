def normalize_hardware(hw: dict):
    return {
        "cpu": hw.get("cpu", "").lower(),
        "gpu": hw.get("gpu", "").lower(),
        "wifi": hw.get("wifi", "").lower(),
        "ethernet": hw.get("ethernet", "").lower(),
        "laptop": hw.get("laptop", False)
    }
