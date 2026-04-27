def resolve_kexts(config: dict):
    cpu = config.get("cpu", "").lower()
    gpu = config.get("gpu", "").lower()
    wifi = config.get("wifi", "").lower()
    ethernet = config.get("ethernet", "").lower()
    laptop = config.get("laptop", False)

    kexts = set()

    # =========================
    # 🧱 Core (ต้องมี)
    # =========================
    kexts.update([
        "Lilu.kext",
        "VirtualSMC.kext",
        "SMCProcessor.kext",
        "SMCSuperIO.kext",
        "WhateverGreen.kext"
    ])

    # =========================
    # 💻 Laptop only
    # =========================
    if laptop:
        kexts.add("SMCBatteryManager.kext")

    # =========================
    # 🧠 CPU (AMD Fix)
    # =========================
    if "amd" in cpu:
        kexts.add("AppleMCEReporterDisabler.kext")

    # =========================
    # 🎮 GPU
    # =========================
    if "amd apu" in gpu or "vega" in gpu:
        # AMD iGPU (Ryzen APU)
        kexts.add("NootedRed.kext")

    # Intel iGPU → WhateverGreen พอแล้ว

    # =========================
    # 📶 WIFI
    # =========================
    if "intel" in wifi:
        # เลือกตาม macOS version ภายนอก
        kexts.add("AirportItlwm.kext")

    elif "broadcom" in wifi:
        kexts.update([
            "AirportBrcmFixup.kext",
            "BrcmPatchRAM3.kext",
            "BrcmFirmwareData.kext"
        ])

    # =========================
    # 🌐 Ethernet
    # =========================
    if "realtek" in ethernet:
        kexts.add("RealtekRTL8111.kext")

    elif "intel" in ethernet:
        kexts.add("IntelMausi.kext")

    # =========================
    # 🔊 Audio
    # =========================
    kexts.add("AppleALC.kext")

    # =========================
    # 🔌 USB
    # =========================
    kexts.update([
        "USBToolBox.kext",
        "UTBMap.kext"
    ])

    return sorted(list(kexts))
