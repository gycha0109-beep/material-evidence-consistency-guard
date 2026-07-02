# T16.5 Error Log

## 2026-07-02

- Command: `cd src && python -m unittest tests/test_gate_rules.py`
- Failure: Case 02 reached output rendering after R-001, but `render_review_report` assumed `evidence_document.tested_product` was an object. In the corrected absent-report model it is `null`.
- Fix: Treat absent `tested_product` as an empty object only for Markdown rendering. Rule logic and output schema are unchanged.
