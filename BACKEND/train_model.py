import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Identify symptom columns
sym_cols = [c for c in df.columns if c.lower().startswith("symptom")]

# Clean symptom text: strip, lowercase, replace spaces with underscore
for c in sym_cols:
    df[c] = df[c].astype(str).str.strip().str.lower().str.replace(" ", "_")

# Replace 'nan' strings (from astype str) with empty
df[sym_cols] = df[sym_cols].replace("nan", "")

# Target
y = df["Disease"].astype(str).str.strip()

# Features: symptom columns only
X_raw = df[sym_cols]

# One-hot encode the symptom categories
X = pd.get_dummies(X_raw)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Save model + feature names
joblib.dump(model, "model.pkl")
joblib.dump(X.columns.tolist(), "features.pkl")

print("✅ Model trained successfully!")
print("Features:", len(X.columns))
