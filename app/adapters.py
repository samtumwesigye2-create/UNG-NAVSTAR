import os, json, urllib.request
def fetch_json(url:str,timeout:float=5):
 req=urllib.request.Request(url,headers={"User-Agent":"UNG-NAVSTAR/1.0"})
 with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)
def adapter_status():
 return {"constellation_url_configured":bool(os.getenv("CONSTELLATION_URL")),"orion_url_configured":bool(os.getenv("ORION_URL")),"space_weather_url_configured":bool(os.getenv("SPACE_WEATHER_URL"))}
