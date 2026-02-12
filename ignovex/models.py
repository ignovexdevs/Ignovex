from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class RiskLevel(str, Enum):
    DISTRIBUTED  = "DISTRIBUTED"    # 0–25
    MODERATE     = "MODERATE"       # 26–50
    CONCENTRATED = "CONCENTRATED"   # 51–75
    DOMINATED    = "DOMINATED"      # 76–100


@dataclass
class HolderRecord:
    address:        str
    balance:        float   # token units held
    wallet_age_days: float  # days since first on-chain tx
    is_lp:          bool = False


@dataclass
class TokenDistribution:
    token_mint:       str
    total_supply:     float
    holders:          List[HolderRecord]
    lp_total_balance: float = 0.0
    timestamp:        float = field(default_factory=time.time)

    def holder_count(self) -> int:
        return len(self.holders)

    def non_lp_holders(self) -> List[HolderRecord]:
        return [h for h in self.holders if not h.is_lp]


@dataclass
class SignalResult:
    name:      str
    score:     float   # 0–100 (higher = more risk)
    triggered: bool
    detail:    str
    weight:    float


@dataclass
class ConcentrationReport:
    risk_level:     RiskLevel
    risk_score:     float
    signals:        List[SignalResult]
    recommendation: str
    timestamp:      float = field(default_factory=time.time)
