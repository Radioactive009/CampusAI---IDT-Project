import json
import os
import subprocess
import time

import psutil


MODELS = [
    "codellama",
    "phi",
    "starcoder2:3b"
]

QUESTIONS = [
    "What is the minimum attendance required to appear for the semester-end examination?",
    "Can a student with 68% attendance apply for attendance condonation?",
    "How is CGPA calculated?"
]


def run_model(model, question):

    print()
    print("=" * 60)
    print("Model:", model)
    print("Question:", question)

    process = subprocess.Popen(
        [
            "ollama",
            "run",
            model,
            question
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    max_memory = 0
    cpu_samples = []

    while process.poll() is None:

        try:

            cpu = psutil.cpu_percent(
                interval=0.5
            )

            memory = psutil.virtual_memory().percent

            cpu_samples.append(cpu)

            max_memory = max(
                max_memory,
                memory
            )

        except Exception:
            pass

    stdout, stderr = process.communicate()

    return {
        "model": model,
        "cpu_average_percent": round(
            sum(cpu_samples) / len(cpu_samples),
            2
        ) if cpu_samples else None,
        "memory_max_percent": round(
            max_memory,
            2
        ),
        "return_code": process.returncode
    }


def main():

    results = []

    for model in MODELS:

        model_results = []

        for question in QUESTIONS:

            result = run_model(
                model,
                question
            )

            model_results.append(result)

        results.extend(
            model_results
        )

    os.makedirs(
        "evaluation/results",
        exist_ok=True
    )

    with open(
        "evaluation/results/resource_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2
        )

    print()
    print("=" * 60)
    print("RESOURCE MEASUREMENT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()