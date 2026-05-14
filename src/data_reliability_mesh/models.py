from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class AssetKind(str, Enum):
    TABLE = "table"
    DASHBOARD = "dashboard"
    FEATURE = "feature"
    PIPELINE = "pipeline"


class RemediationAction(str, Enum):
    REBUILD = "REBUILD"
    BACKFILL = "BACKFILL"
    SKIP = "SKIP"
    ALERT_HUMAN = "ALERT_HUMAN"
    USE_FALLBACK = "USE_FALLBACK"
    ROLLBACK = "ROLLBACK"
    INCREASE_ALERT_THRESHOLD = "INCREASE_ALERT_THRESHOLD"


@dataclass
class DataAsset:
    asset_id: str
    label: str
    kind: AssetKind
    owner: str
    freshness_minutes: int
    freshness_slo_minutes: int
    null_rate: float
    volume_delta: float
    schema_drift: float
    business_criticality: int
    monthly_revenue_dependency: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LineageEdge:
    source: str
    target: str
    propagation_probability: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AnomalyFinding:
    asset_id: str
    severity: float
    reasons: list[str]
    reliability_score: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ContractStatus:
    asset_id: str
    label: str
    slo_name: str
    target: str
    actual: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RemediationDecision:
    asset_id: str
    action: RemediationAction
    confidence: float
    rationale: str
    expected_mttr_reduction_minutes: int

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["action"] = self.action.value
        return payload


@dataclass
class TrainingSummary:
    episodes: int
    average_reward: float
    action_histogram: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

