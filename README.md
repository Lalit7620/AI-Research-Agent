# AI Research & Knowledge Agent

An AI-powered research assistant that combines web research with Retrieval-Augmented Generation (RAG) over user-uploaded documents.

The application allows authenticated users to ask research questions, search for current information on the web, retrieve relevant information from their private documents, and generate a synthesized research report.

## Features

- User registration and authentication
- AI-powered research assistant
- Web/browser research
- Retrieval-Augmented Generation (RAG)
- PDF document upload
- PDF text extraction
- Recursive text chunking
- Semantic embeddings
- ChromaDB vector storage
- User-specific document retrieval
- Hybrid web + document research
- Research history
- Saved research reports
- Document listing and deletion
- Markdown report rendering
- REST APIs using Django REST Framework
- Session-based browser authentication
- JWT API authentication foundation

---

## Architecture

```text
                    User
                     |
                     v
              Django Dashboard
                     |
                     v
             Django REST API
                     |
                     v
              Research Agent
                     |
          +----------+----------+
          |                     |
          v                     v
     Web Research              RAG
          |                     |
          v                     v
   Browser Search        ChromaDB Vector Store
                                |
                                v
                         User Documents
                                |
                                v
                         Retrieved Chunks
          |                     |
          +----------+----------+
                     |
                     v
              LLM Synthesis
                     |
                     v
              Research Report
                     |
                     v
                Django UI
```

---

## RAG Pipeline

Uploaded documents follow this pipeline:

```text
PDF
 |
 v
PyMuPDF
 |
 v
Text Extraction
 |
 v
Recursive Chunking
 |
 v
BGE Embeddings
 |
 v
ChromaDB
 |
 v
Semantic Retrieval
 |
 v
Relevant Document Chunks
 |
 v
Research Agent
 |
 v
LLM-generated Research Report
```

For a research question, the system can combine:

```text
User Query
     |
     +-------------------+
     |                   |
     v                   v
 Web Search             RAG
     |                   |
     v                   v
Current Web Data    Private Documents
     |                   |
     +---------+---------+
               |
               v
        Evidence / Context
               |
               v
        LLM Synthesis
               |
               v
        Research Report
```

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- Django Authentication
- Django REST Framework SimpleJWT

### Agentic AI

- Agno
- Groq
- GPT-OSS-120B
- Browser/Web Search

### RAG

- PyMuPDF
- LangChain Text Splitters
- Sentence Transformers
- BAAI/bge-small-en-v1.5
- ChromaDB

### Frontend

- Django Templates
- HTML
- Tailwind CSS
- Vanilla JavaScript
- Marked.js
- DOMPurify

### Database

- SQLite for local development
- ChromaDB for vector storage

---

## Project Structure

```text
AI-Research-Agent/
│
├── accounts/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── documents/
│   ├── services/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── context_builder.py
│   │   └── ingestion.py
│   │
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── research/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── tools.py
│   │
│   ├── templates/
│   │   └── research/
│   │       ├── base.html
│   │       └── dashboard.html
│   │
│   ├── static/
│   │   └── research/
│   │       ├── css/
│   │       └── js/
│   │
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── config/
│
├── media/
├── db/
│   └── chroma/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Research-Agent.git
cd AI-Research-Agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=openai/gpt-oss-120b
```

Never commit the real `.env` file.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## How the System Works

### Research workflow

```text
User enters research question
            |
            v
       Django API
            |
            v
      ResearchRequest
            |
            v
       ResearchAgent
            |
       +----+----+
       |         |
       v         v
  Web Search    RAG
       |         |
       |         v
       |    ChromaDB
       |         |
       |         v
       |   Relevant chunks
       |         |
       +----+----+
            |
            v
       LLM synthesis
            |
            v
      ResearchReport
            |
            v
       Dashboard UI
```

### Document workflow

```text
User uploads PDF
       |
       v
Django stores document
       |
       v
PDF text extraction
       |
       v
Text chunking
       |
       v
Sentence Transformer embeddings
       |
       v
ChromaDB
```

When the user asks a question, the query is embedded and used to retrieve the most relevant chunks from the user's own documents.

---

## API Endpoints

### Research

```text
GET  /api/research/
POST /api/research/
```

### Research History

```text
GET /api/research/history/
```

### Research Detail

```text
GET /api/research/<request_id>/
```

### Documents

```text
GET    /api/documents/
POST   /api/documents/upload/
DELETE /api/documents/<document_id>/
```

### Authentication

```text
POST /api/token/
POST /api/token/refresh/
```

Browser authentication uses Django sessions.

---

## Security

The application implements user-level access control for research requests and uploaded documents.

Document retrieval is filtered by the authenticated user's ID so that one user cannot retrieve another user's vectorized document chunks.

Environment variables are used for API credentials.

Sensitive files such as:

```text
.env
db.sqlite3
media/
db/chroma/
```

are excluded from version control.

---

## Current Limitations

This project is currently a local development/portfolio application.

It is not presented as a production deployment.

Current limitations include:

- SQLite is used for local development
- ChromaDB is stored locally
- Uploaded files are stored locally
- Research requests currently run synchronously
- Production deployment configuration is not included
- Background task processing is not implemented

---

## Future Improvements

Potential future improvements include:

- PostgreSQL
- Redis and background task processing
- Asynchronous research jobs
- Production deployment
- Streaming research responses
- Improved citation/source tracking
- Research planning
- Multi-agent orchestration
- Automated testing
- Docker deployment
- More advanced document processing

---

## Project Status

**Completed portfolio version**

The current version demonstrates an end-to-end AI research workflow combining:

- Agentic AI
- Web research
- RAG
- Embeddings
- Vector databases
- Document processing
- Django/DRF
- Authentication
- REST APIs
- Frontend integration

---

## Author

Lalit Kumar Sahoo

GitHub: https://github.com/Lalit7620
