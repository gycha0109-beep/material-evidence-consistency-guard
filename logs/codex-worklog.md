# Codex 작업 로그

***
자동 transcript hook을 설치하기 전에 프로젝트를 시작하여
hook으로 로그를 수집하지 못했습니다..

아래 내용은 실제 수행 순서를 기준으로 편집, 발췌 없이 전체를 Ctrl+C, Ctrl+V한 작업 기록입니다.
구분을 위해서 프롬프트 시작점마다 커밋명과 하이푼(-)으로 구분했습니다.
**



## 01 feat: initialize Codex plugin scaffold and CLI entrypoint

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 첫 번째 구현 Task를 수행하세요.

프로젝트 목적:
상품 등록 정보, 상품정보고시, 상세페이지, 시험성적서 사이의 정합성을 비교하여 사람이 검토해야 하는 항목을 찾는 Codex 플러그인입니다.

절대 하지 말 것:

* 법적 판정
* 판매 승인 또는 차단
* 인증서 진위 판정
* 허위광고 판정
* OCR SaaS, 무신사 API, 챗봇, 상품 추천
* 규칙 엔진, 입력 파서, fixture 데이터, PDF 파서 구현
* 불필요한 리팩터링

먼저 git status와 현재 파일 구조를 확인하세요. 기존 파일이 있으면 내용을 읽고, 이미 존재하는 구조를 최대한 유지하세요.

이번 Task의 목표는 제출용 플러그인 골격과 최소 CLI 진입점을 만드는 것입니다.

반드시 아래 구조를 사용하세요.

submission root/
├─ src/
│  ├─ .codex-plugin/plugin.json
│  ├─ skills/material-evidence-consistency-guard/SKILL.md
│  ├─ scripts/run_guard.py
│  ├─ output/.gitkeep
│  ├─ pyproject.toml
│  └─ README.md
├─ README.md
└─ logs/.gitkeep

구현 요구사항:

1. src/.codex-plugin/plugin.json을 생성하세요.

   * name: material-evidence-consistency-guard
   * version: 0.1.0
   * 짧은 설명은 상품 속성, 상세페이지 주장, 시험성적서의 정합성을 사람 검토 전에 확인하는 도구라는 뜻이어야 합니다.
   * 법적 판정이나 자동 승인을 하지 않는다는 범위를 설명에 포함하세요.

2. src/skills/material-evidence-consistency-guard/SKILL.md를 생성하세요.

   * YAML front matter에 name과 description을 포함하세요.
   * 입력 파일은 product-draft.json, product-notice.json, detail-page.md, test-report.md 또는 제한적 PDF, validation-policy.yml이라는 점을 명시하세요.
   * 출력 파일은 findings.json, review-report.md, evidence-map.json, human-review-queue.md라는 점을 명시하세요.
   * 사람이 최종 판단한다는 점을 명시하세요.
   * 아직 구현되지 않은 기능을 사실처럼 설명하지 마세요.

3. src/scripts/run_guard.py를 생성하세요.

   * 표준 라이브러리만 사용하세요.
   * positional argument로 input directory 하나를 받으세요.
   * --out 옵션으로 output directory를 받으세요.
   * output directory가 없으면 생성하세요.
   * output directory에 run-meta.json을 생성하세요.
   * run-meta.json에는 input_dir, output_dir, generated_at, status를 포함하세요.
   * status는 현재 단계에서는 "initialized"로 고정하세요.
   * 아직 fixture가 없어도 실행 가능한 구조여야 합니다.
   * 입력 디렉터리가 없어도 명확한 오류 메시지와 non-zero exit code를 반환하세요.

4. src/pyproject.toml을 생성하세요.

   * Python 버전만 최소로 지정하세요.
   * 외부 의존성은 추가하지 마세요.

5. 루트 README.md와 src/README.md를 생성하세요.

   * 루트 README.md는 제출 안내, src/ 이동 후 실행 명령, 범위 제한을 담으세요.
   * src/README.md는 구현 시작 안내와 현재 CLI 실행 방법만 담으세요.
   * 구현되지 않은 규칙을 완료된 것처럼 쓰지 마세요.

검증:
반드시 src/를 작업 디렉터리로 두고 아래 명령을 실행하세요.

python scripts/run_guard.py --help
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo

두 번째 명령이 fixture 폴더 부재 때문에 실패한다면, 이번 Task에서는 fixtures/cases/01-pass-consistent/.gitkeep만 생성해서 명령이 성공하게 하세요. 단, 실제 fixture 파일은 만들지 마세요.

완료 기준:

* 위 두 명령이 성공한다.
* output/demo/run-meta.json이 생성된다.
* 불필요한 외부 의존성이나 기능이 추가되지 않는다.

최종 보고 형식:

1. 수정 파일 목록
2. 실행한 검증 명령과 결과
3. 아직 구현하지 않은 기능
4. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [README.md](D:/Ji_hwan/material-evidence-consistency-guard/README.md)
- [src/.codex-plugin/plugin.json](D:/Ji_hwan/material-evidence-consistency-guard/src/.codex-plugin/plugin.json)
- [src/skills/material-evidence-consistency-guard/SKILL.md](D:/Ji_hwan/material-evidence-consistency-guard/src/skills/material-evidence-consistency-guard/SKILL.md)
- [src/scripts/run_guard.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_guard.py)
- [src/pyproject.toml](D:/Ji_hwan/material-evidence-consistency-guard/src/pyproject.toml)
- [src/README.md](D:/Ji_hwan/material-evidence-consistency-guard/src/README.md)
- [src/output/.gitkeep](D:/Ji_hwan/material-evidence-consistency-guard/src/output/.gitkeep)
- [src/fixtures/cases/01-pass-consistent/.gitkeep](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/.gitkeep)
- [src/output/demo/run-meta.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/run-meta.json)
- [logs/.gitkeep](D:/Ji_hwan/material-evidence-consistency-guard/logs/.gitkeep)

2. 실행한 검증 명령과 결과
- `cd src; python scripts/run_guard.py --help` 성공
- `cd src; python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo` 성공
- `output/demo/run-meta.json` 생성 확인
- 추가로 `python -m py_compile scripts/run_guard.py` 성공
- Codex plugin/skill validator도 시도했지만 로컬 Python에 `yaml` 모듈이 없어 validator 자체가 실행되지 않았습니다. 이번 Task 요구사항상 외부 의존성을 추가하지 않았습니다.

3. 아직 구현하지 않은 기능
- 규칙 엔진, 입력 파서, fixture 데이터, PDF 파서
- `findings.json`, `review-report.md`, `evidence-map.json`, `human-review-queue.md` 생성
- 법적 판정, 판매 승인/차단, 인증서 진위 판정, 허위광고 판정

4. git diff 요약
- 기존 루트 `README.md`를 제출 안내와 실행 방법 중심으로 확장
- `src/` 아래 Codex 플러그인 manifest, skill 문서, 최소 CLI, pyproject, README 추가
- fixture 폴더 부재로 검증 명령이 실패하지 않도록 `.gitkeep`만 추가
- 외부 의존성은 추가하지 않음
- 현재 `git status --short`: `README.md` 수정, `src/`와 `logs/` 신규 추가됨

## 02 feat: define CLI contract and error handling

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 두 번째 구현 Task를 수행하세요.

먼저 git status와 기존 src/scripts/run_guard.py, src/README.md, src/tests 구조를 확인하세요. T01에서 만든 플러그인 골격과 CLI를 유지하고, 불필요한 리팩터링은 하지 마세요.

이번 Task 목표:
run_guard.py의 CLI 실행 계약과 실패 처리 규약을 고정합니다.

이번 Task에서 구현할 것:

1. input directory positional argument 검증
2. --out output directory 검증
3. --overwrite 플래그 지원
4. 입력 경로가 없을 때 non-zero exit code와 명확한 stderr 메시지
5. output directory가 이미 있고 --overwrite가 없을 때 non-zero exit code와 명확한 stderr 메시지
6. 성공 시 output directory에 run-meta.json 생성
7. run-meta.json에 최소한 아래 필드를 포함

   * input_dir
   * output_dir
   * generated_at
   * status
   * tool_version
8. src/tests/test_cli_contract.py 추가

   * 정상 실행
   * 없는 input directory
   * 기존 output directory + --overwrite 없음
   * 기존 output directory + --overwrite 있음
   * --help

이번 Task에서 절대 구현하지 말 것:

* product-draft.json 등 실제 파일 계약 검증
* 규칙 R-001~R-006
* PDF 파싱
* findings.json 등 최종 산출물
* 외부 라이브러리
* UI 또는 API

검증:
반드시 아래 명령을 실행하세요.

cd src
python -m unittest tests/test_cli_contract.py
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite

완료 기준:

* 단위 테스트가 모두 통과한다.
* 정상 실행은 run-meta.json을 만든다.
* 실패 케이스는 traceback 대신 명확한 오류를 stderr에 출력한다.
* 기존 파일 구조와 T01 산출물을 깨지 않는다.

최종 보고 형식:

1. 수정 파일 목록
2. CLI 계약 변경 사항
3. 실행한 테스트와 결과
4. 남아 있는 미구현 범위
5. git diff 요약

출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/run_guard.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_guard.py)
- [src/tests/test_cli_contract.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_cli_contract.py)
- [src/README.md](D:/Ji_hwan/material-evidence-consistency-guard/src/README.md)
- [README.md](D:/Ji_hwan/material-evidence-consistency-guard/README.md)
- [src/output/demo/run-meta.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/run-meta.json)

2. CLI 계약 변경 사항
- `input_dir`가 없으면 exit code `2`, stderr에 `input directory does not exist` 출력
- `--out` 경로가 기존 파일이면 exit code `2`, stderr에 `output path is not a directory` 출력
- `--out` 디렉터리가 이미 있고 `--overwrite`가 없으면 exit code `2`, stderr에 `output directory already exists ... use --overwrite` 출력
- `--overwrite`가 있으면 기존 output directory에 `run-meta.json` 작성
- `run-meta.json`에 `tool_version: "0.1.0"` 추가

3. 실행한 테스트와 결과
- `cd src; python -m unittest tests/test_cli_contract.py` 성공, 5개 테스트 통과
- `cd src; python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite` 성공
- 실패 케이스는 traceback 없이 명확한 stderr 메시지를 검증했습니다.

4. 남아 있는 미구현 범위
- `product-draft.json` 등 실제 입력 파일 계약 검증
- 규칙 `R-001~R-006`
- PDF 파싱
- `findings.json`, `review-report.md`, `evidence-map.json`, `human-review-queue.md`
- UI, API, 외부 라이브러리 연동

5. git diff 요약
- `run_guard.py`: `--overwrite` 추가, output directory 충돌 처리 추가, `tool_version` 메타데이터 추가
- `test_cli_contract.py`: 정상 실행, 입력 없음, output 충돌, overwrite 성공, help 테스트 추가
- README 2개: 실행 예시를 `--overwrite` 포함 계약으로 갱신
- `output/demo/run-meta.json`: 검증 실행 결과로 재생성됨
- 현재 상태: `README.md`, `src/README.md`, `src/output/demo/run-meta.json`, `src/scripts/run_guard.py` 수정, `src/tests/` 신규 추가됨

## 03 T03: implement input contract validation

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 입력 계약 검증기를 구현하세요.

먼저 git status와 기존 scripts/run_guard.py, fixtures/cases/01-pass-consistent, tests 구조를 확인하세요. 기존 CLI 계약을 유지하고 불필요한 리팩터링은 하지 마세요.

이번 Task 목표:
입력 폴더가 플러그인 실행에 필요한 최소 파일 계약을 만족하는지 검증하는 validate_input.py를 구현합니다.

입력 계약:
필수 파일:

* product-draft.json
* product-notice.json
* detail-page.md
* validation-policy.yml

시험성적서 입력:

* test-report.md가 있으면 우선 사용
* test-report.md가 없고 test-report.pdf가 있으면 허용
* 둘 다 없으면 검증 실패

JSON 최소 top-level 필드:
product-draft.json:

* product_id
* product_name
* variants
* material_components
* high_risk_materials

product-notice.json:

* product_id
* material_disclosure
* fill_disclosure
* variant_scope

validation-policy.yml:

* high_risk_materials
* material_aliases
* required_evidence_rules
* ratio_tolerance

detail-page.md 필수 섹션:

* ## Product Identity
* ## Material Claims
* ## Fill Claims
* ## Certification Or Evidence Claims
* ## Care Or Safety Claims

구현 요구사항:

