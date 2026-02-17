from __future__ import annotations

from typing import List

from .models import SignalResult


def compute_risk_score(signals: List[SignalResult]) -> float:
    """Weighted average of signal scores, returns 0–100."""
    total_weight = sum(s.weight for s in signals)
    if total_weight == 0:
        return 0.0
    return sum(s.score * s.weight for s in signals) / total_weight


def triggered_count(signals: List[SignalResult]) -> int:
    return sum(1 for s in signals if s.triggered)


def dominant_signal(signals: List[SignalResult]) -> SignalResult | None:
    if not signals:
        return None
    return max(signals, key=lambda s: s.score)
