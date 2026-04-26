def resolve_kexts(config: dict):
    cpu = config.get("cpu", "").lower()
    gpu = config.get("gpu", "").lower()
    wifi = config.get("wifi", "").lower()
    ethernet = config.get("ethernet", "").lower()

    kexts = set()

    # =========================
    # 🧱 Core (ต้องมีเสมอ)
    # =========================
    kexts.update([
        "Lilu.kext",
        "VirtualSMC.kext",
        "SMCProcessor.kext",
        "SMCSuperIO.kext"
    ])

    # =========================
    # 🎮 GPU
    # =========================
    if "intel" in gpu or "amd" in gpu:
        kexts.add("WhateverGreen.kext")

    # AMD iGPU (เฉพาะบางเคส)
    if "amd" in gpu:
        kexts.add("NootedRed.kext")

    # =========================
    # 📶 WIFI
    # =========================
    if "intel" in wifi:
        kexts.add("AirportItlwm.kext")

    elif "broadcom" in wifi:
        kexts.update([
            "AirportBrcmFixup.kext",
            "BrcmPatchRAM3.kext"
        ])

    # =========================
    # 🌐 Ethernet
    # =========================
    if "realtek" in ethernet:
        kexts.add("RealtekRTL8111.kext")

    elif "intel" in ethernet:
        kexts.add("IntelMausi.kext")

    # =========================
    # 🔊 Audio (default)
    # =========================
    kexts.add("AppleALC.kext")

    # =========================
    # 🧰 USB Fix
    # =========================
    kexts.add("USBToolBox.kext")

    return list(kexts)
