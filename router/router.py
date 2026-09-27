from providers import openai_provider, groq_provider

PROVIDERS = {
    "openai": openai_provider,
    "groq": groq_provider,
}


def route(prompt: str, provider: str = "groq", model: str | None = None) -> dict:
    """Route a prompt to the specified provider.

    Args:
        prompt: The user prompt to send.
        provider: One of 'openai' or 'groq'.
        model: Optional model override. Defaults to each provider's default.

    Returns:
        A dict with keys: content, usage, model, provider.
    """
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider '{provider}'. Choose from: {list(PROVIDERS)}")

    module = PROVIDERS[provider]
    kwargs = {"prompt": prompt}
    if model:
        kwargs["model"] = model

    return module.complete(**kwargs)