1. src/scripts/validate_input.py를 추가하세요.
2. Python 표준 라이브러리만 우선 사용하세요.
3. YAML은 기존 pyproject.toml에 외부 의존성이 없다면 최소한의 단순 YAML subset 파서를 직접 구현하거나, validation-policy.yml fixture를 JSON-compatible YAML 형태로 제한하세요.
4. 검증 실패는 파일명, 필드명 또는 섹션명을 포함한 명확한 오류로 반환하세요.
5. validate_input.py는 CLI로 input directory 하나를 받아 검사 결과를 stdout에 JSON으로 출력하세요.
6. src/scripts/run_guard.py가 validate_input 로직을 호출하도록 연결하세요.
7. src/tests/test_validate_input.py를 추가하세요.

   * 정상 fixture
   * test-report.md와 test-report.pdf가 모두 없는 경우
   * product-draft.json 필수 key 누락
   * detail-page.md 필수 섹션 누락
   * validation-policy.yml 필수 key 누락

이번 Task에서 절대 구현하지 말 것:

* PDF 텍스트 추출
* 상품명, SKU, 소재, 혼용률 비교
* R-001~R-006 finding 생성
* output 파일 4종 생성
* 외부 OCR, API, UI

검증:
cd src
python -m unittest tests/test_validate_input.py
python scripts/validate_input.py fixtures/cases/01-pass-consistent
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite

완료 기준:

* 유효 fixture는 통과한다.
* 잘못된 fixture는 파일과 필드 수준으로 실패 원인을 보여준다.
* run_guard.py는 입력 계약 실패 시 후속 처리를 하지 않고 종료한다.

최종 보고 형식:

1. 수정 파일 목록
2. 입력 계약 요약
3. 실행한 테스트와 결과
4. YAML 처리 방식
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/validate_input.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/validate_input.py)
- [src/scripts/run_guard.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_guard.py)
- [src/tests/test_validate_input.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_validate_input.py)
- [src/fixtures/cases/01-pass-consistent/product-draft.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/product-draft.json)
- [src/fixtures/cases/01-pass-consistent/product-notice.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/product-notice.json)
- [src/fixtures/cases/01-pass-consistent/detail-page.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/detail-page.md)
- [src/fixtures/cases/01-pass-consistent/test-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/test-report.md)
- [src/fixtures/cases/01-pass-consistent/validation-policy.yml](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/validation-policy.yml)
- [src/output/demo/run-meta.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/run-meta.json)

2. 입력 계약 요약
- 필수 파일: `product-draft.json`, `product-notice.json`, `detail-page.md`, `validation-policy.yml`
- 시험성적서: `test-report.md` 우선, 없으면 `test-report.pdf` 허용, 둘 다 없으면 실패
- JSON/YAML top-level 필수 key와 `detail-page.md` 필수 `##` 섹션을 검증
- 실패 시 파일명과 누락 key/section을 포함한 오류를 반환
- `run_guard.py`는 입력 계약 실패 시 stderr에 오류를 출력하고 output 생성 단계로 진행하지 않음

3. 실행한 테스트와 결과
- `cd src; python -m unittest tests/test_validate_input.py` 성공, 5개 통과
- `cd src; python scripts/validate_input.py fixtures/cases/01-pass-consistent` 성공, `{"ok": true, "errors": []}`
- `cd src; python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite` 성공
- 추가 확인: `python -m unittest tests/test_cli_contract.py` 성공, 기존 CLI 계약 테스트 5개 통과

4. YAML 처리 방식
- 외부 라이브러리는 추가하지 않았습니다.
- `validation-policy.yml`은 표준 라이브러리만으로 처리하는 제한된 subset 파서를 사용합니다.
- 지원 범위는 top-level `key: value` 형식과 JSON-compatible object 형식입니다. 중첩 YAML은 이번 Task 범위에서 지원하지 않습니다.

5. git diff 요약
- `validate_input.py` 신규 추가: 입력 디렉터리 계약 검증 CLI 및 재사용 함수 구현
- `run_guard.py` 수정: 기존 CLI 계약 유지하면서 입력 검증 호출 추가
- 정상 fixture 파일 추가: 실제 비교 데이터가 아닌 최소 계약 통과용 placeholder
- `test_validate_input.py` 신규 추가: 정상/누락 시험성적서/JSON key 누락/섹션 누락/YAML key 누락 테스트
- `output/demo/run-meta.json`은 검증 실행으로 timestamp만 갱신됨

## 04 T04: add material taxonomy and normalization utilities

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 소재 taxonomy와 validation policy fixture를 구현하세요.

먼저 git status와 src/fixtures, src/scripts, src/tests의 기존 상태를 확인하세요. 이미 구현된 입력 검증 로직을 깨지 마세요.

이번 Task 목표:
고위험 소재, 소재 alias, 모호 alias, 혼용률 수치 처리를 재사용 가능한 작은 모듈로 만듭니다.

수정 또는 생성 대상:
- src/fixtures/policy/validation-policy.yml
- src/scripts/normalize_inputs.py
- src/tests/test_taxonomy.py
- 필요한 경우 src/README.md의 입력 정책 설명

필수 정책:
high_risk_materials:
- duck_down_cluster
- duck_feather
- goose_down_cluster
- goose_feather
- cashmere

명확 alias 예시:
- 오리 솜털 → duck_down_cluster
- 오리깃털 / 오리 깃털 → duck_feather
- 거위 솜털 → goose_down_cluster
- 거위 깃털 → goose_feather
- 캐시미어 → cashmere

모호 alias 예시:
- down
- feather
- 다운
- 깃털

구현 요구사항:
1. normalize_inputs.py에 아래 기능을 추가하세요.
   - normalize_material(value)
   - normalize_percentage(value)
   - material_match(left, right)
2. normalize_material은 canonical code 또는 ambiguous 상태를 반환해야 합니다.
3. ambiguous alias는 자동 불일치로 처리하지 않도록 설계하세요.
4. normalize_percentage는 "80%", 80, "80.0"을 float 또는 int 숫자로 변환하세요.
5. 정책 파일에서 alias와 고위험 소재를 읽도록 하세요.
6. 외부 라이브러리를 추가하지 마세요.
7. test_taxonomy.py를 추가하세요.
   - 명확 alias 변환
   - 모호 alias 처리
   - percentage parsing
   - 동일 소재 match
   - 다른 소재 mismatch

이번 Task에서 절대 구현하지 말 것:
- R-001~R-006
- finding 생성
- PDF parsing
- 상세페이지 claim parser
- 최종 출력 파일

검증:
cd src
python -m unittest tests/test_taxonomy.py

완료 기준:
- 명확 alias는 canonical material로 변환된다.
- 종이 없는 down 또는 feather는 ambiguous로 남는다.
- 모호한 alias가 자동 mismatch로 취급되지 않는다.
- 기존 input validation test가 깨지지 않는다.

최종 보고 형식:
1. 수정 파일 목록
2. canonical material 목록
3. ambiguous 처리 방식
4. 테스트 결과
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/fixtures/policy/validation-policy.yml](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/policy/validation-policy.yml)
- [src/scripts/normalize_inputs.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/normalize_inputs.py)
- [src/tests/test_taxonomy.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_taxonomy.py)
- [src/README.md](D:/Ji_hwan/material-evidence-consistency-guard/src/README.md)

2. canonical material 목록
- `duck_down_cluster`
- `duck_feather`
- `goose_down_cluster`
- `goose_feather`
- `cashmere`

3. ambiguous 처리 방식
- `down`, `feather`, `다운`, `깃털`은 `normalize_material()`에서 `{"status": "ambiguous", ...}`로 반환됩니다.
- `material_match()`는 한쪽이라도 canonical이 아니면 `matched: None`, `status: "ambiguous"`를 반환합니다.
- 따라서 모호 alias는 자동 mismatch로 처리되지 않습니다.

4. 테스트 결과
- `cd src; python -m unittest tests/test_taxonomy.py` 성공, 6개 통과
- 기존 회귀 확인:
  - `python -m unittest tests/test_validate_input.py` 성공, 5개 통과
  - `python -m unittest tests/test_cli_contract.py` 성공, 5개 통과

5. git diff 요약
- taxonomy 정책 fixture 추가: 고위험 소재, 명확 alias, 모호 alias, tolerance 포함
- `normalize_inputs.py` 추가: `normalize_material`, `normalize_percentage`, `material_match` 구현
- `test_taxonomy.py` 추가: alias, ambiguous, percentage, match/mismatch 테스트
- `src/README.md`에 정책 fixture와 JSON-compatible YAML 제한 설명 추가
- 외부 라이브러리, R-rule, finding 생성, PDF parsing, claim parser는 추가하지 않음

## 05 T05 : add baseline fixture for consistent product evidence test

입력 --------------------------------------------------------------------------------------------------

T05 — 정상 fixture Case 01 완성
목적

이후 모든 규칙의 기준점이 될 정상 일치 fixture를 고정합니다.

수정 파일
src/fixtures/cases/01-pass-consistent/product-draft.json
src/fixtures/cases/01-pass-consistent/product-notice.json
src/fixtures/cases/01-pass-consistent/detail-page.md
src/fixtures/cases/01-pass-consistent/test-report.md
src/fixtures/cases/01-pass-consistent/validation-policy.yml
src/fixtures/cases/01-pass-consistent/expected-findings.json
구현 범위
오리 솜털 80%·오리 깃털 20%
동일 SKU
동일 옵션 범위
상세페이지 동일 주장
expected findings 없음
구현하지 말아야 할 것
규칙 코드
임의 모호성
PDF fixture
다중 옵션 차이
검증 방법
cd src
python scripts/validate_input.py fixtures/cases/01-pass-consistent
완료 기준
입력 계약 통과
fixture 내부의 모든 수치·SKU·소재가 일관됨
expected-findings.json은 빈 finding 목록
Codex 구현 프롬프트
현재 repository에서 Material Evidence Consistency Guard의 Case 01 정상 fixture를 완성하세요.

먼저 git status와 src/fixtures/cases/01-pass-consistent의 현재 파일을 확인하세요. 이 Task는 fixture 데이터만 다룹니다. 구현 코드나 규칙 엔진을 수정하지 마세요.

이번 Task 목표:
향후 모든 규칙 테스트의 baseline이 되는 정상 일치 fixture를 만듭니다.

fixture 요구사항:
- product_id: MUS-OUTER-00031
- internal SKU: NW-DP-2026-01
- product_name: 노르딕 오리 다운 파카
- 옵션: 블랙 / M, 블랙 / L
- 겉감: 나일론 100%
- 충전재: 오리 솜털 80%, 오리 깃털 20%
- product-draft.json, product-notice.json, detail-page.md, test-report.md, validation-policy.yml을 모두 포함
- 시험성적서에는 동일 상품명, 동일 SKU, BLACK_ALL_SIZES 범위, 동일 충전재 혼용률이 있어야 함
- detail-page.md에는 필수 섹션을 모두 포함하고, 명시적 수치·소재·옵션 범위가 시험성적서와 일치해야 함
- expected-findings.json에는 findings 빈 배열을 넣어야 함

주의:
- "100% 다운", "프리미엄", "인증 완료" 같은 불필요한 claim을 넣지 마세요.
- 모호 alias인 down 또는 feather 단독 표현을 사용하지 마세요.
- PDF를 추가하지 마세요.
- 코드 파일을 변경하지 마세요.

검증:
cd src
python scripts/validate_input.py fixtures/cases/01-pass-consistent

완료 기준:
- 입력 검증이 성공한다.
- fixture의 상품명, SKU, 옵션 범위, 소재, 혼용률이 모든 파일에서 일치한다.
- expected-findings.json은 빈 finding 목록이다.

최종 보고 형식:
1. 생성 또는 수정한 fixture 파일
2. fixture의 핵심 일치 값 요약
3. 실행한 검증 명령과 결과
4. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 생성 또는 수정한 fixture 파일
- [product-draft.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/product-draft.json)
- [product-notice.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/product-notice.json)
- [detail-page.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/detail-page.md)
- [test-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/test-report.md)
- [validation-policy.yml](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/validation-policy.yml)
- [expected-findings.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/expected-findings.json)

2. fixture의 핵심 일치 값 요약
- `product_id`: `MUS-OUTER-00031`
- `internal_sku`: `NW-DP-2026-01`
- `product_name`: `노르딕 오리 다운 파카`
- 옵션 범위: `BLACK_ALL_SIZES`
- 옵션: `블랙 / M`, `블랙 / L`
- 겉감: `나일론 100%`
- 충전재: `오리 솜털 80%`, `오리 깃털 20%`
- `expected-findings.json`: `{"findings": []}`

3. 실행한 검증 명령과 결과
- `cd src; python scripts/validate_input.py fixtures/cases/01-pass-consistent`
- 결과: 성공

