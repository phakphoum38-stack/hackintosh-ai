import os
import torch
from core.model import BootModel

MODEL_PATH = "models/latest.pth"

def load_latest_model():

    model = BootModel()

    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH))

    model.eval()

    return model
