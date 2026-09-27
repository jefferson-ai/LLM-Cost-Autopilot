from fastapi import FastAPI
from pydantic import BaseModel

from app.llm.client import ask_llm


app = FastAPI(
    title="LLM Cost Autopilot",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {"message": "LLM Cost Autopilot is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = ask_llm(request.prompt)

    return {
        "response": response.output_text
    }