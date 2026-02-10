from fastapi import WebSocket
from typing import Set

active_connections: Set[WebSocket] = set()


def add_connection(ws: WebSocket) -> None:
    active_connections.add(ws)


def remove_connection(ws: WebSocket) -> None:
    active_connections.discard(ws)
