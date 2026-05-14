from __future__ import annotations

from .models import AssetKind, DataAsset, LineageEdge


def sample_assets() -> list[DataAsset]:
    return [
        DataAsset(
            asset_id="raw_meta_spend",
            label="Raw Meta Spend Feed",
            kind=AssetKind.TABLE,
            owner="growth-data",
            freshness_minutes=22,
            freshness_slo_minutes=15,
            null_rate=0.01,
            volume_delta=-0.32,
            schema_drift=0.08,
            business_criticality=8,
            monthly_revenue_dependency=420000,
        ),
        DataAsset(
            asset_id="stg_campaign_attribution",
            label="Campaign Attribution Staging",
            kind=AssetKind.PIPELINE,
            owner="marketing-analytics",
            freshness_minutes=88,
            freshness_slo_minutes=30,
            null_rate=0.14,
            volume_delta=-0.44,
            schema_drift=0.22,
            business_criticality=10,
            monthly_revenue_dependency=910000,
        ),
        DataAsset(
            asset_id="fct_daily_revenue",
            label="Daily Revenue Fact",
            kind=AssetKind.TABLE,
            owner="finance-data",
            freshness_minutes=64,
            freshness_slo_minutes=20,
            null_rate=0.04,
            volume_delta=-0.08,
            schema_drift=0.03,
            business_criticality=10,
            monthly_revenue_dependency=1200000,
        ),
        DataAsset(
            asset_id="dash_ceo_growth_board",
            label="CEO Growth Board",
            kind=AssetKind.DASHBOARD,
            owner="exec-analytics",
            freshness_minutes=70,
            freshness_slo_minutes=30,
            null_rate=0.0,
            volume_delta=-0.02,
            schema_drift=0.0,
            business_criticality=9,
            monthly_revenue_dependency=1500000,
        ),
        DataAsset(
            asset_id="feature_ltv_propensity",
            label="LTV Propensity Feature",
            kind=AssetKind.FEATURE,
            owner="ml-platform",
            freshness_minutes=34,
            freshness_slo_minutes=45,
            null_rate=0.06,
            volume_delta=-0.19,
            schema_drift=0.12,
            business_criticality=7,
            monthly_revenue_dependency=360000,
        ),
    ]


def sample_edges() -> list[LineageEdge]:
    return [
        LineageEdge("raw_meta_spend", "stg_campaign_attribution", 0.84),
        LineageEdge("stg_campaign_attribution", "fct_daily_revenue", 0.72),
        LineageEdge("fct_daily_revenue", "dash_ceo_growth_board", 0.93),
        LineageEdge("stg_campaign_attribution", "feature_ltv_propensity", 0.58),
        LineageEdge("feature_ltv_propensity", "dash_ceo_growth_board", 0.41),
    ]

