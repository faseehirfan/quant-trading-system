"""Canonical market-data models shared across the system."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class DailyBar(BaseModel):
    """Canonical normalized daily OHLCV bar."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    symbol: str = Field(min_length=1)
    date: date
    open: Decimal = Field(gt=0)
    high: Decimal = Field(gt=0)
    low: Decimal = Field(gt=0)
    close: Decimal = Field(gt=0)
    volume: int = Field(ge=0)
    source: str = Field(min_length=1)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        """Use uppercase ticker symbols across the codebase."""
        return value.upper()

    @model_validator(mode="after")
    def validate_price_relationships(self) -> DailyBar:
        """Reject bars whose OHLC relationship is impossible."""
        if self.low > self.high:
            raise ValueError("low cannot exceed high")
        if not (self.low <= self.open <= self.high):
            raise ValueError("open must be between low and high")
        if not (self.low <= self.close <= self.high):
            raise ValueError("close must be between low and high")
        return self
