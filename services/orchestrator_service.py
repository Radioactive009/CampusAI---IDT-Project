from services.retrieval_client import retrieve_from_service
from services.llm_client import generate_with_llm_service


def process_question(
    question: str,
    top_k: int = 3
):

    # Step 1: Retrieve relevant information
    retrieval_results = retrieve_from_service(
        question,
        top_k
    )

    # Step 2: Build context
    context_parts = []
    sources = []

    for result in retrieval_results:

        chunk = result["chunk"]

        context_parts.append(
            f"Source: {chunk['filename']}\n"
            f"{chunk['text']}"
        )

        if chunk["filename"] not in sources:
            sources.append(chunk["filename"])

    context = "\n\n".join(context_parts)

    # Step 3: Build LLM prompt
    prompt = f"""
You are CampusAI, an assistant for ABC University.

Answer the user's question using the university context below.

Rules:
- Use the provided context as the primary source.
- Do not invent university policies.
- If the answer is not available in the context,
  say that the information is not available
  in the university knowledge base.
- Keep the answer clear and concise.

University Context:
{context}

User Question:
{question}

Answer:
"""

    # Step 4: Send prompt to LLM Service
    answer = generate_with_llm_service(
        prompt
    )

    # Step 5: Return final result
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieval_results
    }