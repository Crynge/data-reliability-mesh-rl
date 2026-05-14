from src.data_reliability_mesh import ReliabilityMeshEngine


def test_overview_contains_health_score() -> None:
    engine = ReliabilityMeshEngine()
    overview = engine.overview()
    assert overview["mesh_health_score"] > 0
    assert overview["highest_risk_assets"]


def test_incident_report_contains_decision() -> None:
    engine = ReliabilityMeshEngine()
    report = engine.incident_report("stg_campaign_attribution")
    assert report["decision"]["action"] in {
        "REBUILD",
        "BACKFILL",
        "SKIP",
        "ALERT_HUMAN",
        "USE_FALLBACK",
        "ROLLBACK",
        "INCREASE_ALERT_THRESHOLD",
    }
    assert report["blast_radius"]

