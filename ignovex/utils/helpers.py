from __future__ import annotations

import time
from ..models import RiskLevel


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def format_supply(supply: float) -> str:
    if supply >= 1_000_000_000:
        return f"{supply / 1_000_000_000:.2f}B"
    if supply >= 1_000_000:
        return f"{supply / 1_000_000:.2f}M"
    if supply >= 1_000:
        return f"{supply / 1_000:.2f}K"
    return f"{supply:.0f}"


def format_pct(value: float) -> str:
    return f"{value:.1f}%"


def format_score(score: float) -> str:
    return f"{score:.1f}"


def format_gini(g: float) -> str:
    return f"{g:.3f}"


def ts_to_str(ts: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def level_color(level: RiskLevel) -> str:
    return {
        RiskLevel.DISTRIBUTED:  "#22c55e",
        RiskLevel.MODERATE:     "#f59e0b",
        RiskLevel.CONCENTRATED: "#ef4444",
        RiskLevel.DOMINATED:    "#dc2626",
    }.get(level, "#6b7280")


def level_badge(level: RiskLevel) -> str:
    return {
        RiskLevel.DISTRIBUTED:  "DISTRIBUTED — safe",
        RiskLevel.MODERATE:     "MODERATE — watch",
        RiskLevel.CONCENTRATED: "CONCENTRATED — alert",
        RiskLevel.DOMINATED:    "DOMINATED — critical",
    }.get(level, "UNKNOWN")


def score_bar(score: float, width: int = 20) -> str:
    filled = round((score / 100.0) * width)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {score:.0f}/100"
