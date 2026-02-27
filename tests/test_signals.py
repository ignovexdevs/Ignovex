import pytest
from ignovex.models import HolderRecord, TokenDistribution
from ignovex.signals import (
    gini_signal, whale_dominance_signal, fresh_wallet_signal,
    lp_concentration_signal, run_all_signals,
    GINI_TRIGGER, WHALE_TOP10_PCT, FRESH_WALLET_PCT, LP_CONCENTRATION_PCT,
    GINI_WEIGHT, WHALE_WEIGHT, FRESH_WEIGHT, LP_WEIGHT,
)
from tests.conftest import make_dist


class TestGiniSignal:
    def test_equal_dist_not_triggered(self, equal_dist):
        r = gini_signal(equal_dist)
        assert r.triggered is False
        assert r.name == "gini"

    def test_concentrated_triggered(self, concentrated_dist):
        r = gini_signal(concentrated_dist)
        assert r.triggered is True

    def test_score_range(self, equal_dist):
        r = gini_signal(equal_dist)
        assert 0.0 <= r.score <= 100.0

    def test_concentrated_higher_score_than_equal(self, equal_dist, concentrated_dist):
        r_eq = gini_signal(equal_dist)
        r_con = gini_signal(concentrated_dist)
        assert r_con.score > r_eq.score

    def test_single_holder_max_gini(self):
        holders = [HolderRecord("solo", 1_000_000.0, 30.0)]
        dist = make_dist(holders=holders, total_supply=1_000_000.0)
        r = gini_signal(dist)
        # Single holder returns 0 (no inequality measurable)
        assert r.score == 0.0

    def test_empty_holders(self):
        dist = make_dist(holders=[], total_supply=1_000_000.0)
        r = gini_signal(dist)
        assert r.score == 0.0
        assert r.triggered is False

    def test_weight_correct(self, equal_dist):
        r = gini_signal(equal_dist)
        assert r.weight == GINI_WEIGHT

    def test_detail_contains_gini(self, equal_dist):
        r = gini_signal(equal_dist)
        assert "Gini=" in r.detail

    def test_lp_holders_excluded(self):
        holders = [
            HolderRecord("lp", 900_000.0, 10.0, is_lp=True),
            HolderRecord("h1", 50_000.0, 30.0),
            HolderRecord("h2", 50_000.0, 30.0),
        ]
        dist = make_dist(holders=holders, total_supply=1_000_000.0)
        r = gini_signal(dist)
        # only 2 equal holders → gini=0
        assert r.score == 0.0


class TestWhaleDominanceSignal:
    def test_equal_dist_all_top10(self, equal_dist):
        # 10 equal holders → top-10 = 100% → triggers above 40% threshold
        r = whale_dominance_signal(equal_dist)
        assert r.triggered is True
        assert r.score == pytest.approx(100.0, abs=0.1)

    def test_concentrated_triggered(self, concentrated_dist):
        r = whale_dominance_signal(concentrated_dist)
        assert r.triggered is True

    def test_score_range(self, equal_dist):
        r = whale_dominance_signal(equal_dist)
        assert 0.0 <= r.score <= 100.0

    def test_equal_dist_score(self, equal_dist):
        r = whale_dominance_signal(equal_dist)
        # 10 equal holders, top-10 = all = 100%
        assert r.score == pytest.approx(100.0, abs=0.1)
        assert r.triggered is True

    def test_large_holder_pool_low_whale_pct(self):
        holders = [HolderRecord(f"h{i}", 1000.0, 30.0) for i in range(200)]
        dist = make_dist(holders=holders, total_supply=200_000.0)
        r = whale_dominance_signal(dist)
        # top-10 hold 10/200 = 5%
        assert r.score < WHALE_TOP10_PCT
        assert r.triggered is False

    def test_weight_correct(self, equal_dist):
        r = whale_dominance_signal(equal_dist)
        assert r.weight == WHALE_WEIGHT

    def test_detail_contains_pct(self, concentrated_dist):
        r = whale_dominance_signal(concentrated_dist)
        assert "%" in r.detail

    def test_zero_supply_no_crash(self):
        holders = [HolderRecord("h", 100.0, 30.0)]
        dist = make_dist(holders=holders, total_supply=0.0)
        r = whale_dominance_signal(dist)
        assert r.score >= 0.0

    def test_empty_holders_zero_score(self):
        dist = make_dist(holders=[], total_supply=1_000_000.0)
        r = whale_dominance_signal(dist)
        assert r.score == 0.0
        assert r.triggered is False


