import json
import os
import time
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = [
    "codellama",
    "phi",
    "starcoder2:3b"
]

DATASET_FILE = "evaluation/evaluation_dataset.json"
RESULTS_DIR = "evaluation/results"


def load_dataset():
    with open(DATASET_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_response(model, question):

    payload = {
        "model": model,
        "prompt": question,
        "stream": False
    }

    start_time = time.perf_counter()

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    end_time = time.perf_counter()

    response.raise_for_status()

    result = response.json()

    latency = end_time - start_time

    return {
        "answer": result.get("response", ""),
        "latency_seconds": round(latency, 3),
        "prompt_tokens": result.get("prompt_eval_count", 0),
        "response_tokens": result.get("eval_count", 0),
        "total_tokens": (
            result.get("prompt_eval_count", 0)
            + result.get("eval_count", 0)
        )
    }


def evaluate_model(model, dataset):

    results = []

    print()
    print("=" * 60)
    print(f"Evaluating model: {model}")
    print("=" * 60)

    for index, item in enumerate(dataset, start=1):

        print(
            f"[{index}/{len(dataset)}] "
            f"Question {item['id']}"
        )

        try:

            output = generate_response(
                model,
                item["question"]
            )

            result = {
                "id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "expected_answer": item["expected_answer"],
                "model": model,
                "answer": output["answer"],
                "latency_seconds": output["latency_seconds"],
                "prompt_tokens": output["prompt_tokens"],
                "response_tokens": output["response_tokens"],
                "total_tokens": output["total_tokens"],
                "error": None
            }

        except Exception as error:

            result = {
                "id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "expected_answer": item["expected_answer"],
                "model": model,
                "answer": "",
                "latency_seconds": None,
                "prompt_tokens": 0,
                "response_tokens": 0,
                "total_tokens": 0,
                "error": str(error)
            }

        results.append(result)

    return results


def save_results(model, results):

    filename = model.replace(":", "_") + "_results.json"

    filepath = os.path.join(
        RESULTS_DIR,
        filename
    )

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print(f"Results saved to: {filepath}")


def main():

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    dataset = load_dataset()

    print(
        f"Loaded {len(dataset)} evaluation questions."
    )

    for model in MODELS:

        results = evaluate_model(
            model,
            dataset
        )

        save_results(
            model,
            results
        )

    print()
    print("=" * 60)
    print("ALL MODEL EVALUATIONS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()