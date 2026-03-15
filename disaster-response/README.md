# Disaster Response Coordination System

A real-time multiplayer web app where multiple users simultaneously coordinate emergency response on an animated city grid during a live disaster simulation. All connected clients see the same live state synced via WebSockets.

## Features

- **Animated City Grid**: 10x10 grid with zones colored by severity (green to red)
- **Emergency Resources**: Ambulances, fire trucks, and shelters shown as icons on the grid
- **Auto-Spawning Incidents**: Fires, collapses, and medical emergencies spawn automatically
- **Resource Assignment**: Click a resource, then click a zone to assign it to an incident
- **Conflict Resolution**: If two users assign the same resource simultaneously, the backend picks the higher-priority incident
- **Central Event Queue**: All simulation ticks and user actions processed in order
- **Global Stats Bar**: Lives saved, active incidents, connected users, simulation tick
- **Live Activity Feed**: Last 10 events with timestamps and color-coded types
- **Real-Time Sync**: All clients update within ~100ms of any state change

## Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3.11+, FastAPI, uvicorn    |
| Frontend | React 18, Vite, plain CSS modules |
| State    | In-memory (no database)           |
| Sync     | WebSocket broadcast               |

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### Backend

```bash
cd disaster-response/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The backend runs at http://localhost:8000.

### Frontend

```bash
cd disaster-response/frontend
npm install
npm run dev
```

The frontend runs at http://localhost:5173.

### Verify

- Backend health: http://localhost:8000/
- Full state dump: http://localhost:8000/health
- Open http://localhost:5173 in your browser

## API

| Endpoint       | Method    | Description              |
|----------------|-----------|--------------------------|
| `/`            | GET       | Status and current tick  |
| `/health`      | GET       | Full game state as JSON  |
| `/ws`          | WebSocket | Real-time game sync      |

### WebSocket Messages

**Server to Client:**
- `state_sync` — full game state
- `activity` — single activity log entry
- `error` — error message

**Client to Server:**
- `assign` — `{resource_id, zone_id}`
- `ping` — keepalive

## How to Play

1. Start both the backend and frontend servers
2. Open http://localhost:5173 in your browser
3. Watch incidents spawn on the grid (colored zones)
4. Click a resource icon (ambulance, fire truck, or shelter) to select it
5. Click a zone with an active incident to assign the resource
6. The resource will respond for 5 seconds, then resolve the incident
7. Unresolved incidents escalate in severity and eventually fail
8. Press Escape to deselect a resource

## Multiplayer Demo

To see the real-time multiplayer sync in action:

1. Start the backend and frontend servers as described above
2. Open **two browser windows** side by side, both at http://localhost:5173
3. Both windows will show the same live simulation state
4. The "Connected Users" counter in the stats bar will show 2
5. In one window, select a resource and assign it to an incident
6. Watch the assignment appear instantly in the other window
7. Try assigning the same resource from both windows at the same time — the backend will resolve the conflict by picking the higher-severity incident
8. The activity feed in both windows will show a "conflict" entry when this happens

This demonstrates the full real-time sync: every state change on the backend is broadcast to all connected clients within ~100ms.
