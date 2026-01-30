from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SimTick:
    tick: int


@dataclass
class UserAction:
    action_type: str
    resource_id: Optional[str] = None
    zone_id: Optional[str] = None
    arrival_order: int = 0
