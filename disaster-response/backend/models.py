from pydantic import BaseModel
from typing import Optional


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
