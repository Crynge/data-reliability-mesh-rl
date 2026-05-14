from __future__ import annotations

import sys

import httpx


def main() -> int:
    base = "http://127.0.0.1:8014"
    with httpx.Client(timeout=20.0) as client:
        health = client.get(f"{base}/health")
        overview = client.get(f"{base}/api/overview")
        incident = client.get(f"{base}/api/incidents/stg_campaign_attribution")

    if health.status_code != 200:
        raise SystemExit("health check failed")
    if overview.status_code != 200 or "mesh_health_score" not in overview.json():
        raise SystemExit("overview check failed")
    if incident.status_code != 200 or "decision" not in incident.json():
        raise SystemExit("incident check failed")

    print("api smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

