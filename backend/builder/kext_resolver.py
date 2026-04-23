def resolve_kexts(config):

    cpu = config.get("cpu", "")
    gpu = config.get("gpu", "")

    kexts = ["Lilu.kext", "VirtualSMC.kext"]

    if "Intel" in gpu:
        kexts.append("WhateverGreen.kext")

    if "AMD" in gpu:
        kexts.append("NootedRed.kext")

    return kexts
