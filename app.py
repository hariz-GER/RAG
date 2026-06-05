import os

from dotenv import load_dotenv
from openai import OpenAI

from embedder import Embedder
from vectorstore import VectorStore


def make_answer(question, context):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Answer using only the provided HR policy context. If the answer is not in the context, say you do not know.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
    )

    return response.output_text


def main():
    load_dotenv()

    collection_name = os.getenv("COLLECTION_NAME", "hr_policy")
    embedder = Embedder()
    store = VectorStore(collection_name=collection_name)

    print("HR Policy RAG Assistant")
    print("Ask a question, or type 'exit' to quit.")

    while True:
        question = input("\nQuestion: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        query_embedding = embedder.embed_query(question)
        results = store.search(query_embedding)
        documents = results.get("documents", [[]])[0]
        context = "\n\n".join(documents)

        answer = make_answer(question, context)
        print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    main()