```json
{
  "ok": true,
  "errors": []
}
```

4. git diff 요약
- Case 01 fixture의 placeholder 내용을 정상 일치 baseline 데이터로 교체
- `expected-findings.json` 신규 추가
- 코드 파일, 규칙 엔진, PDF fixture는 변경하지 않음

## 06 T06: parse structured test report markdown

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 test-report.md 파서를 구현하세요.

먼저 git status와 기존 fixture Case 01, normalize_inputs.py, validate_input.py를 확인하세요. 기존 입력 계약을 깨지 마세요.

이번 Task 목표:
test-report.md를 구조화된 Python dict로 파싱하고, 핵심 필드 누락 여부를 명시적으로 보존합니다.

지원할 test-report.md 구조:
- YAML-like front matter
  - report_id
  - issuer
  - issued_at
  - valid_until optional
  - tested_product_name
  - tested_product_identifier
  - tested_variant_scope
- ## Tested Materials 섹션
  - component
  - material
  - percentage
- ## Tested Results 섹션 optional

구현 요구사항:
1. src/scripts/parse_test_report.py를 생성하세요.
2. parse_test_report(path, policy) 함수를 제공하세요.
3. 반환 결과에는 최소한 아래를 포함하세요.
   - document_status: parsed 또는 incomplete
   - report_id
   - issuer
   - issued_at
   - tested_product
   - tested_materials
   - missing_fields
4. 소재와 percentage는 기존 normalize_inputs.py를 재사용하세요.
5. 값이 없으면 추정하지 말고 missing_fields에 넣으세요.
6. test-report.md가 존재하지 않거나 읽을 수 없으면 명확한 예외 또는 상태를 반환하세요.
7. src/tests/test_parse_test_report.py를 작성하세요.
   - Case 01 정상 parsing
   - tested_product_identifier 누락
   - tested_materials 누락
   - percentage 형식 변환
   - ambiguous material alias 보존

이번 Task에서 절대 구현하지 말 것:
- PDF parsing
- R-001~R-006
- findings.json 생성
- 상세페이지 claim 비교
- 사람 검토 큐 생성

검증:
cd src
python -m unittest tests/test_parse_test_report.py

완료 기준:
- Case 01 test-report.md가 구조화된 결과로 변환된다.
- 누락 필드는 추정되지 않고 missing_fields에 남는다.
- 소재 alias와 혼용률 parsing은 기존 정규화 모듈을 재사용한다.

최종 보고 형식:
1. 수정 파일 목록
2. test-report.md 파싱 결과 구조 요약
3. 누락 필드 처리 방식
4. 테스트 결과
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/parse_test_report.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/parse_test_report.py)
- [src/tests/test_parse_test_report.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_parse_test_report.py)
- [src/fixtures/cases/01-pass-consistent/test-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/01-pass-consistent/test-report.md)

2. test-report.md 파싱 결과 구조 요약
- `document_status`: `parsed` 또는 `incomplete`
- `report_id`, `issuer`, `issued_at`
- `tested_product`: `name`, `identifier`, `variant_scope`, `valid_until`
- `tested_materials`: `component`, `material`, 정규화된 `normalized_material`, 숫자 변환된 `percentage`
- `missing_fields`: 누락된 front matter field 또는 material field 목록

Case 01은 front matter와 `## Tested Materials`, `## Tested Results` 구조로 정리했고, `오리 솜털 80%`, `오리 깃털 20%`가 canonical 소재와 숫자 percentage로 파싱됩니다.

3. 누락 필드 처리 방식
- 값을 추정하지 않습니다.
- 필수 front matter가 없으면 예: `front_matter.tested_product_identifier`
- Tested Materials 섹션이 없으면 `tested_materials`
- material row 내부 필드가 없으면 예: `tested_materials[0].percentage`
- 누락이 하나라도 있으면 `document_status`는 `incomplete`입니다.

4. 테스트 결과
- `cd src; python -m unittest tests/test_parse_test_report.py` 성공, 5개 통과
- 회귀 확인:
  - `python scripts/validate_input.py fixtures/cases/01-pass-consistent` 성공
  - `python -m unittest tests/test_validate_input.py` 성공
  - `python -m unittest tests/test_taxonomy.py` 성공
  - `python -m unittest tests/test_cli_contract.py` 성공

5. git diff 요약
- `parse_test_report.py` 신규 추가: front matter, Tested Materials 섹션, 소재/percentage 정규화 파싱
- `test_parse_test_report.py` 신규 추가: 정상 Case 01, 누락 필드, percentage 변환, ambiguous alias 보존 테스트
- Case 01 `test-report.md`를 지원 파서 구조로 갱신
- PDF parsing, R-rule, findings 생성, 상세페이지 비교, human review queue는 구현하지 않음

## 07 T07: build normalized input model

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 전체 입력 정규화 모델을 구현하세요.

먼저 git status와 기존 validate_input.py, parse_test_report.py, normalize_inputs.py, Case 01 fixture를 확인하세요. 기존 parser와 taxonomy 함수를 최대한 재사용하세요. 불필요한 파일 이동이나 리팩터링은 금지합니다.

이번 Task 목표:
다섯 입력 파일을 하나의 normalized model로 조합하고, run_guard.py가 output directory에 normalized.json을 생성하게 합니다.

정규화 모델 최소 구조:
- product
  - product_id
  - product_name
  - internal_sku optional
- variants
  - variant_id
  - option_name
  - material_components
- notice
  - variant_scope
  - material_disclosure
  - fill_disclosure
- detail_claims
  - section
  - raw_text
  - explicit_materials
  - explicit_percentages
  - explicit_scope
- evidence_document
  - document_status
  - tested_product
  - tested_materials
  - issuer
  - issued_at
  - missing_fields
- uncertainties
  - field
  - status
  - reason

구현 요구사항:
1. product-draft.json과 product-notice.json을 읽어 canonical material과 percentage를 적용하세요.
2. detail-page.md는 우선 명시적 숫자와 소재 표현만 추출하세요.
3. detail-page의 정성 표현은 지금 처리하지 마세요.
4. test-report.md는 parse_test_report.py를 재사용하세요.
5. 모호 alias는 ambiguous 상태로 uncertainties에 남기세요.
6. run_guard.py가 입력 검증 후 normalized.json을 output directory에 저장하게 하세요.
7. src/tests/test_normalizer.py를 작성하세요.
   - Case 01의 product_id, SKU, 옵션, 소재, 비율, evidence가 정상 정규화되는지 검증
   - unknown 또는 ambiguous 상태가 보존되는지 검증

이번 Task에서 절대 구현하지 말 것:
- R-001~R-006 finding
- PDF parsing
- 최종 4개 출력물
- 법적 판단, 승인/차단
- 웹/API 연동

검증:
cd src
python -m unittest tests/test_normalizer.py
python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite

완료 기준:
- output/demo/normalized.json이 생성된다.
- Case 01의 주요 비교 값이 구조화된 모델에 포함된다.
- 누락과 alias 모호 상태가 별도 상태값으로 보존된다.

최종 보고 형식:
1. 수정 파일 목록
2. normalized model 핵심 구조
3. 테스트 결과
4. 생성된 normalized.json 경로
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/build_normalized_model.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/build_normalized_model.py)
- [src/scripts/run_guard.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_guard.py)
- [src/tests/test_normalizer.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_normalizer.py)
- [src/output/demo/normalized.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/normalized.json)
- [src/output/demo/run-meta.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/run-meta.json)

2. normalized model 핵심 구조
- `product`: `product_id`, `product_name`, `internal_sku`
- `variants`: option별 `variant_id`, `option_name`, `sku`, `scope`, 정규화된 `material_components`
- `notice`: `variant_scope`, 정규화된 `material_disclosure`, `fill_disclosure`
- `detail_claims`: 섹션별 `raw_text`, 명시적 소재, percentage, scope
- `evidence_document`: `parse_test_report.py` 결과를 재사용한 시험성적서 구조
- `uncertainties`: `unknown`, `ambiguous`, `missing` 상태를 별도 목록으로 보존

3. 테스트 결과
- `cd src; python -m unittest tests/test_normalizer.py` 성공, 3개 통과
- `cd src; python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite` 성공
- 회귀 확인:
  - `python -m unittest tests/test_parse_test_report.py` 성공
  - `python -m unittest tests/test_validate_input.py` 성공
  - `python -m unittest tests/test_taxonomy.py` 성공
  - `python -m unittest tests/test_cli_contract.py` 성공

4. 생성된 normalized.json 경로
- [src/output/demo/normalized.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/normalized.json)

5. git diff 요약
- `build_normalized_model.py` 신규 추가: 5개 입력 파일을 하나의 normalized model로 조합
- `run_guard.py` 수정: 입력 검증 후 `normalized.json` 생성
- `test_normalizer.py` 신규 추가: Case 01 핵심 값과 unknown/ambiguous 보존 검증
- `run-meta.json`은 검증 실행으로 timestamp 갱신
- R-rule, PDF parsing, 최종 4개 출력물, 법적 판단/승인 로직은 추가하지 않음

## 08 T08: add evidence gate rules for missing and incomplete reports

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 첫 번째 규칙 게이트를 구현하세요.

먼저 git status와 normalized.json 생성 흐름, existing scripts, Case 01 fixture를 확인하세요. 기존 parser와 정규화 구조를 유지하세요.

이번 Task 목표:
R-001과 R-002를 구현하고, 이 규칙들이 발생하면 이후 비교 규칙을 실행하지 않도록 gate를 만듭니다.

규칙 정의:
R-001:
- 고위험 소재 또는 충전재가 product-draft에 존재
- 그런데 test-report.md와 test-report.pdf가 모두 없음
- severity: blocker

R-002:
- 시험성적서 파일은 있으나 document_status가 incomplete 또는 unreadable
- 또는 아래 핵심 필드 중 하나 이상 누락
  - tested_product_name 또는 tested_product_identifier
  - tested_materials
  - issuer
  - issued_at
- severity: blocker

우선순위:
1. 시험성적서 입력 자체가 없으면 R-001만 생성
2. 시험성적서 입력은 있으나 추출 실패 또는 핵심 필드 부족이면 R-002만 생성
3. R-001 또는 R-002가 생성되면 R-003~R-006은 실행하지 않음
4. 향후 하위 규칙은 아직 구현하지 않아도 되지만, rules result에 halted=true와 halt_reason을 남기세요.

구현 요구사항:
1. src/scripts/run_rules.py를 생성하거나 기존 파일에 최소한의 구조로 구현하세요.
2. finding 구조는 최소한 아래를 포함해야 합니다.
   - finding_id
   - rule_id
   - severity
   - status
   - message
   - evidence_refs
   - human_action
3. run_guard.py가 normalized model 뒤에 rules 실행 결과를 생성하도록 연결하세요.
4. output directory에 rules-debug.json을 생성해도 됩니다. 단, 최종 findings.json은 아직 만들지 마세요.
5. src/tests/test_gate_rules.py를 추가하세요.
   - 고위험 소재 + report 없음 → R-001만
   - report 존재 + 핵심 필드 누락 → R-002만
   - R-001/R-002 발생 시 halted=true
   - Case 01은 gate 통과

이번 Task에서 절대 구현하지 말 것:
- R-003~R-006
- PDF 실제 텍스트 추출
- 최종 Markdown report
- alias 불일치 확정
- UI, API, OCR

검증:
cd src
python -m unittest tests/test_gate_rules.py

완료 기준:
- R-001 또는 R-002 발생 시 하위 비교가 중단된다.
- 문서 없음과 문서 읽기 실패가 구분된다.
- existing Case 01은 gate를 통과한다.

최종 보고 형식:
1. 수정 파일 목록
2. R-001/R-002 gate 동작 설명
3. 테스트 결과
4. 하위 규칙 중단 방식
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/run_rules.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_rules.py)
- [src/scripts/run_guard.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_guard.py)
- [src/tests/test_gate_rules.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_gate_rules.py)
- [src/output/demo/rules-debug.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/rules-debug.json)
- [src/output/demo/run-meta.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/run-meta.json)

2. R-001/R-002 gate 동작 설명
- `R-001`: `product-draft.json`에 고위험 소재 또는 충전재가 있고 `test-report.md`와 `test-report.pdf`가 모두 없으면 blocker finding 1건 생성
- `R-002`: 시험성적서 입력은 있으나 normalized evidence가 `incomplete`이거나 핵심 필드가 누락되면 blocker finding 1건 생성
- Case 01은 `halted=false`, findings 없음으로 gate 통과

