import time
import pytest
from ignovex.models import HolderRecord, TokenDistribution, SignalResult, ConcentrationReport, RiskLevel


class TestHolderRecord:
    def test_basic_creation(self):
        h = HolderRecord(address="abc", balance=1000.0, wallet_age_days=10.0)
        assert h.address == "abc"
        assert h.balance == 1000.0
        assert h.wallet_age_days == 10.0
        assert h.is_lp is False

    def test_lp_holder(self):
        h = HolderRecord(address="lp", balance=500_000.0, wallet_age_days=5.0, is_lp=True)
        assert h.is_lp is True

    def test_zero_balance(self):
        h = HolderRecord(address="dust", balance=0.0, wallet_age_days=100.0)
        assert h.balance == 0.0

    def test_fresh_wallet(self):
        h = HolderRecord(address="new", balance=50_000.0, wallet_age_days=1.5)
        assert h.wallet_age_days < 7

    def test_old_wallet(self):
        h = HolderRecord(address="veteran", balance=50_000.0, wallet_age_days=365.0)
        assert h.wallet_age_days >= 7


class TestTokenDistribution:
    def test_holder_count(self, equal_dist):
        assert equal_dist.holder_count() == 10

    def test_non_lp_holders_excludes_lp(self):
        from ignovex.models import HolderRecord, TokenDistribution
        holders = [
            HolderRecord("h1", 100_000.0, 30.0, is_lp=False),
            HolderRecord("h2", 100_000.0, 30.0, is_lp=True),
        ]
        dist = TokenDistribution("mint", 200_000.0, holders, lp_total_balance=100_000.0)
        assert len(dist.non_lp_holders()) == 1
        assert dist.non_lp_holders()[0].address == "h1"

    def test_timestamp_auto(self):
        from ignovex.models import TokenDistribution
        before = time.time()
        dist = TokenDistribution("mint", 1_000_000.0, [])
        after = time.time()
        assert before <= dist.timestamp <= after

    def test_empty_holders(self):
        from ignovex.models import TokenDistribution
        dist = TokenDistribution("mint", 1_000_000.0, [])
        assert dist.holder_count() == 0
        assert dist.non_lp_holders() == []

    def test_all_lp_holders(self):
        from ignovex.models import HolderRecord, TokenDistribution
        holders = [HolderRecord(f"lp{i}", 100_000.0, 10.0, is_lp=True) for i in range(5)]
        dist = TokenDistribution("mint", 500_000.0, holders)
        assert dist.non_lp_holders() == []

    def test_lp_balance_field(self, lp_heavy_dist):
        assert lp_heavy_dist.lp_total_balance == 600_000.0


class TestSignalResult:
    def test_triggered_true(self):
        s = SignalResult(name="gini", score=80.0, triggered=True, detail="high", weight=0.35)
        assert s.triggered is True
        assert s.score == 80.0

    def test_triggered_false(self):
        s = SignalResult(name="gini", score=20.0, triggered=False, detail="low", weight=0.35)
        assert s.triggered is False

    def test_score_bounds(self):
        s = SignalResult(name="test", score=100.0, triggered=True, detail="max", weight=1.0)
        assert s.score == 100.0

    def test_weight_field(self):
        s = SignalResult(name="whale", score=50.0, triggered=True, detail="ok", weight=0.30)
        assert s.weight == 0.30


class TestRiskLevel:
    def test_all_levels_exist(self):
        assert RiskLevel.DISTRIBUTED
        assert RiskLevel.MODERATE
        assert RiskLevel.CONCENTRATED
        assert RiskLevel.DOMINATED

    def test_level_values(self):
        assert RiskLevel.DISTRIBUTED.value == "DISTRIBUTED"
        assert RiskLevel.DOMINATED.value == "DOMINATED"


class TestConcentrationReport:
    def test_creation(self):
        report = ConcentrationReport(
            risk_level=RiskLevel.MODERATE,
            risk_score=45.0,
            signals=[],
            recommendation="Watch closely.",
        )
        assert report.risk_level == RiskLevel.MODERATE
        assert report.risk_score == 45.0

    def test_timestamp_auto(self):
        before = time.time()
        report = ConcentrationReport(RiskLevel.DISTRIBUTED, 10.0, [], "Safe.")
        after = time.time()
        assert before <= report.timestamp <= after
