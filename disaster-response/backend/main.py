import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models import initial_game_state
from broadcaster import serialize_state, add_connection, remove_connection, broadcast, active_connections
from event_queue import enqueue_action

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


async def _handle_disconnect(ws: WebSocket) -> None:
    remove_connection(ws)
    game_state.connected_users = max(0, game_state.connected_users - 1)
    await broadcast(game_state)


async def _handle_message(ws: WebSocket, raw: str) -> None:
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        await ws.send_text(json.dumps({
            "type": "error",
            "payload": {"message": "Invalid JSON"},
        }))
        return

    msg_type = msg.get("type")
    payload = msg.get("payload", {})

    if msg_type == "assign":
        resource_id = payload.get("resource_id")
        zone_id = payload.get("zone_id")
        if resource_id and zone_id:
            await enqueue_action("assign", resource_id=resource_id, zone_id=zone_id)
        else:
            await ws.send_text(json.dumps({
                "type": "error",
                "payload": {"message": "assign requires resource_id and zone_id"},
            }))
    elif msg_type == "ping":
        pass
    else:
        await ws.send_text(json.dumps({
            "type": "error",
            "payload": {"message": f"Unknown message type: {msg_type}"},
        }))


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
            await _handle_message(ws, data)
    except WebSocketDisconnect:
        await _handle_disconnect(ws)
    except Exception:
        await _handle_disconnect(ws)
