from services.document_service import load_documents


documents = load_documents()

print(f"Number of documents loaded: {len(documents)}")

for document in documents:
    print("\n-----------------------------")
    print(f"File: {document['filename']}")
    print(f"Characters: {len(document['text'])}")
    print("-----------------------------")