from __future__ import annotations
from math import sqrt
from typing import Any

PROVENANCE={"MEASURED","DERIVED","ASSIMILATED","MODELED","FORECAST","SIMULATED"}

def relationship_graph(nodes:list[dict], edges:list[dict]):
 return {"nodes":nodes,"edges":edges,"interrogable":True}

def magnetic_connectivity(points:list[dict]):
 return {"connections":[{"a":p.get("id"),"b":points[i+1].get("id"),"provenance":"MODELED","uncertainty":p.get("uncertainty",0.2)} for i,p in enumerate(points[:-1])]}

def lineage(product:dict):
 return {"product_id":product.get("id"),"chain":product.get("lineage",[]),"provenance":product.get("provenance","DERIVED")}

def uncertainty_heatmap(samples:list[dict]):
 return {"samples":[{**s,"visual_weight":min(1.0,max(0.0,float(s.get("uncertainty",0))))} for s in samples]}

def forecast_ghosts(states:list[dict]):
 return {"ghosts":[{**s,"render":"TRANSLUCENT","provenance":"FORECAST"} for s in states]}

def correlation_explorer(events:list[dict]):
 return {"nodes":events,"edges":[{"a":events[i].get("id"),"b":events[i+1].get("id"),"relation":"CORRELATED","causation":False} for i in range(len(events)-1)]}

def coverage_shells(sensors:list[dict]):
 return {"shells":[{"sensor_id":s.get("id"),"radius":s.get("range",0),"provenance":"DERIVED"} for s in sensors]}

def fuse_measurements(measurements:list[dict]):
 valid=[m for m in measurements if isinstance(m.get("value"),(int,float))]
 if not valid:return {"value":None,"contributors":[]}
 weights=[max(.0001,float(m.get("confidence",1))) for m in valid]; total=sum(weights)
 return {"value":sum(m["value"]*w for m,w in zip(valid,weights))/total,"contributors":[{"id":m.get("id"),"weight":w/total} for m,w in zip(valid,weights)],"provenance":"ASSIMILATED"}

def spacecraft_bubble(state:dict):
 return {"spacecraft_id":state.get("id"),"environment":state.get("environment",{}),"nav_uncertainty":state.get("uncertainty"),"next_contact":state.get("next_contact"),"links":state.get("links",[])}

def proximity(objects:list[dict],threshold:float=1.0):
 out=[]
 for i,a in enumerate(objects):
  for b in objects[i+1:]:
   d=sqrt(sum((float(a.get(k,0))-float(b.get(k,0)))**2 for k in ("x","y","z")))
   if d<=threshold:out.append({"a":a.get("id"),"b":b.get("id"),"distance":d,"uncertainty":[a.get("uncertainty"),b.get("uncertainty")]})
 return {"approaches":out}

def route_risk(samples:list[dict]):
 return {"corridor":[{**s,"risk_index":min(1.0,max(0.0,float(s.get("environment_risk",0))+.25*float(s.get("uncertainty",0))))} for s in samples]}

def comms_mesh(nodes:list[dict],links:list[dict]): return {"nodes":nodes,"links":links,"confirmed_radio_status_required":True}

def resilience(nodes:list[dict],links:list[dict],remove_id:str):
 kept=[n for n in nodes if n.get("id")!=remove_id]; ids={n.get("id") for n in kept}
 return {"removed":remove_id,"remaining_nodes":kept,"remaining_links":[e for e in links if e.get("a") in ids and e.get("b") in ids]}

def twin_difference(a:dict,b:dict): return {"a":a,"b":b,"comparison":"OVERLAY","provenance_pair":[a.get("provenance"),b.get("provenance")]}

def model_battle(models:list[dict]): return {"models":models,"ranking_deferred_until_observations":True}

def anomaly_constellations(events:list[dict]):
 groups={}
 for e in events: groups.setdefault(e.get("type","UNKNOWN"),[]).append(e)
 return {"groups":[{"type":k,"events":v} for k,v in groups.items()]}

def explain_object(obj:dict):
 return {"what":obj.get("type"),"id":obj.get("id"),"source":obj.get("source"),"last_update":obj.get("timestamp"),"uncertainty":obj.get("uncertainty"),"provenance":obj.get("provenance"),"related":obj.get("related",[]),"forecast":obj.get("forecast"),"history":obj.get("history",[])}

def bookmark(state:dict): return {"camera":state.get("camera"),"time":state.get("time"),"layers":state.get("layers",[]),"selection":state.get("selection")}

def mission_record(frames:list[dict]): return {"frames":frames,"count":len(frames),"immutable_export_ready":True}

def search_catalog(query:str,objects:list[dict]):
 q=query.lower(); return [o for o in objects if q in str(o.get("id","")).lower() or q in str(o.get("name","")).lower() or q in str(o.get("type","")).lower()]


def trajectory_dynamics(body: dict, samples: int = 360):
    """Orbit/trajectory analysis contract: propagated path, resonance diagnostics and uncertainty."""
    return {"body": body, "samples": max(32,min(samples,5000)), "layers":["propagated_trajectory","resonance_pattern","ground_track","uncertainty_cone","monte_carlo"], "provenance":"MODELED"}

def model_learning_diagnostics(prediction: float, target: float, model_version: str = "navstar-residual-baseline-v1"):
    """Visible model-error/backprop diagnostics; never promotes a model automatically."""
    error=prediction-target
    loss=error*error
    return {"model_version":model_version,"prediction":prediction,"target":target,"error":error,"loss":loss,
            "learning_flow":["forward_pass","loss","backpropagation","parameter_update","validation"],
            "promotion":"REQUIRES_VALIDATION","operational_model_changed":False}

def model_training_history(points: list[dict]):
    """Expose train/validation loss history for Model Lab visualization."""
    return {"points":points,"count":len(points),"purpose":"MODEL_LAB","automatic_operational_promotion":False}
