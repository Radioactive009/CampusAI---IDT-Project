from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to CampusAI"
    }


@app.get("/ask")
def ask(question: str):

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "codellama",
        "prompt": question,
        "stream": False
    }

    response = requests.post(url, json=data)

    result = response.json()

    return {
        "question": question,
        "answer": result["response"]
    }