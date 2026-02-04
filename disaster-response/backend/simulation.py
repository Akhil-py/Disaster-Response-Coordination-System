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

_severity4_tick_counts: dict[str, int] = {}


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


async def simulation_loop(game_state: GameState) -> None:
    while True:
        await asyncio.sleep(TICK_INTERVAL)
        game_state.tick += 1
        await enqueue_tick(game_state.tick)


def process_tick(game_state: GameState) -> None:
    _spawn_incident(game_state)
    _escalate_incidents(game_state)
    _auto_fail_incidents(game_state)
