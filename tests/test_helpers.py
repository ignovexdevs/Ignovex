import pytest
from ignovex.models import RiskLevel
from ignovex.utils.helpers import (
    clamp, format_supply, format_pct, format_score,
    format_gini, ts_to_str, level_color, level_badge, score_bar,
)


class TestClamp:
    def test_within_range(self):
        assert clamp(50.0, 0.0, 100.0) == 50.0

    def test_below_min(self):
        assert clamp(-10.0, 0.0, 100.0) == 0.0

    def test_above_max(self):
        assert clamp(150.0, 0.0, 100.0) == 100.0

    def test_at_boundary(self):
        assert clamp(0.0, 0.0, 100.0) == 0.0
        assert clamp(100.0, 0.0, 100.0) == 100.0


class TestFormatSupply:
    def test_billions(self):
        assert format_supply(1_000_000_000) == "1.00B"

    def test_millions(self):
        assert format_supply(5_500_000) == "5.50M"

    def test_thousands(self):
        assert format_supply(3_200) == "3.20K"

    def test_small(self):
        assert format_supply(500) == "500"

    def test_1b_token_supply(self):
        assert "B" in format_supply(1_073_000_000)


class TestFormatPct:
    def test_basic(self):
        assert format_pct(42.5) == "42.5%"

    def test_zero(self):
        assert format_pct(0.0) == "0.0%"

    def test_100(self):
        assert format_pct(100.0) == "100.0%"


class TestFormatScore:
    def test_basic(self):
        assert format_score(75.3) == "75.3"

    def test_zero(self):
        assert format_score(0.0) == "0.0"


class TestFormatGini:
    def test_three_decimals(self):
        assert format_gini(0.654321) == "0.654"

    def test_zero(self):
        assert format_gini(0.0) == "0.000"


class TestTsToStr:
    def test_returns_string(self):
        import time
        result = ts_to_str(time.time())
        assert isinstance(result, str)
        assert len(result) > 0

    def test_format_pattern(self):
        import time
        result = ts_to_str(time.time())
        assert "-" in result
        assert ":" in result


class TestLevelColor:
    def test_distributed_green(self):
        assert level_color(RiskLevel.DISTRIBUTED) == "#22c55e"

    def test_moderate_amber(self):
        assert level_color(RiskLevel.MODERATE) == "#f59e0b"

    def test_concentrated_red(self):
        assert level_color(RiskLevel.CONCENTRATED) == "#ef4444"

    def test_dominated_darkred(self):
        assert level_color(RiskLevel.DOMINATED) == "#dc2626"


class TestLevelBadge:
    def test_distributed_badge(self):
        badge = level_badge(RiskLevel.DISTRIBUTED)
        assert "DISTRIBUTED" in badge

    def test_dominated_badge(self):
        badge = level_badge(RiskLevel.DOMINATED)
        assert "DOMINATED" in badge

    def test_concentrated_alert(self):
        badge = level_badge(RiskLevel.CONCENTRATED)
        assert "alert" in badge.lower() or "CONCENTRATED" in badge


class TestScoreBar:
    def test_zero_score(self):
        bar = score_bar(0.0, width=10)
        assert "0/100" in bar

    def test_full_score(self):
        bar = score_bar(100.0, width=10)
        assert "100/100" in bar

    def test_contains_brackets(self):
        bar = score_bar(50.0)
        assert "[" in bar and "]" in bar

    def test_custom_width(self):
        bar = score_bar(50.0, width=20)
        assert len(bar) > 0
