import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# Sample dataset (feel free to replace with real data)
data = {
    "temperature": [24, 28, 30, 32, 25, 27, 29, 31],
    "humidity": [50, 60, 55, 65, 52, 58, 61, 67],
    "light_level": [300, 200, 150, 100, 320, 180, 160, 90],
    "sound_level": [40, 45, 50, 55, 42, 48, 53, 58],
    "motion": [1, 1, 1, 1, 0, 0, 1, 1],
    "light": [1, 1, 1, 0, 1, 0, 0, 0]  # target output
}
df = pd.DataFrame(data)

# Features & label
X = df[["temperature", "humidity", "light_level", "sound_level", "motion"]]
y = df["light"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Export the model
dump(model, "light.pkl")
print("✅ light.pkl saved successfully!")
