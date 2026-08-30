from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.llm_service import generate_response


app = FastAPI(
    title="CampusAI LLM Service",
    description="Service responsible for communicating with Ollama and local LLM models",
    version="2.0.0"
)


class LLMRequest(BaseModel):
    prompt: str
    model: str = "codellama"


@app.get("/")
def home():

    return {
        "service": "LLM Service",
        "status": "running",
        "default_model": "codellama"
    }


@app.post("/generate")
def generate(request: LLMRequest):

    if not request.prompt.strip():

        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty."
        )

    try:

        answer = generate_response(
            request.prompt,
            request.model
        )

        return {
            "response": answer,
            "model": request.model
        }

    except Exception:

        raise HTTPException(
            status_code=503,
            detail="LLM service could not generate a response."
        )


@app.get("/health")
def health():

    return {
        "service": "LLM Service",
        "status": "healthy"
    }