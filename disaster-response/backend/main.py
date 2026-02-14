import asyncio
import json
import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models import initial_game_state
from broadcaster import serialize_state, add_connection, remove_connection, broadcast, active_connections
from event_queue import enqueue_action, consumer_loop, UserAction
from simulation import simulation_loop, process_tick, record_assignment_time, _add_log
from conflict import register_assign, has_conflict, resolve_conflict, log_conflict_entries, clear_pending

logger = logging.getLogger(__name__)

game_state = initial_game_state()


async def _on_tick() -> None:
    process_tick(game_state)
    await broadcast(game_state)


async def _on_action(action: UserAction) -> None:
    if action.action_type == "assign":
        resource = game_state.resources.get(action.resource_id)
        if not resource:
            return
        if resource.status != "idle":
            return

        zone = game_state.zones.get(action.zone_id)
        if not zone:
            return
        if not zone.incident_id:
            return

        incident = game_state.incidents.get(zone.incident_id)
        if not incident:
            return
        if incident.assigned_resource_id is not None:
            return

        register_assign(action)
        if has_conflict(action.resource_id):
            winner, losers = resolve_conflict(action.resource_id, game_state)
            log_conflict_entries(losers, game_state)
            action = winner

        resource.status = "responding"
        resource.assigned_incident_id = incident.id
        resource.zone_id = action.zone_id
        incident.assigned_resource_id = resource.id
        record_assignment_time(incident.id)

        _add_log(
            game_state,
            f"{resource.type.upper()} assigned to {incident.type} at {zone.id}",
            "assign",
        )
        clear_pending()

    await broadcast(game_state)


@asynccontextmanager
async def lifespan(app: FastAPI):
    sim_task = asyncio.create_task(simulation_loop(game_state))
    queue_task = asyncio.create_task(consumer_loop(_on_tick, _on_action))
    yield
    sim_task.cancel()
    queue_task.cancel()


app = FastAPI(title="Disaster Response Coordination", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "tick": game_state.tick}


@app.get("/health")
async def health():
    return serialize_state(game_state)


async def _handle_disconnect(ws: WebSocket) -> None:
    remove_connection(ws)
    game_state.connected_users = max(0, game_state.connected_users - 1)
    await broadcast(game_state)


async def _handle_message(ws: WebSocket, raw: str) -> None:
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        await ws.send_text(json.dumps({
            "type": "error",
            "payload": {"message": "Invalid JSON"},
        }))
        return

    msg_type = msg.get("type")
    payload = msg.get("payload", {})

    if msg_type == "assign":
        resource_id = payload.get("resource_id")
        zone_id = payload.get("zone_id")
        if resource_id and zone_id:
            await enqueue_action("assign", resource_id=resource_id, zone_id=zone_id)
        else:
            await ws.send_text(json.dumps({
                "type": "error",
                "payload": {"message": "assign requires resource_id and zone_id"},
            }))
    elif msg_type == "ping":
        pass
    else:
        await ws.send_text(json.dumps({
            "type": "error",
            "payload": {"message": f"Unknown message type: {msg_type}"},
        }))


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    add_connection(ws)
    game_state.connected_users += 1

    state_msg = json.dumps({
        "type": "state_sync",
        "payload": serialize_state(game_state),
    })
    await ws.send_text(state_msg)
    await broadcast(game_state)

    try:
        while True:
            data = await ws.receive_text()
            await _handle_message(ws, data)
    except WebSocketDisconnect:
        await _handle_disconnect(ws)
    except Exception:
        await _handle_disconnect(ws)