class TestFreshWalletSignal:
    def test_all_old_not_triggered(self, equal_dist):
        r = fresh_wallet_signal(equal_dist)
        assert r.triggered is False

    def test_fresh_wallet_dist_triggered(self, fresh_wallet_dist):
        r = fresh_wallet_signal(fresh_wallet_dist)
        assert r.triggered is True

    def test_50pct_fresh_triggers(self):
        holders = [HolderRecord(f"n{i}", 100.0, 2.0) for i in range(5)]
        holders += [HolderRecord(f"o{i}", 100.0, 30.0) for i in range(5)]
        dist = make_dist(holders=holders)
        r = fresh_wallet_signal(dist)
        assert r.triggered is True

    def test_score_range(self, fresh_wallet_dist):
        r = fresh_wallet_signal(fresh_wallet_dist)
        assert 0.0 <= r.score <= 100.0

    def test_all_fresh_max_score(self):
        holders = [HolderRecord(f"n{i}", 100.0, 1.0) for i in range(10)]
        dist = make_dist(holders=holders)
        r = fresh_wallet_signal(dist)
        assert r.score == 100.0

    def test_empty_holders_no_crash(self):
        dist = make_dist(holders=[])
        r = fresh_wallet_signal(dist)
        assert r.score == 0.0
        assert r.triggered is False

    def test_weight_correct(self, equal_dist):
        r = fresh_wallet_signal(equal_dist)
        assert r.weight == FRESH_WEIGHT

    def test_exactly_7_days_not_fresh(self):
        holders = [HolderRecord("h", 100.0, 7.0)]
        dist = make_dist(holders=holders)
        r = fresh_wallet_signal(dist)
        assert r.triggered is False


class TestLpConcentrationSignal:
    def test_no_lp_not_triggered(self, equal_dist):
        r = lp_concentration_signal(equal_dist)
        assert r.triggered is False
        assert r.score == 0.0

    def test_heavy_lp_triggered(self, lp_heavy_dist):
        r = lp_concentration_signal(lp_heavy_dist)
        assert r.triggered is True

    def test_score_equals_pct(self):
        dist = make_dist(total_supply=1_000_000.0, lp_balance=300_000.0)
        r = lp_concentration_signal(dist)
        assert r.score == pytest.approx(30.0, abs=0.01)

    def test_100pct_lp_max_score(self):
        dist = make_dist(total_supply=1_000_000.0, lp_balance=1_000_000.0)
        r = lp_concentration_signal(dist)
        assert r.score == 100.0

    def test_weight_correct(self, equal_dist):
        r = lp_concentration_signal(equal_dist)
        assert r.weight == LP_WEIGHT

    def test_zero_supply_no_crash(self):
        dist = make_dist(total_supply=0.0, lp_balance=0.0)
        r = lp_concentration_signal(dist)
        assert r.score == 0.0


class TestRunAllSignals:
    def test_returns_four_signals(self, equal_dist):
        signals = run_all_signals(equal_dist)
        assert len(signals) == 4

    def test_signal_names(self, equal_dist):
        signals = run_all_signals(equal_dist)
        names = [s.name for s in signals]
        assert "gini" in names
        assert "whale_dominance" in names
        assert "fresh_wallet" in names
        assert "lp_concentration" in names

    def test_weights_sum_to_one(self, equal_dist):
        signals = run_all_signals(equal_dist)
        total = sum(s.weight for s in signals)
        assert total == pytest.approx(1.0, abs=0.001)

    def test_dominated_dist_all_high(self, dominated_dist):
        signals = run_all_signals(dominated_dist)
        triggered = [s for s in signals if s.triggered]
        assert len(triggered) >= 2
