from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import initial_game_state
from broadcaster import serialize_state

app = FastAPI(title="Disaster Response Coordination")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_state = initial_game_state()


@app.get("/")
async def root():
    return {"status": "ok", "tick": game_state.tick}


@app.get("/health")
async def health():
    return serialize_state(game_state)
