from __future__ import annotations

from typing import List

from .models import HolderRecord, TokenDistribution, SignalResult

# --- Thresholds ---
GINI_TRIGGER        = 0.65   # Gini coefficient >= 0.65
WHALE_TOP10_PCT     = 40.0   # top-10 wallets hold >= 40% of supply
FRESH_WALLET_PCT    = 20.0   # >= 20% of holders are fresh (<7 days)
LP_CONCENTRATION_PCT = 50.0  # LP holds >= 50% of total supply

# --- Weights (must sum to 1.0) ---
GINI_WEIGHT        = 0.35
WHALE_WEIGHT       = 0.30
FRESH_WEIGHT       = 0.20
LP_WEIGHT          = 0.15


def _gini(balances: List[float]) -> float:
    if len(balances) < 2:
        return 0.0
    total = sum(balances)
    if total == 0:
        return 0.0
    n = len(balances)
    s = sorted(balances)
    cumsum = sum((2 * (i + 1) - n - 1) * v for i, v in enumerate(s))
    return cumsum / (n * total)


def gini_signal(dist: TokenDistribution) -> SignalResult:
    balances = [h.balance for h in dist.non_lp_holders()]
    g = _gini(balances)
    score = min(g * 100.0, 100.0)
    triggered = g >= GINI_TRIGGER
    return SignalResult(
        name="gini",
        score=score,
        triggered=triggered,
        detail=f"Gini={g:.3f} ({'triggered' if triggered else 'ok'}, threshold={GINI_TRIGGER})",
        weight=GINI_WEIGHT,
    )


def whale_dominance_signal(dist: TokenDistribution) -> SignalResult:
    holders = sorted(dist.non_lp_holders(), key=lambda h: h.balance, reverse=True)
    top10_bal = sum(h.balance for h in holders[:10])
    total = dist.total_supply if dist.total_supply > 0 else 1.0
    pct = (top10_bal / total) * 100.0
    score = min(pct, 100.0)
    triggered = pct >= WHALE_TOP10_PCT
    return SignalResult(
        name="whale_dominance",
        score=score,
        triggered=triggered,
        detail=f"Top-10 wallets hold {pct:.1f}% of supply (threshold={WHALE_TOP10_PCT}%)",
        weight=WHALE_WEIGHT,
    )


def fresh_wallet_signal(dist: TokenDistribution) -> SignalResult:
    holders = dist.non_lp_holders()
    if not holders:
        return SignalResult(
            name="fresh_wallet", score=0.0, triggered=False,
            detail="No non-LP holders", weight=FRESH_WEIGHT,
        )
    fresh = [h for h in holders if h.wallet_age_days < 7]
    pct = (len(fresh) / len(holders)) * 100.0
    score = min(pct * 2.0, 100.0)  # 50% fresh = score 100
    triggered = pct >= FRESH_WALLET_PCT
    return SignalResult(
        name="fresh_wallet",
        score=score,
        triggered=triggered,
        detail=f"{pct:.1f}% holders are fresh wallets (<7 days, threshold={FRESH_WALLET_PCT}%)",
        weight=FRESH_WEIGHT,
    )


def lp_concentration_signal(dist: TokenDistribution) -> SignalResult:
    total = dist.total_supply if dist.total_supply > 0 else 1.0
    pct = (dist.lp_total_balance / total) * 100.0
    score = min(pct, 100.0)
    triggered = pct >= LP_CONCENTRATION_PCT
    return SignalResult(
        name="lp_concentration",
        score=score,
        triggered=triggered,
        detail=f"LP holds {pct:.1f}% of total supply (threshold={LP_CONCENTRATION_PCT}%)",
        weight=LP_WEIGHT,
    )


def run_all_signals(dist: TokenDistribution) -> list[SignalResult]:
    return [
        gini_signal(dist),
        whale_dominance_signal(dist),
        fresh_wallet_signal(dist),
        lp_concentration_signal(dist),
    ]
