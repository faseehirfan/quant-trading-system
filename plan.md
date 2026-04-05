# Master Project Plan: Quant Trading System

## Summary
Build a Python-based quantitative trading system that is resume-strong, testable, and eventually hostable. The project should start as a local-first monolith focused on engineering quality, correctness, and paper trading, then expand in controlled phases toward better data quality, multi-symbol support, stronger risk controls, and production-style deployment.

The project’s primary goal is to demonstrate strong software engineering for trading systems. Profitability is a secondary outcome. Version 1 should prove the end-to-end workflow: ingest historical data, generate signals without lookahead bias, backtest, run daily paper-trading decisions through IBKR, persist state, and recover safely after restarts.

## Locked Technical Decisions
- Language/runtime: Python `3.12` for active development; revisit `3.13` after the system is stable.
- Packaging/tooling: `uv`, `pyproject.toml`, `pytest`, `ruff`, `mypy`.
- Core data layer: `pandas` and `numpy`.
- Historical data provider for v1: `yfinance`, wrapped behind a `MarketDataProvider` interface.
- Broker integration for v1: `ib_insync`, wrapped behind a `BrokerClient` interface.
- Persistence for v1: SQLite with SQLAlchemy.
- Operator interface: Typer CLI.
- Configuration: Pydantic Settings with environment variables.
- Architecture: Python monolith with clean internal modules; local-first, Docker/VPS later.
- Trading scope for v1: U.S. equities, daily bars, SPY first, long-only, cash-account assumptions, no leverage, no shorting.

## Implementation Plan

### Phase 1: Foundation and Core Contracts
- Create a single application package with modules for `config`, `data`, `strategies`, `backtest`, `risk`, `broker`, `execution`, `storage`, and `monitoring`.
- Define the canonical internal types up front so every layer shares the same contracts.
- Establish CLI entrypoints: `ingest-data`, `backtest`, `report`, `run-paper`.
- Add typed configuration for paths, broker credentials, symbol list, strategy parameters, transaction costs, and run mode.
- Set up structured logging and stable run IDs from the beginning.
- Add a basic SQLAlchemy schema for runs, orders, fills, positions, and bot state.

### Phase 2: Data Ingestion and Validation
- Implement `MarketDataProvider` with an initial `YahooFinanceDataProvider`.
- Normalize raw data into a canonical daily OHLCV schema before any strategy or backtest logic touches it.
- Persist normalized market data to local files for inspection and reproducibility; use the database for run state, not as the primary v1 historical bar store.
- Add validation for duplicates, missing fields, bad ordering, invalid dates, and non-monotonic bars.
- Make ingestion deterministic and idempotent for repeated runs.

### Phase 3: Baseline Strategy, Risk, and Backtesting
- Implement a deterministic long-only moving-average crossover baseline for SPY daily bars.
- Use explicit signal timing rules that avoid lookahead bias: decisions are based only on information available at the close of the decision bar, with fills modeled on the next tradable bar under the backtest assumptions.
- Build a chronological backtest engine that tracks cash, position, equity curve, order events, and transaction costs.
- Add a minimal risk engine that enforces long-only, one-position-at-a-time, fixed sizing, and cash-availability checks.
- Generate backtest artifacts: trade ledger, equity curve data, summary metrics, and a simple human-readable report.

### Phase 4: Paper-Trading Execution Loop
- Implement `BrokerClient` with an initial `IBKRBrokerClient` using `ib_insync`.
- Build a daily paper-trading runner that:
  1. loads the latest normalized data,
  2. computes the current signal,
  3. reconciles broker balances/positions,
  4. checks whether action is needed,
  5. runs risk checks,
  6. submits a paper order if valid,
  7. records the full run outcome.
- Make the runner restart-safe by persisting bot state and order/run history before and after broker actions.
- Ensure the runner avoids duplicate orders across repeated executions on the same decision date.

### Phase 5: Local Operations and Developer Quality
- Add a clean README with setup, CLI usage, and architecture overview.
- Add local run conventions for logs, data directories, and environment files.
- Add quality gates: lint, type-check, tests, and a small set of make-style or `uv` task aliases if useful.
- Keep the project easy to demo locally on a laptop with minimal external setup beyond Python and IBKR paper access.

### Phase 6: Resume-Strong Extensions After V1
- Add strategy improvements incrementally behind the same strategy interface:
  - 200-day trend filter
  - RSI filter
  - volatility filter
  - volume filter
  - improved exits such as trailing stop, fixed stop, or time-based exit
