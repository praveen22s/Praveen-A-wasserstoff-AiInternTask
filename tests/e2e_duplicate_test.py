import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from backend.main import app
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

@pytest.mark.asyncio
async def test_duplicate_guess_results_in_game_over():
    transport = ASGITransport(app=app)  # Use ASGITransport explicitly
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response1 = await ac.post("/game/guess", json={"guess": "Paper", "persona": "cheery"})
        print("Response 1:", response1.status_code, response1.json())

        assert response1.status_code == 200
        assert "You beat the seed!" in response1.json()["result"]  # Check the "result" field
        assert "guesses_so_far" in response1.json()

        # Duplicate guess (should return 400)
        response2 = await ac.post("/game/guess", json={"guess": "Paper", "persona": "cheery"})
        print("Response 2:", response2.status_code, response2.json())

        assert response2.status_code == 400
        assert "Game Over" in response2.json()["detail"]["message"]