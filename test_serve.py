import requests
import json

url = "http://localhost:13121/chat"

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
print(1)
response = requests.post(url, headers=headers, data=json.dumps(data))
print(2)
response_json = response.json()
print(3)
print(response_json)