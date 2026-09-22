import os
from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_3d(): r=c.get("/3d"); assert r.status_code==200 and "NAVSTAR 3D DIGITAL TWIN" in r.text
def test_prod_unlocked_without_key(monkeypatch):
 monkeypatch.delenv("NAVSTAR_API_KEY",raising=False); r=c.get("/api/v1/production/feeds"); assert r.status_code==200
def test_prod_locked(monkeypatch):
 monkeypatch.setenv("NAVSTAR_API_KEY","secret"); r=c.get("/api/v1/production/feeds"); assert r.status_code==401
def test_prod_key(monkeypatch):
 monkeypatch.setenv("NAVSTAR_API_KEY","secret"); r=c.get("/api/v1/production/feeds",headers={"X-API-Key":"secret"}); assert r.status_code==200
