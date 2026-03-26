import { useState, useEffect } from "react";
import { ConcentrationReport, RiskLevel } from "./types";
import RiskGauge from "./components/RiskGauge";
import SignalBreakdown from "./components/SignalBreakdown";
import HolderDistribution from "./components/HolderDistribution";

const RISK_LEVELS: RiskLevel[] = ["DISTRIBUTED", "MODERATE", "CONCENTRATED", "DOMINATED"];

function mockReport(): ConcentrationReport {
  const idx = Math.floor(Math.random() * 4);
  const level = RISK_LEVELS[idx];
  const bases = [12, 38, 63, 88];
  const score = bases[idx] + (Math.random() * 10 - 5);
  const gini   = score * 0.85;
  const whale  = 20 + idx * 20 + Math.random() * 10;
  const fresh  = idx * 15 + Math.random() * 10;
  const lp     = idx * 18 + Math.random() * 10;
  return {
    risk_level: level,
    risk_score: Math.min(Math.max(score, 0), 100),
    signals: [
      { name: "gini",            score: Math.min(gini, 100),  triggered: gini > 65,  detail: `Gini=${(gini/100).toFixed(3)} concentration index`,      weight: 0.35 },
      { name: "whale_dominance", score: Math.min(whale, 100), triggered: whale > 40, detail: `Top-10 wallets hold ${whale.toFixed(1)}% of supply`,      weight: 0.30 },
      { name: "fresh_wallet",    score: Math.min(fresh*2, 100), triggered: fresh > 20, detail: `${fresh.toFixed(1)}% of holders are fresh wallets (<7d)`, weight: 0.20 },
      { name: "lp_concentration",score: Math.min(lp, 100),   triggered: lp > 50,    detail: `LP holds ${lp.toFixed(1)}% of total supply`,              weight: 0.15 },
    ],
    recommendation: {
      DISTRIBUTED:  "Token distribution looks healthy. Low concentration risk.",
      MODERATE:     "Some concentration detected. Monitor top holders closely.",
      CONCENTRATED: "High concentration risk. Potential sell pressure from whales.",
      DOMINATED:    "CRITICAL: Supply dominated by few wallets. Extreme rug risk.",
    }[level],
    timestamp: Date.now() / 1000,
  };
}

const MOCK_HOLDERS = [
  { rank: 1, address: "8xKpW3mNQjvZpTfR9xLm", pct: 18.4, age: 62 },
  { rank: 2, address: "3TaRqBnVuYsXcDgHkWpL", pct: 12.1, age: 45 },
  { rank: 3, address: "9PmZhFjKsNrXoQeWdGtY", pct: 8.7,  age: 4  },
  { rank: 4, address: "6BsLcVmQxNpYtRwZjHfE", pct: 6.3,  age: 30 },
  { rank: 5, address: "2DkGrWnMhXbTcPvJqZeA", pct: 5.1,  age: 3  },
];

export default function App() {
  const [report, setReport] = useState<ConcentrationReport>(mockReport());

  useEffect(() => {
    const id = setInterval(() => setReport(mockReport()), 4000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ minHeight: "100vh", background: "#020d0a", color: "#e2e8f0", fontFamily: "monospace", padding: "32px 24px" }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ marginBottom: 32, borderBottom: "1px solid #0d2420", paddingBottom: 20 }}>
          <h1 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: "#5eead4", letterSpacing: 2 }}>
            IGNOVEX
          </h1>
          <div style={{ fontSize: 11, color: "#4b5563", marginTop: 4, letterSpacing: 1 }}>
            TOKEN HOLDER CONCENTRATION RISK ENGINE · SOLANA
          </div>
          <div style={{ fontSize: 11, color: "#0d9488", marginTop: 8 }}>
            ● LIVE · updating every 4s
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          {/* Left */}
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div style={{ background: "#030f0d", border: "1px solid #0d2420", borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 11, color: "#4b5563", textTransform: "uppercase", letterSpacing: 1, marginBottom: 16 }}>
                Concentration Risk Score
              </div>
              <RiskGauge report={report} />
            </div>

            <div style={{ background: "#030f0d", border: "1px solid #0d2420", borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 11, color: "#4b5563", textTransform: "uppercase", letterSpacing: 1, marginBottom: 16 }}>
                Top Holders
              </div>
              <HolderDistribution holders={MOCK_HOLDERS} />
            </div>
          </div>

          {/* Right */}
          <div style={{ background: "#030f0d", border: "1px solid #0d2420", borderRadius: 12, padding: 20 }}>
            <div style={{ fontSize: 11, color: "#4b5563", textTransform: "uppercase", letterSpacing: 1, marginBottom: 16 }}>
              Signal Breakdown
            </div>
            <SignalBreakdown signals={report.signals} />
          </div>
        </div>

        <div style={{ marginTop: 32, fontSize: 11, color: "#1f2937", textAlign: "center" }}>
          built by ignovexdev · holderwatch · ginitracker
        </div>
      </div>
    </div>
  );
}
