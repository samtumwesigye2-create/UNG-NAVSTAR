from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_observation_updates_twin():
    r=client.post("/api/v1/observations",json={"sensor_id":"TEST-SW","measurement_type":"solar_wind_dynamic_pressure","value":4.0,"units":"nPa"})
    assert r.status_code == 200
    s=client.get("/api/v1/twin/snapshot").json()
    assert len(s["observations"]) >= 1
    mp=next(x for x in s["boundaries"] if x["boundary_type"]=="MAGNETOPAUSE")
    assert mp["standoff_re"] < 10.0
