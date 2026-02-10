# tarstats

`tarstats` prints compact statistics for one or more tar archives.

## Install

### From source (with uv)

```console
uv sync
```

## Command line usage

Run through `uv` in this repository:

```console
uv run tarstats --help
```

or install with

```console
uv tool install .
```

Basic example:

```console
uv run tarstats tests/testdata/testtar.tgz
```

JSON output:

```console
uv run tarstats --json tests/testdata/testtar.tgz
```

Totals across multiple archives:

```console
uv run tarstats --totals tests/testdata/testtar.tgz tests/testdata/testtar.tgz
```

Human-readable rounded values:

```console
uv run tarstats --human tests/testdata/testtar.tgz
```

`--json` and `--human` are mutually exclusive.

## Use as a module

```python
from tarstats import tarstat, tarstats

single = tarstat("tests/testdata/testtar.tgz")
print(single.to_dict())

archives, summary = tarstats([
    "tests/testdata/testtar.tgz",
    "tests/testdata/testtar.tgz",
])

for item in archives:
    print(item.to_text(human=False))

print(summary.to_dict())
```

Available public imports:

- `tarstats.tarstat(path)`
- `tarstats.tarstats(paths)`
- `tarstats.Stats`
- `tarstats.StatsEncoder`
- `tarstats.main` (CLI entry function)
