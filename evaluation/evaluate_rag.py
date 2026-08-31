import json
import os
import requests


RAG_URL = "http://127.0.0.1:8000/ask"

DATASET_FILE = "evaluation/evaluation_dataset.json"

OUTPUT_FILE = (
    "evaluation/results/rag_results.json"
)


def load_dataset():

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def ask_rag(question):

    response = requests.post(
        RAG_URL,
        json={
            "question": question
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()


def main():

    dataset = load_dataset()

    results = []

    for index, item in enumerate(
        dataset,
        start=1
    ):

        print(
            f"[{index}/{len(dataset)}] "
            f"{item['question']}"
        )

        try:

            result = ask_rag(
                item["question"]
            )

            results.append(
                {
                    "id": item["id"],
                    "category": item["category"],
                    "question": item["question"],
                    "expected_answer": item[
                        "expected_answer"
                    ],
                    "answer": result.get(
                        "answer",
                        ""
                    ),
                    "sources": result.get(
                        "sources",
                        []
                    ),
                    "retrieved_chunks": result.get(
                        "retrieved_chunks",
                        []
                    ),
                    "error": None
                }
            )

        except Exception as error:

            results.append(
                {
                    "id": item["id"],
                    "category": item["category"],
                    "question": item["question"],
                    "expected_answer": item[
                        "expected_answer"
                    ],
                    "answer": "",
                    "sources": [],
                    "retrieved_chunks": [],
                    "error": str(error)
                }
            )

    os.makedirs(
        "evaluation/results",
        exist_ok=True
    )

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
        "RAG evaluation complete."
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()