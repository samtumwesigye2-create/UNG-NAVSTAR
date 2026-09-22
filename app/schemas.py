from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import uuid4
from pydantic import BaseModel, Field

class Provenance(str, Enum):
    MEASURED="MEASURED"; DERIVED="DERIVED"; ASSIMILATED="ASSIMILATED"; MODELED="MODELED"; FORECAST="FORECAST"; SIMULATED="SIMULATED"

class Vec3(BaseModel):
    x: float; y: float; z: float

class Uncertainty(BaseModel):
    sigma: float | None = None
    covariance: list[list[float]] | None = None

class Observation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    sensor_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    measurement_type: str
    value: float | Vec3
    units: str
    coordinate_frame: str = "GSM"
    provenance: Provenance = Provenance.MEASURED
    quality: float = Field(default=1.0, ge=0, le=1)
    uncertainty: Uncertainty | None = None

class SpacecraftState(BaseModel):
    spacecraft_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    position: Vec3
    velocity: Vec3
    coordinate_frame: str = "GSM"
    provenance: Provenance = Provenance.MEASURED
    uncertainty: Uncertainty | None = None

class BoundaryState(BaseModel):
    boundary_type: Literal["BOW_SHOCK","MAGNETOPAUSE","MAGNETOTAIL"]
    standoff_re: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Provenance = Provenance.MODELED
    model_version: str = "phase1-parametric-v1"

class TwinEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    schema_version: str = "1.0"
    source_service: str = "twin-state"
    event_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sequence_number: int
    provenance: Provenance
    payload: dict[str, Any]

class SceneDelta(BaseModel):
    sequence: int
    simulation_time: datetime
    created: list[dict[str, Any]] = []
    updated: list[dict[str, Any]] = []
    removed: list[str] = []

class TwinSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: str(uuid4()))
    simulation_time: datetime
    sequence: int
    observations: list[Observation]
    spacecraft: list[SpacecraftState]
    boundaries: list[BoundaryState]
