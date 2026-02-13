import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models import initial_game_state
from broadcaster import serialize_state, add_connection, remove_connection, broadcast, active_connections

logger = logging.getLogger(__name__)

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


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    add_connection(ws)
    game_state.connected_users += 1

    state_msg = json.dumps({
        "type": "state_sync",
        "payload": serialize_state(game_state),
    })
    await ws.send_text(state_msg)
    await broadcast(game_state)

    try:
        while True:
            data = await ws.receive_text()
    except WebSocketDisconnect:
        remove_connection(ws)
        game_state.connected_users = max(0, game_state.connected_users - 1)
    except Exception:
        remove_connection(ws)
        game_state.connected_users = max(0, game_state.connected_users - 1)
