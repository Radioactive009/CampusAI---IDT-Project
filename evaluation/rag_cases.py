import json


INPUT_FILE = "evaluation/results/rag_analysis.json"


def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    questions = data["questions"]

    relevant = [
        x for x in questions
        if x["retrieval_quality"] == "relevant"
    ]

    partial = [
        x for x in questions
        if x["retrieval_quality"]
        == "partially_relevant"
    ]

    print()
    print("=" * 70)
    print("RAG CASE ANALYSIS")
    print("=" * 70)

    print()
    print("TOTAL QUESTIONS:", len(questions))

    print()
    print("=" * 70)
    print("CASE 1 — RELEVANT RETRIEVAL")
    print("=" * 70)

    if relevant:

        case = relevant[0]

        print(
            "Question:",
            case["question"]
        )

        print(
            "Sources:",
            case["sources"]
        )

        print(
            "Context coverage:",
            case["context_coverage_percent"],
            "%"
        )

        print(
            "Expected:",
            case["expected_answer"]
        )

        print(
            "Answer:",
            case["answer"]
        )

    print()
    print("=" * 70)
    print("CASE 2 — PARTIALLY RELEVANT RETRIEVAL")
    print("=" * 70)

    if partial:

        case = partial[0]

        print(
            "Question:",
            case["question"]
        )

        print(
            "Sources:",
            case["sources"]
        )

        print(
            "Context coverage:",
            case["context_coverage_percent"],
            "%"
        )

        print(
            "Expected:",
            case["expected_answer"]
        )

        print(
            "Answer:",
            case["answer"]
        )

    else:

        print(
            "No partially relevant cases found."
        )


if __name__ == "__main__":
    main()