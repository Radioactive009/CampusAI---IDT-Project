from services.retrieval_service import retrieve_relevant_chunks
from services.llm_service import generate_response


def generate_rag_response(question: str, top_k: int = 3):

    results = retrieve_relevant_chunks(
        question,
        top_k=top_k
    )

    context_parts = []
    sources = []
    retrieved_chunks = []

    for result in results:

        chunk = result["chunk"]
        distance = result["distance"]

        context_parts.append(
            f"Source: {chunk['filename']}\n"
            f"{chunk['text']}"
        )

        if chunk["filename"] not in sources:
            sources.append(chunk["filename"])

        retrieved_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "filename": chunk["filename"],
            "distance": distance,
            "text": chunk["text"]
        })

    context = "\n\n".join(context_parts)

    prompt = f"""
You are CampusAI, an assistant for ABC University.

Answer the user's question using the provided university context.

Rules:
- Use the provided context as the primary source of information.
- Do not invent university policies.
- If the answer cannot be found in the context, say that the
  information is not available in the university knowledge base.
- Keep the answer clear and concise.

University Context:
{context}

User Question:
{question}

Answer:
"""

    answer = generate_response(prompt)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks
    }