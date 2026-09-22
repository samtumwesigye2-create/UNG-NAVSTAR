from fastapi import APIRouter
from pydantic import BaseModel
from .engines import particle_field, forecast, nav_solution, comms, mission_check, correlate, scientific_probe, health
from .integrations import constellation_product, orion_product
from .state import twin

r=APIRouter(prefix="/api/v1")
class Pressure(BaseModel): pressure: float=2.0; imf_bz: float=0.0
class NavReq(BaseModel): origin:dict; destination:dict
class Nodes(BaseModel): nodes:list[dict]
class Mission(BaseModel): activities:list[dict]
class Events(BaseModel): events:list[dict]
class Probe(BaseModel): position:dict; pressure:float=2.0; imf_bz:float=0.0

@r.post("/simulation/field")
def field(x:Pressure): return particle_field(x.pressure,x.imf_bz)
@r.post("/forecast")
def fc(x:Pressure): return forecast(x.pressure)
@r.post("/navigation/solve")
def nav(x:NavReq): return nav_solution(x.origin,x.destination)
@r.post("/comms/analyze")
def cm(x:Nodes): return comms(x.nodes)
@r.post("/mission/check")
def mission(x:Mission): return mission_check(x.activities)
@r.post("/events/correlate")
def events(x:Events): return correlate(x.events)
@r.post("/lab/probe")
def probe(x:Probe): return scientific_probe(x.position,x.pressure,x.imf_bz)
@r.get("/system/health")
def syshealth(): return health()
@r.get("/integrations/constellation")
def constellation(): return constellation_product([s.model_dump(mode="json") for s in twin.spacecraft.values()])
@r.get("/integrations/orion")
def orion(): return orion_product(twin.snapshot().model_dump(mode="json"))

from .analysis_layers import relationship_graph, magnetic_connectivity, lineage, uncertainty_heatmap, forecast_ghosts, correlation_explorer, coverage_shells, fuse_measurements, spacecraft_bubble, proximity, route_risk, comms_mesh, resilience, twin_difference, model_battle, anomaly_constellations, explain_object, bookmark, mission_record, search_catalog, trajectory_dynamics, model_learning_diagnostics, model_training_history

@r.post("/analysis/{layer}")
def analysis_layer(layer:str, body:dict):
    table={
      "relationship-graph":lambda:relationship_graph(body.get("nodes",[]),body.get("edges",[])),
      "magnetic-connectivity":lambda:magnetic_connectivity(body.get("points",[])),
      "lineage":lambda:lineage(body),
      "uncertainty-heatmap":lambda:uncertainty_heatmap(body.get("samples",[])),
      "forecast-ghosts":lambda:forecast_ghosts(body.get("states",[])),
      "correlations":lambda:correlation_explorer(body.get("events",[])),
      "coverage-shells":lambda:coverage_shells(body.get("sensors",[])),
      "sensor-fusion":lambda:fuse_measurements(body.get("measurements",[])),
      "spacecraft-bubble":lambda:spacecraft_bubble(body),
      "proximity":lambda:proximity(body.get("objects",[]),body.get("threshold",1.0)),
      "route-risk":lambda:route_risk(body.get("samples",[])),
      "comms-mesh":lambda:comms_mesh(body.get("nodes",[]),body.get("links",[])),
      "resilience":lambda:resilience(body.get("nodes",[]),body.get("links",[]),body.get("remove_id","")),
      "twin-difference":lambda:twin_difference(body.get("a",{}),body.get("b",{})),
      "model-battle":lambda:model_battle(body.get("models",[])),
      "anomaly-constellations":lambda:anomaly_constellations(body.get("events",[])),
      "explain":lambda:explain_object(body),
      "bookmark":lambda:bookmark(body),
      "mission-record":lambda:mission_record(body.get("frames",[])),
      "search":lambda:search_catalog(body.get("query",""),body.get("objects",[])),
      "trajectory-dynamics":lambda:trajectory_dynamics(body.get("body",{}),body.get("samples",360)),
      "model-learning":lambda:model_learning_diagnostics(float(body.get("prediction",0)),float(body.get("target",0)),body.get("model_version","navstar-residual-baseline-v1")),
      "model-training-history":lambda:model_training_history(body.get("points",[]))
    }
    if layer not in table:
      from fastapi import HTTPException
      raise HTTPException(404,"unknown analysis layer")
    return table[layer]()
