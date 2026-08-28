def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_document_chunks(documents, chunk_size=100, overlap=20):

    all_chunks = []

    for document in documents:

        chunks = chunk_text(
            document["text"],
            chunk_size,
            overlap
        )

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "chunk_id": f"{document['filename']}_{index}",
                "filename": document["filename"],
                "text": chunk
            })

    return all_chunks