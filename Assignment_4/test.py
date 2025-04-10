import os
import time
import requests
import subprocess

def test_docker():
    # Clean up if container already exists
    subprocess.run("docker rm -f score-container", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step 1: Build Docker image
    subprocess.run("docker build -t flask-score-app .", shell=True, check=True)
    
    # Step 2: Run Docker container
    subprocess.run("docker run -d -p 5000:5000 --name score-container flask-score-app", shell=True, check=True)

    try:
        # Step 3: Wait a bit for the container to start
        time.sleep(5)

        # Step 4: Send request to /score endpoint
        response = requests.post("http://localhost:5000/score", json={"text": "This is a test"})

        # Assertions
        assert response.status_code == 200
        assert "score" in response.json()

        print("✅ Docker container test passed!")

    finally:
        # Step 5: Stop and remove the container after test
        subprocess.run("docker stop score-container", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("docker rm score-container", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
