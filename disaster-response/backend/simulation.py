import asyncio
import logging
from models import GameState
from event_queue import enqueue_tick

logger = logging.getLogger(__name__)

TICK_INTERVAL = 2.0


async def simulation_loop(game_state: GameState) -> None:
    while True:
        await asyncio.sleep(TICK_INTERVAL)
        game_state.tick += 1
        await enqueue_tick(game_state.tick)


def process_tick(game_state: GameState) -> None:
    pass
