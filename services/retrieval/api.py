from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.retrieval_service import retrieve_relevant_chunks


app = FastAPI(
    title="CampusAI Retrieval Service",
    description="Service responsible for retrieving relevant university information",
    version="1.0.0"
)


class RetrievalRequest(BaseModel):
    question: str
    top_k: int = 3


@app.get("/")
def home():
    return {
        "service": "Retrieval Service",
        "status": "running"
    }


@app.post("/retrieve")
def retrieve(request: RetrievalRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        results = retrieve_relevant_chunks(
            request.question,
            top_k=request.top_k
        )

        return {
            "question": request.question,
            "results": results
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Retrieval failed."
        )

@app.get("/health")
def health():
    return {
        "service": "Retrieval Service",
        "status": "healthy"
    }