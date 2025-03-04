from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with Flask

# Load trained model
model = joblib.load("ids_model.pkl")

@app.route("/", methods=["GET"])
def home():
    return "🚀 AI IDS Running!"

@app.route("/detect", methods=["POST"])  # ✅ Ensure only POST method is allowed
def detect():
    """Receives packet details, predicts intrusion."""
    try:
        data = request.get_json()  # ✅ Ensure request data is JSON
        length = data.get("length")
        protocol = data.get("protocol")

        if length is None or protocol is None:
            return jsonify({"error": "Missing input fields"}), 400

        # Convert input into DataFrame (Fixes sklearn warning)
        input_data = pd.DataFrame([[length, protocol]], columns=["length", "protocol"])

        # Make prediction
        prediction = model.predict(input_data)[0]
        result = "⚠️ Intrusion Detected!" if prediction == 1 else "✔️ Normal Traffic"

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # ✅ Return error message

if __name__ == "__main__":
    app.run(debug=True)
