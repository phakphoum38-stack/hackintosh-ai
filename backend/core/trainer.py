from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from backend.core.dataset import load_dataset
import joblib
import os

def train():
    texts, labels = load_dataset()

    print(f"Loaded samples: {len(texts)}")

    if len(texts) == 0:
        print("⚠️ No training data. Exit safely.")
        return

    # กัน mismatch
    if len(texts) != len(labels):
        raise ValueError("Dataset mismatch: texts != labels")

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=1000)
    model.fit(X, labels)

    os.makedirs("backend/model", exist_ok=True)

    joblib.dump(vectorizer, "backend/model/vectorizer.pkl")
    joblib.dump(model, "backend/model/intent_model.pkl")

    print("✅ Training completed successfully")

if __name__ == "__main__":
    train()
