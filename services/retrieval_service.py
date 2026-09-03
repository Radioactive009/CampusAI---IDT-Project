import faiss
import pickle
import numpy as np
import re
from pathlib import Path

from services.embedding_service import generate_embeddings


VECTOR_STORE_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "vector_store"
)

INDEX_PATH = VECTOR_STORE_DIR / "index.faiss"
METADATA_PATH = VECTOR_STORE_DIR / "metadata.pkl"


def load_vector_store():
    index = faiss.read_index(str(INDEX_PATH))

    with open(METADATA_PATH, "rb") as file:
        chunks = pickle.load(file)

    return index, chunks


def is_repository_question(question: str) -> bool:
    question_lower = question.lower()

    repository_keywords = [
        "code",
        "function",
        "class",
        "method",
        "file",
        "module",
        "api",
        "endpoint",
        "docker",
        "dockerfile",
        "docker compose",
        "container",
        "devops",
        "deployment",
        "repository",
        "source code",
        "implementation",
        "bug",
        "error",
        "exception",
        "refactor",
        "dependency",
        "ollama",
        "faiss",
        "embedding",
        "retrieval service",
        "llm service",
        "application service",
        "process_question",
        "generate_response",
        "generate_with_llm_service",
        "retrieve_relevant_chunks",
    ]

    return any(
        keyword in question_lower
        for keyword in repository_keywords
    )


def extract_code_symbols(question: str):
    """
    Extract identifiers such as:
    process_question
    generate_response
    retrieve_relevant_chunks
    """

    symbols = []

    # Symbols written with ()
    matches = re.findall(
        r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
        question
    )

    for match in matches:
        if len(match) >= 4:
            symbols.append(match.lower())

    # snake_case identifiers
    matches = re.findall(
        r"\b[a-zA-Z_][a-zA-Z0-9_]*_[a-zA-Z0-9_]+\b",
        question
    )

    for match in matches:
        match = match.lower()

        if len(match) >= 4 and match not in symbols:
            symbols.append(match)

    return symbols


def find_symbol_chunks(
    question: str,
    chunks,
    top_k: int
):
    """
    Directly search repository chunks for exact
    function/class symbols before using FAISS.
    """

    symbols = extract_code_symbols(question)

    if not symbols:
        return []

    matches = []

    for chunk in chunks:

        if chunk.get("source_type") != "repository":
            continue

        text = chunk.get("text", "")
        text_lower = text.lower()

        for symbol in symbols:

            # Function definition
            if re.search(
                rf"\bdef\s+{re.escape(symbol)}\s*\(",
                text_lower
            ):
                matches.append({
                    "chunk": chunk,
                    "distance": -10.0
                })
                break

            # Class definition
            if re.search(
                rf"\bclass\s+{re.escape(symbol)}\b",
                text_lower
            ):
                matches.append({
                    "chunk": chunk,
                    "distance": -10.0
                })
                break

    return matches[:top_k]


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3
):
    index, chunks = load_vector_store()

    repository_question = is_repository_question(
        question
    )

    target_source = (
        "repository"
        if repository_question
        else "university"
    )

    # -------------------------------------------------
    # 1. Direct code-symbol lookup
    # -------------------------------------------------
    if repository_question:

        direct_results = find_symbol_chunks(
            question,
            chunks,
            top_k
        )

        if direct_results:
            return direct_results

    # -------------------------------------------------
    # 2. Normal semantic FAISS retrieval
    # -------------------------------------------------
    query_embedding = generate_embeddings(
        [question]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    candidate_k = min(
        max(top_k * 10, 50),
        index.ntotal
    )

    distances, indices = index.search(
        query_embedding,
        candidate_k
    )

    results = []

    for distance, index_id in zip(
        distances[0],
        indices[0]
    ):

        if index_id == -1:
            continue

        chunk = chunks[index_id]

        if chunk.get("source_type") != target_source:
            continue

        results.append({
            "chunk": chunk,
            "distance": float(distance)
        })

    return results[:top_k]