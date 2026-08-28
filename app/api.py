from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.rag_service import generate_rag_response


app = FastAPI(
    title="CampusAI",
    description="University Knowledge Assistant",
    version="2.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to CampusAI",
        "version": "2.0.0",
        "mode": "RAG"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = generate_rag_response(
            request.question,
            top_k=3
        )

        return {
            "question": result["question"],
            "answer": result["answer"],
            "sources": [
                chunk["filename"]
                for chunk in [
                    result["context"]
                ]
            ]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )