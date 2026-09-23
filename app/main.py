from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from .routes import r
from .production_routes import p
from .schemas import Observation, SpacecraftState
from .state import twin
from .frame_propagation import register_frame, convert_position, link_timing

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

@app.post("/api/v1/frames/register")
def frame_register(body: dict):
    return register_frame(body["source"],body["destination"],body["matrix"],body.get("timestamp"),body.get("version","ung-frame-v1"))

@app.post("/api/v1/frames/convert")
def frame_convert(body: dict):
    return convert_position(body["position"],body["source"],body["destination"])

@app.post("/api/v1/propagation/link")
def propagation_link(body: dict):
    return link_timing(body["origin_m"],body["destination_m"],float(body.get("speed_mps",299792458.0)))

@app.get("/3d",response_class=HTMLResponse)
def webgl():
    return FileResponse("app/webgl.html")

@app.get("/",response_class=HTMLResponse)
def home():
    return FileResponse("app/operator.html")
