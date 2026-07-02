# Material Evidence Consistency Guard

This directory contains the runnable Codex plugin submission files, fixtures, scripts, and tests.

## Inputs

Each fixture input directory uses these five input types:

- `product-draft.json`
- `product-notice.json`
- `detail-page.md`
- `test-report.md` or `test-report.pdf`
- `validation-policy.yml`

`test-report.md` is used first when present. If Markdown is missing and `test-report.pdf` exists, the guard attempts limited text extraction through the optional `pypdf` dependency. If both are absent, validation still succeeds and the rules layer can classify missing evidence as R-001 when high-risk material or fill is present. No OCR, image analysis, external SaaS, or web API is used.

## Outputs

The main human-review outputs are:

- `findings.json`
- `evidence-map.json`
- `review-report.md`
- `human-review-queue.md`

The CLI also writes `run-meta.json`, `normalized.json`, and `rules-debug.json` for traceability and debugging.

## Implemented Rules

- R-001: high-risk material or fill exists, but no test-report input was supplied.
- R-002: a report exists, but it is unreadable or lacks required comparison fields.
- R-003: the test-report target product or SKU does not clearly connect to the registered product.
- R-004: material or fill ratios differ beyond the configured tolerance after product-evidence linking.
- R-005: explicit detail-page material, ratio, or all-option scope claims exceed the test-report evidence scope.
- R-006: variant materials differ while test-report evidence covers only part of the option set.

## Priority Gates

The rules run conservatively:

1. R-001 handles absent evidence for high-risk material or fill and stops downstream rules.
2. R-002 handles unreadable or incomplete report evidence and stops downstream rules.
3. R-003 handles target product or SKU mismatch and stops R-004 through R-006 when mismatch is high severity.
4. R-004 through R-006 run only after the higher-priority gates allow comparison.

Ambiguous aliases are preserved as review findings or uncertainties rather than automatic high-severity mismatches.

## Fixtures

The regression suite covers these canonical fixtures:

- `01-pass-consistent`
- `02-missing-evidence`
- `03-report-extraction-failure`
- `04-product-target-mismatch`
- `05-ratio-conflict`
- `06-detail-overclaim`
- `07-variant-scope-gap`
- `08-ambiguous-alias`

## Commands

Run one fixture:

```powershell
python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite
```

Run the fixture regression suite:

```powershell
python scripts/run_fixture_suite.py
```

Run all tests:

```powershell
python -m unittest discover -s tests
```

## Scope Limits

This tool does not make legal determinations, approve or block sales, judge certificate authenticity, or decide whether advertising is false. It does not use OCR SaaS, Musinsa APIs, chatbots, or product recommendations. The output is a consistency review aid only, and a human reviewer makes the final judgment.
