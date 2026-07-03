# Material Evidence Consistency Guard

Material Evidence Consistency Guard는 상품 등록 정보, 상품 정보 고시, 상세 페이지, 시험 성적서 간의 소재·혼용률·적용 범위의 일관성을 자동으로 점검하여 사람이 추가 검토해야 할 항목을 찾아주는 Codex 플러그인입니다.

## 제출 구조

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

## 실행 방법

```powershell
cd src
python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite
```

실행이 완료되면 다음 4개의 주요 검토 결과가 생성됩니다.

- `findings.json`
- `evidence-map.json`
- `review-report.md`
- `human-review-queue.md`

추가로 디버깅 및 추적을 위한 아래 파일도 함께 생성됩니다.

- `run-meta.json`
- `normalized.json`
- `rules-debug.json`.

## Fixture 회귀 테스트

Canonical Fixture 8개에 대해 회귀 테스트를 실행합니다.

```powershell
cd src
python scripts/run_fixture_suite.py
```

전체 단위 테스트를 실행하려면 다음 명령을 사용합니다.

```powershell
cd src
python -m unittest discover -s tests
```

## 90초 데모 순서

1. 이 README를 열어 프로젝트 목적과 범위 제한을 확인합니다.
2. `cd src`를 실행합니다.
3. `python scripts/run_fixture_suite.py`를 실행하여 8개의 Fixture가 모두 통과하는지 확인합니다.
4. `python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite`를 실행합니다.
5. `output/final-demo/findings.json`을 열어 R-005와 R-006 탐지 결과를 확인합니다.
6. `output/final-demo/review-report.md와 human-review-queue.md`를 열어 사람이 검토해야 할 내용을 확인합니다.

## 범위 제한

이 프로젝트는 다음 기능을 수행하지 않습니다.

- 법적 적합성 또는 위법 여부를 판단하지 않습니다.
- 판매 승인 또는 판매 차단을 결정하지 않습니다.
- 시험성적서의 진위 여부를 판정하지 않습니다.
- 허위광고 여부를 판단하지 않습니다.
- OCR SaaS를 사용하지 않습니다.
- 무신사 API를 사용하지 않습니다.
- 챗봇 기능을 제공하지 않습니다.
- 상품 추천 기능을 제공하지 않습니다.

본 도구는 상품 정보와 시험성적서 간의 일관성을 검토하기 위한 보조 도구이며, 최종 판단은 반드시 사람이 수행합니다.