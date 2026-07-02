# Material Evidence Consistency Review

## Run Summary

- Run ID: run-2026-07-02T03:03:28.018715+00:00
- Blocker: 0
- High: 2
- Medium: 0
- Review: 0

## Product Identity

- Product ID: MUS-OUTER-00031
- Product Name: 노르딕 오리 다운 파카
- Internal SKU: NW-DP-2026-01
- Evidence Product: {
  "name": "노르딕 오리 다운 파카",
  "identifier": "NW-DP-2026-01",
  "variant_scope": "BLACK_ALL_SIZES",
  "valid_until": null
}

## Evidence Coverage

- Evidence Status: parsed
- Issuer: Korea Textile Test Lab
- Issued At: 2026-01-15
- Missing Fields: None

## Findings By Severity

### high - R-005 - F-R005-002

- Product: 노르딕 오리 다운 파카
- Option Scope: BLACK_ALL_SIZES
- Message: Detail page applies an explicit claim to all options, while the test report scope is narrower.
- Status: needs_human_review
- Evidence Refs: detail_claims[2].explicit_scope, evidence_document.tested_product.variant_scope
- Expected Value: Not specified
- Actual Value: Not specified
- Human Action: Confirm the latest production specification, product notice, detail page, and test report baseline values.

### high - R-006 - F-R006-001

- Product: 노르딕 오리 다운 파카
- Option Scope: BLACK_ALL_SIZES
- Message: Variant materials differ, but the test report scope covers only part of the registered option set.
- Status: needs_human_review
- Evidence Refs: variants, evidence_document.tested_product.variant_scope
- Expected Value: Not specified
- Actual Value: Not specified
- Human Action: Confirm which options are covered by the test report before comparing variant-specific materials.


## Source Comparison

- Claim ID: product-identity
  - Text: 노르딕 오리 다운 파카
  - Scope: NW-DP-2026-01
  - Support Status: supported
  - Supporting Sources: product, evidence_document.tested_product
  - Conflicting Sources: None
  - Review Reason: Human review makes the final product identity judgment.
- Claim ID: detail-claim-1
  - Text: - product_id: MUS-OUTER-00031
- product_name: 노르딕 오리 다운 파카
- internal_sku: NW-DP-2026-01
- option_scope: all_variants
- options: 블랙 / M, 블랙 / L, 베이지 / M
  - Scope: []
  - Support Status: supported
  - Supporting Sources: detail_claims[0], evidence_document.tested_materials
  - Conflicting Sources: None
  - Review Reason: No rule finding conflicts with this explicit claim in the current implemented checks.
- Claim ID: detail-claim-2
  - Text: - 겉감: 나일론 100%
  - Scope: []
  - Support Status: supported
  - Supporting Sources: detail_claims[1], evidence_document.tested_materials
  - Conflicting Sources: None
  - Review Reason: No rule finding conflicts with this explicit claim in the current implemented checks.
- Claim ID: detail-claim-3
  - Text: - 전 옵션 오리 다운 충전재
- 적용 범위: 전 옵션
- 적용 SKU: NW-DP-2026-01
  - Scope: [
  "ALL_OPTIONS"
]
  - Support Status: conflicting
  - Supporting Sources: detail_claims[2], evidence_document.tested_materials
  - Conflicting Sources: detail_claims[2].explicit_scope, evidence_document.tested_product.variant_scope, variants
  - Review Reason: Detail claim is linked to an R-005 finding; human review determines final handling.
- Claim ID: detail-claim-4
  - Text: - 시험성적서 참조 SKU: NW-DP-2026-01
- 시험성적서 참조 범위: BLACK_ALL_SIZES
- 시험성적서 충전재: 오리 솜털 80%, 오리 깃털 20%
  - Scope: [
  "BLACK_ALL_SIZES"
]
  - Support Status: supported
  - Supporting Sources: detail_claims[3], evidence_document.tested_materials
  - Conflicting Sources: None
  - Review Reason: No rule finding conflicts with this explicit claim in the current implemented checks.
- Claim ID: detail-claim-5
  - Text: - 케어 및 안전 관련 추가 소재 주장은 이 fixture에 포함하지 않는다.
  - Scope: []
  - Support Status: supported
  - Supporting Sources: detail_claims[4], evidence_document.tested_materials
  - Conflicting Sources: None
  - Review Reason: No rule finding conflicts with this explicit claim in the current implemented checks.
- Claim ID: variant-scope
  - Text: Variant material coverage against test report scope
  - Scope: BLACK_ALL_SIZES
  - Support Status: conflicting
  - Supporting Sources: variants, evidence_document.tested_product.variant_scope
  - Conflicting Sources: variants, evidence_document.tested_product.variant_scope
  - Review Reason: Variant-specific evidence coverage requires human review before final action.

## Required Human Decisions

- F-R005-002 (R-005): Confirm the latest production specification, product notice, detail page, and test report baseline values.
  - Suggested Reviewer: 상세페이지 콘텐츠 담당자
- F-R006-001 (R-006): Confirm which options are covered by the test report before comparing variant-specific materials.
  - Suggested Reviewer: 품질관리 담당자

## Scope Limitation

This result does not determine legal compliance, sales approval or blocking, certificate authenticity, or whether a violation occurred. Final judgment is made by a human reviewer.
