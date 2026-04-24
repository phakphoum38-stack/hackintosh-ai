import json
import os

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "dataset.json"
)

def load_dataset():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

        if not content:
            return []

        data = json.loads(content)

    # แปลงเป็น X, y สำหรับ training
    texts = [item["text"] for item in data]
    labels = [item["intent"] for item in data]

    return texts, labels
