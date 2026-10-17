---
title: GitHub RAG Chatbot
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

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
│   ├── main.py                # FastAPI app (API, CORS, rate limit, serves the frontend)
│   ├── rag.py                 # question -> retrieve -> Gemini -> answer
│   ├── retriever.py           # ChromaDB search + cross-encoder reranking
│   ├── generator.py           # Gemini client
│   ├── github_documents.py    # downloads the FastAPI docs into data/
│   ├── chunker.py             # splits the documents into chunks
│   └── embeddings.py          # creates embeddings and fills ChromaDB
│
├── frontend/
│   └── frontend/              # React + Vite app
│       ├── src/
│       ├── package.json
│       └── vite.config.js
│
├── chroma_db/                 # the prebuilt vector database
├── data/                      # downloaded documentation (source of the database)
├── scripts/                   # small debugging helpers
├── tests/                     # API tests (pytest)
│
├── Dockerfile
├── .dockerignore
├── .env.example
├── requirements.txt
├── requirements-dev.txt
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

Copy `.env.example` to `.env` in the project root and fill in your keys:

```env
GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your `.env` file or expose your API keys publicly.

The `.gitignore` file already excludes `.env`.

---

## Build the RAG Database

The repository already contains a prebuilt `chroma_db/`, so you only need this section if you want to rebuild it.

Run these from the project root (use `-m`, because the files import each other):

```bash
# 1. Download the selected FastAPI docs into data/ (needs GITHUB_TOKEN)
python -m backend.github_documents

# 2. Chunk the documents and store the embeddings in chroma_db/
python -m backend.embeddings
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
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## API

### `GET /health`

Checks whether the backend is running. Returns `{"status": "ok"}`.

### `POST /ask`

Asks a question about the FastAPI documentation.

Request body:

```json
{ "question": "What is a path parameter?" }
```

Response:

```json
{ "question": "What is a path parameter?", "answer": "..." }
```

| Status | Meaning |
| --- | --- |
| `200` | Answer generated |
| `422` | Question is empty or longer than `MAX_QUESTION_LENGTH` |
| `429` | Rate limit reached (per IP) |
| `502` | The answer could not be generated (retrieval or Gemini error, see the logs) |
| `503` | `GEMINI_API_KEY` is not configured on the server |

### Screenshots

<img width="1899" height="907" alt="image" src="https://github.com/user-attachments/assets/50cae444-a5d1-446a-a6d6-d700ca98f7d8" />

<img width="1903" height="905" alt="image" src="https://github.com/user-attachments/assets/ee5e22ef-a1b7-4570-9c3b-283505cfbad9" />




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

The web interface is a React + Vite app located in:

```text
frontend/frontend/
```

Run it (the backend must already be running):

```bash
cd frontend/frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

The backend allows requests from `http://localhost:5173` and `http://127.0.0.1:5173` (see CORS in `backend/main.py`).

By default the frontend sends requests to `http://127.0.0.1:8000`. To use another backend URL, create `frontend/frontend/.env` with:

```env
VITE_API_URL=http://your-backend-url
```

---

## Deployment (Docker)

The `Dockerfile` builds the React frontend and the Python backend into one image.
The backend serves the frontend too, so the whole app is available on **one link**.

### Run with Docker locally

```bash
docker build -t rag-chatbot .
docker run -p 7860:7860 -e GEMINI_API_KEY=your_gemini_api_key rag-chatbot
```

Then open `http://localhost:7860`.

### Deploy on Hugging Face Spaces (free)

1. Create an account on https://huggingface.co and a new **Space**:
   choose **Docker** as the SDK (blank template) and keep it public.
2. In the Space, open **Settings → Variables and secrets** and add a **secret**
   named `GEMINI_API_KEY` with your Gemini key.
3. Upload the project from this folder (the upload command handles the large
   `chroma_db` file for you):

```bash
pip install -U huggingface_hub
hf auth login
hf upload YOUR_USERNAME/YOUR_SPACE_NAME . . --repo-type=space --exclude ".git/*" --exclude "venv/*" --exclude ".venv/*" --exclude ".env" --exclude "frontend/frontend/node_modules/*" --exclude "frontend/frontend/dist/*" --exclude "data/*"
```

4. The Space builds the image (the first build takes several minutes) and then
   your app is live at `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`.

> The block at the very top of this README (between `---`) is the Hugging Face Spaces configuration. Keep it.

### Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `GEMINI_API_KEY` | required | Google Gemini API key (use a secret, never commit it) |
| `ALLOWED_ORIGINS` | empty | Extra frontend URLs allowed by CORS, separated by commas (only needed if the frontend is hosted on a different domain) |
| `RATE_LIMIT_REQUESTS` | `10` | Questions allowed per IP in the time window |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Length of the rate-limit window |
| `MAX_QUESTION_LENGTH` | `500` | Maximum characters in a question |
| `GEMINI_MODEL` | `gemini-3.1-flash-lite` | Gemini model used to generate answers |
| `LOG_LEVEL` | `INFO` | Use `DEBUG` to also log the retrieved chunks and the context sent to Gemini |
| `PORT` | `7860` | Port the server listens on (most hosts set this automatically) |

The rate limit protects your Gemini quota on a public link.

### Deploy on other hosts (Render, Railway, Fly.io, ...)

Any host that can build a `Dockerfile` works:

1. Create a new **Web Service** from this GitHub repository and choose the **Dockerfile** runtime.
2. Add `GEMINI_API_KEY` as a secret / environment variable.
3. Use `/health` as the health check path. The first start can take a minute while the models load,
   and because PyTorch and the models run inside the container, choose a plan with 2 GB of RAM or more.

The host sets `PORT` automatically and the app already listens on it.

### Run the tests

```bash
pip install -r requirements-dev.txt
pytest
```

The tests use fakes for Gemini and ChromaDB, so they need no API key.

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
| React + Vite          | Frontend                  |

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
