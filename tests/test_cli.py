from click.testing import CliRunner
from infradocs.cli import cli
from pathlib import Path

SAMPLE = Path(__file__).parent.parent / "sample-data"

def test_validate_command_passes(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--input", str(SAMPLE)])
    assert result.exit_code == 0

def test_build_command(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["build", "--input", str(SAMPLE), "--output", str(tmp_path / "site")])
    assert result.exit_code == 0
    assert (tmp_path / "site" / "index.html").exists()
