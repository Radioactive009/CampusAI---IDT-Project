from services.retrieval_service import retrieve_relevant_chunks


questions = [
    "What is the minimum attendance required?",
    "Can I get attendance condonation with 68% attendance?",
    "Can students apply for examination revaluation?",
    "What is the hostel entry deadline?",
    "How do students register for campus placements?"
]


for question in questions:

    print("\n========================================")
    print(f"QUESTION: {question}")
    print("========================================")

    results = retrieve_relevant_chunks(
        question,
        top_k=3
    )

    for i, result in enumerate(results, start=1):

        chunk = result["chunk"]

        print(f"\nResult {i}")
        print(f"Distance: {result['distance']}")
        print(f"Source: {chunk['filename']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Text: {chunk['text'][:300]}")