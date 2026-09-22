from __future__ import annotations
from datetime import datetime, timezone
from math import sqrt
from typing import Any

def particle_field(pressure: float=2.0, imf_bz: float=0.0):
    density=max(.1,5.0*pressure/2.0)
    return {"solar_wind_pressure_npa":pressure,"imf_bz_nt":imf_bz,"density_index":density,
            "field_vector":{"x":-pressure,"y":0.0,"z":imf_bz},"provenance":"MODELED"}

def forecast(pressure: float=2.0):
    horizons=[15,60,180,360,720,1440]
    return {"initialized_at":datetime.now(timezone.utc).isoformat(),"ensemble_size":5,
      "horizons":[{"minutes":m,"magnetopause_re":max(6,min(15,10*(2/max(.1,pressure))**(1/6))),
      "uncertainty_re":round(.15+.00035*m,3)} for m in horizons],
      "physics_model":"phase1-parametric-v1","ml_model":"navstar-residual-baseline-v1","provenance":"FORECAST"}

def nav_solution(origin: dict, destination: dict):
    dx=destination["x"]-origin["x"]; dy=destination["y"]-origin["y"]; dz=destination["z"]-origin["z"]
    d=sqrt(dx*dx+dy*dy+dz*dz)
    return {"position":origin,"destination":destination,"remaining_distance_re":d,
      "trajectory":[origin,{"x":origin["x"]+dx/2,"y":origin["y"]+dy/2,"z":origin["z"]+dz/2},destination],
      "uncertainty_re":0.05,"provenance":"DERIVED"}

def comms(nodes: list[dict]):
    links=[]
    for i,a in enumerate(nodes):
      for b in nodes[i+1:]:
        d=sqrt(sum((a[k]-b[k])**2 for k in ("x","y","z")))
        links.append({"a":a["id"],"b":b["id"],"range_re":d,"geometric_available":d<80})
    return {"links":links,"note":"Geometric availability only; not a confirmed radio link."}

def mission_check(activities:list[dict]):
    conflicts=[]
    ordered=sorted(activities,key=lambda x:x.get("start",""))
    for a,b in zip(ordered,ordered[1:]):
      if a.get("spacecraft_id")==b.get("spacecraft_id") and a.get("end","")>b.get("start",""):
        conflicts.append({"a":a.get("id"),"b":b.get("id"),"type":"TIME_OVERLAP"})
    return {"activities":activities,"conflicts":conflicts,"status":"CONFLICT" if conflicts else "FEASIBLE"}

def correlate(events:list[dict]):
    return {"event_count":len(events),"correlations":[{"left":events[i].get("id"),"right":events[i+1].get("id"),
      "relation":"TEMPORAL_ASSOCIATION","causation_claimed":False} for i in range(max(0,len(events)-1))]}

def scientific_probe(position:dict, pressure:float=2.0, imf_bz:float=0.0):
    return {"position":position,"sample":particle_field(pressure,imf_bz),"provenance":"MODELED"}

def health():
    return {"gateway":"UP","twin_state":"UP","physics":"UP","particles":"UP","forecast":"UP","ai":"BASELINE",
      "navigation":"UP","comms":"UP","mission":"UP","events":"UP","scientific_lab":"UP","integrations":"ADAPTER_READY"}
