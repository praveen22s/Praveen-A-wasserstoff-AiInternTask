from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

import logging

from backend.api.routes.game import router as game_router
from backend.db.session import engine, Base
from backend.db.models import GuessCounter

# --------------------------- #
#         Logging             #
# --------------------------- #
logging.basicConfig(level=logging.DEBUG)

# --------------------------- #
#     Initialize Database     #
# --------------------------- #
Base.metadata.create_all(bind=engine)

# --------------------------- #
#     Create FastAPI App      #
# --------------------------- #
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="What Beats Rock API",
    description="Backend for the What Beats Rock game with GenAI validation.",
    version="1.0.0",
)

# --------------------------- #
#     Add Middleware          #
# --------------------------- #
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for security if deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------- #
#   Rate Limit Error Handler  #
# --------------------------- #
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please slow down."},
    )

# --------------------------- #
#         Routes              #
# --------------------------- #
app.include_router(game_router, prefix="/game", tags=["game"])

@app.get("/")
async def root():
    return {"message": "Welcome to the What Beats Rock game!"}
