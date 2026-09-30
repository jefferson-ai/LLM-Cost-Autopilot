from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_unknown_provider_returns_400():
    response = client.post("/chat", json={"prompt": "hi", "provider": "badprovider"})
    assert response.status_code == 400
    assert "Unknown provider" in response.json()["detail"]


def test_chat_returns_cost():
    fake_result = {
        "content": "Hello!",
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        "model": "openai/gpt-oss-20b",
        "provider": "groq",
    }
    with patch("app.main.route", return_value=fake_result):
        response = client.post("/chat", json={"prompt": "hi", "provider": "groq"})

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello!"
    assert "estimated_cost_usd" in data


def test_chat_missing_key_returns_503():
    from providers.groq_provider import ProviderConfigError
    with patch("app.main.route", side_effect=ProviderConfigError("GROQ_API_KEY is not set.")):
        response = client.post("/chat", json={"prompt": "hi", "provider": "groq"})

    assert response.status_code == 503
