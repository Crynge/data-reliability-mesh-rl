from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.data_reliability_mesh import ReliabilityMeshEngine

app = FastAPI(title="Data Reliability Mesh RL", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ReliabilityMeshEngine()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "data-reliability-mesh-rl"}


@app.get("/api/overview")
def overview() -> dict:
    return engine.overview()


@app.get("/api/assets")
def assets() -> dict:
    return {"items": engine.list_assets()}


@app.get("/api/contracts")
def contracts() -> dict:
    return {"items": engine.contract_status()}


@app.get("/api/lineage/{asset_id}")
def lineage(asset_id: str) -> dict:
    try:
        return engine.lineage_view(asset_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/incidents/{asset_id}")
def incident(asset_id: str) -> dict:
    try:
        return engine.incident_report(asset_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/train")
def train(episodes: int = Query(default=140, ge=10, le=2000)) -> dict:
    return engine.train(episodes=episodes)

