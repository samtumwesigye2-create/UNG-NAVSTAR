from app.engines import particle_field,forecast,nav_solution,comms,mission_check,correlate,scientific_probe,health
def test_physics_forecast(): assert forecast(4)["horizons"][0]["magnetopause_re"] < 10
def test_particles(): assert particle_field(2,-5)["field_vector"]["z"] == -5
def test_nav(): assert nav_solution({"x":0,"y":0,"z":0},{"x":3,"y":4,"z":0})["remaining_distance_re"] == 5
def test_comms(): assert comms([{"id":"a","x":0,"y":0,"z":0},{"id":"b","x":1,"y":0,"z":0}])["links"][0]["geometric_available"]
def test_mission_conflict(): assert mission_check([{"id":"a","spacecraft_id":"s","start":"1","end":"3"},{"id":"b","spacecraft_id":"s","start":"2","end":"4"}])["status"]=="CONFLICT"
def test_correlation_no_causation(): assert not correlate([{"id":"a"},{"id":"b"}])["correlations"][0]["causation_claimed"]
def test_probe_health(): assert scientific_probe({"x":1,"y":2,"z":3})["provenance"]=="MODELED" and health()["navigation"]=="UP"
