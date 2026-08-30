import requests


OLLAMA_URL = "http://host.docker.internal:11434/api/generate"


def generate_response(question: str, model: str = "codellama") -> str:

    data = {
        "model": model,
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