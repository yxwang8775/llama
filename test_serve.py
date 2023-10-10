import requests
import json

url = "http://localhost:5000/chat"

headers = {
    "Content-Type": "application/json"
}

data = {
    "dialogs": [
        [
            {"role": "system", "content": "Always answer with Haiku"},
            {"role": "user", "content": "I am going to Paris, what should I see?"}
        ]
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
response_json = response.json()

print(response_json)