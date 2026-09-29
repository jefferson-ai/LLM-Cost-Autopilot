import os
from openai import OpenAI

class ProviderConfigError(RuntimeError):
    """Raised when a required provider environment variable is missing."""


def get_client() -> OpenAI:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise ProviderConfigError(
            "GROQ_API_KEY is not set. Add it to your .env file."
        )
    return OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")



def complete(prompt: str, model: str = "openai/gpt-oss-20b") -> dict:
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return {
        "content": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "model": response.model,
        "provider": "groq",
    }
