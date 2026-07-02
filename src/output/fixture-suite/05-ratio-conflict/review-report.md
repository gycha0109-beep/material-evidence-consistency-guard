# Material Evidence Consistency Review

## Run Summary

- Run ID: run-2026-07-02T03:03:27.534339+00:00
- Blocker: 0
- High: 1
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

### high - R-004 - F-R004-001

- Product: 노르딕 오리 다운 파카
- Option Scope: BLACK_ALL_SIZES
- Message: Material ratio values differ across product inputs and test report beyond the configured tolerance.
- Status: needs_human_review
- Evidence Refs: variants[0].material_components.충전재.materials[0], notice.fill_disclosure.충전재[0], detail_claims[2].explicit_materials[0], evidence_document.tested_materials[0]
- Expected Value: Not specified
- Actual Value: Not specified
- Human Action: Confirm the latest production specification, product notice, detail page, and test report baseline values.


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
- option_scope: BLACK_ALL_SIZES
- options: 블랙 / M
  - Scope: [
  "BLACK_ALL_SIZES"
]
  - Support Status: conflicting
  - Supporting Sources: detail_claims[0], evidence_document.tested_materials
  - Conflicting Sources: detail_claims[2].explicit_materials[0], evidence_document.tested_materials[0], notice.fill_disclosure.충전재[0], variants[0].material_components.충전재.materials[0]
  - Review Reason: Material ratio conflict exists elsewhere in this run; human review determines final handling.
- Claim ID: detail-claim-2
  - Text: - 겉감: 나일론 100%
  - Scope: []
  - Support Status: conflicting
  - Supporting Sources: detail_claims[1], evidence_document.tested_materials
  - Conflicting Sources: detail_claims[2].explicit_materials[0], evidence_document.tested_materials[0], notice.fill_disclosure.충전재[0], variants[0].material_components.충전재.materials[0]
  - Review Reason: Material ratio conflict exists elsewhere in this run; human review determines final handling.
- Claim ID: detail-claim-3
  - Text: - 충전재: 오리 솜털 80%, 오리 깃털 20%
- 적용 범위: BLACK_ALL_SIZES
- 적용 SKU: NW-DP-2026-01
  - Scope: [
  "BLACK_ALL_SIZES"
]
  - Support Status: conflicting
  - Supporting Sources: detail_claims[2], evidence_document.tested_materials
  - Conflicting Sources: detail_claims[2].explicit_materials[0], evidence_document.tested_materials[0], notice.fill_disclosure.충전재[0], variants[0].material_components.충전재.materials[0]
  - Review Reason: Material ratio conflict exists elsewhere in this run; human review determines final handling.
- Claim ID: detail-claim-4
  - Text: - 시험성적서 참조 SKU: NW-DP-2026-01
- 시험성적서 충전재: 오리 솜털 70%, 오리 깃털 30%
  - Scope: []
  - Support Status: conflicting
  - Supporting Sources: detail_claims[3], evidence_document.tested_materials
  - Conflicting Sources: detail_claims[2].explicit_materials[0], evidence_document.tested_materials[0], notice.fill_disclosure.충전재[0], variants[0].material_components.충전재.materials[0]
  - Review Reason: Material ratio conflict exists elsewhere in this run; human review determines final handling.
- Claim ID: detail-claim-5
  - Text: - 케어 및 안전 관련 추가 소재 주장은 이 fixture에 포함하지 않는다.
  - Scope: []
  - Support Status: conflicting
  - Supporting Sources: detail_claims[4], evidence_document.tested_materials
  - Conflicting Sources: detail_claims[2].explicit_materials[0], evidence_document.tested_materials[0], notice.fill_disclosure.충전재[0], variants[0].material_components.충전재.materials[0]
  - Review Reason: Material ratio conflict exists elsewhere in this run; human review determines final handling.

## Required Human Decisions

- F-R004-001 (R-004): Confirm the latest production specification, product notice, detail page, and test report baseline values.
  - Suggested Reviewer: 품질관리 담당자

## Scope Limitation

This result does not determine legal compliance, sales approval or blocking, certificate authenticity, or whether a violation occurred. Final judgment is made by a human reviewer.
