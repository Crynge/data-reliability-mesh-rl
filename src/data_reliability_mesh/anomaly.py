from __future__ import annotations

from .models import AnomalyFinding, DataAsset


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def score_asset(asset: DataAsset) -> AnomalyFinding:
    reasons: list[str] = []
    severity = 0.0

    freshness_ratio = asset.freshness_minutes / max(asset.freshness_slo_minutes, 1)
    if freshness_ratio > 1:
        severity += min((freshness_ratio - 1.0) * 18, 35)
        reasons.append(f"freshness breached at {asset.freshness_minutes}m vs {asset.freshness_slo_minutes}m")

    if asset.null_rate > 0.05:
        severity += min(asset.null_rate * 120, 24)
        reasons.append(f"null-rate spike at {asset.null_rate:.0%}")

    if abs(asset.volume_delta) > 0.15:
        severity += min(abs(asset.volume_delta) * 60, 24)
        reasons.append(f"volume drift at {asset.volume_delta:+.0%}")

    if asset.schema_drift > 0.1:
        severity += min(asset.schema_drift * 100, 22)
        reasons.append(f"schema drift at {asset.schema_drift:.0%}")

    severity += asset.business_criticality * 1.6
    reliability_score = _clamp(100 - severity, 8, 98)
    if not reasons:
        reasons.append("healthy within monitored thresholds")

    return AnomalyFinding(
        asset_id=asset.asset_id,
        severity=round(_clamp(severity, 0, 100), 2),
        reasons=reasons,
        reliability_score=round(reliability_score, 2),
    )


def score_assets(assets: list[DataAsset]) -> list[AnomalyFinding]:
    return [score_asset(asset) for asset in assets]

