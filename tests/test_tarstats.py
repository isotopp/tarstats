from __future__ import annotations

from pathlib import Path

from tarstats.cli import main
from tarstats.core import tarstat, tarstats

TEST_TAR = Path(__file__).parent / "testdata" / "testtar.tgz"


def test_tarstat_collects_counts() -> None:
    stats = tarstat(str(TEST_TAR))

    assert stats.name.endswith("testtar.tgz")
    assert stats.size == 112640
    assert stats.filesize == 547
    assert stats.filecounter == 2
    assert stats.dircounter == 1
    assert stats.symlinkcounter == 1
    assert stats.hardlinkcounter == 0
    assert stats.devcounter == 0


def test_tarstats_returns_archive_stats_and_summary() -> None:
    archives, summary = tarstats([str(TEST_TAR), str(TEST_TAR)])

    assert len(archives) == 2
    assert summary.total is True
    assert summary.name == "total"
    assert summary.size == 225280
    assert summary.filesize == 1094
    assert summary.filecounter == 4


def test_cli_json_with_totals(capsys) -> None:
    rc = main(["--json", "--totals", str(TEST_TAR)])

    captured = capsys.readouterr()
    assert rc == 0
    lines = [line for line in captured.out.strip().splitlines() if line]
    assert len(lines) == 2
    assert '"type": "archive"' in lines[0]
    assert '"type": "total"' in lines[1]


def test_cli_rejects_json_and_human_together(capsys) -> None:
    rc = main(["--json", "--human", str(TEST_TAR)])

    captured = capsys.readouterr()
    assert rc == 2
    assert "mutually exclusive" in captured.err
