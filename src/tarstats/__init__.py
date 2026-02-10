"""tarstats developer reference.

`tarstats` can be used both as a command-line tool and as a Python module.

Quick start
-----------

Install development dependencies in this repository:

    uv sync

Run the CLI:

    uv run tarstats --help

Run as a module:

    uv run python -m tarstats --help

Public API
----------

Use :func:`tarstat` for one archive and :func:`tarstats` for many archives.

Example:

    from tarstats import tarstat, tarstats

    single = tarstat("tests/testdata/testtar.tgz")
    print(single.to_dict())

    archives, summary = tarstats([
        "tests/testdata/testtar.tgz",
        "tests/testdata/testtar.tgz",
    ])
    print(summary.to_text(human=True))

Key objects:

- :class:`Stats`: in-memory counters for one archive or totals.
- :class:`StatsEncoder`: JSON encoder for :class:`Stats`.
- :func:`main`: CLI entry function used by the `tarstats` console script.

Developer notes
---------------

- Core reusable logic lives in ``tarstats.core``.
- CLI parsing and output behavior live in ``tarstats.cli``.
- Keep new library behavior testable independent of CLI I/O.
"""

from .cli import main
from .core import Stats, StatsEncoder, tarstat, tarstats

__all__ = ["Stats", "StatsEncoder", "main", "tarstat", "tarstats"]
