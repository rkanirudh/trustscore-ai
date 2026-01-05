import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

print("🔄 Starting anomaly model training...")

DATA_PATH = os.path.join("data", "fraud.csv")
MODEL_PATH = os.path.join("model", "anomaly_model.pkl")

# Load dataset
df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded dataset with shape: {df.shape}")

# 🔍 ADD THIS LINE HERE
print("📊 Columns:", df.columns.tolist())

# Select correct numeric column
numeric_cols = ["Amount"]
df = df[numeric_cols].dropna()

# Train model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df)

# Save model
joblib.dump(model, MODEL_PATH)
print(f"✅ Model successfully saved at: {MODEL_PATH}")
