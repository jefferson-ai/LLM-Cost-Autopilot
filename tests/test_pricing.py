from pricing.pricing import estimate_cost


def test_estimate_cost_openai_gpt4o_mini():
    usage = {"prompt_tokens": 100, "completion_tokens": 50}
    cost = estimate_cost("openai", "gpt-4o-mini", usage)
    # (100/1M * 0.15) + (50/1M * 0.60) = 0.000015 + 0.00003 = 0.000045
    assert abs(cost - 0.000045) < 1e-9


def test_estimate_cost_unknown_model_returns_zero():
    usage = {"prompt_tokens": 1000, "completion_tokens": 500}
    cost = estimate_cost("openai", "gpt-99-unknown", usage)
    assert cost is None


def test_estimate_cost_groq():
    usage = {"prompt_tokens": 200, "completion_tokens": 100}
    cost = estimate_cost("groq", "openai/gpt-oss-20b", usage)
    # (200/1M * 0.60) + (100/1M * 0.60) = 0.00012 + 0.00006 = 0.00018
    assert abs(cost - 0.00018) < 1e-9
