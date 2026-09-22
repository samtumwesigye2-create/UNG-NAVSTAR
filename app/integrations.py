from datetime import datetime, timezone
def constellation_product(spacecraft:list):
    return {"source":"CONSTELLATION","timestamp":datetime.now(timezone.utc).isoformat(),"spacecraft":spacecraft,
            "contract":"NAVSTAR spacecraft/orbit-state adapter"}
def orion_product(snapshot:dict, active_events:list|None=None):
    return {"destination":"ORION","timestamp":datetime.now(timezone.utc).isoformat(),
      "summary":{"sequence":snapshot.get("sequence"),"spacecraft_count":len(snapshot.get("spacecraft",[])),
      "active_event_count":len(active_events or [])},"provenance":"DERIVED"}