3. 테스트 결과
- `cd src; python -m unittest tests/test_gate_rules.py` 성공, 5개 통과
- `python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite` 성공
- 회귀 확인:
  - `test_normalizer.py` 성공
  - `test_parse_test_report.py` 성공
  - `test_validate_input.py` 성공
  - `test_cli_contract.py` 성공

4. 하위 규칙 중단 방식
- `R-001` 발생 시 `halted=true`, `halt_reason="R-001 blocker: test report input is missing"`
- `R-002` 발생 시 `halted=true`, `halt_reason="R-002 blocker: test report is incomplete or unreadable"`
- `skipped_rules`에 아직 미구현인 `R-003`~`R-006`을 남겨 downstream 비교 중단 상태를 명시합니다.

5. git diff 요약
- `run_rules.py` 신규 추가: R-001/R-002 gate 및 finding 구조 구현
- `run_guard.py` 수정: normalized model 생성 후 `rules-debug.json` 저장
- `test_gate_rules.py` 신규 추가: report 없음, report incomplete, halted, Case 01 통과 검증
- `output/demo/run-meta.json`은 검증 실행으로 timestamp 갱신
- R-003~R-006, PDF 텍스트 추출, 최종 report/findings 생성은 구현하지 않음

## 09 T09: add product target matching gate

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 R-003 시험 대상 상품/SKU 연결 게이트를 구현하세요.

먼저 git status와 run_rules.py, normalized model, Case 01 fixture를 확인하세요. R-001/R-002 gate 동작을 유지해야 합니다.

이번 Task 목표:
시험성적서의 시험 대상 상품이 현재 등록 상품과 연결되는지 최소한의 보수적 규칙으로 확인합니다.

R-003 정의:
- 비교 대상:
  - product.product_id
  - product.internal_sku
  - product.product_name
  - evidence_document.tested_product.identifier
  - evidence_document.tested_product.name
- SKU가 둘 다 존재하고 다르면 mismatch
- SKU가 동일하면 matched
- SKU가 없거나 한쪽만 있고 상품명 핵심 토큰이 명확히 다르면 mismatch
- 상품명 토큰 관계가 불확실하면 ambiguous review
- mismatch일 때 R-003 severity high 생성
- R-003 mismatch가 생성되면 R-004~R-006 비교를 중단

구현 요구사항:
1. 기존 R-001/R-002 gate 이후에만 R-003을 실행하세요.
2. fuzzy matching 라이브러리를 추가하지 마세요.
3. 상품명 비교는 공백, 특수문자, 대소문자 제거와 토큰 비교 정도로 제한하세요.
4. SKU 불일치와 이름 불일치의 근거값을 finding에 포함하세요.
5. ambiguous 상태는 high finding이 아니라 review finding으로 처리하세요.
6. src/fixtures/cases/04-product-target-mismatch fixture를 완성하세요.
   - 등록 SKU: NW-DP-2026-01
   - 시험성적서 SKU: UW-GV-02
   - 혼용률은 우연히 같게 구성
7. src/tests/test_product_target_rule.py를 추가하세요.
   - SKU mismatch → R-003 high, lower rules halted
   - Case 01 → matched
   - SKU 동일 + 이름 일부 차이 → high가 아닌 review 또는 matched
   - R-001/R-002가 발생한 경우 R-003이 실행되지 않음

이번 Task에서 절대 구현하지 말 것:
- R-004~R-006
- 상세페이지 claim 분석 확장
- PDF parsing
- 자동 매핑 또는 자동 수정

검증:
cd src
python -m unittest tests/test_product_target_rule.py

완료 기준:
- R-003 mismatch는 소재·혼용률 비교를 막는다.
- 불확실한 상품명은 불일치 확정이 아니라 review다.
- Case 01은 정상 연결된다.

최종 보고 형식:
1. 수정 파일 목록
2. 상품/SKU 연결 판정 기준
3. ambiguous 처리 방식
4. 테스트 결과
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/run_rules.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_rules.py)
- [src/tests/test_product_target_rule.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_product_target_rule.py)
- [src/fixtures/cases/04-product-target-mismatch/product-draft.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/04-product-target-mismatch/product-draft.json)
- [src/fixtures/cases/04-product-target-mismatch/product-notice.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/04-product-target-mismatch/product-notice.json)
- [src/fixtures/cases/04-product-target-mismatch/detail-page.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/04-product-target-mismatch/detail-page.md)
- [src/fixtures/cases/04-product-target-mismatch/test-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/04-product-target-mismatch/test-report.md)
- [src/fixtures/cases/04-product-target-mismatch/validation-policy.yml](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/04-product-target-mismatch/validation-policy.yml)
- [src/fixtures/cases/04-product-target-mismatch/expected-findings.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/04-product-target-mismatch/expected-findings.json)

2. 상품/SKU 연결 판정 기준
- `R-001`, `R-002`가 없을 때만 `R-003` 실행
- 등록 SKU와 시험성적서 SKU가 모두 있고 동일하면 match
- 둘 다 있고 다르면 `R-003` high finding
- SKU가 부족하면 상품명 토큰을 공백, 특수문자, 대소문자 정규화 후 비교
- 상품명 토큰이 전혀 겹치지 않으면 high mismatch
- mismatch finding에는 등록 SKU/name, 시험성적서 SKU/name 근거값을 포함

3. ambiguous 처리 방식
- SKU 판단이 불가능하거나 상품명 토큰이 일부만 겹치면 high가 아닌 `severity: review` finding으로 남깁니다.
- review finding은 `halted=true`를 만들지 않습니다.
- high mismatch만 `R-004`~`R-006`을 중단합니다.

4. 테스트 결과
- `cd src; python -m unittest tests/test_product_target_rule.py` 성공, 5개 통과
- 회귀 확인:
  - `python -m unittest tests/test_gate_rules.py` 성공
  - `python -m unittest tests/test_normalizer.py` 성공
  - `python -m unittest tests/test_parse_test_report.py` 성공
  - `python -m unittest tests/test_validate_input.py` 성공
  - `python -m unittest tests/test_cli_contract.py` 성공
- `python scripts/validate_input.py fixtures/cases/04-product-target-mismatch` 성공

5. git diff 요약
- `run_rules.py`: R-003 SKU/name target 연결 판정 추가, high mismatch 시 downstream halt
- `test_product_target_rule.py`: SKU mismatch, Case 01 match, partial name review, R-001/R-002 precedence 테스트 추가
- `04-product-target-mismatch` fixture 신규 추가: 등록 SKU `NW-DP-2026-01`, 시험성적서 SKU `UW-GV-02`, 혼용률은 동일
- R-004~R-006, PDF parsing, 자동 매핑/수정은 구현하지 않음

## 10 T10: add ratio conflict rule

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 R-004 혼용률 수치 충돌 규칙을 구현하세요.

먼저 git status와 run_rules.py, normalize_inputs.py, Case 01, R-001~R-003 tests를 확인하세요. 기존 gate 순서를 바꾸지 마세요.

이번 Task 목표:
상품 연결이 확인된 경우에만 충전재 또는 소재의 혼용률 수치를 비교합니다.

R-004 정의:
- R-001/R-002/R-003이 없고 product-evidence link가 matched일 때만 실행
- 동일 component와 동일 canonical material 기준으로 비교
- product-draft, product-notice, detail-page의 명시 수치, test-report를 비교
- validation-policy.yml의 ratio_tolerance를 사용
- 허용 오차를 넘으면 R-004 severity high
- 소재 alias가 ambiguous이면 불일치 확정 금지, review finding 생성
- 합계 오류는 이번 Task에서 별도 규칙으로 만들지 마세요

구현 요구사항:
1. Case 03-ratio-conflict fixture를 완성하세요.
   - product draft, notice, detail page: 오리 솜털 80%, 오리 깃털 20%
   - test report: 오리 솜털 70%, 오리 깃털 30%
   - SKU와 옵션 범위는 일치
2. src/tests/test_ratio_rule.py를 추가하세요.
   - Case 03 → R-004 high
   - Case 01 → R-004 없음
   - SKU mismatch fixture → R-004 없음
   - report 없음 fixture → R-004 없음
   - ambiguous "down 80 / feather 20" → high 불일치가 아니라 review
3. finding에는 비교한 source별 값과 evidence reference를 포함하세요.
4. 불일치 원인을 "법적 위반"으로 표현하지 마세요.
5. human_action은 최신 생산분, 상품 고시, 상세페이지, 시험성적서 기준값 확인으로 제한하세요.

이번 Task에서 절대 구현하지 말 것:
- R-005, R-006
- 상세페이지의 정성 표현 판정
- PDF parsing
- 값 자동 수정
- 판매 승인/차단

검증:
cd src
python -m unittest tests/test_ratio_rule.py

완료 기준:
- 80/20과 70/30이 R-004 high로 나온다.
- R-003 mismatch 또는 R-001/R-002 halt 상태에서는 R-004가 절대 나오지 않는다.
- alias 모호 시 high 확정이 아닌 review가 나온다.

최종 보고 형식:
1. 수정 파일 목록
2. R-004 비교 범위와 허용 오차 처리
3. alias 모호 처리
4. 테스트 결과
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/run_rules.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_rules.py)
- [src/scripts/build_normalized_model.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/build_normalized_model.py)
- [src/tests/test_ratio_rule.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_ratio_rule.py)
- [src/fixtures/cases/03-ratio-conflict/product-draft.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/03-ratio-conflict/product-draft.json)
- [src/fixtures/cases/03-ratio-conflict/product-notice.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/03-ratio-conflict/product-notice.json)
- [src/fixtures/cases/03-ratio-conflict/detail-page.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/03-ratio-conflict/detail-page.md)
- [src/fixtures/cases/03-ratio-conflict/test-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/03-ratio-conflict/test-report.md)
- [src/fixtures/cases/03-ratio-conflict/validation-policy.yml](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/03-ratio-conflict/validation-policy.yml)
- [src/fixtures/cases/03-ratio-conflict/expected-findings.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/03-ratio-conflict/expected-findings.json)

2. R-004 비교 범위와 허용 오차 처리
- R-001/R-002/R-003 high가 없고 상품-SKU 연결이 통과한 경우에만 R-004를 실행합니다.
- 동일 `component`와 동일 canonical material 기준으로 `product-draft`, `product-notice`, `detail-page`, `test-report`의 명시 수치를 비교합니다.
- `validation-policy.yml`의 `ratio_tolerance`를 사용하며, 최대값과 최소값 차이가 tolerance를 넘으면 `R-004` high finding을 생성합니다.
- finding에는 비교 source별 percentage, material, evidence reference를 포함합니다.

3. alias 모호 처리
- 소재 alias가 `ambiguous`이면 high mismatch로 확정하지 않습니다.
- 대신 `R-004` `severity: review` finding을 생성하고, 사람이 기준값과 소재 해석을 확인하도록 남깁니다.
- “법적 위반” 표현이나 자동 수정은 넣지 않았습니다.

4. 테스트 결과
- `cd src; python -m unittest tests/test_ratio_rule.py` 성공, 5개 통과
- 회귀 확인:
  - `test_product_target_rule.py` 성공
  - `test_gate_rules.py` 성공
  - `test_normalizer.py`, `test_parse_test_report.py`, `test_validate_input.py`, `test_taxonomy.py`, `test_cli_contract.py` 묶음 성공
- `python scripts/validate_input.py fixtures/cases/03-ratio-conflict` 성공

5. git diff 요약
- `run_rules.py`: R-004 ratio comparison, review handling for ambiguous aliases, R-004 high halt 추가
- `build_normalized_model.py`: detail-page percentage 추출에서 `%` 없는 숫자도 허용
- `03-ratio-conflict` fixture 신규 추가: draft/notice/detail은 80/20, test-report는 70/30
- `test_ratio_rule.py` 신규 추가: Case 03 high, Case 01 정상, R-003/R-001 halt 시 R-004 미실행, ambiguous review 검증
- R-005/R-006, PDF parsing, 자동 수정, 판매 승인/차단은 구현하지 않음

## 11 T11: add explicit detail claim overreach rule

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 R-005 상세페이지 명시 표현 초과 규칙을 구현하세요.

먼저 git status와 detail-page parsing, run_rules.py, R-001~R-004 gate 동작을 확인하세요. 기존 설계를 유지하고 불필요한 NLP나 리팩터링을 추가하지 마세요.

이번 Task 목표:
상세페이지의 명시적 수치, 소재, 옵션 범위가 상품·시험성적서 범위를 넘는지 찾습니다.

