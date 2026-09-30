"""Smoke test: call Groq via the router and print cost estimate."""
from dotenv import load_dotenv

load_dotenv()

from router.router import route
from pricing.pricing import estimate_cost

result = route(prompt="HI.", provider="groq")

cost = estimate_cost(
    provider=result["provider"],
    model=result["model"],
    usage=result["usage"],
)

print(f"Response : {result['content']}")
print(f"Model    : {result['model']} ({result['provider']})")
print(f"Usage    : {result['usage']}")
print(f"Est. cost: ${cost:.8f} USD")