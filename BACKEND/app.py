from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from model import predict_disease

app = Flask(__name__)
CORS(app)

# Load dataset once to serve symptoms
df = pd.read_csv("dataset.csv")
sym_cols = [c for c in df.columns if c.lower().startswith("symptom")]

def get_all_symptoms():
    s = set()
    for col in sym_cols:
        s.update(df[col].dropna().astype(str).str.strip().str.lower().tolist())
    s.discard("")
    s.discard("nan")
    # Convert underscores/format
    return sorted([x.replace("_", " ") for x in s])

ALL_SYMPTOMS = get_all_symptoms()

@app.route("/symptoms", methods=["GET"])
def symptoms():
    return jsonify({"symptoms": ALL_SYMPTOMS})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or {}
        symptoms = data.get("symptoms", [])

        if not isinstance(symptoms, list) or len(symptoms) == 0:
            return jsonify({"error": "No symptoms provided"}), 400

        prediction, confidence = predict_disease(symptoms)

        response = {
            "prediction": str(prediction),
            "confidence": float(confidence),
            "severity": "High" if confidence >= 70 else "Moderate",
            "precautions": [
                "Stay hydrated",
                "Get adequate rest",
                "Monitor symptoms",
                "Consult a doctor if condition worsens"
            ]
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
