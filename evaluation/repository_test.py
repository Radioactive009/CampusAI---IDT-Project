import json
import requests
from pathlib import Path


API_URL = "http://127.0.0.1:8000/ask"

OUTPUT_FILE = "evaluation/results/repository_test_results.json"


QUESTIONS = [
    # Architecture
    "What component receives the user's question first, and what services does it communicate with afterward?",
    "How does the application service communicate with the retrieval service?",
    "How does the application service communicate with the LLM service?",
    "What is the complete flow of a user question from the application API to the final LLM response?",

    # LLM and Ollama
    "Which component is responsible for communicating with Ollama?",

    # RAG and Retrieval
    "Which component performs vector similarity search?",
    "How does the retrieval service obtain relevant university information?",

    # Error handling
    "What happens if the LLM service is unavailable?",
    "What happens if the retrieval service is unavailable?",

    # Docker / DevOps
    "Which Docker services are required for the complete CampusAI application?",
    "Why is host.docker.internal used in the CampusAI Docker architecture?",

    # Repository / Code understanding
    "What does the process_question function do?",
    "What does retrieve_relevant_chunks do?",
    "What does create_vector_store do?",
    "What is the purpose of chunk_text in the CampusAI pipeline?"
]


def main():

    results = []

    # Make sure output directory exists
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 70)
    print("CAMPUSAI REPOSITORY / DEVOPS EVALUATION")
    print("=" * 70)
    print()

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

            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError:
                data = {}

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
                "retrieved_chunks": data.get(
                    "retrieved_chunks",
                    []
                ),
                "error": None
            }

            # Record HTTP errors
            if response.status_code != 200:
                result["error"] = data.get(
                    "detail",
                    f"HTTP {response.status_code}"
                )

        except requests.exceptions.Timeout:

            result = {
                "id": i,
                "question": question,
                "status_code": None,
                "answer": "",
                "sources": [],
                "retrieved_chunks": [],
                "error": "Request timed out after 300 seconds"
            }

        except requests.exceptions.ConnectionError as error:

            result = {
                "id": i,
                "question": question,
                "status_code": None,
                "answer": "",
                "sources": [],
                "retrieved_chunks": [],
                "error": f"Connection error: {str(error)}"
            }

        except Exception as error:

            result = {
                "id": i,
                "question": question,
                "status_code": None,
                "answer": "",
                "sources": [],
                "retrieved_chunks": [],
                "error": str(error)
            }

        results.append(result)

        # Print quick result
        if result["error"] is None:
            print(
                f"    Status: {result['status_code']} - SUCCESS"
            )
        else:
            print(
                f"    Status: ERROR - {result['error']}"
            )

        print()

    # Save results
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    # Summary
    successful = sum(
        1
        for result in results
        if result["status_code"] == 200
        and result["error"] is None
    )

    failed = len(results) - successful

    print("=" * 70)
    print("REPOSITORY EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"Total questions: {len(results)}"
    )

    print(
        f"Successful: {successful}"
    )

    print(
        f"Failed: {failed}"
    )

    print()
    print(
        "Repository test results saved to:"
    )

    print(
        output_path
    )


if __name__ == "__main__":
    main()