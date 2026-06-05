# Quick Start Guide - RAG Document Assistant

## 🚀 Get Started in 3 Steps

### Step 1: Install & Setup
```bash
# Navigate to project directory
cd /Users/hariz/Desktop/RAG/RAG_HR_Assistant

# Install dependencies (if not done already)
pip3 install flask openpyxl python-docx google-genai

# Verify .env file has your Gemini API key
cat .env
```

### Step 2: Start the Web Application
```bash
python3 web_app.py
```

You should see:
```
WARNING: This is a development server. Do not use it in production.
* Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser
Visit: **http://localhost:5000**

---

## 📤 How to Use

### Upload a Document
1. Click the upload area or drag & drop a file
2. Supported formats: **PDF, Excel (.xlsx, .xls), Word (.docx, .doc)**
3. Wait for "File processed successfully" message

### Ask Questions
1. Type your question in the search box
2. Press Enter or click "Search"
3. View the answer and source documents

---

## 📋 Example Questions

After uploading an HR policy document:
- "What is the leave policy?"
- "What are working hours?"
- "What is the code of conduct?"
- "Tell me about remote work"

---

## ⚙️ Configuration

### API Key Setup

If you haven't set your Gemini API key:

1. Go to [ai.google.dev](https://ai.google.dev)
2. Create a free API key
3. Edit `.env` file:
```env
GEMINI_API_KEY=your_key_here
```

### Optional: Chroma Cloud

For persistent storage across sessions:

1. Visit [trychroma.com](https://www.trychroma.com/)
2. Update `.env` with your credentials:
```env
CHROMA_API_KEY=your_key
CHROMA_TENANT=your_tenant
CHROMA_DATABASE=RAG
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Quota exceeded" | Wait for daily reset or enable paid billing |
| "Port 5000 already in use" | Change port in web_app.py: `app.run(port=5001)` |
| "File upload fails" | Check file format and size (<50MB) |
| "No answers found" | Document may not contain relevant info |

---

## 📚 File Structure

```
RAG_HR_Assistant/
├── web_app.py          ← Start this file
├── file_processor.py   ← Handles PDF, Excel, Word
├── .env               ← Your API keys
└── templates/
    └── index.html     ← Web interface
```

---

## 🎯 What Happens During Upload?

1. **Extract** → Reads text from your document
2. **Chunk** → Splits into meaningful pieces
3. **Embed** → Converts to vector embeddings
4. **Store** → Saves in Chroma database
5. **Ready** → You can now query the document

---

## 🔑 API Keys

### Getting Gemini API Key (Free)
1. Visit [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key" 
3. Copy the key starting with `AQ...`
4. Paste in `.env` file

### Free Tier Limits
- **Quota:** 1,500 requests/day
- **Rate:** 15 requests/minute
- If exceeded: Wait for next day's reset (midnight UTC)

---

## 💡 Tips

✅ **Best Practices:**
- Upload one document at a time
- Ask specific questions
- Use keywords from the document
- Start with small test files

❌ **Avoid:**
- Uploading >50MB files
- Rapid repeated queries
- Non-text based PDFs (scanned images)

---

## 🆘 Getting Help

**If something doesn't work:**

1. Check `.env` file has valid API key
2. Ensure all dependencies installed: `pip3 install -r requirements.txt`
3. Verify file format is supported
4. Check console output for error messages
5. Try a smaller test file first

---

## 🎉 You're Ready!

Start uploading documents and asking questions. Enjoy your RAG assistant!

```bash
python3 web_app.py
```

Then visit: **http://localhost:5000** 🚀
