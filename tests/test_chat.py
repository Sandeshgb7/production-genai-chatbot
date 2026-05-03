import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_chat():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/chat",
            json={
                "user_id": "test",
                "session_id": "s1",
                "message": "Hello"
            },
        )

    assert response.status_code == 200
    assert "response" in response.json()