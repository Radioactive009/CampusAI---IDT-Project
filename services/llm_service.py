import requests


OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL_NAME = "codellama"


def generate_response(question: str) -> str:

    data = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]