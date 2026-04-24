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
            return [], []

        data = json.loads(content)

    # 🔥 รองรับหลาย format กันพัง
    texts = []
    labels = []

    for item in data:
        if isinstance(item, dict):
            if "text" in item and "intent" in item:
                texts.append(item["text"])
                labels.append(item["intent"])

            elif "x" in item and "y" in item:
                texts.append(item["x"])
                labels.append(item["y"])

        elif isinstance(item, list) and len(item) >= 2:
            texts.append(str(item[0]))
            labels.append(str(item[1]))

    return texts, labels
