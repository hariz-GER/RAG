import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.genai as genai

from answer_utils import concise_fallback, limit_answer
from embedder import Embedder
from vectorstore import VectorStore
from chunker import Chunker
from file_processor import process_file

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
embedder = Embedder()
chunker = Chunker()
store = VectorStore(collection_name="rag_documents")


def make_answer(question, context):
    """Generate only the answer requested by the user."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Never expose the full retrieved document when Gemini is unavailable.
    if not api_key or api_key == "your_gemini_api_key_here":
        return concise_fallback(question, context)
    
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""You answer questions using only the provided document context.

Rules:
- Return only the exact information requested by the question.
- Never summarize the document or include unrelated details.
- For a skills question, return only a comma-separated list of skills.
- Use at most 3 short sentences.
- If the answer is absent, reply exactly: I do not know based on the provided document.

Context:
{context}

Question: {question}

Direct answer:"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return limit_answer(response.text)
    except Exception as e:
        app.logger.warning("Gemini answer generation failed: %s", e)
        return concise_fallback(question, context)


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and RAG processing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'.pdf', '.xlsx', '.xls', '.docx', '.doc'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'error': f'Unsupported file type. Allowed: {allowed_extensions}'}), 400
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Extract text
        text = process_file(file_path)
        
        # Chunk text
        chunks = chunker.chunk(text)
        
        # Format chunks for VectorStore (add page metadata)
        formatted_chunks = [
            {"text": chunk, "page": 1} 
            for chunk in chunks
        ]
        
        # Embed all chunks
        embeddings = [embedder.embed_query(chunk) for chunk in chunks]
        
        # Store in vector database
        store.add_chunks(formatted_chunks, embeddings)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'message': f'File processed successfully. {len(chunks)} chunks stored.',
            'chunks_count': len(chunks)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/query', methods=['POST'])
def query_documents():
    """Query the RAG system"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Embed query
        query_embedding = embedder.embed_query(question)
        
        # Search
        results = store.search(query_embedding)
        documents = results.get("documents", [[]])[0]
        
        if not documents:
            return jsonify({
                'answer': 'No relevant documents found in the database.',
                'sources': []
            }), 200
        
        context = "\n\n".join(documents)
        
        # Generate answer (or just return context if no API key)
        answer = make_answer(question, context)
        
        return jsonify({
            'answer': answer,
            # Do not print retrieved resume chunks beneath the focused answer.
            'sources': []
        }), 200
    
    except Exception as e:
        error_str = str(e)
        return jsonify({'error': f'Error: {error_str}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8001)
