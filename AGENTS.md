# AGENTS.md

This document defines expectations for human developers and coding agents working on this repository.

## Project summary

- Project: `tarstats`
- Purpose: produce summary statistics for tar archives
- Language: Python
- Packaging: `uv` + `pyproject.toml` (`hatchling` build backend)
- Source layout: `src/` package layout

## Development environment

- Python version: use a version compatible with `requires-python` in `pyproject.toml`
- Install deps: `uv sync`
- Add runtime dependency: `uv add <package>`
- Add dev dependency: `uv add --dev <package>`

## Required quality workflow

Run these commands before submitting changes:

```console
uv run ruff format src tests
uv run ruff check --fix src tests
uv run mypy src
uv run pytest
```

## Coding guidelines

- Keep the public API importable from `tarstats` (`src/tarstats/__init__.py`)
- Keep CLI code in `src/tarstats/cli.py`; keep reusable logic in `src/tarstats/core.py`
- Preserve backward-compatible CLI flags unless intentionally changing behavior
- Prefer explicit types and small focused functions
- Keep user-facing docs in `README.md` up to date when behavior changes

## Testing guidelines

- Add or update tests for all behavior changes
- Prefer deterministic tests against `tests/testdata/`
- Avoid network access in tests

## Release checklist

- Bump version in `pyproject.toml` when making a release
- Ensure lint, type-check, and tests pass
- Verify CLI help text: `uv run tarstats --help`

## Agents-only guardrails

- Do not rewrite history or run destructive git commands unless explicitly requested
- Do not remove or silently change public API behavior without tests and README updates
- Do not introduce new dependencies without clear need
- Do not bypass the required quality workflow; if a step fails, report it explicitly
- Keep edits minimal and targeted; avoid drive-by refactors unrelated to the task
