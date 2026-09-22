import json, os, sqlite3
from pathlib import Path
DB_PATH=Path(os.getenv("NAVSTAR_DB","data/navstar.db"))
def _db():
 DB_PATH.parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(DB_PATH); c.execute("CREATE TABLE IF NOT EXISTS records(kind TEXT,id TEXT,ts TEXT,payload TEXT,PRIMARY KEY(kind,id))"); return c
def put(kind,id,ts,payload):
 with _db() as c:c.execute("INSERT OR REPLACE INTO records VALUES(?,?,?,?)",(kind,id,ts,json.dumps(payload)))
def get(kind,id):
 with _db() as c:
  r=c.execute("SELECT payload FROM records WHERE kind=? AND id=?",(kind,id)).fetchone(); return json.loads(r[0]) if r else None
def list_kind(kind,limit=100):
 with _db() as c:return [json.loads(r[0]) for r in c.execute("SELECT payload FROM records WHERE kind=? ORDER BY ts DESC LIMIT ?",(kind,limit))]
