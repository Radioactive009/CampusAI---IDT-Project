from services.document_service import load_documents
from services.chunking_service import create_document_chunks
from services.embedding_service import generate_embeddings
from services.vector_store_service import create_vector_store


documents = load_documents()

chunks = create_document_chunks(documents)

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(texts)

index = create_vector_store(
    embeddings,
    chunks
)

print(f"Number of chunks: {len(chunks)}")
print(f"Number of vectors in FAISS: {index.ntotal}")
print(f"Vector dimension: {index.d}")