import json
import os


RESULTS_DIR = "evaluation/results"


def load_json(filename):

    path = os.path.join(
        RESULTS_DIR,
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    quality = load_json(
        "quality_summary.json"
    )

    resource = {}

    resource_path = os.path.join(
        RESULTS_DIR,
        "resource_results.json"
    )

    if os.path.exists(resource_path):

        resource = load_json(
            "resource_results.json"
        )

    report = {}

    for model, values in quality.items():

        report[model] = {
            "questions": values["questions"],
            "accuracy_percent": values["accuracy_percent"],
            "hallucination_rate_percent": values[
                "hallucination_rate_percent"
            ],
            "average_similarity": values[
                "average_similarity"
            ],
            "average_latency_seconds": values[
                "average_latency_seconds"
            ],
            "average_total_tokens": values[
                "average_total_tokens"
            ]
        }

    output_path = os.path.join(
        RESULTS_DIR,
        "final_comparison.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2
        )

    print()
    print("=" * 70)
    print("FINAL MODEL COMPARISON")
    print("=" * 70)

    for model, values in report.items():

        print()
        print(model)

        for key, value in values.items():

            print(
                f"{key}: {value}"
            )

    print()
    print(
        f"Saved to: {output_path}"
    )


if __name__ == "__main__":
    main()