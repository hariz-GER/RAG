def chunk_text(pages, chunk_size=800, overlap=120):
    chunks = []

    for page_number, page_text in enumerate(pages, start=1):
        text = " ".join(page_text.split())

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(
                    {
                        "page": page_number,
                        "text": chunk,
                    }
                )

            start += chunk_size - overlap

    return chunks
