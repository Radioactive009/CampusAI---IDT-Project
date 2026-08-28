from services.document_service import load_documents
from services.chunking_service import create_document_chunks
from services.embedding_service import generate_embeddings
from services.vector_store_service import create_vector_store


def build_knowledge_base():

    print("Loading documents...")
    documents = load_documents()

    print(f"Loaded {len(documents)} documents.")

    print("\nCreating chunks...")
    chunks = create_document_chunks(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\nGenerating embeddings...")
    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    print(f"Generated {len(embeddings)} embeddings.")
    print(f"Embedding dimension: {embeddings.shape[1]}")

    print("\nCreating FAISS vector store...")
    index = create_vector_store(
        embeddings,
        chunks
    )

    print(f"Stored {index.ntotal} vectors in FAISS.")

    print("\nKnowledge base created successfully!")


if __name__ == "__main__":
    build_knowledge_base()