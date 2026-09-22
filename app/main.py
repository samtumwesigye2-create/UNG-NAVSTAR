from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from .schemas import Observation, SpacecraftState
from .state import twin

app=FastAPI(title="UNG-NAVSTAR Digital Twin Core",version="0.1.0")

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
    return """<!doctype html><html><head><title>UNG-NAVSTAR</title><style>body{margin:0;background:#050912;color:#d9e7ff;font-family:system-ui}header{padding:18px 24px;border-bottom:1px solid #263248}main{display:grid;grid-template-columns:1fr 320px;height:calc(100vh - 68px)}#scene{display:grid;place-items:center;background:radial-gradient(circle,#12254a,#050912 60%)}.earth{width:240px;height:240px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#69b7ff,#1453a0 45%,#061329 72%);box-shadow:0 0 80px #245dbb}.panel{padding:20px;border-left:1px solid #263248}.tag{font-size:12px;border:1px solid #4e6489;padding:4px 8px;border-radius:20px}</style></head><body><header><b>UNG-NAVSTAR</b> · Digital Twin Core <span class='tag'>LIVE</span></header><main><section id='scene'><div class='earth'></div></section><aside class='panel'><h3>Twin State</h3><pre id='state'>connecting…</pre></aside></main><script>const p=document.getElementById('state');const proto=location.protocol==='https:'?'wss':'ws';const ws=new WebSocket(proto+'://'+location.host+'/api/v1/twin/stream');ws.onmessage=e=>{const x=JSON.parse(e.data);p.textContent=JSON.stringify(x,null,2)};</script></body></html>"""
