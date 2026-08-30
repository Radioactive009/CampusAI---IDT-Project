from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.orchestrator_service import process_question
from services.llm_client import generate_with_llm_service


app = FastAPI(
    title="CampusAI",
    description="University Knowledge Assistant",
    version="3.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "Welcome to CampusAI",
        "version": "3.0.0",
        "architecture": "Application → Retrieval → LLM"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = process_question(
            request.question,
            top_k=3
        )

        return result

    except Exception:

        raise HTTPException(
            status_code=503,
            detail="Unable to process request."
        )


@app.post("/test-llm-service")
def test_llm_service(request: QuestionRequest):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        answer = generate_with_llm_service(
            request.question
        )

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception:

        raise HTTPException(
            status_code=503,
            detail="LLM Service is unavailable."
        )

@app.get("/health")
def health():
    return {
        "service": "Application Service",
        "status": "healthy"
    }