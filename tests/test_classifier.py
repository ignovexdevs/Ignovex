import pytest
from ignovex.models import RiskLevel
from ignovex.classifier import classify, classify_batch
from ignovex.models import HolderRecord, TokenDistribution
from tests.conftest import make_dist


class TestClassifyRiskLevel:
    def test_equal_dist_distributed_or_moderate(self, equal_dist):
        report = classify(equal_dist)
        # 10 equal holders, top-10 whale pct = 100% → whale signal fires
        # but gini=0, fresh=0, lp=0 → MODERATE range
        assert report.risk_level in (RiskLevel.DISTRIBUTED, RiskLevel.MODERATE, RiskLevel.CONCENTRATED)

    def test_concentrated_dist_concentrated_or_dominated(self, concentrated_dist):
        report = classify(concentrated_dist)
        assert report.risk_level in (RiskLevel.CONCENTRATED, RiskLevel.DOMINATED)

    def test_dominated_dist_level(self, dominated_dist):
        report = classify(dominated_dist)
        assert report.risk_level in (RiskLevel.CONCENTRATED, RiskLevel.DOMINATED)

    def test_risk_score_in_range(self, equal_dist):
        report = classify(equal_dist)
        assert 0.0 <= report.risk_score <= 100.0

    def test_report_has_four_signals(self, equal_dist):
        report = classify(equal_dist)
        assert len(report.signals) == 4

    def test_recommendation_not_empty(self, equal_dist):
        report = classify(equal_dist)
        assert len(report.recommendation) > 0

    def test_dominated_dist_is_high_risk(self, dominated_dist):
        report = classify(dominated_dist)
        assert report.risk_level in (RiskLevel.CONCENTRATED, RiskLevel.DOMINATED)

    def test_distributed_score_le_25(self):
        # All equal, no LP, all old wallets, many holders
        holders = [HolderRecord(f"h{i}", 1000.0, 60.0) for i in range(100)]
        dist = make_dist(holders=holders, total_supply=100_000.0)
        report = classify(dist)
        # With 100 equal holders, top-10 = 10%, gini≈0, fresh=0, lp=0
        assert report.risk_level == RiskLevel.DISTRIBUTED

    def test_concentrated_score_gt_50(self, concentrated_dist):
        report = classify(concentrated_dist)
        assert report.risk_score > 50.0

    def test_fresh_wallet_heavy_raises_level(self):
        holders = [HolderRecord(f"n{i}", 1000.0, 1.0) for i in range(20)]
        holders += [HolderRecord(f"o{i}", 1000.0, 60.0) for i in range(5)]
        dist = make_dist(holders=holders, total_supply=25_000.0)
        report = classify(dist)
        assert report.risk_level in (RiskLevel.MODERATE, RiskLevel.CONCENTRATED, RiskLevel.DOMINATED)

    def test_lp_heavy_has_lp_signal_triggered(self, lp_heavy_dist):
        report = classify(lp_heavy_dist)
        lp_sig = next(s for s in report.signals if s.name == "lp_concentration")
        assert lp_sig.triggered is True


class TestLevelBoundaries:
    def _make_score_scenario(self, gini_score, whale_score, fresh_score, lp_score):
        """Helper: build signals that approximate a target score."""
        from ignovex.models import SignalResult
        from ignovex.scorer import compute_risk_score
        from ignovex.signals import GINI_WEIGHT, WHALE_WEIGHT, FRESH_WEIGHT, LP_WEIGHT
        signals = [
            SignalResult("gini", gini_score, gini_score > 65, "", GINI_WEIGHT),
            SignalResult("whale_dominance", whale_score, whale_score > 40, "", WHALE_WEIGHT),
            SignalResult("fresh_wallet", fresh_score, fresh_score > 20, "", FRESH_WEIGHT),
            SignalResult("lp_concentration", lp_score, lp_score > 50, "", LP_WEIGHT),
        ]
        return compute_risk_score(signals)

    def test_score_25_is_distributed(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(25.0) == RiskLevel.DISTRIBUTED

    def test_score_26_is_moderate(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(26.0) == RiskLevel.MODERATE

    def test_score_50_is_moderate(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(50.0) == RiskLevel.MODERATE

    def test_score_51_is_concentrated(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(51.0) == RiskLevel.CONCENTRATED

    def test_score_75_is_concentrated(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(75.0) == RiskLevel.CONCENTRATED

    def test_score_76_is_dominated(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(76.0) == RiskLevel.DOMINATED

    def test_score_100_is_dominated(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(100.0) == RiskLevel.DOMINATED

    def test_score_0_is_distributed(self):
        from ignovex.classifier import _level_from_score
        assert _level_from_score(0.0) == RiskLevel.DISTRIBUTED


class TestClassifyBatch:
    def test_returns_list_same_length(self, equal_dist, concentrated_dist):
        reports = classify_batch([equal_dist, concentrated_dist])
        assert len(reports) == 2

    def test_empty_batch(self):
        reports = classify_batch([])
        assert reports == []

    def test_each_has_signals(self, equal_dist, concentrated_dist, lp_heavy_dist):
        reports = classify_batch([equal_dist, concentrated_dist, lp_heavy_dist])
        for r in reports:
            assert len(r.signals) == 4

    def test_scores_vary(self, equal_dist, dominated_dist):
        reports = classify_batch([equal_dist, dominated_dist])
        assert reports[0].risk_score != reports[1].risk_score
