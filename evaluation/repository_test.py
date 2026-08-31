import json
import requests


API_URL = "http://127.0.0.1:8000/ask"

OUTPUT_FILE = "evaluation/results/repository_test_results.json"


QUESTIONS = [
    "What component receives the user's question first, and what services does it communicate with afterward?",
    "How does the application service communicate with the retrieval service?",
    "How does the application service communicate with the LLM service?",
    "What is the complete flow of a user question from the application API to the final LLM response?",
    "Which component is responsible for communicating with Ollama?",
    "Which component performs vector similarity search?",
    "How does the retrieval service obtain relevant university information?",
    "What happens if the LLM service is unavailable?",
    "What happens if the retrieval service is unavailable?",
    "Which Docker services are required for the complete CampusAI application?"
]


def main():

    results = []

    for i, question in enumerate(
        QUESTIONS,
        start=1
    ):

        print(
            f"[{i}/{len(QUESTIONS)}] {question}"
        )

        try:

            response = requests.post(
                API_URL,
                json={
                    "question": question
                },
                timeout=300
            )

            data = response.json()

            result = {
                "id": i,
                "question": question,
                "status_code": response.status_code,
                "answer": data.get(
                    "answer",
                    ""
                ),
                "sources": data.get(
                    "sources",
                    []
                ),
                "error": None
            }

        except Exception as error:

            result = {
                "id": i,
                "question": question,
                "status_code": None,
                "answer": "",
                "sources": [],
                "error": str(error)
            }

        results.append(result)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print(
        "Repository test results saved to:"
    )
    print(
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()