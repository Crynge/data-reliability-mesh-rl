from __future__ import annotations

from .anomaly import score_asset, score_assets
from .lineage import propagate_impact, reverse_root_causes
from .models import ContractStatus, RemediationDecision, RemediationAction
from .rl import MeshRemediationAgent
from .sample_data import sample_assets, sample_edges


class ReliabilityMeshEngine:
    def __init__(self) -> None:
        self.assets = sample_assets()
        self.edges = sample_edges()
        self.agent = MeshRemediationAgent()
        self.last_training = self.agent.train(episodes=180)

    def overview(self) -> dict:
        findings = score_assets(self.assets)
        avg_reliability = round(sum(item.reliability_score for item in findings) / len(findings), 2)
        highest_risk = sorted(findings, key=lambda item: item.severity, reverse=True)[:3]
        return {
            "mesh_health_score": avg_reliability,
            "predicted_failure_probability_24h": round((100 - avg_reliability) / 100, 3),
            "assets": [asset.as_dict() for asset in self.assets],
            "findings": [item.as_dict() for item in findings],
            "highest_risk_assets": [item.as_dict() for item in highest_risk],
            "last_training": self.last_training.as_dict(),
        }

    def list_assets(self) -> list[dict]:
        findings = {finding.asset_id: finding for finding in score_assets(self.assets)}
        rows = []
        for asset in self.assets:
            finding = findings[asset.asset_id]
            rows.append(
                {
                    **asset.as_dict(),
                    "reliability_score": finding.reliability_score,
                    "severity": finding.severity,
                    "confidence_badge": self._badge_for_score(finding.reliability_score),
                }
            )
        return rows

    def contract_status(self) -> list[dict]:
        contracts: list[ContractStatus] = []
        for asset in self.assets:
            freshness_ok = asset.freshness_minutes <= asset.freshness_slo_minutes
            contracts.append(
                ContractStatus(
                    asset_id=asset.asset_id,
                    label=asset.label,
                    slo_name="freshness",
                    target=f"< {asset.freshness_slo_minutes}m",
                    actual=f"{asset.freshness_minutes}m",
                    status="healthy" if freshness_ok else "breached",
                )
            )
            contracts.append(
                ContractStatus(
                    asset_id=asset.asset_id,
                    label=asset.label,
                    slo_name="null-rate",
                    target="< 5%",
                    actual=f"{asset.null_rate:.1%}",
                    status="healthy" if asset.null_rate <= 0.05 else "warning",
                )
            )
        return [contract.as_dict() for contract in contracts]

    def lineage_view(self, asset_id: str) -> dict:
        return {
            "asset_id": asset_id,
            "downstream_impact": propagate_impact(self.edges, asset_id),
            "upstream_root_causes": reverse_root_causes(self.edges, asset_id),
        }

    def incident_report(self, asset_id: str) -> dict:
        asset = self._get_asset(asset_id)
        finding = score_asset(asset)
        freshness_ratio = asset.freshness_minutes / max(asset.freshness_slo_minutes, 1)
        state = self.agent.encode_state(finding.severity, freshness_ratio, asset.business_criticality)
        action = self.agent.best_action(state)
        decision = RemediationDecision(
            asset_id=asset_id,
            action=action,
            confidence=round(min(0.98, 0.55 + finding.severity / 180), 3),
            rationale=self._rationale_for(asset.label, finding.reasons, action),
            expected_mttr_reduction_minutes=int(18 + asset.business_criticality * 4 + freshness_ratio * 6),
        )
        return {
            "asset": asset.as_dict(),
            "finding": finding.as_dict(),
            "decision": decision.as_dict(),
            "blast_radius": propagate_impact(self.edges, asset_id),
            "candidate_root_causes": reverse_root_causes(self.edges, asset_id),
        }

    def train(self, episodes: int = 140) -> dict:
        self.last_training = self.agent.train(episodes=episodes)
        return self.last_training.as_dict()

    def _get_asset(self, asset_id: str):
        for asset in self.assets:
            if asset.asset_id == asset_id:
                return asset
        raise KeyError(f"Unknown asset: {asset_id}")

    def _badge_for_score(self, score: float) -> str:
        if score >= 78:
            return "green"
        if score >= 56:
            return "yellow"
        return "red"

    def _rationale_for(self, label: str, reasons: list[str], action: RemediationAction) -> str:
        joined = "; ".join(reasons[:2])
        return f"{action.value} selected for {label} because {joined}. Policy favors the fastest high-confidence action that lowers downstream incident risk."

