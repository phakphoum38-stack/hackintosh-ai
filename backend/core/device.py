import torch
import platform

def get_device():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("DEVICE:", device)
    print("CPU:", platform.processor())
    return device
