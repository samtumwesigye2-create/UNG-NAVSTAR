import os
from fastapi import APIRouter, Depends, HTTPException, Request
from .security import require_api_key
from .production import audit, configured_feeds, ingest, replay
p=APIRouter(prefix="/api/v1/production",tags=["production"])

@p.get("/feeds")
def feeds(_:None=Depends(require_api_key)): return {"feeds":{k:bool(v) for k,v in configured_feeds().items()}}

@p.post("/ingest/{feed}")
def run_ingest(feed:str, request:Request, _:None=Depends(require_api_key)):
 urls=configured_feeds()
 if feed not in urls or not urls[feed]: raise HTTPException(409,"feed is not configured")
 audit("INGEST_REQUEST",request.client.host if request.client else "unknown",{"feed":feed})
 return {"feed":feed,"data":ingest(urls[feed],feed)}

@p.get("/replay/{kind}")
def get_replay(kind:str, _:None=Depends(require_api_key)): return {"kind":kind,"records":replay(kind)}

@p.get("/audit")
def get_audit(_:None=Depends(require_api_key)): return {"records":replay("audit")}
