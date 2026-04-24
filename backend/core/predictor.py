import joblib

vectorizer = joblib.load("backend/model/vectorizer.pkl")
model = joblib.load("backend/model/intent_model.pkl")

def predict(text: str):
    X = vectorizer.transform([text])
    intent = model.predict(X)[0]
    return intent
