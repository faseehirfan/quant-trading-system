"""Provider interface for historical market data."""

from __future__ import annotations

from datetime import date
from typing import Protocol

from app.data.models import DailyBar


class MarketDataProvider(Protocol):
    """Fetch historical daily bars for one or more symbols."""

    def fetch_daily_bars(
        self,
        symbol: str,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[DailyBar]:
        """Return normalized daily bars ordered by trading date."""
