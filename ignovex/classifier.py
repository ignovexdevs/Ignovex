from __future__ import annotations

from .models import TokenDistribution, ConcentrationReport, RiskLevel
from .signals import run_all_signals
from .scorer import compute_risk_score

_RECOMMENDATIONS: dict[RiskLevel, str] = {
    RiskLevel.DISTRIBUTED:  "Token distribution looks healthy. Low concentration risk.",
    RiskLevel.MODERATE:     "Some concentration detected. Monitor top holders closely.",
    RiskLevel.CONCENTRATED: "High concentration risk. Potential sell pressure from whales.",
    RiskLevel.DOMINATED:    "CRITICAL: Supply dominated by few wallets. Extreme rug risk.",
}


def _level_from_score(score: float) -> RiskLevel:
    if score <= 25.0:
        return RiskLevel.DISTRIBUTED
    if score <= 50.0:
        return RiskLevel.MODERATE
    if score <= 75.0:
        return RiskLevel.CONCENTRATED
    return RiskLevel.DOMINATED


def classify(dist: TokenDistribution) -> ConcentrationReport:
    signals = run_all_signals(dist)
    score   = compute_risk_score(signals)
    level   = _level_from_score(score)
    return ConcentrationReport(
        risk_level=level,
        risk_score=score,
        signals=signals,
        recommendation=_RECOMMENDATIONS[level],
    )


def classify_batch(dists: list[TokenDistribution]) -> list[ConcentrationReport]:
    return [classify(d) for d in dists]
