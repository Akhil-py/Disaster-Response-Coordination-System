import asyncio
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class SimTick:
    tick: int


@dataclass
class UserAction:
    action_type: str
    resource_id: Optional[str] = None
    zone_id: Optional[str] = None
    arrival_order: int = 0


event_queue: asyncio.Queue = asyncio.Queue(maxsize=200)
_action_counter: int = 0


async def enqueue_tick(tick: int) -> None:
    if event_queue.qsize() > 100:
        try:
            event_queue.get_nowait()
        except asyncio.QueueEmpty:
            pass
    await event_queue.put(SimTick(tick=tick))


async def enqueue_action(action_type: str, resource_id: str = None, zone_id: str = None) -> None:
    global _action_counter
    _action_counter += 1
    if event_queue.qsize() > 100:
        try:
            event_queue.get_nowait()
        except asyncio.QueueEmpty:
            pass
    await event_queue.put(UserAction(
        action_type=action_type,
        resource_id=resource_id,
        zone_id=zone_id,
        arrival_order=_action_counter,
    ))
