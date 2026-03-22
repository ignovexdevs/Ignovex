import { SignalResult } from "../types";

interface Props { signals: SignalResult[]; }

const SIGNAL_LABELS: Record<string, string> = {
  gini:            "Gini Coefficient",
  whale_dominance: "Whale Dominance",
  fresh_wallet:    "Fresh Wallets",
  lp_concentration:"LP Concentration",
};

export default function SignalBreakdown({ signals }: Props) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {signals.map(s => (
        <div key={s.name} style={{
          background: "#030f0d",
          border: `1px solid ${s.triggered ? "#0f766e" : "#1f2937"}`,
          borderRadius: 8, padding: "10px 14px",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
            <span style={{ fontSize: 12, fontWeight: 600, color: s.triggered ? "#5eead4" : "#6b7280" }}>
              {s.triggered ? "[TRIGGERED]" : "[ inactive ]"} {SIGNAL_LABELS[s.name] ?? s.name}
            </span>
            <span style={{ fontSize: 12, fontWeight: 700, color: s.triggered ? "#0d9488" : "#4b5563" }}>
              {s.score.toFixed(0)}
            </span>
          </div>
          <div style={{ background: "#011a17", borderRadius: 4, height: 5, marginBottom: 6 }}>
            <div style={{
              width: `${s.score}%`, height: "100%", borderRadius: 4,
              background: s.triggered ? "#0d9488" : "#374151",
              transition: "width 0.4s ease",
            }} />
          </div>
          <div style={{ fontSize: 11, color: "#6b7280" }}>{s.detail}</div>
          <div style={{ fontSize: 10, color: "#374151", marginTop: 2 }}>
            weight: {(s.weight * 100).toFixed(0)}%
          </div>
        </div>
      ))}
    </div>
  );
}
