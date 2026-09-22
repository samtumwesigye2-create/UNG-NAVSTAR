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
