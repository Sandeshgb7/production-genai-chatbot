import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core import get_current_user


@pytest.mark.asyncio
async def test_chat(monkeypatch):

    # override auth
    app.dependency_overrides[get_current_user] = lambda: "test_user"

    # mock LLM
    async def fake_llm(messages):
        return "mock response"

    monkeypatch.setattr("app.services.llm.generate_response", fake_llm)

    # mock DB write
    monkeypatch.setattr("app.services.chat.save_to_db", lambda *args, **kwargs: None)

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

    # cleanup
    app.dependency_overrides = {}