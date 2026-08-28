from services.document_service import load_documents
from services.chunking_service import create_document_chunks


documents = load_documents()

chunks = create_document_chunks(documents)

print(f"Documents loaded: {len(documents)}")
print(f"Total chunks created: {len(chunks)}")

for chunk in chunks:
    print("\n-----------------------------")
    print(f"Chunk ID: {chunk['chunk_id']}")
    print(f"Source: {chunk['filename']}")
    print(f"Text: {chunk['text'][:200]}...")
    print("-----------------------------")