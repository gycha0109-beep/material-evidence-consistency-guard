# Final Verification

## Execution Date

2026-07-02 16:12:17 +09:00

## Commands

```powershell
cd src
python scripts/run_fixture_suite.py
python -m unittest discover -s tests
python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite
```

## Results

- `python scripts/run_fixture_suite.py`: passed; 8 canonical fixtures passed.
- `python -m unittest discover -s tests`: passed; 64 tests passed.
- `python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite`: passed; exit code 0.
- Final demo findings: R-005 high and R-006 high for human review.

## Generated Output Files

`src/output/final-demo/` contains:

- `findings.json`
- `evidence-map.json`
- `review-report.md`
- `human-review-queue.md`
- `normalized.json`
- `rules-debug.json`
- `run-meta.json`

## Remaining Limitations

- No legal determination.
- No sales approval or blocking.
- No certificate authenticity judgment.
- No false-advertising judgment.
- No OCR SaaS, image analysis, Musinsa API integration, chatbot, or product recommendation.
- PDF support is limited fallback text extraction only.
- Human review remains the final decision point.
