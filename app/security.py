import hmac, os
from fastapi import Header, HTTPException
API_KEY=os.getenv("NAVSTAR_API_KEY","")
def require_api_key(x_navstar_key:str|None=Header(default=None)):
 if API_KEY and (not x_navstar_key or not hmac.compare_digest(x_navstar_key,API_KEY)): raise HTTPException(401,"invalid NAVSTAR API key")
 return True
