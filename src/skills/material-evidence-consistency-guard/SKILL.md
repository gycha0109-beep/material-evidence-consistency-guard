---
name: material-evidence-consistency-guard
description: Run conservative material evidence consistency checks across product draft data, product notices, detail-page claims, and test-report evidence for human review without making legal, approval, or authenticity decisions.
---

# Material Evidence Consistency Guard

Use this skill when preparing a human review workflow for consistency between product registration information, product information notices, detail-page claims, and test-report evidence.

## Inputs

The input directory uses:

- `product-draft.json`
- `product-notice.json`
- `detail-page.md`
- `test-report.md` or a limited `test-report.pdf` fallback
- `validation-policy.yml`

`test-report.md` has priority. If Markdown is absent and a PDF is present, the current implementation only attempts limited text extraction. If both report files are absent, that is represented as absent evidence for the rules layer rather than a structural input error.

## Outputs

The implemented review artifacts are:

- `findings.json`
- `review-report.md`
- `evidence-map.json`
- `human-review-queue.md`

The CLI also writes `run-meta.json`, `normalized.json`, and `rules-debug.json`.

## Implemented Checks

The current rules cover:

- R-001 missing report evidence for high-risk material or fill
- R-002 unreadable or incomplete report evidence
- R-003 product/SKU target mismatch
- R-004 explicit material ratio conflict
- R-005 explicit detail-page material, ratio, or all-option scope overclaim
- R-006 variant material differences with partial evidence scope

Ambiguous aliases are preserved for review rather than treated as confirmed mismatches.

## Review Boundary

The tool is for pre-review consistency preparation. A human reviewer makes the final judgment. This skill does not provide legal determinations, sales approval or blocking decisions, certificate authenticity judgments, false-advertising judgments, OCR SaaS, Musinsa API integration, chatbot behavior, or product recommendations.
