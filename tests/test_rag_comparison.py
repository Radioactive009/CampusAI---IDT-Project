from services.llm_service import generate_response
from services.rag_service import generate_rag_response


questions = [
    "What is the minimum attendance required for semester-end examinations?",
    "Can I get attendance condonation if I have 68% attendance?",
    "What is the hostel entry deadline?",
    "How do I register for campus placements?"
]


for question in questions:

    print("\n")
    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    # -----------------------------------------
    # WITHOUT RAG
    # -----------------------------------------

    print("\n")
    print("-" * 80)
    print("WITHOUT RAG")
    print("-" * 80)

    normal_answer = generate_response(question)

    print(normal_answer)

    # -----------------------------------------
    # WITH RAG
    # -----------------------------------------

    print("\n")
    print("-" * 80)
    print("WITH RAG")
    print("-" * 80)

    rag_result = generate_rag_response(
        question,
        top_k=3
    )

    print(rag_result["answer"])

    # -----------------------------------------
    # RETRIEVED CONTEXT
    # -----------------------------------------

    print("\n")
    print("-" * 80)
    print("RETRIEVED CONTEXT")
    print("-" * 80)

    print(rag_result["context"][:1000])