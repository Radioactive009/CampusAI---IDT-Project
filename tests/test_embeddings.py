from services.document_service import load_documents
from services.chunking_service import create_document_chunks
from services.embedding_service import generate_embeddings


documents = load_documents()

chunks = create_document_chunks(documents)

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(texts)

print(f"Number of chunks: {len(chunks)}")
print(f"Number of embeddings: {len(embeddings)}")
print(f"Embedding dimension: {embeddings.shape[1]}")

print("\nFirst chunk:")
print(chunks[0]["text"])

print("\nFirst embedding:")
print(embeddings[0])