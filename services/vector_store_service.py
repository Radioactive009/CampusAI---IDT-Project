import faiss
import numpy as np
import pickle
from pathlib import Path


VECTOR_STORE_DIR = Path(__file__).resolve().parent.parent / "data" / "vector_store"

INDEX_PATH = VECTOR_STORE_DIR / "index.faiss"
METADATA_PATH = VECTOR_STORE_DIR / "metadata.pkl"


def create_vector_store(embeddings, chunks):

    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    with open(METADATA_PATH, "wb") as file:
        pickle.dump(chunks, file)

    return index