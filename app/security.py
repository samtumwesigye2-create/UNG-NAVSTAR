import hmac, os
from fastapi import Header, HTTPException

def require_api_key(x_api_key:str|None=Header(default=None)):
 expected=os.getenv("NAVSTAR_API_KEY","").strip()
 if not expected: return None
 if not x_api_key or not hmac.compare_digest(x_api_key,expected): raise HTTPException(401,"invalid API key")
 return None
