# Material Evidence Consistency Guard

This directory contains the first implementation scaffold for the Codex plugin submission.

## Current CLI

```powershell
python scripts/run_guard.py --help
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite
```

The current CLI validates that the input directory exists, requires `--overwrite` for an existing output directory, and writes `run-meta.json`. Consistency rules, input parsing, fixture data, and PDF parsing are not implemented in this task.

## Input Policy Fixture

The shared material taxonomy fixture is `fixtures/policy/validation-policy.yml`. It is intentionally JSON-compatible YAML so the current implementation can read it with the Python standard library. Ambiguous aliases such as `down`, `feather`, `다운`, and `깃털` are preserved as ambiguous instead of being treated as mismatches.
