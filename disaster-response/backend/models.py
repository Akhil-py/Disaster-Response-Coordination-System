from pydantic import BaseModel, Field
from typing import Optional, Dict, List


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
