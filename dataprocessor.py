import os

from dotenv import load_dotenv

from chunker import chunk_text
from embedder import Embedder
from pdfreader import read_pdf
from vectorstore import VectorStore


def build_index():
    load_dotenv()

    pdf_path = os.getenv("PDF_PATH", "resources/HRPolicy.pdf")
    collection_name = os.getenv("COLLECTION_NAME", "hr_policy")
 
    pages = read_pdf(pdf_path)
    print(f"Loaded {len(pages)} pages from {pdf_path}")

    chunks = chunk_text(pages)
    print(f"Created {len(chunks)} chunks")

    embedder = Embedder()
    embeddings = embedder.embed_texts([chunk["text"] for chunk in chunks])

    store = VectorStore(collection_name=collection_name)
    store.add_chunks(chunks, embeddings)

    print(f"Indexed {len(chunks)} chunks into collection '{collection_name}'")


if __name__ == "__main__":
    build_index()
