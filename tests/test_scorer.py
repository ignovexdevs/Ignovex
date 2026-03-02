import pytest
from ignovex.models import SignalResult
from ignovex.scorer import compute_risk_score, triggered_count, dominant_signal


def make_signal(name, score, triggered=True, weight=0.25):
    return SignalResult(name=name, score=score, triggered=triggered, detail="test", weight=weight)


class TestComputeRiskScore:
    def test_all_zero_score(self):
        signals = [make_signal(f"s{i}", 0.0, False) for i in range(4)]
        assert compute_risk_score(signals) == pytest.approx(0.0)

    def test_all_100_score(self):
        signals = [make_signal(f"s{i}", 100.0) for i in range(4)]
        assert compute_risk_score(signals) == pytest.approx(100.0)

    def test_weighted_average(self):
        signals = [
            make_signal("a", 80.0, weight=0.35),
            make_signal("b", 60.0, weight=0.30),
            make_signal("c", 40.0, weight=0.20),
            make_signal("d", 20.0, weight=0.15),
        ]
        expected = (80 * 0.35 + 60 * 0.30 + 40 * 0.20 + 20 * 0.15)
        assert compute_risk_score(signals) == pytest.approx(expected, abs=0.01)

    def test_empty_signals_returns_zero(self):
        assert compute_risk_score([]) == 0.0

    def test_single_signal(self):
        signals = [make_signal("only", 75.0, weight=1.0)]
        assert compute_risk_score(signals) == pytest.approx(75.0)

    def test_result_in_range(self, equal_dist):
        from ignovex.signals import run_all_signals
        signals = run_all_signals(equal_dist)
        score = compute_risk_score(signals)
        assert 0.0 <= score <= 100.0

    def test_concentrated_higher_than_equal(self, equal_dist, concentrated_dist):
        from ignovex.signals import run_all_signals
        s_eq  = compute_risk_score(run_all_signals(equal_dist))
        s_con = compute_risk_score(run_all_signals(concentrated_dist))
        assert s_con > s_eq

    def test_unequal_weights_respected(self):
        signals = [
            make_signal("heavy", 100.0, weight=0.9),
            make_signal("light", 0.0, weight=0.1),
        ]
        score = compute_risk_score(signals)
        assert score == pytest.approx(90.0)


class TestTriggeredCount:
    def test_none_triggered(self):
        signals = [make_signal(f"s{i}", 10.0, triggered=False) for i in range(4)]
        assert triggered_count(signals) == 0

    def test_all_triggered(self):
        signals = [make_signal(f"s{i}", 80.0, triggered=True) for i in range(4)]
        assert triggered_count(signals) == 4

    def test_mixed(self):
        signals = [
            make_signal("a", 80.0, triggered=True),
            make_signal("b", 10.0, triggered=False),
            make_signal("c", 70.0, triggered=True),
            make_signal("d", 5.0, triggered=False),
        ]
        assert triggered_count(signals) == 2

    def test_empty(self):
        assert triggered_count([]) == 0


class TestDominantSignal:
    def test_returns_highest_score(self):
        signals = [
            make_signal("a", 30.0),
            make_signal("b", 90.0),
            make_signal("c", 50.0),
        ]
        dom = dominant_signal(signals)
        assert dom.name == "b"

    def test_empty_returns_none(self):
        assert dominant_signal([]) is None

    def test_single_signal(self):
        signals = [make_signal("only", 55.0)]
        assert dominant_signal(signals).name == "only"

    def test_tie_returns_one(self):
        signals = [make_signal("a", 80.0), make_signal("b", 80.0)]
        dom = dominant_signal(signals)
        assert dom.score == 80.0
