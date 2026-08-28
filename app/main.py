import requests

url = "http://localhost:11434/api/generate"

data = {
    "model": "codellama",
    "prompt": "What is a university?",
    "stream": False
}

response = requests.post(url, json=data)

result = response.json()

print(result["response"])