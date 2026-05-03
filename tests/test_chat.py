import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

from app.core import get_current_user


@pytest.mark.asyncio
async def test_chat(monkeypatch):

    async def fake_llm(messages):
        return "mock response"

    # 👇 mock the real LLM call
    monkeypatch.setattr("app.services.llm.generate_response", fake_llm)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/chat",
            json={
                "session_id": "s1",
                "message": "Hello"
            },
            headers={"Authorization": "Bearer testtoken"}
        )

    assert response.status_code == 200
    assert response.json()["response"] == "mock response"

app.dependency_overrides[get_current_user] = lambda: "test_user"