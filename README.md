# Disaster Response Coordination System

A real-time multiplayer dashboard where multiple users coordinate emergency response across a city grid during a simulated disaster. The simulation runs continuously in the background — incidents spawn, resources deplete, priorities shift — and every connected user sees it live.

## What You See (Frontend)

- An animated city map with color-coded zones (severity levels)
- Emergency resources (ambulances, fire trucks, shelters) as moving icons
- Incident cards popping up in real-time (building collapse, fire, medical emergency)
- Other users' cursors/actions visible live
- A global stats bar: lives saved, response time avg, resources deployed
- Controls to assign resources, declare a zone critical, or trigger a new disaster event

## What's Happening Under the Hood (Backend)

- **WebSocket server** — pushes state to all clients in real-time, syncs actions
- **Simulation engine** — continuously spawns incidents, ages them, escalates unhandled ones
- **Resource allocation algorithm** — pathfinding (Dijkstra/A*) to route resources optimally
- **Conflict resolution** — if two users assign the same resource, backend arbitrates based on priority score
- **Event queue** — all user actions and simulation ticks go through a central queue, processed in order

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python (FastAPI + WebSockets) |
| Frontend | React + Leaflet (or canvas grid) |
| State sync | WebSocket broadcast with event sourcing |
| Database | None — fully in-memory, zero setup friction |

## The Demo Moment

Open two browser windows side by side, hand one to someone else, and say _"there's a fire in Zone 3 and only one truck — we both just tried to send it there, watch what happens."_ The system resolves it, reroutes, and the simulation keeps running.
