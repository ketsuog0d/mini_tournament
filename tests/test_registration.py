import pytest
from httpx import AsyncClient
from app.main import app
from datetime import datetime, timedelta
from uuid import UUID

@pytest.mark.asyncio
async def test_tournament_and_player_registration():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создание турнира
        start_time = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
        response = await client.post("/tournaments", json={
            "name": "Weekend Cup",
            "max_players": 2,
            "start_at": start_time
        })
        assert response.status_code == 201
        tournament = response.json()
        tid = tournament["id"]

        # Первый игрок
        response = await client.post(f"/tournaments/{tid}/register", json={
            "name": "Alice",
            "email": "alice@example.com"
        })
        assert response.status_code == 200
        assert response.json()["email"] == "alice@example.com"

        # Повторный email (ошибка)
        response = await client.post(f"/tournaments/{tid}/register", json={
            "name": "Duplicate",
            "email": "alice@example.com"
        })
        assert response.status_code == 400

        # Второй игрок
        response = await client.post(f"/tournaments/{tid}/register", json={
            "name": "Bob",
            "email": "bob@example.com"
        })
        assert response.status_code == 200

        # Превышение лимита (ошибка)
        response = await client.post(f"/tournaments/{tid}/register", json={
            "name": "Charlie",
            "email": "charlie@example.com"
        })
        assert response.status_code == 400
