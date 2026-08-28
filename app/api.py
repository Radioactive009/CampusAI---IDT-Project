from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

from services.llm_service import generate_response


app = FastAPI(
    title="CampusAI",
    description="University Knowledge Assistant",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to CampusAI"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        answer = generate_response(request.question)

        return {
            "question": request.question,
            "answer": answer
        }

    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is unavailable."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )