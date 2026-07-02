---
name: material-evidence-consistency-guard
description: Prepare a minimal consistency-review run for product draft data, product notices, detail-page claims, and test-report evidence without making legal or approval decisions.
---

# Material Evidence Consistency Guard

Use this skill when preparing a human review workflow for consistency between product registration information, product information notices, detail-page claims, and test-report evidence.

## Inputs

The intended input directory may contain:

- `product-draft.json`
- `product-notice.json`
- `detail-page.md`
- `test-report.md` or a limited PDF form of the test report
- `validation-policy.yml`

This first implementation only initializes a run and writes metadata. It does not parse, validate, or compare these files yet.

## Outputs

The planned review artifacts are:

- `findings.json`
- `review-report.md`
- `evidence-map.json`
- `human-review-queue.md`

This first implementation only creates `run-meta.json`. The listed review artifacts are not implemented yet.

## Review Boundary

The tool is for pre-review consistency preparation. A human reviewer makes the final judgment. This skill does not provide legal determinations, sales approval or blocking decisions, certificate authenticity judgments, or false-advertising judgments.
