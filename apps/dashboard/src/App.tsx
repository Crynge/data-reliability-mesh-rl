import { useEffect, useState } from "react";

type Finding = {
  asset_id: string;
  severity: number;
  reliability_score: number;
  reasons: string[];
};

type Asset = {
  asset_id: string;
  label: string;
  owner: string;
  kind: string;
  confidence_badge?: string;
  severity?: number;
  reliability_score?: number;
};

type Overview = {
  mesh_health_score: number;
  predicted_failure_probability_24h: number;
  findings: Finding[];
  highest_risk_assets: Finding[];
  last_training: {
    episodes: number;
    average_reward: number;
    action_histogram: Record<string, number>;
  };
};

const fallbackOverview: Overview = {
  mesh_health_score: 67.4,
  predicted_failure_probability_24h: 0.326,
  findings: [
    {
      asset_id: "stg_campaign_attribution",
      severity: 74.8,
      reliability_score: 25.2,
      reasons: ["freshness breached", "null-rate spike", "schema drift"]
    },
    {
      asset_id: "fct_daily_revenue",
      severity: 58.4,
      reliability_score: 41.6,
      reasons: ["freshness breached", "business criticality pressure"]
    }
  ],
  highest_risk_assets: [
    {
      asset_id: "stg_campaign_attribution",
      severity: 74.8,
      reliability_score: 25.2,
      reasons: ["freshness breached", "null-rate spike", "schema drift"]
    }
  ],
  last_training: {
    episodes: 180,
    average_reward: 26.9,
    action_histogram: {
      BACKFILL: 49,
      REBUILD: 51,
      USE_FALLBACK: 38,
      ALERT_HUMAN: 21
    }
  }
};

const fallbackAssets: Asset[] = [
  {
    asset_id: "stg_campaign_attribution",
    label: "Campaign Attribution Staging",
    owner: "marketing-analytics",
    kind: "pipeline",
    confidence_badge: "red",
    severity: 74.8,
    reliability_score: 25.2
  },
  {
    asset_id: "fct_daily_revenue",
    label: "Daily Revenue Fact",
    owner: "finance-data",
    kind: "table",
    confidence_badge: "yellow",
    severity: 58.4,
    reliability_score: 41.6
  },
  {
    asset_id: "dash_ceo_growth_board",
    label: "CEO Growth Board",
    owner: "exec-analytics",
    kind: "dashboard",
    confidence_badge: "yellow",
    severity: 50.3,
    reliability_score: 49.7
  }
];

function App() {
  const apiBase = (import.meta.env.VITE_API_BASE as string | undefined) ?? "http://127.0.0.1:8014";
  const [overview, setOverview] = useState<Overview>(fallbackOverview);
  const [assets, setAssets] = useState<Asset[]>(fallbackAssets);

  useEffect(() => {
    Promise.all([
      fetch(`${apiBase}/api/overview`).then((res) => res.json()),
      fetch(`${apiBase}/api/assets`).then((res) => res.json())
    ])
      .then(([nextOverview, nextAssets]) => {
        setOverview(nextOverview);
        setAssets(nextAssets.items);
      })
      .catch(() => {
        // Dashboard intentionally retains seed data as an offline demo surface.
      });
  }, [apiBase]);

  return (
    <main className="shell">
      <section className="hero panel">
        <div>
          <p className="eyebrow">Autonomous Reliability Command Mesh</p>
          <h1>Data trust with predictive quality, lineage blast radius, and RL-driven remediation.</h1>
          <p className="lede">
            A command-center dashboard for data platform, analytics, and marketing operations teams that need to know
            what is breaking, what is likely to break next, and which action reduces business risk fastest.
          </p>
        </div>
        <div className="hero-metrics">
          <div className="metric deep">
            <span>Mesh Health</span>
            <strong>{overview.mesh_health_score}</strong>
          </div>
          <div className="metric">
            <span>Predicted 24h Failure</span>
            <strong>{Math.round(overview.predicted_failure_probability_24h * 100)}%</strong>
          </div>
          <div className="metric">
            <span>Training Reward</span>
            <strong>{overview.last_training.average_reward}</strong>
          </div>
        </div>
      </section>

      <section className="grid">
        <article className="panel span-7">
          <div className="section-head">
            <h2>Asset Confidence Matrix</h2>
            <p>Every table, feature, and dashboard gets a live trust badge.</p>
          </div>
          <div className="asset-list">
            {assets.map((asset) => (
              <div className="asset-row" key={asset.asset_id}>
                <div>
                  <h3>{asset.label}</h3>
                  <p>
                    {asset.kind} • {asset.owner}
                  </p>
                </div>
                <div className={`badge badge-${asset.confidence_badge ?? "yellow"}`}>{asset.confidence_badge}</div>
                <div className="mini-score">
                  <span>severity</span>
                  <strong>{asset.severity ?? 0}</strong>
                </div>
                <div className="mini-score">
                  <span>reliability</span>
                  <strong>{asset.reliability_score ?? 0}</strong>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className="panel span-5">
          <div className="section-head">
            <h2>Top Incident Narrative</h2>
            <p>Policy-ready explanation generated from anomaly evidence and remediation logic.</p>
          </div>
          <div className="incident-card">
            <h3>{overview.highest_risk_assets[0]?.asset_id ?? "stg_campaign_attribution"}</h3>
            <p>
              Freshness breach, volume contraction, and schema instability are compounding across the attribution
              layer. Recommended move: backfill or rebuild before downstream executive reporting is trusted again.
            </p>
            <ul>
              {(overview.highest_risk_assets[0]?.reasons ?? []).map((reason) => (
                <li key={reason}>{reason}</li>
              ))}
            </ul>
          </div>
        </article>

        <article className="panel span-6">
          <div className="section-head">
            <h2>RL Action Histogram</h2>
            <p>Policy behavior after synthetic training episodes.</p>
          </div>
          <div className="bars">
            {Object.entries(overview.last_training.action_histogram).map(([action, count]) => (
              <div className="bar-row" key={action}>
                <span>{action}</span>
                <div className="bar-track">
                  <div className="bar-fill" style={{ width: `${Math.min(100, count * 1.6)}%` }} />
                </div>
                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="panel span-6">
          <div className="section-head">
            <h2>Reliability Posture</h2>
            <p>How the mesh prevents silent data damage.</p>
          </div>
          <div className="posture-grid">
            <div className="posture-card">
              <strong>Predict</strong>
              <p>Detect freshness, null-rate, schema, and telemetry anomalies before downstream confidence collapses.</p>
            </div>
            <div className="posture-card">
              <strong>Trace</strong>
              <p>Map blast radius through lineage and surface which dashboards and features inherit the risk.</p>
            </div>
            <div className="posture-card">
              <strong>Repair</strong>
              <p>Use RL-guided remediation policies to backfill, rebuild, alert, or switch to fallbacks.</p>
            </div>
            <div className="posture-card">
              <strong>Explain</strong>
              <p>Turn pipeline noise into business-ready incident narratives for executives and operators.</p>
            </div>
          </div>
        </article>
      </section>
    </main>
  );
}

export default App;

