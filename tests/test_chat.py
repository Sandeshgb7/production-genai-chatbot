import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# 👇 import auth dependency
from app.core import get_current_user


@pytest.mark.asyncio
async def test_chat(monkeypatch):

    # ✅ override auth (skip JWT validation)
    app.dependency_overrides[get_current_user] = lambda: "test_user"

    # ✅ mock LLM
    async def fake_llm(messages):
        return "mock response"

    #monkeypatch.setattr("app.services.llm.generate_response", fake_llm)
    monkeypatch.setattr("app.agent.generate_response", fake_llm)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/chat",
            json={
                "session_id": "s1",
                "message": "Hello"
            }
        )

    assert response.status_code == 200
    assert response.json()["response"] == "mock response"