interface HolderRow { rank: number; address: string; pct: number; age: number; }

interface Props { holders: HolderRow[]; }

export default function HolderDistribution({ holders }: Props) {
  const maxPct = Math.max(...holders.map(h => h.pct), 1);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      <div style={{ display: "grid", gridTemplateColumns: "24px 1fr 60px 60px", gap: 8, fontSize: 10, color: "#4b5563", textTransform: "uppercase", letterSpacing: 1, paddingBottom: 6, borderBottom: "1px solid #0d1f1d" }}>
        <span>#</span><span>Address</span><span style={{ textAlign: "right" }}>%</span><span style={{ textAlign: "right" }}>Age</span>
      </div>
      {holders.map(h => (
        <div key={h.rank} style={{ display: "grid", gridTemplateColumns: "24px 1fr 60px 60px", gap: 8, alignItems: "center" }}>
          <span style={{ fontSize: 11, color: "#4b5563" }}>{h.rank}</span>
          <div>
            <div style={{ fontSize: 11, color: "#99f6e4", fontFamily: "monospace" }}>
              {h.address.slice(0, 8)}...{h.address.slice(-4)}
            </div>
            <div style={{ background: "#011a17", borderRadius: 2, height: 3, marginTop: 3 }}>
              <div style={{ width: `${(h.pct / maxPct) * 100}%`, height: "100%", background: "#0d9488", borderRadius: 2 }} />
            </div>
          </div>
          <span style={{ fontSize: 11, color: "#5eead4", textAlign: "right" }}>{h.pct.toFixed(1)}%</span>
          <span style={{ fontSize: 11, color: h.age < 7 ? "#f59e0b" : "#4b5563", textAlign: "right" }}>{h.age.toFixed(0)}d</span>
        </div>
      ))}
    </div>
  );
}
