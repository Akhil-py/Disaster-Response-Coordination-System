from fastapi import WebSocket
from typing import Set
from models import GameState

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
