# GitHub RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for answering questions about FastAPI documentation.

The system retrieves relevant documentation from a vector database and uses Google Gemini to generate a natural-language answer.

---

## Features

* FastAPI backend
* Google Gemini for answer generation
* Sentence Transformers for embeddings
* ChromaDB vector database
* Semantic similarity search
* Markdown-aware document chunking
* REST API
* Simple web frontend
* CORS support

---

## Architecture

```text
FastAPI Documentation
        ↓
Document Loading
        ↓
Document Chunking
        ↓
Text Embeddings
        ↓
ChromaDB
        ↓
Semantic Retrieval
        ↓
Relevant Context
        ↓
Google Gemini
        ↓
Generated Answer
```

---

## Project Structure

```text
github-rag-chatbot/
│
├── backend/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── generator.py
│   ├── github_documents.py
│   ├── github_loader.py
│   ├── main.py
│   ├── rag.py
│   ├── retriever.py
│   ├── test_models.py
│   └── test_similarity.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How It Works

When a user asks a question, the system follows these steps:

1. The user sends a question through the frontend.
2. The FastAPI backend receives the question.
3. The question is converted into an embedding using Sentence Transformers.
4. ChromaDB searches for semantically similar documentation chunks.
5. The most relevant chunks are selected.
6. The retrieved chunks are combined into a context.
7. The context and the user's question are sent to Google Gemini.
8. Gemini generates the final answer.
9. The answer is returned to the frontend.

---

## Requirements

Before running the project, make sure you have:

* Python 3.11+
* Git
* Google Gemini API key
* GitHub token if GitHub repository loading is used

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aqdarahmad/github-rag-chatbot.git
cd github-rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```powershell
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your `.env` file or expose your API keys publicly.

The `.gitignore` file already excludes `.env`.

---

## Build the RAG Database

The project uses a document processing pipeline to prepare the documentation for retrieval.

Run:

```bash
python backend/github_loader.py
```

Then:

```bash
python backend/chunker.py
```

Then:

```bash
python backend/embeddings.py
```

The process:

```text
GitHub Repository
        ↓
Document Loading
        ↓
File Filtering
        ↓
Chunking
        ↓
Embedding Generation
        ↓
ChromaDB
```

The generated vector database is stored locally in:

```text
chroma_db/
```

---

## Run the Backend

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### Health Check

Open:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "GitHub RAG Chatbot is running"
}
```

---

## API

### `GET /`

Checks whether the backend is running.

Example response:

```json
{
  "message": "GitHub RAG Chatbot is running"
}
```

---

### `POST /ask`

Sends a question to the RAG chatbot.

Request:

```json
{
  "question": "What is a path parameter?"
}
```

Example response:

```json
{
  "question": "What is a path parameter?",
  "answer": "A path parameter is a variable declared in the URL path..."
}
```

---

## Interactive API Documentation

FastAPI automatically provides interactive API documentation.

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to test the API directly.

---

## Frontend

The project includes a simple web interface located in:

```text
frontend/
```

Files:

```text
frontend/
├── index.html
├── script.js
└── style.css
```

The frontend sends user questions to the FastAPI backend and displays the generated answers.

---

## Example

### Question

```text
What is a path parameter?
```

### Answer

```text
A path parameter is a variable declared in the URL path using
the same syntax used by Python format strings. Its value is
passed to the function as an argument.
```

---

## RAG Pipeline

The complete Retrieval-Augmented Generation pipeline is:

```text
User Question
      ↓
Sentence Transformer
      ↓
Question Embedding
      ↓
ChromaDB Similarity Search
      ↓
Top Relevant Chunks
      ↓
Context Construction
      ↓
Google Gemini
      ↓
Final Answer
```

---

## Technologies

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Main programming language |
| FastAPI               | Backend REST API          |
| ChromaDB              | Vector database           |
| Sentence Transformers | Text embeddings           |
| Google Gemini         | Answer generation         |
| Requests              | GitHub API communication  |
| HTML                  | Frontend structure        |
| CSS                   | Frontend styling          |
| JavaScript            | Frontend logic            |

---

## Future Improvements

* Support arbitrary public GitHub repositories
* Allow users to enter a GitHub repository URL
* Automatically load and index repositories
* Repository-specific chat sessions
* Authentication
* Streaming responses
* Improved retrieval and reranking
* Better chunk selection
* Multi-repository support

---

## License

This project is licensed under the MIT License.