- Expand from single-symbol to a small ranked basket after the single-symbol workflow is stable.
- Add more realistic execution assumptions in backtests as needed, such as slippage modeling and explicit fill rules.
- Add richer reporting and experiment comparison for parameter sets and runs.

### Phase 7: Production-Style Infrastructure
- Add Docker support after the local paper-trading workflow is stable.
- Standardize mounted volumes for `data/`, `logs/`, and SQLite storage.
- Add scheduled daily execution for the paper bot.
- Prepare for VPS deployment on a low-cost host such as DigitalOcean or Hetzner.
- In the hosted phase, move persistent operational state from SQLite to Postgres if concurrent access, reliability, or inspection needs justify it.
- Keep the system monolithic even in hosted form; do not split services unless operational complexity clearly requires it.

## Public Interfaces and Core Types
- `MarketDataProvider`
  - Responsibility: fetch raw historical daily bars for one or more symbols.
  - Initial implementation: Yahoo Finance.
- `Strategy`
  - Responsibility: consume normalized bars and emit dated `buy`, `sell`, or `hold` decisions plus metadata.
  - Initial implementation: moving-average crossover.
- `RiskEngine`
  - Responsibility: validate proposed actions against account state and portfolio rules.
- `BrokerClient`
  - Responsibility: reconcile positions/cash, submit paper orders, fetch order status and fills.
  - Initial implementation: Interactive Brokers paper account through `ib_insync`.
- `RunStore`
  - Responsibility: persist runs, orders, fills, positions, and bot state.

Canonical internal models:
- `DailyBar`: symbol, trading date, open, high, low, close, volume, source.
- `Signal`: symbol, decision date, action, strategy ID, strategy parameters, reasoning metadata.
- `OrderIntent`: symbol, side, quantity, decision timestamp, reason, originating signal/run ID.
- `ExecutionResult`: broker order ID, timestamps, status, fill info, errors.
- `RunRecord`: run ID, mode (`ingest`, `backtest`, `paper`), inputs, outputs, status, error summary.
- `PositionState`: symbol, quantity, average cost, mark date, unrealized/realized PnL as needed.
- `BotState`: last processed decision date, dedupe markers, latest successful run state.

## Testing and Acceptance Criteria

### Unit and Integration Tests
- Data tests:
  - provider output normalizes into canonical schema
  - duplicate, missing, or out-of-order bars are rejected or flagged
  - date handling is stable and consistent across ingestion and strategy logic
- Strategy tests:
  - crossover signals trigger on the correct bars
  - no future data is used
  - repeated runs on the same data produce identical signals
- Backtest tests:
  - entry/exit sequencing matches strategy intent
  - cash, holdings, and equity remain internally consistent
  - transaction-cost assumptions affect results correctly
- Risk tests:
  - short orders are rejected
  - second concurrent positions are rejected in v1
  - buys without sufficient cash are rejected
  - fixed sizing produces expected quantities
- Paper-run tests:
  - no order is sent when the signal implies no state change
  - restart/re-run on the same day does not duplicate orders
  - broker reconciliation updates local state correctly
  - failures are logged and persisted clearly

### Acceptance Milestones
- V1 is complete when the system can:
  - ingest SPY daily history locally,
  - backtest the baseline strategy,
  - produce a readable report,
  - run one deterministic daily IBKR paper-trading cycle,
  - persist enough state to recover safely after interruption.
- Post-v1 phase work should not begin until the above workflow is stable and test-covered.

## Engineering Workflow
- Use trunk-based development with short-lived branches from `main`.
- Branch naming should match Linear and follow `feature/<identifier>-title` for feature work.
- Use `fix/<identifier>-title`, `docs/<identifier>-title`, and `chore/<identifier>-title` for non-feature work.
- Use Conventional Commits for all commits, such as `feat(data): add canonical daily bar schema`.
- Keep PRs small and ticket-scoped: one implementation-sized Linear ticket should usually map to one PR.
- Link every PR back to its Linear ticket and merge frequently rather than batching large changes.

## Assumptions and Defaults
- The project is optimized for resume/interview value first, profit second.
- Daily bars are the only supported frequency in v1.
- SPY is the first productionized symbol; support for 1 to 3 symbols can be added only after SPY is stable.
- Historical data and generated reports can live in local files in v1; operational run state lives in SQLite.
- `yfinance` is acceptable for v1 because it reduces setup friction, but the data provider must remain swappable.
- IBKR is used only for paper execution in v1, not as the required historical data source.
- Docker, Postgres, dashboards, alerts, multi-symbol portfolio logic, and live deployment are explicitly deferred until after the local end-to-end paper workflow works reliably.
