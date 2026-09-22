# UNG-NAVSTAR

**Navigation, Analysis, Visualization, Space Tracking & Astronomical Reconnaissance**

Phase 1 establishes the Digital Twin Core: canonical state schemas, an in-memory authoritative twin-state service, snapshot APIs, provenance, and a WebSocket delta stream.

## Run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` and API docs at `/docs`.

## Phase-1 acceptance path

POST an observation or spacecraft state -> Twin State updates -> a `SceneDelta` is broadcast over `/api/v1/twin/stream` -> connected clients update without refresh.
