"""Tests for the canonical daily bar schema."""

from datetime import date
from decimal import Decimal

import pytest

from app.data.models import DailyBar


def test_daily_bar_normalizes_symbol_and_keeps_required_fields() -> None:
    bar = DailyBar(
        symbol="spy",
        date=date(2024, 1, 2),
        open=Decimal("470.25"),
        high=Decimal("472.00"),
        low=Decimal("469.10"),
        close=Decimal("471.50"),
        volume=123456,
        source="yfinance",
    )

    assert bar.symbol == "SPY"
    assert bar.source == "yfinance"
    assert bar.close == Decimal("471.50")


def test_daily_bar_rejects_invalid_ohlc_relationships() -> None:
    with pytest.raises(ValueError, match="low cannot exceed high"):
        DailyBar(
            symbol="SPY",
            date=date(2024, 1, 2),
            open=Decimal("470.25"),
            high=Decimal("469.00"),
            low=Decimal("470.00"),
            close=Decimal("469.50"),
            volume=123456,
            source="yfinance",
        )
