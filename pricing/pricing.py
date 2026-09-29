# Pricing per 1M tokens (USD) — update as providers change rates
# Source: provider pricing pages

PRICING: dict[str, dict[str, float]] = {
    "openai": {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    },
    "groq": {
        "openai/gpt-oss-20b": {"input": 0.60, "output": 0.60},
    },
}


def estimate_cost(provider: str, model: str, usage: dict) -> float | None:
    """Estimate the cost of a completion call in USD.

    Args:
        provider: Provider name (e.g. 'openai', 'groq').
        model: Model name as returned by the API.
        usage: Dict with 'prompt_tokens' and 'completion_tokens'.

    Returns:
        Estimated cost in USD.
    """
    rates = PRICING.get(provider, {}).get(model)
    if not rates:
        return None # Unknown model — cost tracking not available yet

    input_cost = (usage["prompt_tokens"] / 1_000_000) * rates["input"]
    output_cost = (usage["completion_tokens"] / 1_000_000) * rates["output"]
    return round(input_cost + output_cost, 8)
