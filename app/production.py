from __future__ import annotations
import json, os, time, urllib.request
from datetime import datetime, timezone
from .persistence import put, list_kind

def audit(action:str, actor:str="system", detail:dict|None=None):
 r={"id":f"audit-{time.time_ns()}","timestamp":datetime.now(timezone.utc).isoformat(),"action":action,"actor":actor,"detail":detail or {}}
 put("audit",r["id"],r); return r

def ingest(url:str, kind:str):
 req=urllib.request.Request(url,headers={"User-Agent":"UNG-NAVSTAR/1.0"})
 with urllib.request.urlopen(req,timeout=5) as resp: data=json.load(resp)
 rid=str(data.get("id",f"{kind}-{time.time_ns()}")) if isinstance(data,dict) else f"{kind}-{time.time_ns()}"
 put(kind,rid,{"id":rid,"payload":data,"ingested_at":datetime.now(timezone.utc).isoformat()}); audit("INGEST",detail={"kind":kind,"id":rid}); return data

def configured_feeds():
 return {k:os.getenv(v,"") for k,v in {"constellation":"CONSTELLATION_URL","orion":"ORION_URL","space_weather":"SPACE_WEATHER_URL"}.items()}

def replay(kind:str): return list_kind(kind)
