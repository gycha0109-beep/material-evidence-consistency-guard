# Material Evidence Consistency Guard

This directory contains the first implementation scaffold for the Codex plugin submission.

## Current CLI

```powershell
python scripts/run_guard.py --help
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite
```

The current CLI validates that the input directory exists, requires `--overwrite` for an existing output directory, and writes `run-meta.json`. Consistency rules, input parsing, fixture data, and PDF parsing are not implemented in this task.
