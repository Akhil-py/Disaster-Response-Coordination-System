from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import uuid


class Zone(BaseModel):
    id: str
    row: int
    col: int
    severity: int = 0
    incident_id: Optional[str] = None


class Incident(BaseModel):
    id: str
    type: str
    zone_id: str
    severity: int
    spawned_at: float
    resolved_at: Optional[float] = None
    assigned_resource_id: Optional[str] = None
    lives_at_risk: int


class Resource(BaseModel):
    id: str
    type: str
    zone_id: str
    status: str = "idle"
    assigned_incident_id: Optional[str] = None
    cooldown_until: float = 0.0


class GameState(BaseModel):
    zones: Dict[str, Zone] = Field(default_factory=dict)
    incidents: Dict[str, Incident] = Field(default_factory=dict)
    resources: Dict[str, Resource] = Field(default_factory=dict)
    lives_saved: int = 0
    lives_lost: int = 0
    total_incidents: int = 0
    resolved_incidents: int = 0
    connected_users: int = 0
    tick: int = 0
    activity_log: List[dict] = Field(default_factory=list)


def initial_game_state() -> GameState:
    zones: Dict[str, Zone] = {}
    for row in range(10):
        for col in range(10):
            zone_id = f"zone_{row}_{col}"
            zones[zone_id] = Zone(id=zone_id, row=row, col=col)

    resources: Dict[str, Resource] = {}

    ambulance_positions = ["zone_0_0", "zone_5_0", "zone_9_9"]
    for zone_id in ambulance_positions:
        rid = str(uuid.uuid4())
        resources[rid] = Resource(id=rid, type="ambulance", zone_id=zone_id)

    fire_truck_positions = ["zone_0_9", "zone_5_5", "zone_9_0"]
    for zone_id in fire_truck_positions:
        rid = str(uuid.uuid4())
        resources[rid] = Resource(id=rid, type="fire_truck", zone_id=zone_id)

    shelter_positions = ["zone_2_2", "zone_7_7"]
    for zone_id in shelter_positions:
        rid = str(uuid.uuid4())
        resources[rid] = Resource(id=rid, type="shelter", zone_id=zone_id)

    return GameState(zones=zones, resources=resources)
