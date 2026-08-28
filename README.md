# CampusAI – University Knowledge Assistant

## Exercise 1 – Basic LLM Application

CampusAI is an LLM-based university assistant. The application will
eventually answer student questions using a university knowledge base.

In Exercise 1, the application communicates with Code Llama through
the Ollama API.

## Architecture

User
  ↓
FastAPI Application
  ↓
LLM Service
  ↓
Ollama API
  ↓
Code Llama
  ↓
Response

## Technologies

- Python
- FastAPI
- Uvicorn
- Ollama
- Code Llama
- Requests

## Project Structure

CampusAI/
│
├── app/
│   ├── main.py
│   └── api.py
│
├── services/
│   └── llm_service.py
│
├── data/
├── tests/
├── docker/
├── requirements.txt
└── README.md

## How to Run

### 1. Activate virtual environment

Windows:

venv\Scripts\activate

### 2. Start Ollama

Make sure Ollama is running and Code Llama is available.

### 3. Start FastAPI

uvicorn app.api:app --reload

### 4. Open API documentation

http://127.0.0.1:8000/docs

## API

### POST /ask

Request:

{
    "question": "What is machine learning?"
}

Response:

{
    "question": "What is machine learning?",
    "answer": "..."
}

## Exercise 1 Result

The application successfully accepts a user question through a
FastAPI endpoint and sends the question to Code Llama through
Ollama's API.

## Future Development

Exercise 2:
Add a university knowledge base, document processing, chunking,
and embeddings.

Exercise 3:
Add vector similarity, retrieval, and RAG.

Exercise 4:
Separate the application into services and implement orchestration.

Exercise 5:
Dockerize the complete application.