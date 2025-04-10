import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score

from flask import Flask, request, jsonify
import pickle
from score import score 
from auxilary import simple_split #simple_split is used in vectorizer
import numpy as np

app = Flask(__name__)

# Load model and vectorizer once at startup

with open("svm.pkl", "rb") as file:
    model = pickle.load(file)
with open("custom_vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

@app.route("/score", methods=["POST"])
def score_():
    """API endpoint for scoring text input."""
    data = request.get_json()
    text = data.get("text", "")
    threshold = data.get("threshold", 0.5)  # Default threshold 0.5
    
    # Score the text
    prediction, propensity = score(text, model, threshold)
    
    return jsonify({
    "prediction": bool(prediction),
    "propensity": float(propensity) if isinstance(propensity, np.generic) else propensity
})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000,debug=True)
