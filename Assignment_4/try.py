import requests

url = "http://127.0.0.1:5000/score"
data_json = {"text": "You won 10k for free. Press the below link to get it."}

response = requests.post(url=url, json=data_json)

print("Status Code:", response.status_code)
print("Raw Text Response:", response.text)

try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print(" Response is not valid JSON.")
