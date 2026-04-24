import json
import os

def load_dataset():

    path = "database/boot_dataset.json"

    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    cleaned = []

    for i, d in enumerate(data):

        if "x" not in d or "y" not in d:
            continue

        x = list(d["x"])

        # 🔥 บังคับให้มี 3 ค่า
        if len(x) < 3:
            x += [0] * (3 - len(x))   # pad
        else:
            x = x[:3]                # ตัดให้เหลือ 3

        cleaned.append({
            "x": x,
            "y": d["y"]
        })

    return cleaned
