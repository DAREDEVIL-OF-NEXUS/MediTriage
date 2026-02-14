import os
import joblib
import numpy as np
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "features.pkl")

def ensure_model_exists():
    # If model files not found, train them
    if not (os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH)):
        print("⚠ model.pkl / features.pkl not found. Training model now...")
        subprocess.check_call(["python", os.path.join(BASE_DIR, "train_model.py")])
        print("✅ Model trained on server.")

ensure_model_exists()

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURES_PATH)

def _clean(sym: str) -> str:
    return str(sym).strip().lower().replace(" ", "_")

def predict_disease(symptom_list):
    x = np.zeros(len(feature_names), dtype=int)

    cleaned = [_clean(s) for s in symptom_list if str(s).strip()]
    for sym in cleaned:
        suffix = "_" + sym
        for i, fname in enumerate(feature_names):
            if fname.endswith(suffix):
                x[i] = 1

    x = x.reshape(1, -1)
    pred = model.predict(x)[0]

    if hasattr(model, "predict_proba"):
        conf = float(np.max(model.predict_proba(x)[0]) * 100.0)
    else:
        conf = 0.0

    return pred, round(conf, 2)
