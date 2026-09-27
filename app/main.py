from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from router.router import route
from pricing.pricing import estimate_cost


app = FastAPI(
    title="LLM Cost Autopilot",
    version="0.2.0",
)


class ChatRequest(BaseModel):
    prompt: str
    provider: str = "groq"
    model: str | None = None


@app.get("/")
def root():
    return {"message": "LLM Cost Autopilot is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        result = route(
            prompt=request.prompt,
            provider=request.provider,
            model=request.model,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    cost = estimate_cost(
        provider=result["provider"],
        model=result["model"],
        usage=result["usage"],
    )

    return {
        "content": result["content"],
        "usage": result["usage"],
        "model": result["model"],
        "provider": result["provider"],
        "estimated_cost_usd": cost,
    }