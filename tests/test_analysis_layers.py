from app.analysis_layers import *
def test_fusion(): assert round(fuse_measurements([{"id":"a","value":2,"confidence":1},{"id":"b","value":4,"confidence":1}])["value"],2)==3
def test_proximity(): assert proximity([{"id":"a","x":0,"y":0,"z":0},{"id":"b","x":.5,"y":0,"z":0}],1)["approaches"]
def test_correlation_not_causation(): assert correlation_explorer([{"id":"a"},{"id":"b"}])["edges"][0]["causation"] is False
def test_resilience(): assert not resilience([{"id":"a"},{"id":"b"}],[{"a":"a","b":"b"}],"a")["remaining_links"]
def test_search(): assert search_catalog("sat",[{"id":"SAT-1","type":"spacecraft"}])


def test_trajectory_dynamics_contract():
    from app.analysis_layers import trajectory_dynamics
    x=trajectory_dynamics({"id":"SC-1"},720)
    assert x["samples"]==720
    assert "monte_carlo" in x["layers"]
    assert x["provenance"]=="MODELED"

def test_model_learning_diagnostics_contract():
    from app.analysis_layers import model_learning_diagnostics
    x=model_learning_diagnostics(.7,1.0)
    assert round(x["loss"],2)==.09
    assert "backpropagation" in x["learning_flow"]
    assert x["operational_model_changed"] is False
    assert x["promotion"]=="REQUIRES_VALIDATION"
