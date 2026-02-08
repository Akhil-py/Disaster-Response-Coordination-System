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


def resolve_conflict(resource_id: str, game_state: GameState) -> tuple[UserAction, list[UserAction]]:
    actions = _pending_assigns.get(resource_id, [])
    if len(actions) <= 1:
        return (actions[0] if actions else None, [])

    def sort_key(action: UserAction) -> tuple:
        zone = game_state.zones.get(action.zone_id)
        incident_severity = 0
        if zone and zone.incident_id:
            incident = game_state.incidents.get(zone.incident_id)
            if incident:
                incident_severity = incident.severity
        return (-incident_severity, action.arrival_order)

    sorted_actions = sorted(actions, key=sort_key)
    winner = sorted_actions[0]
    losers = sorted_actions[1:]
    return (winner, losers)


def log_conflict_entries(losers: list[UserAction], game_state: GameState) -> None:
    for loser in losers:
        resource = game_state.resources.get(loser.resource_id)
        resource_type = resource.type if resource else "unknown"
        entry = {
            "timestamp": time.time(),
            "message": f"Resource {resource_type} reassigned to higher priority incident",
            "type": "conflict",
        }
        game_state.activity_log.append(entry)
        if len(game_state.activity_log) > 50:
            game_state.activity_log = game_state.activity_log[-50:]
