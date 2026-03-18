import { RiskLevel, ConcentrationReport } from "../types";

interface Props { report: ConcentrationReport; }

const LEVEL_COLOR: Record<RiskLevel, string> = {
  DISTRIBUTED:  "#22c55e",
  MODERATE:     "#f59e0b",
  CONCENTRATED: "#ef4444",
  DOMINATED:    "#dc2626",
};

export default function RiskGauge({ report }: Props) {
  const color = LEVEL_COLOR[report.risk_level];
  const pct   = report.risk_score;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <div style={{ textAlign: "center" }}>
        <div style={{ fontSize: 60, fontWeight: 800, color, lineHeight: 1 }}>
          {pct.toFixed(0)}
        </div>
        <div style={{ fontSize: 11, color: "#6b7280", textTransform: "uppercase", letterSpacing: 2, marginTop: 4 }}>
          Risk Score
        </div>
        <div style={{
          display: "inline-block", marginTop: 10,
          padding: "4px 18px", borderRadius: 20,
          background: `${color}22`, border: `1px solid ${color}`,
          color, fontSize: 13, fontWeight: 700,
        }}>
          {report.risk_level}
        </div>
      </div>

      {/* Bar */}
      <div style={{ background: "#0a1a0a", borderRadius: 6, height: 8 }}>
        <div style={{
          width: `${pct}%`, height: "100%", borderRadius: 6,
          background: `linear-gradient(90deg, #22c55e, ${color})`,
          transition: "width 0.5s ease",
        }} />
      </div>

      {/* Recommendation */}
      <div style={{
        background: "#030f03", border: "1px solid #0d3a0d",
        borderRadius: 8, padding: "10px 14px",
        fontSize: 12, color: "#86efac", lineHeight: 1.6,
      }}>
        <span style={{ color: "#0d9488", fontWeight: 700 }}>→ </span>
        {report.recommendation}
      </div>
    </div>
  );
}
