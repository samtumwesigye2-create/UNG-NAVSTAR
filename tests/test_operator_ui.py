from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_analysis_ui_served():
 r=client.get("/"); assert r.status_code==200; assert "relationship-graph" in r.text; assert "Analysis Layers" in r.text
def test_relationship_api():
 r=client.post("/api/v1/analysis/relationship-graph",json={"nodes":[{"id":"NAVSTAR"}],"edges":[]}); assert r.status_code==200; assert r.json()["interrogable"] is True
