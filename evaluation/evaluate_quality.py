import json
import glob
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


RESULTS_DIR = "evaluation/results"

MODEL = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def calculate_similarity(expected, actual):

    embeddings = MODEL.encode(
        [expected, actual]
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)


def classify(score):

    if score >= 0.75:
        return "correct"

    elif score >= 0.55:
        return "partially_correct"

    else:
        return "incorrect"


def evaluate_file(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    for item in data:

        if item.get("error"):
            item["similarity_score"] = 0
            item["quality"] = "incorrect"
            item["hallucination"] = True
            continue

        expected = item["expected_answer"]
        actual = item["answer"]

        score = calculate_similarity(
            expected,
            actual
        )

        item["similarity_score"] = round(
            score,
            4
        )

        item["quality"] = classify(score)

        item["hallucination"] = score < 0.55

    return data


def summarize(data):

    total = len(data)

    correct = sum(
        1
        for x in data
        if x["quality"] == "correct"
    )

    partial = sum(
        1
        for x in data
        if x["quality"] == "partially_correct"
    )

    incorrect = sum(
        1
        for x in data
        if x["quality"] == "incorrect"
    )

    hallucinations = sum(
        1
        for x in data
        if x["hallucination"]
    )

    accuracy = correct / total * 100

    hallucination_rate = (
        hallucinations / total * 100
    )

    avg_similarity = sum(
        x["similarity_score"]
        for x in data
    ) / total

    avg_latency = sum(
        x["latency_seconds"]
        for x in data
        if x["latency_seconds"] is not None
    ) / total

    avg_tokens = sum(
        x["total_tokens"]
        for x in data
    ) / total

    return {
        "questions": total,
        "correct": correct,
        "partially_correct": partial,
        "incorrect": incorrect,
        "accuracy_percent": round(
            accuracy,
            2
        ),
        "hallucination_rate_percent": round(
            hallucination_rate,
            2
        ),
        "average_similarity": round(
            avg_similarity,
            4
        ),
        "average_latency_seconds": round(
            avg_latency,
            2
        ),
        "average_total_tokens": round(
            avg_tokens,
            2
        )
    }


def main():

    summary = {}

    files = glob.glob(
        os.path.join(
            RESULTS_DIR,
            "*_results.json"
        )
    )

    for filepath in files:

        model_name = os.path.basename(
            filepath
        ).replace(
            "_results.json",
            ""
        )

        print(
            f"Evaluating {model_name}..."
        )

        data = evaluate_file(
            filepath
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

        summary[model_name] = summarize(
            data
        )

    summary_file = (
        "evaluation/results/"
        "quality_summary.json"
    )

    with open(
        summary_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=2
        )

    print()
    print("=" * 60)
    print("QUALITY EVALUATION COMPLETE")
    print("=" * 60)

    for model, result in summary.items():

        print()
        print(model)

        print(
            "Accuracy:",
            result["accuracy_percent"],
            "%"
        )

        print(
            "Hallucination:",
            result["hallucination_rate_percent"],
            "%"
        )

        print(
            "Similarity:",
            result["average_similarity"]
        )

        print(
            "Latency:",
            result["average_latency_seconds"],
            "seconds"
        )

        print(
            "Tokens:",
            result["average_total_tokens"]
        )


if __name__ == "__main__":
    main()