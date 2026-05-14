# Architecture

## Control Plane

The verified control plane is centered around the Python package in `src/data_reliability_mesh` and exposed via FastAPI in `services/mesh_api`.

### Core flow

1. asset telemetry is profiled into a normalized reliability state
2. anomaly detectors assign severity and evidence
3. lineage propagation estimates downstream blast radius
4. the remediation agent scores possible actions
5. contracts summarize whether SLA-like expectations still hold
6. the dashboard renders confidence, impact, and recommended actions

## Reliability Scoring

Each asset is scored from multiple signals:

- freshness lag
- null-rate risk
- volume drift
- schema drift
- incident criticality
- downstream blast radius

The current implementation uses deterministic heuristics plus simulated policy learning so the platform remains runnable without proprietary telemetry.

## RL Remediation Layer

The reinforcement-learning-inspired agent uses:

- a state encoder over anomaly signatures
- a prioritized replay buffer
- iterative Q-value updates from a synthetic environment
- policy recommendation across actions such as `BACKFILL`, `REBUILD`, `USE_FALLBACK`, and `ALERT_HUMAN`

This gives the repository a functional closed loop while leaving room for deeper PyTorch-based agents later.

## Polyglot Modules

The repo includes expansion surfaces for:

- Rust streaming detection
- Go lineage ingestion and remediation execution
- Scala propagation learning
- Java telemetry enrichment
- Cypher lineage investigation
- SQL contract repair procedures
- C++ distance kernels

These modules are architecture-real, but the Python + frontend core is the fully verified runtime in this environment.

