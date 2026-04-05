# Quant Trading System

Quant trading system with backtesting, risk controls, and IBKR paper execution.

## Project Direction
The canonical project roadmap lives in [`plan.md`](plan.md). It replaces the earlier planning drafts and is the single planning source of truth for the repo.

## Local Setup
This project targets Python `3.12` and uses `uv` for environment and dependency management.

```bash
uv sync
cp .env.example .env
uv run pytest
uv run ruff check .
uv run mypy app
```

The first implementation batch is intentionally local-first:
- daily-bar workflows only
- `yfinance` for historical data
- `ib_insync` for Interactive Brokers paper execution
- SQLite for operational state

## Repository Layout
```text
app/
  backtest/
  broker/
  config/
  data/
  execution/
  monitoring/
  risk/
  storage/
  strategies/
tests/
scripts/
data/
logs/
```

## Configuration
Typed settings live in [`app/config/settings.py`](app/config/settings.py) and load from environment variables. Start from [`.env.example`](.env.example) and override values locally as needed.

Current configuration areas:
- application environment and filesystem paths
- default trading symbols
- broker connectivity for IBKR paper trading
- baseline strategy parameters

## CLI
The CLI is exposed through the `qts` entrypoint.

```bash
uv run qts ingest-data
uv run qts backtest
uv run qts report
uv run qts run-paper
```

The commands are stubbed during the foundation phase and will be filled in ticket by ticket.

## Engineering Workflow
- Use trunk-based development with short-lived branches from `main`.
- Branch naming should match Linear and follow `feature/<identifier>-title` for feature work.
- Use `fix/<identifier>-title`, `docs/<identifier>-title`, and `chore/<identifier>-title` for non-feature work.
- Use Conventional Commits for all commits, such as `feat(data): add canonical daily bar schema`.
- Keep PRs small and ticket-scoped: one implementation-sized Linear ticket should usually map to one PR.
- Link every PR back to its Linear ticket and merge frequently rather than batching large changes.

## Review Expectations
- Default review standard is correctness first: bugs, behavior regressions, and missing tests matter more than style nits.
- Changes should include or update tests when they add logic, contracts, or validation.
- Avoid bundling unrelated refactors into the same PR.
