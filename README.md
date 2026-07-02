# Material Evidence Consistency Guard

Material Evidence Consistency Guard is a Codex plugin submission that checks consistency signals across product draft data, product notices, detail-page claims, and test-report evidence so a human reviewer can decide what needs follow-up.

## Submission Structure

```text
submission root/
├─ src/
│  ├─ .codex-plugin/plugin.json
│  ├─ skills/material-evidence-consistency-guard/SKILL.md
│  ├─ fixtures/
│  ├─ scripts/
│  ├─ tests/
│  ├─ output/.gitkeep
│  ├─ pyproject.toml
│  └─ README.md
├─ README.md
└─ logs/
```

## Run A Fixture

```powershell
cd src
python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite
```

The main review outputs are:

- `findings.json`
- `evidence-map.json`
- `review-report.md`
- `human-review-queue.md`

The CLI also writes implementation support files such as `run-meta.json`, `normalized.json`, and `rules-debug.json`.

## Fixture Suite

Run the regression suite for the canonical 8 fixtures:

```powershell
cd src
python scripts/run_fixture_suite.py
```

Run the full unit test set:

```powershell
cd src
python -m unittest discover -s tests
```

## 90-Second Demo

1. Open this README and note the scope limits below.
2. Run `cd src`.
3. Run `python scripts/run_fixture_suite.py` and confirm 8 fixtures pass.
4. Run `python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite`.
5. Open `output/final-demo/findings.json` to see the detected R-005/R-006 review items.
6. Open `output/final-demo/review-report.md` and `output/final-demo/human-review-queue.md` to see what a human reviewer should inspect.

## Scope Limits

This project does not make legal determinations, approve or block sales, judge certificate authenticity, or decide whether advertising is false. It does not use OCR SaaS, Musinsa APIs, chatbots, or product recommendations. The tool produces consistency findings for human review; a person makes the final judgment.
