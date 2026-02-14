import joblib
import numpy as np

model = joblib.load("model.pkl")
feature_names = joblib.load("features.pkl")

feature_set = set(feature_names)

def _clean(sym: str) -> str:
    return str(sym).strip().lower().replace(" ", "_")

def predict_disease(symptom_list):
    x = np.zeros(len(feature_names), dtype=int)

    cleaned = [_clean(s) for s in symptom_list if str(s).strip()]
    # For each cleaned symptom, activate any feature that ends with "_<symptom>"
    # Example feature: "Symptom_3_abdominal_pain"
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
