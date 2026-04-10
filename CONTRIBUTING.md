# Contributing to Ignovex

## Getting Started

```bash
git clone https://github.com/ignovexdev/Ignovex.git
cd Ignovex
pip install -e ".[dev]"
pytest tests/ -v
```

## Branch Strategy

- `main` — stable releases
- `feature/<name>` — new features
- `fix/<name>` — bug fixes

## Commit Style

```
feat(module): description
fix(module): description
test(module): description
docs: description
chore: description
```

## Adding Signals

1. Add signal function to `ignovex/signals.py`
2. Register in `run_all_signals()`
3. Adjust weights to sum to 1.0
4. Add tests in `tests/test_signals.py`
5. Update TypeScript types in `dashboard/src/types.ts`

## Pull Request

- All tests must pass: `pytest tests/ -v`
- New signals require minimum 5 tests each
- Keep core logic dependency-free

## Code of Conduct

Be direct. Ship working code.
