# lead_scoring_api.py

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load trained model and encoder
model = joblib.load("model.joblib")
encoder = joblib.load("encoder.joblib")

@app.route("/")
def home():
    return "Lead Scoring API is live!"

@app.route("/score-lead", methods=["POST"])
def score_lead():
    try:
        # Get JSON input
        data = request.get_json()

        # Extract relevant fields
        input_df = pd.DataFrame([{
            "Industry": data.get("Industry"),
            "Title": data.get("Title"),
            "LeadSource": data.get("LeadSource")
        }])

        # Transform using the trained encoder
        input_encoded = encoder.transform(input_df)

        # Predict with trained model
        prediction = model.predict(input_encoded)[0]

        # Convert prediction to category
        score = int(prediction)
        category = "Hot" if score == 1 else "Cold"

        # Return result
        return jsonify({"score": score, "category": category})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

