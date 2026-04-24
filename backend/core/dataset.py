import json
import os

def load_dataset():

    path = "database/boot_dataset.json"

    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Dataset not found: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("❌ Dataset must be a list of samples")

    # -----------------------------
    # validate แต่ละ sample
    # -----------------------------
    cleaned = []

    for i, d in enumerate(data):

        if "x" not in d or "y" not in d:
            print(f"⚠️ skip index {i}: missing x or y")
            continue

        x = d["x"]
        y = d["y"]

        if x is None or len(x) == 0:
            print(f"⚠️ skip index {i}: empty x")
            continue

        cleaned.append({
            "x": x,
            "y": y
        })

    if len(cleaned) == 0:
        raise ValueError("❌ All dataset entries invalid")

    print(f"✅ Loaded dataset: {len(cleaned)} samples")

    return cleaned