R-005 적용 범위:
- 명시적 percentage 예: 100%, 80%, 20%
- 명시적 소재 예: 오리 솜털, 오리 깃털, 거위 솜털, 캐시미어
- 명시적 옵션 범위 예: 전체 옵션, 전 옵션, 모든 옵션
- 아래는 이번 Task에서 처리하지 않음:
  - 프리미엄
  - 최고급
  - 보온성 우수
  - 피부에 안전
  - 인증 완료
  - 기타 정성 표현

R-005 조건:
1. 상세페이지의 소재/비율이 시험성적서와 명시적으로 다르면 high
2. 상세페이지가 "100% 오리 다운"이라고 말하지만 시험성적서가 오리 솜털 80%, 오리 깃털 20%이면 high
3. 시험성적서가 특정 옵션만 대상으로 하는데 상세페이지가 전체 옵션에 적용한다고 말하면 high
4. R-001/R-002/R-003 halt 상태에서는 실행하지 않음
5. alias가 모호하면 high 확정이 아니라 review

구현 요구사항:
1. detail-page parser는 필요한 명시 claim만 최소한으로 추출하세요.
2. Case 05-detail-overclaim fixture를 완성하세요.
   - product/report: 오리 솜털 80%, 오리 깃털 20%
   - detail page: "100% 오리 다운 충전재"
3. src/tests/test_detail_claim_rule.py를 추가하세요.
   - Case 05 → R-005 high
   - 수치 없는 정성 표현은 R-005 없음
   - R-003 mismatch fixture → R-005 없음
   - alias ambiguous → review
4. finding에 claim 원문과 비교한 시험성적서 값을 포함하세요.
5. 출력 문구에서 "허위", "위반", "불법", "승인 불가"를 사용하지 마세요.

이번 Task에서 절대 구현하지 말 것:
- R-006
- 광고 적법성 판정
- 문구 자동 수정
- 외부 NLP, OCR, API

검증:
cd src
python -m unittest tests/test_detail_claim_rule.py

완료 기준:
- 명시적 수치·소재·옵션 범위 초과만 R-005로 탐지한다.
- 정성 표현은 자동 판정하지 않는다.
- 상위 게이트 실패 시 R-005가 나오지 않는다.

최종 보고 형식:
1. 수정 파일 목록
2. R-005가 처리하는 표현 범위
3. 의도적으로 제외한 표현 범위
4. 테스트 결과
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/run_rules.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_rules.py)
- [src/scripts/build_normalized_model.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/build_normalized_model.py)
- [src/tests/test_detail_claim_rule.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_detail_claim_rule.py)
- [src/fixtures/cases/05-detail-overclaim/product-draft.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/05-detail-overclaim/product-draft.json)
- [src/fixtures/cases/05-detail-overclaim/product-notice.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/05-detail-overclaim/product-notice.json)
- [src/fixtures/cases/05-detail-overclaim/detail-page.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/05-detail-overclaim/detail-page.md)
- [src/fixtures/cases/05-detail-overclaim/test-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/05-detail-overclaim/test-report.md)
- [src/fixtures/cases/05-detail-overclaim/validation-policy.yml](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/05-detail-overclaim/validation-policy.yml)
- [src/fixtures/cases/05-detail-overclaim/expected-findings.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/05-detail-overclaim/expected-findings.json)

2. R-005가 처리하는 표현 범위
- 상세페이지의 명시적 소재 + percentage claim
- `100% 오리 다운` 같은 명시적 충전재 수치 claim
- `전체 옵션`, `전 옵션`, `모든 옵션` 같은 명시적 옵션 범위 표현
- 시험성적서의 tested materials 및 tested scope와 비교하며, finding에는 claim 원문과 시험성적서 기준값을 포함합니다.

3. 의도적으로 제외한 표현 범위
- `프리미엄`
- `최고급`
- `보온성 우수`
- `피부에 안전`
- `인증 완료`
- 기타 정성 표현 전반

4. 테스트 결과
- `cd src; python -m unittest tests/test_detail_claim_rule.py` 성공, 4개 통과
- `python -m unittest discover tests` 성공, 43개 통과
- `python scripts/validate_input.py fixtures/cases/05-detail-overclaim` 성공
- CLI 수준으로 Case 05가 `R-005 high`와 `skipped_rules: ["R-006"]`를 내는 것도 확인했습니다.

5. git diff 요약
- `run_rules.py`: R-005 detail claim 비교, ambiguous review, R-006 halt 추가
- `build_normalized_model.py`: detail-page에서 전체 옵션 계열 명시 scope 추출 추가
- `05-detail-overclaim` fixture 추가: product/report는 80/20, detail page는 `100% 오리 다운 충전재`
- `test_detail_claim_rule.py` 추가: overclaim, 정성 표현 제외, R-003 halt, ambiguous review 검증
- R-006, 문구 자동 수정, 외부 NLP/OCR/API는 구현하지 않음

## 12 T12: add variant scope coverage rule

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 R-006 옵션별 소재 차이와 증빙 범위 불일치 규칙을 구현하세요.

먼저 git status와 run_rules.py, R-005, normalized variants structure를 확인하세요. 상위 gate와 기존 규칙 동작을 절대 깨지 마세요.

이번 Task 목표:
옵션별 소재 또는 충전재가 다르지만 시험성적서가 특정 옵션만 대상으로 하는 경우를 찾습니다.

R-006 조건:
1. product-draft의 variants 사이에서 material_components 또는 fill components가 다름
2. test-report의 tested_variant_scope가 전체 옵션을 명확히 포괄하지 않음
3. 시험성적서가 특정 옵션 또는 특정 색상만 대상으로 함
4. severity high
5. R-001/R-002/R-003 halt 상태에서는 실행하지 않음
6. R-006은 R-005와 동시에 발생할 수 있음

Case 06-variant-scope-gap fixture 요구사항:
- 블랙 / M, 블랙 / L:
  - 오리 솜털 80%
  - 오리 깃털 20%
- 베이지 / M:
  - 폴리에스터 100%
- 시험성적서 범위:
  - BLACK_ALL_SIZES
- 상세페이지에는 "전 옵션 오리 다운 충전재" 문구 포함
- expected finding:
  - R-006 high
  - R-005 high 가능

구현 요구사항:
1. 옵션 범위 문자열은 최소한 아래를 처리하세요.
   - all_variants
   - BLACK_ALL_SIZES
   - 특정 variant_id
2. 범위를 모르면 high로 단정하지 말고 review로 보내세요.
3. R-006 finding에는 옵션별 차이와 시험성적서 범위를 모두 보여주세요.
4. src/tests/test_variant_scope_rule.py를 작성하세요.
   - Case 06 → R-006 high
   - Case 01 → R-006 없음
   - evidence 없음 또는 SKU mismatch → R-006 없음
   - 범위 불명 → review

이번 Task에서 절대 구현하지 말 것:
- 옵션 자동 분리
- 재고/판매 상태 확인
- 무신사 API
- 정책 위반 판정
- 자동 판매 차단

검증:
cd src
python -m unittest tests/test_variant_scope_rule.py

완료 기준:
- 옵션 소재 차이와 증빙 범위 차이가 함께 있는 경우 R-006이 나온다.
- 상위 gate가 막힌 경우 R-006은 절대 실행되지 않는다.
- 범위 불명은 high 확정이 아니라 review다.

최종 보고 형식:
1. 수정 파일 목록
2. 옵션 범위 해석 규칙
3. R-005와 R-006 동시 발생 조건
4. 테스트 결과
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/build_normalized_model.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/build_normalized_model.py)
- [src/scripts/run_rules.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_rules.py)
- [src/tests/test_variant_scope_rule.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_variant_scope_rule.py)
- [src/fixtures/cases/06-variant-scope-gap/product-draft.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/06-variant-scope-gap/product-draft.json)
- [src/fixtures/cases/06-variant-scope-gap/product-notice.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/06-variant-scope-gap/product-notice.json)
- [src/fixtures/cases/06-variant-scope-gap/detail-page.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/06-variant-scope-gap/detail-page.md)
- [src/fixtures/cases/06-variant-scope-gap/test-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/06-variant-scope-gap/test-report.md)
- [src/fixtures/cases/06-variant-scope-gap/validation-policy.yml](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/06-variant-scope-gap/validation-policy.yml)
- [src/fixtures/cases/06-variant-scope-gap/expected-findings.json](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/06-variant-scope-gap/expected-findings.json)

2. 옵션 범위 해석 규칙
- `all_variants`, `all_options`, `ALL_OPTIONS`: 전체 옵션 포괄
- `BLACK_ALL_SIZES`: 해당 scope를 가진 variant만 포괄. 모든 variant가 같은 scope면 전체 포괄, 일부만 해당하면 partial
- 특정 `variant_id`: 해당 variant만 포괄
- 해석 불가 scope는 high로 단정하지 않고 `severity: review`로 남김

3. R-005와 R-006 동시 발생 조건
- 상위 gate `R-001/R-002/R-003`이 통과한 뒤 실행됩니다.
- R-005 high가 있어도 R-006을 계속 평가합니다.
- Case 06처럼 상세페이지가 전 옵션 적용을 말하고, variant별 소재가 다르며, 시험성적서가 `BLACK_ALL_SIZES`만 커버하면 R-005와 R-006이 함께 발생합니다.

4. 테스트 결과
- `cd src; python -m unittest tests/test_variant_scope_rule.py` 성공, 4개 통과
- `python -m unittest discover tests` 성공, 47개 통과
- `python scripts/validate_input.py fixtures/cases/06-variant-scope-gap` 성공
- CLI 수준으로 Case 06이 `R-005 high`와 `R-006 high`를 함께 내는 것도 확인했습니다.

5. git diff 요약
- normalized variants가 variant별 `material_components`를 보존하도록 확장
- R-006 variant material signature 비교 및 evidence scope coverage 판정 추가
- R-005 high 이후에도 R-006 평가 가능하도록 rule flow 조정
- Case 06 fixture와 `test_variant_scope_rule.py` 추가
- 옵션 자동 분리, 판매 상태/API 확인, 정책 위반 판정, 자동 차단은 구현하지 않음

## 13 T13: add limited PDF fallback handling

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 제한적 PDF fallback을 구현하세요.

먼저 git status와 parse_test_report.py, validation flow, R-001/R-002 gate를 확인하세요. PDF는 핵심 기능이 아니라 보조 기능입니다.

이번 Task 목표:
test-report.md가 없을 때만 test-report.pdf를 제한적으로 읽고, 실패하면 추정하지 않고 R-002로 보내는 fallback을 구현합니다.

우선순위:
1. test-report.md가 있으면 무조건 Markdown을 사용
2. Markdown이 없고 test-report.pdf가 있으면 텍스트 추출 시도
3. PDF 텍스트 추출 실패, 텍스트가 너무 짧음, 핵심 필드 추출 실패면 document_status를 unreadable 또는 incomplete로 설정
4. R-002 gate가 이를 처리
5. OCR, 이미지 분석, 외부 SaaS, 웹 API는 절대 사용하지 않음

구현 요구사항:
1. pypdf는 optional dependency로만 추가하세요.
2. pypdf가 설치되지 않은 환경에서도 명확하게 unreadable 상태를 반환하세요.
3. src/fixtures/cases/07-pdf-extraction-failure을 만드세요.
   - 고위험 소재가 있는 product draft
   - test-report.md 없음
   - text extraction 불가 상태를 재현하는 최소 fixture
4. src/tests/test_pdf_fallback.py를 추가하세요.
   - Markdown 우선
   - PDF가 없으면 기존 계약 처리
   - PDF parsing 실패 → R-002
   - PDF parsing 실패 상황에서 R-003~R-006 없음
5. pyproject.toml에는 optional dependency group으로만 pypdf를 추가하세요.

이번 Task에서 절대 구현하지 말 것:
- OCR
- PDF 이미지 렌더링
- 표 인식
- 문서 요약
- 인증서 진위 판정

검증:
cd src
python -m unittest tests/test_pdf_fallback.py

완료 기준:
- test-report.md가 있을 때 PDF는 사용되지 않는다.
- PDF extraction failure는 R-002로 처리된다.
- 실패 시 하위 비교 규칙이 실행되지 않는다.
- OCR 또는 외부 SaaS 의존성이 없다.

