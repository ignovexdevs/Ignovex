# Ignovex — Claude Context

## What this is
Token holder concentration risk engine for Solana. Analyzes 4 on-chain distribution signals and produces a risk score (0–100) with a 4-level classification.

## Core signals
- `gini_signal` — Gini coefficient of holder balances (weight: 35%)
- `whale_dominance_signal` — top-10 wallet supply % (weight: 30%)
- `fresh_wallet_signal` — ratio of wallets <7 days old (weight: 20%)
- `lp_concentration_signal` — LP token supply share (weight: 15%)

## Risk levels
- DISTRIBUTED (0–25): healthy
- MODERATE (26–50): watch
- CONCENTRATED (51–75): alert
- DOMINATED (76–100): critical

## Entry point
```python
from ignovex import classify, TokenDistribution, HolderRecord
report = classify(dist)
```

## Tests
```bash
pytest tests/ -v  # 123 tests
```

## Dashboard
```bash
cd dashboard && npm install && npm run dev
```
