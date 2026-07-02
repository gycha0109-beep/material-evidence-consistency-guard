# Material Evidence Consistency Guard

This directory contains the first implementation scaffold for the Codex plugin submission.

## Current CLI

```powershell
python scripts/run_guard.py --help
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo
```

The current CLI only initializes a run and writes `run-meta.json`. Consistency rules, input parsing, fixture data, and PDF parsing are not implemented in this task.
