from app.persistence import put,get
from app.adapters import adapter_status
def test_persistence(tmp_path,monkeypatch):
 import app.persistence as p
 monkeypatch.setattr(p,"DB_PATH",tmp_path/"x.db"); put("event","e1","2026-01-01",{"id":"e1"}); assert get("event","e1")["id"]=="e1"
def test_adapter_status(): assert "constellation_url_configured" in adapter_status()
