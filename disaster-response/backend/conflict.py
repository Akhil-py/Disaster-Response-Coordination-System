import time
from models import GameState
from event_queue import UserAction

_pending_assigns: dict[str, list[UserAction]] = {}


def register_assign(action: UserAction) -> None:
    resource_id = action.resource_id
    if resource_id not in _pending_assigns:
        _pending_assigns[resource_id] = []
    _pending_assigns[resource_id].append(action)


def has_conflict(resource_id: str) -> bool:
    return len(_pending_assigns.get(resource_id, [])) > 1


def clear_pending() -> None:
    _pending_assigns.clear()


def get_pending(resource_id: str) -> list[UserAction]:
    return _pending_assigns.get(resource_id, [])
