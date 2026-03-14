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
