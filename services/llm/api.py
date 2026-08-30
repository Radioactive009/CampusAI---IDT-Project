from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.llm_service import generate_response


app = FastAPI(
    title="CampusAI LLM Service",
    description="Service responsible for communicating with Ollama and Code Llama",
    version="1.0.0"
)


class LLMRequest(BaseModel):
    prompt: str


@app.get("/")
def home():

    return {
        "service": "LLM Service",
        "status": "running",
        "model": "codellama"
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
            request.prompt
        )

        return {
            "response": answer
        }

    except Exception:

        raise HTTPException(
            status_code=503,
            detail="LLM service could not generate a response."
        )