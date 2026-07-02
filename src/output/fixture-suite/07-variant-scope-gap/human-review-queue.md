# Human Review Queue

## F-R005-002

- Finding ID: F-R005-002
- Rule ID: R-005
- Product: 노르딕 오리 다운 파카
- Why Human Review Is Required: Detail page applies an explicit claim to all options, while the test report scope is narrower.
- Documents To Inspect: detail_claims[2].explicit_scope, evidence_document.tested_product.variant_scope
- Suggested Reviewer: 상세페이지 콘텐츠 담당자
- Decision Options: confirm current source value, request corrected source document, mark as not applicable with rationale
- Human Action: Confirm the latest production specification, product notice, detail page, and test report baseline values.

## F-R006-001

- Finding ID: F-R006-001
- Rule ID: R-006
- Product: 노르딕 오리 다운 파카
- Why Human Review Is Required: Variant materials differ, but the test report scope covers only part of the registered option set.
- Documents To Inspect: variants, evidence_document.tested_product.variant_scope
- Suggested Reviewer: 품질관리 담당자
- Decision Options: confirm current source value, request corrected source document, mark as not applicable with rationale
- Human Action: Confirm which options are covered by the test report before comparing variant-specific materials.
