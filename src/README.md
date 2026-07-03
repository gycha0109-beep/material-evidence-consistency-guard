# Material Evidence Consistency Guard

이 디렉터리에는 실행 가능한 Codex 플러그인 제출 파일, Fixture, 스크립트 및 테스트 코드가 포함되어 있습니다.

## 입력(Input)

각 Fixture 입력 디렉터리는 다음 5가지 입력 파일을 사용합니다.

- `product-draft.json`
- `product-notice.json`
- `detail-page.md`
- `test-report.md` 또는 `test-report.pdf`
- `validation-policy.yml`

`test-report.md`가 존재하면 항상 Markdown을 우선 사용합니다. Markdown이 없고 `test-report.pdf`가 존재하는 경우에만 선택적으로 `pypdf`를 이용한 제한적인 텍스트 추출을 시도합니다.

두 파일이 모두 없는 경우에도 입력 검증은 성공하며, 고위험 소재 또는 충전재가 포함된 경우 규칙 엔진에서 R-001(증빙 누락)으로 처리합니다.

OCR, 이미지 분석, 외부 SaaS 또는 웹 API는 사용하지 않습니다.

## 출력(Output)

사람이 검토하는 주요 출력 파일은 다음과 같습니다.

- `findings.json`
- `evidence-map.json`
- `review-report.md`
- `human-review-queue.md`

추가로 실행 이력과 디버깅을 위해 아래 파일도 생성됩니다.

- `run-meta.json`
- `normalized.json`
- `rules-debug.json`

## 구현된 규칙

- **R-001** : 고위험 소재 또는 충전재가 존재하지만 시험성적서가 제출되지 않은 경우
- **R-002** : 시험성적서는 존재하지만 읽을 수 없거나 비교에 필요한 핵심 정보가 부족한 경우
- **R-003** : 시험성적서의 대상 상품 또는 SKU가 등록 상품과 명확하게 연결되지 않는 경우
- **R-004** : 상품과 시험성적서의 소재 또는 충전재 혼용률이 허용 오차를 초과하여 다른 경우
- **R-005** : 상세페이지의 명시적인 소재, 혼용률 또는 전체 옵션 적용 표현이 시험성적서의 증빙 범위를 초과하는 경우
- **R-006** : 옵션별 소재가 서로 다른데 시험성적서가 일부 옵션만 대상으로 하는 경우

## 우선순위 게이트

규칙은 다음 순서로 보수적으로 실행됩니다.

1. **R-001** : 고위험 소재 또는 충전재에 대한 시험성적서가 없는 경우 하위 규칙을 중단합니다.
2. **R-002** : 시험성적서를 읽을 수 없거나 핵심 정보가 부족한 경우 하위 규칙을 중단합니다.
3. **R-003** : 시험 대상 상품 또는 SKU가 일치하지 않는 경우(R-003 High) R-004~R-006을 중단합니다.
4. **R-004 ~ R-006** : 상위 게이트를 모두 통과한 경우에만 비교를 수행합니다.

모호한 소재 별칭(alias)은 자동으로 High 불일치로 확정하지 않으며, Review Finding 또는 Uncertainty 상태로 보존합니다.

## Fixture 목록

회귀 테스트는 다음 8개의 Canonical Fixture를 사용합니다.

- `01-pass-consistent`
- `02-missing-evidence`
- `03-report-extraction-failure`
- `04-product-target-mismatch`
- `05-ratio-conflict`
- `06-detail-overclaim`
- `07-variant-scope-gap`
- `08-ambiguous-alias`

## 실행 방법

단일 Fixture 실행

```powershell
python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite
```

Fixture 회귀 테스트 실행

```powershell
python scripts/run_fixture_suite.py
```

전체 테스트 실행

```powershell
python -m unittest discover -s tests
```

## 범위 제한

이 도구는 다음 기능을 수행하지 않습니다.

- 법적 적합성 또는 위법 여부를 판단하지 않습니다.
- 판매 승인 또는 판매 차단을 결정하지 않습니다.
- 시험성적서의 진위 여부를 판정하지 않습니다.
- 허위광고 여부를 판단하지 않습니다.
- OCR SaaS를 사용하지 않습니다.
- 무신사 API를 사용하지 않습니다.
- 챗봇 기능을 제공하지 않습니다.
- 상품 추천 기능을 제공하지 않습니다.

본 프로젝트의 출력은 문서 간 일관성을 검토하기 위한 보조 자료이며, 최종 판단은 반드시 사람이 수행합니다.
