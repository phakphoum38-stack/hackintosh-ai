from core.infer import predict
from builder.efi_builder import build_efi

def run_ai(config):

    prediction = predict(config)

    efi = build_efi(config)

    return {
        "prediction": prediction,
        "efi": efi
    }
