import requests


LLM_SERVICE_URL = "http://127.0.0.1:8001/generate"


def generate_with_llm_service(prompt: str) -> str:

    response = requests.post(
        LLM_SERVICE_URL,
        json={
            "prompt": prompt
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]