from services.rag_service import generate_rag_response


questions = [
    "What is the minimum attendance required for semester-end examinations?",
    "Can I get attendance condonation if I have 68% attendance?",
    "Can I apply for examination revaluation?",
    "What is the hostel entry deadline?",
    "How do I register for campus placements?"
]


for question in questions:

    print("\n")
    print("=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    result = generate_rag_response(
        question,
        top_k=3
    )

    print("\nANSWER:")
    print(result["answer"])

    print("\nRETRIEVED CONTEXT:")
    print(result["context"][:1000])