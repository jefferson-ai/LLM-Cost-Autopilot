from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from router.router import route
from pricing.pricing import estimate_cost
from providers.groq_provider import ProviderConfigError


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
    except ProviderConfigError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Provider error: {e}")

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

def start() -> None:
    """Entry point for the `llm-cost-autopilot` CLI command."""
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
