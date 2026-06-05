import os

from dotenv import load_dotenv
import google.genai as genai

from embedder import Embedder
from vectorstore import VectorStore


def make_answer(question, context):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = f"""Answer using only the provided HR policy context. If the answer is not in the context, say you do not know.

Context:
{context}

Question: {question}"""
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text


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
