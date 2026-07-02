"""Run fixture expectations against the CLI outputs."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = SRC_ROOT / "fixtures" / "cases"
OUTPUT_ROOT = SRC_ROOT / "output" / "fixture-suite"
OUTPUT_FILES = {
    "findings.json",
    "review-report.md",
    "evidence-map.json",
    "human-review-queue.md",
}
CASE_NAMES = [
    "02-missing-evidence",
    "03-report-extraction-failure",
    "04-product-target-mismatch",
    "05-ratio-conflict",
    "06-detail-overclaim",
    "07-variant-scope-gap",
    "08-ambiguous-alias",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_case(case_name: str) -> list[str]:
    errors: list[str] = []
    case_dir = CASES_DIR / case_name
    expected = load_json(case_dir / "expected-findings.json")
    output_dir = OUTPUT_ROOT / case_name
    if output_dir.exists():
        shutil.rmtree(output_dir)

    completed = subprocess.run(
        [
            sys.executable,
            str(SRC_ROOT / "scripts" / "run_guard.py"),
            str(case_dir),
            "--out",
            str(output_dir),
            "--overwrite",
        ],
        cwd=SRC_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    expected_exit_code = expected.get("expected_exit_code", 0)
    if completed.returncode != expected_exit_code:
        errors.append(
            f"{case_name}: expected exit code {expected_exit_code}, got {completed.returncode}: {completed.stderr.strip()}"
        )
        return errors

    if completed.returncode != 0:
        return errors

    rules_debug = load_json(output_dir / "rules-debug.json")
    actual_rule_ids = [finding["rule_id"] for finding in rules_debug.get("findings", [])]
    expected_rule_ids = expected.get("expected_rule_ids", [])
    if set(actual_rule_ids) != set(expected_rule_ids):
        errors.append(f"{case_name}: expected rule ids {expected_rule_ids}, got {actual_rule_ids}")

    forbidden_rule_ids = set(expected.get("forbidden_rule_ids", []))
    forbidden_present = sorted(forbidden_rule_ids.intersection(actual_rule_ids))
    if forbidden_present:
        errors.append(f"{case_name}: forbidden rule ids present {forbidden_present}")

    actual_severities = {
        finding["rule_id"]: finding["severity"]
        for finding in rules_debug.get("findings", [])
    }
    for rule_id, severity in expected.get("expected_severities", {}).items():
        if actual_severities.get(rule_id) != severity:
            errors.append(
                f"{case_name}: expected {rule_id} severity {severity}, got {actual_severities.get(rule_id)}"
            )

    if rules_debug.get("halted") != expected.get("expected_halted"):
        errors.append(
            f"{case_name}: expected halted={expected.get('expected_halted')}, got {rules_debug.get('halted')}"
        )

    missing_outputs = sorted(OUTPUT_FILES.difference({path.name for path in output_dir.iterdir()}))
    if missing_outputs:
        errors.append(f"{case_name}: missing output files {missing_outputs}")

    return errors


def main() -> int:
    all_errors: list[str] = []
    for case_name in CASE_NAMES:
        errors = check_case(case_name)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"{case_name}: ok")

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
