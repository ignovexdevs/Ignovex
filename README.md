<div align="center">

<img src="https://capsule-render.vercel.app/api?type=wave&color=0:020d0a,50:042f2e,100:0d9488&height=180&text=Ignovex&fontSize=62&fontColor=5eead4&fontAlignY=55&desc=Token%20Holder%20Concentration%20Risk%20Engine&descAlignY=75&descSize=16" width="100%"/>

### `$IGN : 2voYYbHLyAXtZPLNdQJUgmnbwbPQ3EPPaDC158Mjpump`

[![Tests](https://github.com/ignovexdev/Ignovex/actions/workflows/test.yml/badge.svg)](https://github.com/ignovexdev/Ignovex/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-0d9488?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-5eead4?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-374151?style=flat-square)](LICENSE)
[![123 Tests](https://img.shields.io/badge/tests-123%20passed-22c55e?style=flat-square)]()

</div>

---

Ignovex is a token holder concentration risk engine for Solana. It analyzes four on-chain distribution signals — Gini coefficient, whale dominance, fresh wallet ratio, and LP concentration — and computes a single risk score (0–100) with a four-level classification: **DISTRIBUTED → MODERATE → CONCENTRATED → DOMINATED**.

Most tools watch price. Ignovex watches **who holds** the token. Concentration risk predicts behavior before price reacts.

---

## Engine Architecture

```
TokenDistribution (holders + supply + LP balance)
        │
        ├─ gini_signal          → Gini coefficient ≥ 0.65       [weight: 35%]
        ├─ whale_dominance_signal → top-10 hold ≥ 40% of supply  [weight: 30%]
        ├─ fresh_wallet_signal  → ≥ 20% wallets age < 7 days     [weight: 20%]
        └─ lp_concentration_signal → LP holds ≥ 50% of supply    [weight: 15%]
                │
                ▼
        compute_risk_score() → weighted 0–100
                │
                ▼
        classify() → ConcentrationReport
```

## Risk Classification

| Score | Level | Meaning |
|---|---|---|
| 0–25 | `DISTRIBUTED` | Healthy spread, low risk |
| 26–50 | `MODERATE` | Some concentration, monitor |
| 51–75 | `CONCENTRATED` | High risk, whale pressure likely |
| 76–100 | `DOMINATED` | Critical — rug risk |

## Install

```bash
pip install ignovex
```

## Usage

```python
from ignovex import classify, TokenDistribution, HolderRecord

holders = [
    HolderRecord(address="Whale1...", balance=450_000, wallet_age_days=60),
    HolderRecord(address="New1...",   balance=10_000,  wallet_age_days=2),
    HolderRecord(address="Old1...",   balance=40_000,  wallet_age_days=90),
]

dist = TokenDistribution(
    token_mint="So11111111111111111111111111111111111111112",
    total_supply=1_000_000,
    holders=holders,
    lp_total_balance=200_000,
)

report = classify(dist)

print(report.risk_level)     # CONCENTRATED
print(report.risk_score)     # ~68.4
print(report.recommendation) # High concentration risk...
```

## Run Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
# 123 tests — signals, scorer, classifier, models, helpers
```

## Dashboard

```bash
cd dashboard
npm install
npm run dev
# → http://localhost:5173
```

Live dashboard showing risk gauge, top-holder distribution bars, and all 4 signal breakdowns. Updates every 4 seconds with mock data.

## Docker

```bash
docker compose up
```

---

<div align="center">
<sub>built by ignovexdev · holderwatch · ginitracker</sub>
</div>
