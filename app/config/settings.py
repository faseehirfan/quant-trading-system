"""Typed application settings loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, PositiveInt, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed configuration for local development and later deployment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_env: str = Field(default="development", alias="APP_ENV")
    data_dir: Path = Field(default=Path("./data"), alias="DATA_DIR")
    log_dir: Path = Field(default=Path("./logs"), alias="LOG_DIR")
    sqlite_path: Path = Field(default=Path("./data/quant_trading.db"), alias="SQLITE_PATH")
    default_symbols: list[str] = Field(default_factory=lambda: ["SPY"], alias="DEFAULT_SYMBOLS")

    ibkr_host: str = Field(default="127.0.0.1", alias="IBKR_HOST")
    ibkr_port: PositiveInt = Field(default=7497, alias="IBKR_PORT")
    ibkr_client_id: PositiveInt = Field(default=1, alias="IBKR_CLIENT_ID")

    ma_fast_window: PositiveInt = Field(default=20, alias="MA_FAST_WINDOW")
    ma_slow_window: PositiveInt = Field(default=50, alias="MA_SLOW_WINDOW")
    trade_notional_usd: float = Field(default=10_000.0, alias="TRADE_NOTIONAL_USD")
    transaction_cost_bps: float = Field(default=5.0, alias="TRANSACTION_COST_BPS")

    @field_validator("default_symbols", mode="before")
    @classmethod
    def parse_default_symbols(cls, value: object) -> object:
        """Accept either a list of symbols or a comma-separated env string."""
        if isinstance(value, str):
            return [symbol.strip().upper() for symbol in value.split(",") if symbol.strip()]
        return value

    def broker_settings(self) -> tuple[str, int, int]:
        """Return the broker connection tuple used by IBKR clients."""
        return (self.ibkr_host, int(self.ibkr_port), int(self.ibkr_client_id))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cache settings so the process sees a stable configuration object."""
    return Settings()
