import json


INPUT_FILE = "evaluation/results/rag_results.json"
OUTPUT_FILE = "evaluation/results/rag_analysis.json"


def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    analysis = []

    for item in data:

        retrieved_text = " ".join(
            chunk["chunk"]["text"]
            for chunk in item.get(
                "retrieved_chunks",
                []
            )
            if "chunk" in chunk
        ).lower()

        expected = item[
            "expected_answer"
        ].lower()

        # Simple keyword coverage measurement
        expected_words = set(
            word.strip(
                ".,!?;:"
            )
            for word in expected.split()
            if len(word) > 4
        )

        matched_words = sum(
            1
            for word in expected_words
            if word in retrieved_text
        )

        if expected_words:

            context_coverage = (
                matched_words
                / len(expected_words)
                * 100
            )

        else:

            context_coverage = 0

        if context_coverage >= 50:

            retrieval_quality = "relevant"

        elif context_coverage >= 25:

            retrieval_quality = "partially_relevant"

        else:

            retrieval_quality = "poor"

        analysis.append(
            {
                "id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "sources": item.get(
                    "sources",
                    []
                ),
                "retrieved_chunks_count": len(
                    item.get(
                        "retrieved_chunks",
                        []
                    )
                ),
                "context_coverage_percent": round(
                    context_coverage,
                    2
                ),
                "retrieval_quality":
                    retrieval_quality,
                "answer": item.get(
                    "answer",
                    ""
                ),
                "expected_answer":
                    item["expected_answer"]
            }
        )

    relevant = sum(
        1
        for x in analysis
        if x["retrieval_quality"]
        == "relevant"
    )

    partial = sum(
        1
        for x in analysis
        if x["retrieval_quality"]
        == "partially_relevant"
    )

    poor = sum(
        1
        for x in analysis
        if x["retrieval_quality"]
        == "poor"
    )

    total = len(analysis)

    summary = {
        "total_questions": total,
        "relevant_retrievals": relevant,
        "partially_relevant_retrievals": partial,
        "poor_retrievals": poor,
        "retrieval_relevance_percent":
            round(
                relevant / total * 100,
                2
            )
    }

    output = {
        "summary": summary,
        "questions": analysis
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 60)
    print("RAG ANALYSIS COMPLETE")
    print("=" * 60)

    print(
        "Total questions:",
        total
    )

    print(
        "Relevant:",
        relevant
    )

    print(
        "Partially relevant:",
        partial
    )

    print(
        "Poor:",
        poor
    )

    print(
        "Retrieval relevance:",
        summary[
            "retrieval_relevance_percent"
        ],
        "%"
    )


if __name__ == "__main__":
    main()