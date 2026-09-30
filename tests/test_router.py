import pytest
from unittest.mock import patch
from router.router import route


def test_route_unknown_provider_raises():
    with pytest.raises(ValueError, match="Unknown provider"):
        route("hello", provider="badprovider")


def test_route_calls_groq_by_default():
    fake_result = {
        "content": "Hi!",
        "usage": {"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8},
        "model": "openai/gpt-oss-20b",
        "provider": "groq",
    }
    with patch("providers.groq_provider.complete", return_value=fake_result) as mock:
        result = route("hello", provider="groq")

    mock.assert_called_once_with(prompt="hello")
    assert result["provider"] == "groq"


def test_route_passes_model_override():
    fake_result = {
        "content": "Hi!",
        "usage": {"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8},
        "model": "some-model",
        "provider": "groq",
    }
    with patch("providers.groq_provider.complete", return_value=fake_result):
        result = route("hello", provider="groq", model="some-model")

    assert result["model"] == "some-model"
