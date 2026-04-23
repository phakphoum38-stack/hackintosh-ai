# backend/core/model_registry.py

import os
import torch
from core.model import BootModel

MODEL_PATH = "models/latest.pth"

def load_latest_model():
    """
    โหลดโมเดลล่าสุด (production safe)
    ถ้าไม่มีไฟล์ จะใช้โมเดลใหม่แทน
    """

    model = BootModel()

    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
        print("✅ Loaded trained model")

    else:
        print("⚠️ No model found, using fresh model")

    model.eval()

    return model
