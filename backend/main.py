from backend.core.hardware_scanner import scan_hardware
from backend.core.cpu_patch import patch_cpu
from backend.core.gpu_patch import patch_gpu
from backend.core.config_generator import generate_config
from backend.core.efi_builder import build_efi
from core.cpu_patch import patch_cpu
from core.gpu_patch import patch_gpu
from core.config_generator import generate_config
from core.efi_builder import build_efi

def main():

    print("🚀 Hackintosh AI Builder")

    hardware = scan_hardware()

    cpu_patch = patch_cpu(hardware)
    gpu_patch = patch_gpu(hardware)

    config = generate_config(
        hardware,
        cpu_patch,
        gpu_patch
    )

    build_efi(config)

    print("✅ EFI CREATED")

if __name__ == "__main__":
    main()
