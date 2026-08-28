import faiss
import pickle
import numpy as np
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

    index = faiss.read_index(
        str(INDEX_PATH)
    )

    with open(METADATA_PATH, "rb") as file:
        chunks = pickle.load(file)

    return index, chunks


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3
):

    index, chunks = load_vector_store()

    query_embedding = generate_embeddings(
        [question]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_id in zip(
        distances[0],
        indices[0]
    ):

        if index_id == -1:
            continue

        results.append({
            "chunk": chunks[index_id],
            "distance": float(distance)
        })

    return results