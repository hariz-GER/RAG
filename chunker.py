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


class Chunker:
    """Class wrapper for text chunking"""
    def __init__(self, chunk_size=800, overlap=120):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text):
        """Chunk text into smaller pieces, returning only the text strings"""
        chunks = chunk_text([text], chunk_size=self.chunk_size, overlap=self.overlap)
        return [chunk['text'] for chunk in chunks]
