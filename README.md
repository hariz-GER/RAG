# RAG HR Assistant

This is a small Retrieval-Augmented Generation project like the one shown in the reference image.

## Project Structure

```text
RAG_HR_Assistant/
├── resources/
│   └── HRPolicy.pdf
├── app.py
├── chunker.py
├── dataprocessor.py
├── embedder.py
├── pdfreader.py
├── vectorstore.py
├── requirements.txt
└── .env.example
```

## Run

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your OpenAI API key.
4. Place your PDF at `resources/HRPolicy.pdf`.
5. Build the vector index:

```bash
python3 dataprocessor.py
```

6. Start the chatbot:

```bash
python3 app.py
```
