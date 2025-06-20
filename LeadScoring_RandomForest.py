import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load & prepare data
df = pd.read_csv("leads.csv")
X = df[["Industry", "Title", "LeadSource"]]
y = df["Converted"]

# Encode categorical variables
encoder = OneHotEncoder(handle_unknown='ignore')
X_encoded = encoder.fit_transform(X)

# Train model
model = RandomForestClassifier()
model.fit(X_encoded, y)

# Save model & encoder
joblib.dump(model, "model.joblib")
joblib.dump(encoder, "encoder.joblib")
