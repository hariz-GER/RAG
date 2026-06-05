# RAG Document Assistant

A Retrieval-Augmented Generation (RAG) system that allows you to upload documents (PDF, Excel, Word) and ask questions about them using Google Gemini API.

## Features

✅ **Multiple File Format Support**
- PDF files
- Excel spreadsheets (.xlsx, .xls)
- Word documents (.docx, .doc)

✅ **Intelligent Document Processing**
- Automatic text extraction
- Smart chunking for optimal retrieval
- Vector embeddings using sentence-transformers
- Chroma vector database storage

✅ **Web Interface**
- Beautiful drag-and-drop file upload
- Real-time document processing
- Interactive Q&A interface
- Source document references

✅ **AI-Powered Answers**
- Google Gemini 2.0 Flash for responses
- Context-aware answers based on uploaded documents
- Citation of source documents

## Installation

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
COLLECTION_NAME=rag_documents
CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_chroma_tenant
CHROMA_DATABASE=RAG
```

## Usage

### Web Interface (Recommended)

Start the Flask web application:

```bash
python3 web_app.py
```

Then open your browser and go to:
```
http://localhost:5000
```

**Features:**
1. **Upload Section:** Drag and drop or click to upload PDF, Excel, or Word files
2. **Query Section:** Ask questions about your uploaded documents
3. **Results:** View answers and source references

### CLI Interface (Original)

For the original command-line interface:

```bash
python3 app.py
```

## File Structure

```
RAG_HR_Assistant/
├── app.py                 # Original CLI application
├── web_app.py            # Flask web application
├── file_processor.py     # Handles file format conversion
├── embedder.py           # Document embeddings
├── vectorstore.py        # Chroma vector database
├── chunker.py            # Text chunking logic
├── dataprocessor.py      # Data processing utilities
├── pdfreader.py          # PDF reading utilities
├── templates/
│   └── index.html        # Web UI
├── requirements.txt      # Python dependencies
├── .env                  # Configuration (not in repo)
├── chroma_db/           # Local Chroma database
└── resources/           # Sample documents
```

## Configuration

### API Keys

**Google Gemini API:**
1. Go to [ai.google.dev](https://ai.google.dev)
2. Create an API key
3. Add to `.env` file

**Chroma Cloud (Optional):**
1. Visit [trychroma.com](https://www.trychroma.com/)
2. Create account and get credentials
3. Add to `.env` file

### Max File Size

Default: 50MB per file (configurable in `web_app.py`)

## Supported Document Types

| Format | Extension | Status |
|--------|-----------|--------|
| PDF | .pdf | ✅ Supported |
| Excel | .xlsx, .xls | ✅ Supported |
| Word | .docx, .doc | ✅ Supported |
| Text | .txt | ✅ Supported (via CLI only) |

## API Endpoints

### POST `/upload`
Upload and process a document file.

**Request:**
```bash
curl -X POST -F "file=@document.pdf" http://localhost:5000/upload
```

**Response:**
```json
{
  "success": true,
  "message": "File processed successfully. 10 chunks stored.",
  "chunks_count": 10
}
```

### POST `/query`
Query the RAG system with a question.

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is the leave policy?"}' \
  http://localhost:5000/query
```

**Response:**
```json
{
  "answer": "The leave policy allows...",
  "sources": [
    "Text chunk 1...",
    "Text chunk 2..."
  ]
}
```

## Troubleshooting

### "Quota exceeded" Error
- Your Gemini API free tier is exhausted
- Solutions:
  1. Wait for daily quota reset (midnight UTC)
  2. Enable paid billing in Google AI Studio
  3. Check your usage at [ai.dev/rate-limit](https://ai.dev/rate-limit)

### File Upload Fails
- Check file size (max 50MB)
- Verify file format is supported
- Ensure sufficient disk space

### No Results for Query
- Document might not contain relevant information
- Try different search terms
- Upload more documents with related content

## Performance Tips

1. **Chunk Size:** Adjust in `chunker.py` for different document types
2. **Model Selection:** Change model in `web_app.py` line 32
3. **Batch Processing:** Process multiple files before querying
4. **Vector Storage:** Use Chroma Cloud for persistent storage

## API Key Management

⚠️ **Security Warning:**
- Never commit `.env` file to git
- Keep API keys private
- Use environment variables in production
- Rotate keys regularly

## Development

### Adding New File Formats

Edit `file_processor.py`:

```python
def extract_text_from_custom(file_path):
    """Extract text from custom format"""
    text = ""
    # Your extraction logic here
    return text
```

### Customizing the UI

Edit `templates/index.html` to modify colors, layout, or functionality.

### Changing the Model

In `web_app.py`, line 32:
```python
response = client.models.generate_content(
    model="gemini-2.0-flash",  # Change this
    contents=prompt,
)
```

Available models:
- `gemini-2.0-flash` (faster, cheaper)
- `gemini-2.0-pro` (more capable)
- `gemini-1.5-flash`
- `gemini-1.5-pro`

## Testing

Test file upload with curl:
```bash
curl -X POST -F "file=@test.pdf" http://localhost:5000/upload
```

Test query with curl:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question":"test"}' \
  http://localhost:5000/query
```

## License

This project is open source.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Check API key validity
4. Verify file formats are supported

---

**Happy querying! 🚀**
