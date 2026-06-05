import chromadb


class VectorStore:
    def __init__(self, path="chroma_db", collection_name="hr_policy"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(collection_name)

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

    def search(self, query_embedding, top_k=4):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
