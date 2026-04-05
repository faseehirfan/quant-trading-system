"""Settings tests."""

from app.config.settings import Settings


def test_settings_parse_env_values() -> None:
    settings = Settings(
        APP_ENV="test",
        DATA_DIR="./tmp/data",
        LOG_DIR="./tmp/logs",
        SQLITE_PATH="./tmp/trading.db",
        DEFAULT_SYMBOLS="SPY,QQQ",
        IBKR_HOST="localhost",
        IBKR_PORT=4002,
        IBKR_CLIENT_ID=7,
        MA_FAST_WINDOW=10,
        MA_SLOW_WINDOW=30,
        TRADE_NOTIONAL_USD=2500,
        TRANSACTION_COST_BPS=2.5,
    )

    assert settings.app_env == "test"
    assert settings.default_symbols == ["SPY", "QQQ"]
    assert settings.broker_settings() == ("localhost", 4002, 7)
    assert settings.ma_fast_window == 10
    assert settings.trade_notional_usd == 2500
