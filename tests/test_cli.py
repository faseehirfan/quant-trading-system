"""CLI smoke tests."""

from typer.testing import CliRunner

from app.cli import app

runner = CliRunner()


def test_cli_registers_expected_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "ingest-data" in result.stdout
    assert "backtest" in result.stdout
    assert "report" in result.stdout
    assert "run-paper" in result.stdout
