import os
import pickle
import pytest
import requests
from score import score
from auxilary import simple_split


def test_score():
    """Unit test for the score function."""
    # Load trained model
    with open("svm.pkl", "rb") as file:
        model = pickle.load(file)

    # Smoke test: Ensure function runs without crashing
    text = "This is a test message."
    threshold = 0.5
    prediction, propensity = score(text, model, threshold)
    prediction,propensity = bool(prediction),float(propensity)

    # Format test
    assert isinstance(prediction, bool), "Prediction should be a boolean."
    assert isinstance(propensity, float), "Propensity should be a float."
    
    # Value constraints
    assert 0 <= propensity <= 1, "Propensity score should be between 0 and 1."
    assert prediction in [True, False], "Prediction should be either True or False."
    
    # Edge cases
    assert score(text, model, 0)[0] == True, "Threshold 0 should always return True."
    assert score(text, model, 1)[0] == False, "Threshold 1 should always return False."
    
    # Obvious spam/non-spam cases
    assert score("Win a free iPhone now!!!", model, 0.5)[0] == True, "Spam text should return 1."
    assert score("Hello, how are you today?", model, 0.5)[0] == False, "Non-spam text should return 0."

if __name__ == "__main__":
    test_score()



##
import time
import subprocess
import requests

def test_flask():
    """Integration test for the Flask app."""
    # Launch the Flask app in the background
    process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a bit to ensure the server starts
    time.sleep(2)

    try:
        # Send a POST request to the /score endpoint
        url = "http://127.0.0.1:5000/score"
        payload = {"text": "You won 10k for free. Press the below link to get it.", "threshold": 0.5}
        response = requests.post(url, json=payload)
        
        # Check response format
        assert response.status_code == 200, "Expected status code 200"
        data = response.json()
        assert "prediction" in data, "Response missing 'prediction'"
        assert "propensity" in data, "Response missing 'propensity'"
        assert isinstance(data["prediction"], bool), "Prediction must be boolean"
        assert 0 <= data["propensity"] <= 1, "Propensity must be between 0 and 1"

    finally:
        # Terminate the Flask app
        process.terminate()
        process.wait()
