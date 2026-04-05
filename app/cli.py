"""Typer CLI entrypoints for local operator workflows."""

import typer

app = typer.Typer(help="Quant trading system operator CLI.")


@app.command("ingest-data")
def ingest_data() -> None:
    """Fetch and normalize historical market data."""
    typer.echo("ingest-data is not implemented yet.")


@app.command()
def backtest() -> None:
    """Run the configured backtest workflow."""
    typer.echo("backtest is not implemented yet.")


@app.command()
def report() -> None:
    """Generate a report for a prior run."""
    typer.echo("report is not implemented yet.")


@app.command("run-paper")
def run_paper() -> None:
    """Execute one paper-trading decision cycle."""
    typer.echo("run-paper is not implemented yet.")