최종 보고 형식:
1. 수정 파일 목록
2. Markdown/PDF 우선순위
3. PDF 실패 처리 방식
4. optional dependency 상태
5. 테스트 결과
6. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/parse_test_report.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/parse_test_report.py)
- [src/scripts/build_normalized_model.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/build_normalized_model.py)
- [src/pyproject.toml](D:/Ji_hwan/material-evidence-consistency-guard/src/pyproject.toml)
- [src/tests/test_pdf_fallback.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_pdf_fallback.py)
- [src/fixtures/cases/07-pdf-extraction-failure/*](D:/Ji_hwan/material-evidence-consistency-guard/src/fixtures/cases/07-pdf-extraction-failure)

2. Markdown/PDF 우선순위
- `test-report.md`가 있으면 항상 Markdown parser를 사용합니다.
- `test-report.md`가 없고 `test-report.pdf`가 있을 때만 PDF 텍스트 추출을 시도합니다.
- 둘 다 없으면 기존 입력 계약대로 validation 실패입니다.

3. PDF 실패 처리 방식
- `pypdf` 미설치, PDF 추출 예외, 추출 텍스트 부족, 핵심 필드 부족은 추정하지 않습니다.
- normalized evidence에 `document_status: unreadable` 또는 `incomplete`와 `missing_fields`를 남깁니다.
- 기존 R-002 gate가 이를 blocker로 처리하고 R-003~R-006은 skip합니다.

4. optional dependency 상태
- `pyproject.toml`에만 optional group으로 추가했습니다.

```toml
[project.optional-dependencies]
pdf = [
  "pypdf>=4.0.0"
]
```

- 기본 실행에는 외부 의존성이 필요 없습니다. OCR, 이미지 렌더링, 외부 SaaS/API는 추가하지 않았습니다.

5. 테스트 결과
- `cd src; python -m unittest tests/test_pdf_fallback.py` 성공, 4개 통과
- `python -m unittest discover tests` 성공, 51개 통과
- `python scripts/validate_input.py fixtures/cases/07-pdf-extraction-failure` 성공
- Case 07 run_guard 실행 확인 결과 R-002로 halt되고 R-003~R-006은 skip됨

6. git diff 요약
- PDF fallback parser 추가
- normalized model이 Markdown/PDF 입력 선택 helper를 사용하도록 변경
- PDF extraction failure fixture 추가
- PDF fallback 테스트 추가
- `pypdf`는 optional dependency로만 선언됨

## 14 T14: render findings and evidence map outputs

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 JSON 산출물 2종을 구현하세요.

먼저 git status와 run_rules.py, normalized model, 기존 output 구조를 확인하세요. 규칙 로직을 변경하지 말고 renderer를 분리하세요.

이번 Task 목표:
run_guard.py 실행 후 findings.json과 evidence-map.json을 생성합니다.

findings.json 요구사항:
- run_id
- summary
  - blocker
  - high
  - medium
  - review
- findings 배열
  - finding_id
  - rule_id
  - severity
  - status
  - message
  - evidence_refs
  - expected_value optional
  - actual_value optional
  - human_action

evidence-map.json 요구사항:
- detail claim 또는 상품 속성 claim 단위
- claim_id
- claim_text
- claim_scope
- support_status
  - supported
  - conflicting
  - missing
  - ambiguous
- supporting_sources
- conflicting_sources
- review_reason

구현 요구사항:
1. src/scripts/render_outputs.py를 생성하세요.
2. run_guard.py가 rules 실행 뒤 findings.json과 evidence-map.json을 생성하게 하세요.
3. Case 01은 findings 빈 배열과 supported 상태 evidence map을 생성해야 합니다.
4. Case 03, 05, 06 중 기존 fixture를 사용해 conflicting evidence map이 생성되도록 테스트하세요.
5. src/tests/test_json_outputs.py를 추가하세요.
6. 사람이 최종 판단한다는 범위가 human_action 또는 review_reason에 드러나야 합니다.

이번 Task에서 절대 구현하지 말 것:
- review-report.md
- human-review-queue.md
- HTML/UI/dashboard
- finding 자동 수정
- 법적 판정

검증:
cd src
python -m unittest tests/test_json_outputs.py

완료 기준:
- findings.json과 evidence-map.json이 생성된다.
- 각 finding은 최소 하나 이상의 근거 경로를 가진다.
- Case 01은 false positive 없이 빈 findings를 유지한다.

최종 보고 형식:
1. 수정 파일 목록
2. 두 JSON 출력의 schema 요약
3. 테스트 결과
4. 생성 파일 예시 경로
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/render_outputs.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/render_outputs.py)
- [src/scripts/run_guard.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_guard.py)
- [src/tests/test_json_outputs.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_json_outputs.py)
- [src/output/demo/findings.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/findings.json)
- [src/output/demo/evidence-map.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/evidence-map.json)
- [src/output/demo/run-meta.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/run-meta.json)

2. 두 JSON 출력의 schema 요약
- `findings.json`
  - `run_id`
  - `summary`: `blocker`, `high`, `medium`, `review`
  - `findings[]`: `finding_id`, `rule_id`, `severity`, `status`, `message`, `evidence_refs`, optional `expected_value`, optional `actual_value`, `human_action`
- `evidence-map.json`
  - `claims[]`
  - 각 claim: `claim_id`, `claim_text`, `claim_scope`, `support_status`, `supporting_sources`, `conflicting_sources`, `review_reason`
  - `review_reason`에는 사람이 최종 검토한다는 범위를 남겼습니다.

3. 테스트 결과
- `cd src; python -m unittest tests/test_json_outputs.py` 성공, 4개 통과
- `python -m unittest discover tests` 성공, 55개 통과
- `python scripts/run_guard.py fixtures/cases/01-pass-consistent --out output/demo --overwrite` 성공

4. 생성 파일 예시 경로
- [src/output/demo/findings.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/findings.json)
- [src/output/demo/evidence-map.json](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/evidence-map.json)

5. git diff 요약
- `render_outputs.py` 신규 추가: findings/evidence-map 렌더링 분리
- `run_guard.py` 수정: `run_id` 추가 및 JSON 산출물 2종 생성 연결
- `test_json_outputs.py` 신규 추가: Case 01 빈 findings/supported map, Case 03/05/06 conflict map 검증
- review report, human review queue, HTML/UI, 자동 수정, 법적 판정은 구현하지 않음

## 15 T15: render human review markdown outputs

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 Markdown 산출물 2종을 구현하세요.

먼저 git status와 render_outputs.py, existing findings.json, evidence-map.json 구조를 확인하세요. 규칙 로직은 수정하지 마세요.

이번 Task 목표:
사람 검토용 review-report.md와 human-review-queue.md를 생성합니다.

review-report.md 필수 섹션:
- # Material Evidence Consistency Review
- ## Run Summary
- ## Product Identity
- ## Evidence Coverage
- ## Findings By Severity
- ## Source Comparison
- ## Required Human Decisions
- ## Scope Limitation

human-review-queue.md 필수 항목:
- Finding ID
- Rule ID
- Why Human Review Is Required
- Documents To Inspect
- Suggested Reviewer
- Decision Options

구현 요구사항:
1. findings severity가 blocker, high, review 순으로 정렬되도록 하세요.
2. finding마다 상품명, 옵션 범위, 비교 값, evidence refs, human action을 Markdown으로 표시하세요.
3. human-review-queue에는 자동으로 확정하지 못한 finding 또는 high/blocker finding을 넣으세요.
4. Suggested Reviewer는 "상품등록 담당자", "품질관리 담당자", "상세페이지 콘텐츠 담당자" 범위에서만 제시하세요.
5. Scope Limitation에 아래 의미를 명시하세요.
   - 이 결과는 법적 적합성, 판매 승인/차단, 인증서 진위, 위반 여부를 판정하지 않는다.
   - 최종 판단은 사람이 한다.
6. src/tests/test_markdown_outputs.py를 추가하세요.
   - Case 05 또는 Case 06 실행
   - 두 Markdown 파일 존재
   - finding ID와 rule ID 포함
   - 금지 표현 검사: 불법, 위반 확정, 판매 차단, 승인 불가
   - Case 01은 findings section에 열린 finding이 없음

이번 Task에서 절대 구현하지 말 것:
- HTML UI
- dashboard
- finding 자동 수정
- 고객/브랜드에 자동 전송
- 정책 위반 확정

검증:
cd src
python -m unittest tests/test_markdown_outputs.py
python scripts/run_guard.py fixtures/cases/05-detail-overclaim --out output/demo --overwrite

완료 기준:
- 두 Markdown 출력 파일이 생성된다.
- 사람이 어떤 문서를 확인해야 하는지 알 수 있다.
- 범위 제한 문구가 명확하다.
- 금지된 법적/승인 표현이 없다.

최종 보고 형식:
1. 수정 파일 목록
2. Markdown 출력 구조
3. 테스트 결과
4. 데모에 사용할 추천 output 경로
5. git diff 요약
간다


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- [src/scripts/render_outputs.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/render_outputs.py)
- [src/scripts/run_guard.py](D:/Ji_hwan/material-evidence-consistency-guard/src/scripts/run_guard.py)
- [src/tests/test_markdown_outputs.py](D:/Ji_hwan/material-evidence-consistency-guard/src/tests/test_markdown_outputs.py)
- [src/output/demo/review-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/review-report.md)
- [src/output/demo/human-review-queue.md](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/human-review-queue.md)

2. Markdown 출력 구조
- `review-report.md`
  - `# Material Evidence Consistency Review`
  - `## Run Summary`
  - `## Product Identity`
  - `## Evidence Coverage`
  - `## Findings By Severity`
  - `## Source Comparison`
  - `## Required Human Decisions`
  - `## Scope Limitation`
- `human-review-queue.md`
  - Finding ID
  - Rule ID
  - Why Human Review Is Required
  - Documents To Inspect
  - Suggested Reviewer
  - Decision Options

Findings는 `blocker`, `high`, `review`, `medium` 순으로 정렬됩니다. 추천 담당자는 지정 범위인 `상품등록 담당자`, `품질관리 담당자`, `상세페이지 콘텐츠 담당자`만 사용합니다.

3. 테스트 결과
- `cd src; python -m unittest tests/test_markdown_outputs.py` 성공, 4개 통과
- `python -m unittest discover tests` 성공, 59개 통과
- `python scripts/run_guard.py fixtures/cases/05-detail-overclaim --out output/demo --overwrite` 성공
- 금지 표현 `불법`, `위반 확정`, `판매 차단`, `승인 불가` 미사용 확인

4. 데모에 사용할 추천 output 경로
- [src/output/demo/review-report.md](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/review-report.md)
- [src/output/demo/human-review-queue.md](D:/Ji_hwan/material-evidence-consistency-guard/src/output/demo/human-review-queue.md)

5. git diff 요약
- `render_outputs.py`: Markdown report/queue 렌더링 추가
- `run_guard.py`: JSON 출력 대신 JSON+Markdown 전체 출력 호출로 변경
- `test_markdown_outputs.py`: 파일 생성, finding/rule 포함, 금지 표현, Case 01 no-open-finding 검증 추가
- `output/demo`은 Case 05 데모 실행 결과로 갱신됨
- HTML/UI, dashboard, 자동 수정, 정책 위반 확정은 구현하지 않음

## 16 T16: complete rule fixture cases

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 fixture Case 02~08을 완성하세요.

먼저 git status와 Case 01 fixture, 현재 규칙 R-001~R-006, run_guard.py 출력 형식을 확인하세요. 이번 Task는 fixture와 expected result만 수정합니다. 규칙 코드, parser, renderer는 수정하지 마세요.

각 fixture는 반드시 아래 파일을 포함하세요.
- product-draft.json
- product-notice.json
- detail-page.md
- validation-policy.yml
- test-report.md 또는 필요한 경우 test-report.pdf placeholder
- expected-findings.json

expected-findings.json에는 아래를 포함하세요.
- expected_rule_ids
- forbidden_rule_ids
- expected_severities
- expected_halted boolean

Fixture 요구사항:
1. 02-missing-evidence
   - 고위험 소재 존재
   - test-report.md와 test-report.pdf 없음
   - expected: R-001 blocker
   - forbidden: R-002~R-006

2. 03-report-extraction-failure
   - 시험성적서 입력은 존재하지만 핵심 필드가 누락되거나 unreadable 상태 재현
   - expected: R-002 blocker
   - forbidden: R-003~R-006

3. 04-product-target-mismatch
   - 상품 SKU와 시험성적서 SKU가 명확히 다름
   - expected: R-003 high
   - forbidden: R-004~R-006

4. 05-ratio-conflict
   - 동일 SKU와 동일 대상
   - 등록/고시/상세: 80/20
   - 시험성적서: 70/30
   - expected: R-004 high

5. 06-detail-overclaim
   - 상품/시험성적서: 80/20
   - 상세페이지: 100% 오리 다운 충전재
   - expected: R-005 high

6. 07-variant-scope-gap
   - 블랙 옵션 다운 80/20
   - 베이지 옵션 폴리에스터 100
   - 시험성적서 범위 BLACK_ALL_SIZES
   - 상세페이지: 전 옵션 오리 다운 충전재
   - expected: R-006 high
   - R-005 high가 나오도록 설계해도 됨

7. 08-ambiguous-alias
   - 상품은 오리 솜털/깃털
   - 시험성적서는 down 80 / feather 20
   - SKU는 동일
   - expected: review only
   - forbidden: R-004 high, R-005 high

주의:
- fixture 하나에 의도하지 않은 blocker/high를 추가하지 마세요.
- 실제 회사 데이터, 개인정보, 실제 시험성적서 이미지를 사용하지 마세요.
- 법적 위반이나 인증 진위 문구를 넣지 마세요.

검증:
cd src
각 fixture에 대해 아래 명령을 실행하세요.
python scripts/run_guard.py fixtures/cases/<case-name> --out output/<case-name> --overwrite

완료 기준:
- Case 02~08이 모두 실행된다.
- 각 expected-findings.json이 현재 출력과 논리적으로 맞는다.
- fixture마다 핵심 오류 조건이 하나의 명확한 시나리오로 분리된다.

최종 보고 형식:
1. 생성 또는 수정한 fixture 목록
2. fixture별 expected rule ID
3. fixture별 forbidden rule ID
4. 실행 결과 요약
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 생성 또는 수정한 fixture 목록
- `02-missing-evidence`
- `03-report-extraction-failure`
- `04-product-target-mismatch/expected-findings.json`
- `05-ratio-conflict`
- `06-detail-overclaim`
- `07-variant-scope-gap`
- `08-ambiguous-alias`

2. fixture별 expected rule ID
- `02-missing-evidence`: `R-001`
- `03-report-extraction-failure`: `R-002`
- `04-product-target-mismatch`: `R-003`
- `05-ratio-conflict`: `R-004`
- `06-detail-overclaim`: `R-005`
- `07-variant-scope-gap`: `R-005`, `R-006`
- `08-ambiguous-alias`: `R-004` review

3. fixture별 forbidden rule ID
- `02-missing-evidence`: `R-002`~`R-006`
- `03-report-extraction-failure`: `R-003`~`R-006`
- `04-product-target-mismatch`: `R-004`~`R-006`
- `05-ratio-conflict`: `R-001`, `R-002`, `R-003`, `R-005`, `R-006`
- `06-detail-overclaim`: `R-001`, `R-002`, `R-003`, `R-004`, `R-006`
- `07-variant-scope-gap`: `R-001`~`R-004`
- `08-ambiguous-alias`: `R-001`, `R-002`, `R-003`, `R-005`

4. 실행 결과 요약
- `03-report-extraction-failure`~`08-ambiguous-alias`는 `run_guard.py` 실행 성공 및 expected rule과 일치 확인.
- `02-missing-evidence`는 의도대로 `test-report.md/pdf`가 없지만, 현재 `validate_input.py`가 rule 실행 전에 이를 입력 계약 실패로 차단해서 `run_guard.py`는 exit `2`로 종료됩니다. `run_gate_rules()` 직접 실행 기준으로는 expected인 `R-001 blocker`가 생성됨을 확인했습니다.
- 이번 Task 지시대로 규칙 코드, parser, renderer는 수정하지 않았습니다.

5. git diff 요약
- 신규 fixture 디렉터리 추가: `02`, `03`, `05`, `06`, `07`, `08`
- `04-product-target-mismatch/expected-findings.json`을 새 expected schema로 갱신
- 각 expected 파일에 `expected_rule_ids`, `forbidden_rule_ids`, `expected_severities`, `expected_halted` 추가
- 검증용 output 디렉터리와 캐시는 정리했습니다.

## 16-2 16-2: route missing evidence through R-001 finding

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 T16.5 보정 Task를 수행하세요.

먼저 git status, 현재 src/scripts/validate_input.py, parse_test_report.py, run_guard.py, run_rules.py, Case 02 및 Case 03 fixture, 관련 테스트 파일을 모두 확인하세요.

이번 Task는 설계 충돌 보정입니다.

현재 충돌:

* validate_input.py는 test-report.md와 test-report.pdf가 모두 없으면 입력 계약 오류로 종료합니다.
* 하지만 Case 02는 고위험 소재·충전재에 대한 시험성적서 부재를 R-001 blocker로 생성해야 합니다.
* 따라서 run_guard.py가 validate_input 단계에서 종료되면 R-001까지 도달할 수 없습니다.

이번 Task의 목표:
시험성적서 부재를 입력 계약 오류가 아니라 비즈니스 검수 상태로 분리하고, run_guard.py 전체 흐름에서 Case 02가 R-001을 생성하도록 수정하세요.

반드시 유지할 원칙:

1. 입력 계약 오류와 규칙 finding을 구분합니다.
2. test-report.md와 test-report.pdf가 모두 없는 것은 입력 계약 오류가 아닙니다.
3. 고위험 소재·충전재가 있고 시험성적서가 없으면 R-001 blocker가 처리합니다.
4. 시험성적서 파일은 존재하지만 읽을 수 없거나 핵심 필드가 부족하면 R-002 blocker가 처리합니다.
5. R-001 또는 R-002가 생성되면 R-003~R-006은 실행하지 않습니다.
6. finding이 존재해도 run_guard.py는 정상 실행으로 종료 코드 0을 반환하고 모든 출력 파일을 생성해야 합니다.
7. 법적 판정, 판매 승인/차단, 인증서 진위, OCR, 외부 API는 추가하지 않습니다.
8. 기존 R-003~R-006 규칙 동작과 출력 schema는 변경하지 않습니다.
9. 가능한 최소 범위만 수정하고 불필요한 리팩터링은 하지 마세요.

수정 대상:

* src/scripts/validate_input.py
* src/scripts/parse_test_report.py
* src/scripts/run_guard.py
* src/scripts/run_rules.py
* src/tests/test_validate_input.py
* src/tests/test_gate_rules.py
* src/tests/test_fixture_suite.py
* src/fixtures/cases/02-missing-evidence/expected-findings.json
* src/README.md
* 필요한 경우에만 src/scripts/run_fixture_suite.py

구현 상세:

A. validate_input.py 보정

* 아래 파일은 계속 필수입니다.

  * product-draft.json
  * product-notice.json
  * detail-page.md
  * validation-policy.yml
* test-report.md 또는 test-report.pdf는 존재 여부 자체로 validation failure를 발생시키면 안 됩니다.
* 둘 다 없으면 validation은 성공해야 하며, validation result에 evidence_input_status: "absent"를 남기세요.
* 시험성적서 파일이 존재하지만 실제 핵심 필드가 부족한 경우는 validation error로 만들지 마세요. R-002가 처리해야 합니다.
* 파일 접근 불가, JSON/YAML 파싱 실패, 필수 Markdown 섹션 누락 같은 구조적 입력 오류는 기존처럼 validation error와 exit code 2를 유지하세요.

B. parse_test_report.py 보정

* test-report.md와 test-report.pdf가 둘 다 없으면 예외를 던지지 말고 아래 의미의 구조를 반환하세요.

{
"document_status": "absent",
"source_file": null,
"report_id": null,
"issuer": null,
"issued_at": null,
"tested_product": null,
"tested_materials": [],
"missing_fields": [],
"parse_notes": ["No test-report.md or test-report.pdf was supplied."]
}

* 시험성적서 파일이 존재하지만 읽을 수 없으면 document_status: "unreadable"
* 파일은 읽었으나 핵심 필드가 부족하면 document_status: "incomplete"
* 정상 파싱은 document_status: "parsed"
* test-report.md 우선 규칙은 유지하세요.

C. run_rules.py 보정

* 기존 gate 순서를 아래로 고정하세요.

1. 고위험 소재 존재 여부 확인
2. document_status == "absent"

   * 고위험 소재가 있으면 R-001 blocker 생성
   * halted = true
   * halt_reason = "missing_required_evidence"
   * R-002~R-006을 생성하지 않고 종료
3. document_status in ["unreadable", "incomplete"]

   * R-002 blocker 생성
   * halted = true
   * halt_reason = "evidence_not_extractable_or_incomplete"
   * R-001, R-003~R-006을 생성하지 않고 종료
4. document_status == "parsed"

   * 기존 R-003~R-006 흐름을 유지

* document_status == "absent"인데 고위험 소재가 없다면 기존 정책과 최소한으로 일관되게 처리하세요. 이 Task에서 새 규칙을 만들지 마세요. 필요하다면 finding 없이 진행하거나 existing behavior를 유지하세요.
* R-001과 R-002가 같은 실행에서 동시에 생성되면 안 됩니다.

D. run_guard.py 보정

* validate_input 성공 후에는 test-report가 absent여도 정규화, 규칙 실행, 출력 생성까지 계속 진행하세요.
* R-001 또는 R-002 blocker finding은 실행 실패가 아닙니다.
* Case 02와 Case 03은 process exit code 0으로 종료되어야 합니다.
* 구조적 input validation error만 exit code 2를 유지하세요.
* 예상하지 못한 내부 오류는 기존 non-zero 규약을 유지하세요.
* 아래 출력 파일 4종은 Case 02와 Case 03에서도 생성되어야 합니다.

  * findings.json
  * review-report.md
  * evidence-map.json
  * human-review-queue.md

E. 테스트 보정

1. src/tests/test_validate_input.py

* 시험성적서가 없는 Case 02가 validation success인지 검증하세요.
* evidence_input_status가 "absent"인지 검증하세요.
* 기존 필수 파일 누락은 여전히 validation failure인지 검증하세요.

2. src/tests/test_gate_rules.py

* run_gate_rules 직접 호출 테스트만으로 끝내지 말고, 가능한 기존 테스트 스타일을 유지하면서 Case 02 전체 흐름을 검증하세요.
* Case 02:

  * R-001만 존재
  * severity blocker
  * halted true
  * halt_reason "missing_required_evidence"
  * R-002~R-006 부재
* Case 03:

  * R-002만 존재
  * severity blocker
  * halted true
  * halt_reason "evidence_not_extractable_or_incomplete"
  * R-001, R-003~R-006 부재

3. src/tests/test_fixture_suite.py 및 필요한 경우 run_fixture_suite.py

* Case 02 expected-findings.json에 expected_exit_code 0을 추가하거나 기존 구조에 맞는 방식으로 같은 의미를 검증하세요.
* Case 03도 expected_exit_code 0을 검증하세요.
* fixture suite는 Case 02와 Case 03에서 output 파일 4종이 생성됐는지 검증해야 합니다.

F. fixture expectation 보정
Case 02 expected-findings.json은 최소한 아래 의미를 포함해야 합니다.

{
"expected_rule_ids": ["R-001"],
"forbidden_rule_ids": ["R-002", "R-003", "R-004", "R-005", "R-006"],
"expected_severities": {
"R-001": "blocker"
},
"expected_halted": true,
"expected_exit_code": 0
}

Case 03은 최소한 아래 의미를 포함해야 합니다.

{
"expected_rule_ids": ["R-002"],
"forbidden_rule_ids": ["R-001", "R-003", "R-004", "R-005", "R-006"],
"expected_severities": {
"R-002": "blocker"
},
"expected_halted": true,
"expected_exit_code": 0
}

G. 문서 보정
src/README.md의 시험성적서 입력 규칙을 아래 의미로 수정하세요.

* test-report.md가 있으면 우선 사용한다.
* test-report.md가 없고 test-report.pdf가 있으면 제한적으로 텍스트 추출을 시도한다.
* 둘 다 없는 경우는 입력 계약 오류가 아니다.
* 고위험 소재·충전재가 포함된 경우 R-001 증빙 누락 finding으로 분류한다.
* 시험성적서가 존재하지만 읽을 수 없거나 핵심 비교 정보가 부족한 경우 R-002 finding으로 분류한다.

검증:
반드시 아래 명령을 실행하세요.

cd src

python -m unittest tests/test_validate_input.py
python -m unittest tests/test_gate_rules.py
python -m unittest tests/test_fixture_suite.py

python scripts/run_guard.py fixtures/cases/02-missing-evidence --out output/t16-5-case-02 --overwrite
python scripts/run_guard.py fixtures/cases/03-report-extraction-failure --out output/t16-5-case-03 --overwrite

python scripts/run_fixture_suite.py
python -m unittest discover -s tests

추가 수동 검증:

1. output/t16-5-case-02/findings.json을 확인해 R-001만 존재하는지 확인하세요.
2. output/t16-5-case-03/findings.json을 확인해 R-002만 존재하는지 확인하세요.
3. 두 output 폴더에 findings.json, review-report.md, evidence-map.json, human-review-queue.md가 모두 있는지 확인하세요.
4. Case 02와 Case 03의 process exit code가 0인지 확인하세요.

완료 기준:

* test-report가 없는 Case 02는 validate_input에서 실패하지 않는다.
* Case 02는 run_guard 전체 실행에서 R-001 blocker 하나만 생성한다.
* Case 03은 run_guard 전체 실행에서 R-002 blocker 하나만 생성한다.
* Case 02와 Case 03 모두 R-003~R-006을 생성하지 않는다.
* 두 케이스 모두 exit code 0과 출력 파일 4종 생성을 만족한다.
* fixture suite와 전체 unit test가 통과한다.
* 구조적 입력 오류는 계속 exit code 2로 처리된다.
* 불필요한 새 기능, 규칙, 의존성, 리팩터링이 없다.

최종 보고 형식:

1. 수정 파일 목록
2. 입력 계약 오류와 R-001/R-002 finding의 책임 분리 요약
3. Case 02 전체 실행 결과

   * exit code
   * 생성 rule IDs
   * halted 상태와 halt reason
   * 생성 output 파일 목록
4. Case 03 전체 실행 결과

   * exit code
   * 생성 rule IDs
   * halted 상태와 halt reason
   * 생성 output 파일 목록
5. 실행한 회귀 테스트 명령과 결과
6. 기존 R-003~R-006에 영향이 없음을 확인한 근거
7. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- `src/scripts/validate_input.py`
- `src/scripts/parse_test_report.py`
- `src/scripts/run_rules.py`
- `src/scripts/render_outputs.py`
- `src/scripts/run_fixture_suite.py`
- `src/tests/test_validate_input.py`
- `src/tests/test_gate_rules.py`
- `src/tests/test_pdf_fallback.py`
- `src/tests/test_fixture_suite.py`
- `src/fixtures/cases/02-missing-evidence/expected-findings.json`
- `src/fixtures/cases/03-report-extraction-failure/expected-findings.json`
- `src/README.md`
- `logs/t16-5-error-log.md`

2. 입력 계약 오류와 R-001/R-002 finding 책임 분리 요약
- `test-report.md` / `test-report.pdf` 둘 다 없음: 이제 입력 계약 오류가 아니며 `evidence_input_status: "absent"`로 통과합니다.
- report 부재 + 고위험 소재/충전재 존재: `run_rules.py`에서 R-001 blocker로 처리합니다.
- report 파일 존재 + unreadable/incomplete: R-002 blocker로 처리합니다.
- R-001/R-002 발생 시 `R-003~R-006`은 실행하지 않습니다.
- 구조적 오류, 예: 필수 JSON/MD/policy 파일 누락, JSON/YAML 파싱 오류, 필수 MD 섹션 누락은 기존처럼 exit code `2`입니다.

3. Case 02 전체 실행 결과
- exit code: `0`
- 생성 rule IDs: `["R-001"]`
- halted: `true`
- halt reason: `missing_required_evidence`
- 생성 output 파일 4종 확인:
  - `findings.json`
  - `review-report.md`
  - `evidence-map.json`
  - `human-review-queue.md`

4. Case 03 전체 실행 결과
- exit code: `0`
- 생성 rule IDs: `["R-002"]`
- halted: `true`
- halt reason: `evidence_not_extractable_or_incomplete`
- 생성 output 파일 4종 확인:
  - `findings.json`
  - `review-report.md`
  - `evidence-map.json`
  - `human-review-queue.md`

5. 실행한 회귀 테스트 명령과 결과
- `python -m unittest tests/test_validate_input.py` → OK, 7 tests
- `python -m unittest tests/test_gate_rules.py` → OK, 7 tests
- `python -m unittest tests/test_fixture_suite.py` → OK
- `python scripts/run_guard.py fixtures/cases/02-missing-evidence --out output/t16-5-case-02 --overwrite` → exit code 0
- `python scripts/run_guard.py fixtures/cases/03-report-extraction-failure --out output/t16-5-case-03 --overwrite` → exit code 0
- `python scripts/run_fixture_suite.py` → OK for Case 02~08
- `python -m unittest discover -s tests` → OK, 64 tests

6. 기존 R-003~R-006 영향 확인 근거
- 전체 테스트 `64 tests`가 통과했습니다.
- fixture suite에서 `04-product-target-mismatch`, `05-ratio-conflict`, `06-detail-overclaim`, `07-variant-scope-gap`, `08-ambiguous-alias`가 모두 expected rule 결과와 일치했습니다.

7. git diff 요약
- validation에서 report 부재를 structural error에서 제외했습니다.
- parser에 `document_status: "absent"` 반환 경로를 추가했습니다.
- R-001/R-002 gate 순서와 halt reason을 고정했습니다.
- absent evidence에서도 Markdown renderer가 실패하지 않도록 null-safe 처리했습니다.
- Case 02/03 expected 결과에 `expected_exit_code: 0`을 반영했습니다.
- fixture suite 실행 스크립트와 unittest wrapper를 추가했습니다.
- 최초 회귀 테스트 중 발견한 renderer null 처리 실패는 `logs/t16-5-error-log.md`에 기록했습니다.

## 17 T17: add fixture regression suite

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 fixture regression suite를 구현하세요.

먼저 git status와 fixtures/cases/01~08, expected-findings.json 형식, run_guard.py 출력 형식을 확인하세요. 규칙 로직이나 fixture 내용을 변경하지 마세요. 이번 Task는 테스트 자동화만 구현합니다.

이번 Task 목표:
8개 fixture를 순회 실행하고 expected/forbidden rule, severity, halted 상태, 필수 output 파일을 검증합니다.

구현 요구사항:
1. src/scripts/run_fixture_suite.py를 생성하세요.
2. fixtures/cases 아래 모든 case directory를 정렬 순서로 순회하세요.
3. 각 case를 임시 output directory에 실행하세요.
4. expected-findings.json과 findings.json을 비교하세요.
5. 반드시 검증할 항목:
   - expected_rule_ids
   - forbidden_rule_ids
   - expected_severities
   - expected_halted
   - findings.json 존재
   - evidence-map.json 존재
   - review-report.md 존재
   - human-review-queue.md 존재
6. 실패 시 case 이름, expected, actual, 누락된 rule, 금지 rule을 명확하게 출력하세요.
7. src/tests/test_fixture_suite.py를 추가하세요.
8. 기존 개별 unit test도 유지하세요.
9. Python 표준 라이브러리만 사용하세요.

이번 Task에서 절대 구현하지 말 것:
- 새 규칙
- fixture 수정
- 결과물 schema 변경
- 외부 테스트 프레임워크
- UI, API, OCR

검증:
cd src
python scripts/run_fixture_suite.py
python -m unittest discover -s tests

완료 기준:
- 8개 fixture 전체가 pass한다.
- suite 실패 시 어떤 규칙이 왜 다른지 명확히 출력한다.
- 개별 unit test와 fixture suite가 모두 통과한다.

최종 보고 형식:
1. 수정 파일 목록
2. fixture suite 검증 항목
3. 실행 결과
4. 실패 시 출력 예시
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- `src/scripts/run_fixture_suite.py`
- `src/tests/test_fixture_suite.py`

2. fixture suite 검증 항목
- canonical Case 01~08을 정렬 순서로 실행
- 각 case를 임시 output directory에 실행
- `expected-findings.json`과 `findings.json` 비교
- 검증 항목:
  - `expected_rule_ids`
  - `forbidden_rule_ids`
  - `expected_severities`
  - `expected_halted`
  - `findings.json`
  - `evidence-map.json`
  - `review-report.md`
  - `human-review-queue.md`

3. 실행 결과
- `python scripts/run_fixture_suite.py` → 8 cases passed
- `python -m unittest discover -s tests` → OK, 64 tests

4. 실패 시 출력 예시
```text
05-ratio-conflict: rule mismatch expected=['R-004'] actual=['R-005'] missing=['R-004'] unexpected=['R-005']
05-ratio-conflict: forbidden rule ids present expected_forbidden=['R-001', 'R-002'] actual=['R-002'] forbidden_present=['R-002']
```

5. git diff 요약
- fixture suite가 기존 고정 output 경로 대신 임시 디렉터리를 사용하도록 변경했습니다.
- `findings.json` 기준으로 expected/forbidden rule과 severity를 검증하도록 보정했습니다.
- Case 01 포함 canonical 8개 fixture 통과 메시지를 test에서 확인합니다.
- 규칙 로직, fixture 데이터, output schema는 변경하지 않았습니다.

## 18 T18: finalize submission documentation and verification log

입력 --------------------------------------------------------------------------------------------------

현재 repository에서 Material Evidence Consistency Guard의 제출 문서와 최종 검수를 수행하세요.

먼저 git status와 전체 제출 구조를 확인하세요. 기존 기능 코드를 리팩터링하거나 새 기능을 추가하지 마세요.

이번 Task 목표:
심사자가 README만 보고 fixture 실행과 결과 확인을 할 수 있게 하고, 범위 제한을 명확히 문서화합니다.

수정 대상:
- README.md
- src/README.md
- src/.codex-plugin/plugin.json
- src/skills/material-evidence-consistency-guard/SKILL.md
- logs/final-verification.md

루트 README.md에 반드시 포함:
1. 프로젝트 한 줄 설명
2. 제출 구조
3. 실행 방법
   - cd src
   - python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite
4. fixture suite 실행 방법
5. 생성되는 출력 파일 4종
6. 90초 데모 순서
7. 범위 제한

src/README.md에 반드시 포함:
1. 입력 파일 5종
2. 출력 파일 4종
3. R-001~R-006 요약
4. 우선순위 게이트
5. test-report.md 우선, PDF 제한적 fallback
6. fixture 목록
7. 테스트 명령

반드시 명시할 범위 제한:
- 법적 판정 안 함
- 판매 승인 또는 차단 안 함
- 인증서 진위 판정 안 함
- 허위광고 판정 안 함
- OCR SaaS 안 씀
- 무신사 API 안 씀
- 챗봇 안 만듦
- 상품 추천 안 함
- 사람 검토가 최종 판단

SKILL.md와 plugin.json의 설명도 README와 모순되지 않게 최소한으로 정리하세요.

검증:
cd src
python scripts/run_fixture_suite.py
python -m unittest discover -s tests
python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite

검증이 끝나면 logs/final-verification.md를 생성하세요.
포함 내용:
- 실행 날짜
- 실행 명령
- 결과
- 생성된 output 파일
- 남은 제한 사항

완료 기준:
- README만으로 새 사용자가 실행할 수 있다.
- 모든 fixture suite와 unit test가 통과한다.
- 문서가 구현 범위를 과장하지 않는다.
- logs/final-verification.md가 존재한다.

최종 보고 형식:
1. 수정 파일 목록
2. 실행한 최종 검증 명령과 결과
3. README에 명시한 범위 제한
4. 남은 리스크 또는 미구현 제한
5. git diff 요약


출력 --------------------------------------------------------------------------------------------------

1. 수정 파일 목록
- `README.md`
- `src/README.md`
- `src/.codex-plugin/plugin.json`
- `src/skills/material-evidence-consistency-guard/SKILL.md`
- `logs/final-verification.md`
- 검증 산출물 생성: `src/output/final-demo/`

2. 실행한 최종 검증 명령과 결과
- `cd src`
- `python scripts/run_fixture_suite.py` → 통과, canonical 8 fixtures passed
- `python -m unittest discover -s tests` → 통과, 64 tests OK
- `python scripts/run_guard.py fixtures/cases/07-variant-scope-gap --out output/final-demo --overwrite` → 통과, exit code 0

3. README에 명시한 범위 제한
- 법적 판정 안 함
- 판매 승인 또는 차단 안 함
- 인증서 진위 판정 안 함
- 허위광고 판정 안 함
- OCR SaaS 안 씀
- 무신사 API 안 씀
- 챗봇 안 만듦
- 상품 추천 안 함
- 사람 검토가 최종 판단

4. 남은 리스크 또는 미구현 제한
- PDF는 `test-report.md` 부재 시 제한적 텍스트 추출 fallback만 지원합니다.
- 상세페이지 처리는 명시적 소재, 수치, 옵션 범위 중심입니다.
- 산출물은 검토 보조 자료이며 최종 판단은 사람이 해야 합니다.

5. git diff 요약
- 루트 README를 제출 구조, 실행 방법, fixture suite, 90초 데모, 범위 제한 중심으로 정리했습니다.
- `src/README.md`에 입력/출력, R-001~R-006, 게이트 우선순위, fixture 목록, 테스트 명령을 추가했습니다.
- plugin manifest와 SKILL 설명을 현재 구현 범위와 맞췄습니다.
- `logs/final-verification.md`에 최종 검증 기록을 남겼습니다.
- 규칙 로직과 fixture 내용은 변경하지 않았습니다.