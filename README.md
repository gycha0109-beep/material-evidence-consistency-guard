# Material Evidence Consistency Guard

Submission scaffold for a Codex plugin that helps prepare human review of consistency between product registration data, product notices, detail-page claims, and test-report evidence.

## Run

```powershell
cd src
python scripts/run_guard.py --help
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite
```

## Scope Limits

This project does not make legal determinations, approve or block sales, judge certificate authenticity, or decide whether advertising is false. It also does not implement OCR SaaS integrations, Musinsa APIs, chatbots, product recommendations, rules engines, input parsers, fixture data, or PDF parsing in this task.
