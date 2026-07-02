# Material Evidence Consistency Guard

This directory contains the first implementation scaffold for the Codex plugin submission.

## Current CLI

```powershell
python scripts/run_guard.py --help
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite
```

The current CLI validates the structural input contract, requires `--overwrite` for an existing output directory, and writes run metadata plus normalized, finding, evidence-map, and human-review Markdown outputs.

## Test Report Input

`test-report.md` is used first when present. If it is missing and `test-report.pdf` exists, the guard attempts limited text extraction without OCR or external services.

If both report files are absent, that is not an input contract error. When high-risk material or fill is present, the rules layer classifies the absence as an R-001 evidence-missing finding. If a report file exists but is unreadable or lacks core comparison fields, the rules layer classifies it as R-002.

## Input Policy Fixture

The shared material taxonomy fixture is `fixtures/policy/validation-policy.yml`. It is intentionally JSON-compatible YAML so the current implementation can read it with the Python standard library. Ambiguous aliases such as `down`, `feather`, `다운`, and `깃털` are preserved as ambiguous instead of being treated as mismatches.
