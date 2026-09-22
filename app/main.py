from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from .routes import r
from .production_routes import p
from .schemas import Observation, SpacecraftState
from .state import twin

app=FastAPI(title="UNG-NAVSTAR",version="1.0.0")
app.include_router(r)
app.include_router(p)

@app.get("/health")
def health(): return {"status":"ok","service":"ung-navstar-digital-twin-core"}

@app.get("/ready")
def ready(): return {"ready":True}

@app.get("/api/v1/twin/snapshot")
def snapshot(): return twin.snapshot()

@app.get("/api/v1/twin/state")
def state(): return twin.snapshot()

@app.post("/api/v1/observations")
async def observation(obs: Observation):
    delta=await twin.add_observation(obs); return {"accepted":True,"delta":delta}

@app.post("/api/v1/spacecraft/state")
async def spacecraft(state: SpacecraftState):
    delta=await twin.add_spacecraft(state); return {"accepted":True,"delta":delta}

@app.websocket("/api/v1/twin/stream")
async def stream(ws: WebSocket):
    await ws.accept(); twin.clients.add(ws)
    await ws.send_json({"type":"snapshot","data":twin.snapshot().model_dump(mode="json")})
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect: twin.clients.discard(ws)

@app.get("/",response_class=HTMLResponse)
def home():
    return FileResponse("app/operator.html")
