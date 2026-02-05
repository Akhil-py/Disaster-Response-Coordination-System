import asyncio
import logging
import random
import time
import uuid
from models import GameState, Incident
from event_queue import enqueue_tick

logger = logging.getLogger(__name__)

TICK_INTERVAL = 2.0
MAX_ACTIVE_INCIDENTS = 5
SPAWN_CHANCE = 0.3
INCIDENT_TYPE_WEIGHTS = [("medical", 0.40), ("fire", 0.35), ("collapse", 0.25)]
ESCALATION_THRESHOLD = 10.0
FAIL_TICKS_AT_MAX = 2
RESOLVE_TIME = 5.0
COOLDOWN_DURATION = 8.0

_severity4_tick_counts: dict[str, int] = {}
_assignment_times: dict[str, float] = {}


def _pick_incident_type() -> str:
    r = random.random()
    cumulative = 0.0
    for itype, weight in INCIDENT_TYPE_WEIGHTS:
        cumulative += weight
        if r <= cumulative:
            return itype
    return "medical"


def _spawn_incident(game_state: GameState) -> None:
    active_count = len(game_state.incidents)
    if active_count >= MAX_ACTIVE_INCIDENTS:
        return
    if random.random() > SPAWN_CHANCE:
        return

    available_zones = [
        z for z in game_state.zones.values()
        if z.incident_id is None
    ]
    if not available_zones:
        return

    zone = random.choice(available_zones)
    incident_id = str(uuid.uuid4())
    incident_type = _pick_incident_type()
    lives = random.randint(1, 10)
    now = time.time()

    incident = Incident(
        id=incident_id,
        type=incident_type,
        zone_id=zone.id,
        severity=1,
        spawned_at=now,
        lives_at_risk=lives,
    )

    game_state.incidents[incident_id] = incident
    game_state.zones[zone.id].incident_id = incident_id
    game_state.zones[zone.id].severity = 1
    game_state.total_incidents += 1


def _escalate_incidents(game_state: GameState) -> None:
    now = time.time()
    for incident in list(game_state.incidents.values()):
        age = now - incident.spawned_at
        if age > ESCALATION_THRESHOLD and incident.severity < 4:
            incident.severity = min(incident.severity + 1, 4)
            game_state.zones[incident.zone_id].severity = incident.severity


def _auto_fail_incidents(game_state: GameState) -> None:
    to_remove = []
    for incident in list(game_state.incidents.values()):
        if incident.severity >= 4 and incident.assigned_resource_id is None:
            count = _severity4_tick_counts.get(incident.id, 0) + 1
            _severity4_tick_counts[incident.id] = count
            if count >= FAIL_TICKS_AT_MAX:
                game_state.lives_lost += incident.lives_at_risk
                game_state.zones[incident.zone_id].severity = 0
                game_state.zones[incident.zone_id].incident_id = None
                to_remove.append(incident.id)

    for iid in to_remove:
        del game_state.incidents[iid]
        _severity4_tick_counts.pop(iid, None)
        game_state.resolved_incidents += 1


def _resolve_assigned_incidents(game_state: GameState) -> None:
    now = time.time()
    to_remove = []
    for incident in list(game_state.incidents.values()):
        if incident.assigned_resource_id is None:
            continue
        assign_time = _assignment_times.get(incident.id)
        if assign_time is None:
            continue
        if now - assign_time >= RESOLVE_TIME:
            game_state.lives_saved += incident.lives_at_risk
            resource = game_state.resources.get(incident.assigned_resource_id)
            if resource:
                resource.status = "returning"
                resource.cooldown_until = now + COOLDOWN_DURATION
                resource.assigned_incident_id = None
            game_state.zones[incident.zone_id].severity = 0
            game_state.zones[incident.zone_id].incident_id = None
            incident.resolved_at = now
            to_remove.append(incident.id)

    for iid in to_remove:
        del game_state.incidents[iid]
        _assignment_times.pop(iid, None)
        _severity4_tick_counts.pop(iid, None)
        game_state.resolved_incidents += 1


def _update_cooldowns(game_state: GameState) -> None:
    now = time.time()
    for resource in game_state.resources.values():
        if resource.status == "returning" and now >= resource.cooldown_until:
            resource.status = "idle"
            resource.cooldown_until = 0.0


def record_assignment_time(incident_id: str) -> None:
    _assignment_times[incident_id] = time.time()


def get_stats(game_state: GameState) -> dict:
    return {
        "lives_saved": game_state.lives_saved,
        "lives_lost": game_state.lives_lost,
        "total_incidents": game_state.total_incidents,
        "resolved_incidents": game_state.resolved_incidents,
        "active_incidents": len(game_state.incidents),
    }


async def simulation_loop(game_state: GameState) -> None:
    while True:
        await asyncio.sleep(TICK_INTERVAL)
        game_state.tick += 1
        await enqueue_tick(game_state.tick)


def process_tick(game_state: GameState) -> None:
    _spawn_incident(game_state)
    _escalate_incidents(game_state)
    _resolve_assigned_incidents(game_state)
    _update_cooldowns(game_state)
    _auto_fail_incidents(game_state)
