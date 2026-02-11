import json
import logging
from fastapi import WebSocket
from typing import Set
from models import GameState

logger = logging.getLogger(__name__)

active_connections: Set[WebSocket] = set()


def add_connection(ws: WebSocket) -> None:
    active_connections.add(ws)


def remove_connection(ws: WebSocket) -> None:
    active_connections.discard(ws)


def serialize_state(game_state: GameState) -> dict:
    return {
        "zones": {zid: z.model_dump() for zid, z in game_state.zones.items()},
        "incidents": {iid: i.model_dump() for iid, i in game_state.incidents.items()},
        "resources": {rid: r.model_dump() for rid, r in game_state.resources.items()},
        "lives_saved": game_state.lives_saved,
        "lives_lost": game_state.lives_lost,
        "total_incidents": game_state.total_incidents,
        "resolved_incidents": game_state.resolved_incidents,
        "connected_users": game_state.connected_users,
        "tick": game_state.tick,
        "activity_log": game_state.activity_log,
    }


async def broadcast(game_state: GameState) -> None:
    if not active_connections:
        return
    message = json.dumps({
        "type": "state_sync",
        "payload": serialize_state(game_state),
    })
    dead = []
    for ws in active_connections:
        try:
            await ws.send_text(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        active_connections.discard(ws)
