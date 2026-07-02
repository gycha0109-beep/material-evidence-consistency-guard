# Material Evidence Consistency Review

## Run Summary

- Run ID: run-2026-07-02T03:03:12.665747+00:00
- Blocker: 1
- High: 0
- Medium: 0
- Review: 0

## Product Identity

- Product ID: MUS-OUTER-00031
- Product Name: 노르딕 오리 다운 파카
- Internal SKU: NW-DP-2026-01
- Evidence Product: {
  "name": null,
  "identifier": null,
  "variant_scope": null,
  "valid_until": null
}

## Evidence Coverage

- Evidence Status: unreadable
- Issuer: None
- Issued At: None
- Missing Fields: test-report.pdf extraction unavailable: optional dependency pypdf is not installed

## Findings By Severity

### blocker - R-002 - F-R002-001

- Product: 노르딕 오리 다운 파카
- Option Scope: 
- Message: Test report is present but incomplete or unreadable: test-report.pdf extraction unavailable: optional dependency pypdf is not installed, tested_product_name, tested_product_identifier, tested_materials, issuer, issued_at
- Status: needs_human_review
- Evidence Refs: test-report.md, evidence_document
- Expected Value: Not specified
- Actual Value: Not specified
- Human Action: Confirm report identity, issuer, issue date, tested product identifier, and tested materials.


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
  - Text: - 충전재: 오리 솜털 80%, 오리 깃털 20%
- 적용 범위: BLACK_ALL_SIZES
- 적용 SKU: NW-DP-2026-01
  - Scope: [
  "BLACK_ALL_SIZES"
]
  - Support Status: supported
  - Supporting Sources: detail_claims[2], evidence_document.tested_materials
  - Conflicting Sources: None
  - Review Reason: No rule finding conflicts with this explicit claim in the current implemented checks.
- Claim ID: detail-claim-4
  - Text: - 시험성적서 PDF가 첨부되어 있으나 이 fixture에서는 텍스트 추출 실패를 재현한다.
  - Scope: []
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

## Required Human Decisions

- F-R002-001 (R-002): Confirm report identity, issuer, issue date, tested product identifier, and tested materials.
  - Suggested Reviewer: 품질관리 담당자

## Scope Limitation

This result does not determine legal compliance, sales approval or blocking, certificate authenticity, or whether a violation occurred. Final judgment is made by a human reviewer.
