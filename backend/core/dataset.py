import json
import os

DATA_PATH = "database/boot_dataset.json"

def load_dataset():

    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_sample(features, label):

    data = load_dataset()

    data.append({
        "x": features,
        "y": label
    })

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)
