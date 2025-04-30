# backend/api/game.py

from fastapi import APIRouter, HTTPException, Depends,Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from backend.core.game_logic import GameLinkedList
from backend.core.ai_client import ask_gemini, parse_verdict
from backend.core.cache import get_cached_verdict, set_cached_verdict
from backend.db.models import GuessCounter
from backend.db.session import get_db
import traceback

router = APIRouter()

# Initialize the linked list and seed globally (improve later for sessions)
game_list = GameLinkedList()
SEED_WORD = "Rock"

# ----------------------------- #
#          Pydantic Models      #
# ----------------------------- #

class GuessRequest(BaseModel):
    guess: str
    persona: str = "cheery"

class GuessResponse(BaseModel):
    seed: str
    guess: str
    result: str
    explanation: str
    guesses_so_far: list
    global_guesses: int


class GameStateResponse(BaseModel):
    seed: str
    guesses_so_far: list
    global_guesses: int

# ----------------------------- #
#           Routes              #
# ----------------------------- #
@router.get("/clear-cache")
async def clear_cache():
    """Temporary endpoint to clear the cache."""
    # This depends on how your cache is implemented
    # For Redis, you might use redis.flushall()
    # For a simple in-memory cache, you might reset the cache variable
    
    import redis

    # Connect to the Redis server
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Clear all keys from all databases
    r.flushall()
    return {"message": "Cache cleared successfully"}


limiter = Limiter(key_func=get_remote_address)

from starlette.requests import Request  # ✅ use starlette's Request

@router.post("/guess", response_model=GuessResponse)
@limiter.limit("10/minute")
async def make_guess(
    request: Request,  # ✅ required by SlowAPI
    payload: GuessRequest,  # ✅ renamed from `request` to avoid conflict
    db: Session = Depends(get_db)
):
    global game_list, SEED_WORD

    ai_response = None
    cache_key = f"{SEED_WORD.lower()}_{payload.guess.lower()}"
    cached = await get_cached_verdict(cache_key)

    if cached is not None:
        verdict = cached.get("verdict")
        explanation = cached.get("explanation")
        print(f">>> [Cache Hit] verdict: {verdict}, explanation: {explanation}")
    else:
        try:
            ai_response = await ask_gemini(SEED_WORD, payload.guess, payload.persona)
            print(f"=== Raw AI Response ===\n{repr(ai_response)}\n")

            if not ai_response or not ai_response.strip():
                raise ValueError("Empty or invalid AI response received.")
        except Exception as e:
            print(f"❌ Error while calling Gemini AI: {str(e)}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="AI service failed. Please try again later.")

        try:
            verdict, explanation = parse_verdict(ai_response)
            print(f">>> parse_verdict returned: {verdict}, explanation: {explanation}")
        except ValueError as e:
            print(f"❌ Error parsing AI response: {str(e)}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Error parsing AI response.")

        await set_cached_verdict(cache_key, verdict, explanation)
        print(f">>> Cached verdict and explanation.")

    if not verdict:
        print(">>> Final verdict is falsy. Triggering 400 with explanation.")
        game_list = GameLinkedList()
        SEED_WORD = "Rock"
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Your guess does not beat the seed. Game Over!",
                "explanation": explanation,
                "ai_response": ai_response
            }
        )

    added = game_list.add(payload.guess)
    if not added:
        print(">>> Duplicate guess detected. Triggering 400.")
        game_list = GameLinkedList()
        SEED_WORD = "Rock"
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Duplicate guess! Game Over.",
                "explanation": explanation,
                "ai_response": ai_response
            }
        )

    counter = db.query(GuessCounter).first()
    if not counter:
        counter = GuessCounter(count=1)
        db.add(counter)
    else:
        counter.count += 1
    db.commit()

    SEED_WORD = payload.guess

    return {
        "seed": SEED_WORD,
        "guess": payload.guess,
        "result": "You beat the seed!",
        "explanation": explanation,
        "guesses_so_far": game_list.get_all_guesses(),
        "global_guesses": counter.count,
    }



