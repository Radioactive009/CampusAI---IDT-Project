import requests


RETRIEVAL_SERVICE_URL = "http://retrieval-service:8002/retrieve"


def retrieve_from_service(
    question: str,
    top_k: int = 3
):

    response = requests.post(
        RETRIEVAL_SERVICE_URL,
        json={
            "question": question,
            "top_k": top_k
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["results"]