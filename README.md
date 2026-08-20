# GitHub RAG Chatbot

RAG-based chatbot for answering questions about FastAPI documentation.

## Features

- FastAPI backend
- Google Gemini for answer generation
- Sentence Transformers for embeddings
- ChromaDB vector database
- Semantic search
- Markdown-aware chunking
- Simple web frontend

## Architecture

FastAPI Documentation
        ↓
Document Loading
        ↓
Chunking
        ↓
Embeddings
        ↓
ChromaDB
        ↓
Semantic Retrieval
        ↓
Google Gemini
        ↓
Final Answer

## Project Structure

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
│   └── ...
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── requirements.txt
├── .gitignore
└── README.md

## Requirements

- Python 3.11+
- Git
- Google Gemini API key
- GitHub token (if repository loading is used)

## Installation

### 1. Clone the repository

git clone https://github.com/aqdarahmad/github-rag-chatbot.git

cd github-rag-chatbot

### 2. Create virtual environment

python -m venv venv

### 3. Activate virtual environment

Windows:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt

## Environment Variables

Create a `.env` file in the project root:

GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_gemini_api_key

Never commit the `.env` file.

## Build the RAG Database

Run the document loading / chunking / embedding pipeline:

python backend/github_loader.py

python backend/chunker.py

python backend/embeddings.py

This process:

1. Loads documentation
2. Splits documents into chunks
3. Generates embeddings
4. Stores vectors in ChromaDB

## Run the Backend

From the project root:

uvicorn backend.main:app --reload

The API will be available at:

http://127.0.0.1:8000

## API

### Health Check

GET /

Returns:

{
  "message": "GitHub RAG Chatbot is running"
}

### Ask a Question

POST /ask

Example:

{
  "question": "What is a path parameter?"
}

The system retrieves relevant documentation chunks and sends them to Gemini to generate the answer.

## Frontend

Open:

frontend/index.html

Or serve the frontend using a local HTTP server.

The frontend communicates with the FastAPI backend.

## Example

Question:

What is a path parameter?

Answer:

A path parameter is a variable declared in the URL path...

## RAG Pipeline

The system follows the Retrieval-Augmented Generation approach:

User Question
↓
Embedding
↓
Vector Search
↓
Relevant Chunks
↓
Context
↓
Gemini
↓
Answer

## Technologies

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- Google Gemini
- HTML
- CSS
- JavaScript

## Future Improvements

- Support arbitrary public GitHub repositories
- Allow users to enter a GitHub repository URL
- Automatically clone/index repositories
- Repository-specific chat sessions
- Authentication
- Streaming responses
- Improved retrieval and reranking

## License

MIT
