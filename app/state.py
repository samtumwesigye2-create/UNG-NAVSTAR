from datetime import datetime, timezone
from fastapi import WebSocket
from .schemas import Observation, SpacecraftState, BoundaryState, SceneDelta, TwinSnapshot

class TwinState:
    def __init__(self):
        self.observations: dict[str, Observation] = {}
        self.spacecraft: dict[str, SpacecraftState] = {}
        self.boundaries: dict[str, BoundaryState] = {
            "BOW_SHOCK": BoundaryState(boundary_type="BOW_SHOCK", standoff_re=14.5),
            "MAGNETOPAUSE": BoundaryState(boundary_type="MAGNETOPAUSE", standoff_re=10.0),
            "MAGNETOTAIL": BoundaryState(boundary_type="MAGNETOTAIL", standoff_re=25.0),
        }
        self.sequence=0
        self.clients: set[WebSocket]=set()

    def snapshot(self):
        return TwinSnapshot(simulation_time=datetime.now(timezone.utc), sequence=self.sequence,
            observations=list(self.observations.values()), spacecraft=list(self.spacecraft.values()), boundaries=list(self.boundaries.values()))

    async def publish(self, updated):
        self.sequence += 1
        delta=SceneDelta(sequence=self.sequence, simulation_time=datetime.now(timezone.utc), updated=updated)
        dead=[]
        for ws in self.clients:
            try: await ws.send_json(delta.model_dump(mode="json"))
            except Exception: dead.append(ws)
        for ws in dead: self.clients.discard(ws)
        return delta

    async def add_observation(self, obs: Observation):
        self.observations[obs.id]=obs
        # Phase-1 dynamic boundary response: pressure observations deform the simple parametric surfaces.
        if obs.measurement_type == "solar_wind_dynamic_pressure" and isinstance(obs.value, (int,float)) and obs.value > 0:
            p=float(obs.value)
            self.boundaries["MAGNETOPAUSE"].standoff_re=max(6.0,min(15.0,10.0*(2.0/p)**(1/6)))
            self.boundaries["BOW_SHOCK"].standoff_re=self.boundaries["MAGNETOPAUSE"].standoff_re+4.5
        return await self.publish([{"type":"observation","data":obs.model_dump(mode="json")},{"type":"boundaries","data":[b.model_dump(mode="json") for b in self.boundaries.values()]}])

    async def add_spacecraft(self, state: SpacecraftState):
        self.spacecraft[state.spacecraft_id]=state
        return await self.publish([{"type":"spacecraft","data":state.model_dump(mode="json")}])

twin=TwinState()
