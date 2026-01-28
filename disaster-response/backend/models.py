from pydantic import BaseModel
from typing import Optional


class Zone(BaseModel):
    id: str
    row: int
    col: int
    severity: int = 0
    incident_id: Optional[str] = None
