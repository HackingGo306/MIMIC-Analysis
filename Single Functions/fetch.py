import requests
import json

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{\n  "model": "llama3",\n  "messages": [\n    { "role": "user", "content": "What are God Particles?" }\n  ],\n  "stream": false\n}'

response = requests.post('http://localhost:11434/api/chat', headers=headers, data=data)

# print(response.text)
obj = json.loads(response.text)
print(obj["message"]['content'])