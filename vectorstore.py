import os
import chromadb

class VectorStore:
    def __init__(self, collection_name="hr_policy"):
        self.client = chromadb.CloudClient(
            api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE", "RAG")
        )
        self.collection = self.client.get_or_create_collection(collection_name)
        print(f"✅ Connected to Chroma Cloud — collection: {collection_name}")

    def add_chunks(self, chunks, embeddings):
        ids = [f"chunk-{index}" for index in range(len(chunks))]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"page": chunk["page"]} for chunk in chunks]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )
        print(f"✅ Added {len(chunks)} chunks to Chroma Cloud!")

    def search(self, query_embedding, top_k=4):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )