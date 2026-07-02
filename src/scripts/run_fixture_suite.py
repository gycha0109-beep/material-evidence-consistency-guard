"""Run fixture expectations against CLI outputs."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = SRC_ROOT / "fixtures" / "cases"
OUTPUT_FILES = {
    "findings.json",
    "review-report.md",
    "evidence-map.json",
    "human-review-queue.md",
}
CANONICAL_CASES = {
    "01-pass-consistent",
    "02-missing-evidence",
    "03-report-extraction-failure",
    "04-product-target-mismatch",
    "05-ratio-conflict",
    "06-detail-overclaim",
    "07-variant-scope-gap",
    "08-ambiguous-alias",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def discover_cases() -> list[Path]:
    cases = []
    for case_dir in sorted(CASES_DIR.iterdir(), key=lambda path: path.name):
        if not case_dir.is_dir() or case_dir.name not in CANONICAL_CASES:
            continue
        if not (case_dir / "expected-findings.json").is_file():
            continue
        cases.append(case_dir)
    return cases


def expected_rule_ids(expected: dict) -> list[str]:
    if "expected_rule_ids" in expected:
        return list(expected["expected_rule_ids"])
    return [finding.get("rule_id") for finding in expected.get("findings", []) if finding.get("rule_id")]


def check_case(case_dir: Path, output_parent: Path) -> list[str]:
    errors: list[str] = []
    case_name = case_dir.name
    expected = load_json(case_dir / "expected-findings.json")
    output_dir = output_parent / case_name

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

    missing_outputs = sorted(
        filename for filename in OUTPUT_FILES if not (output_dir / filename).is_file()
    )
    if missing_outputs:
        errors.append(f"{case_name}: missing output files {missing_outputs}")
        return errors

    findings_output = load_json(output_dir / "findings.json")
    rules_debug = load_json(output_dir / "rules-debug.json")
    actual_findings = findings_output.get("findings", [])
    actual_rule_ids = [finding["rule_id"] for finding in actual_findings]
    expected_ids = expected_rule_ids(expected)
    missing_rule_ids = sorted(set(expected_ids).difference(actual_rule_ids))
    unexpected_rule_ids = sorted(set(actual_rule_ids).difference(expected_ids))
    if missing_rule_ids or unexpected_rule_ids:
        errors.append(
            f"{case_name}: rule mismatch expected={expected_ids} actual={actual_rule_ids} "
            f"missing={missing_rule_ids} unexpected={unexpected_rule_ids}"
        )

    forbidden_rule_ids = set(expected.get("forbidden_rule_ids", []))
    forbidden_present = sorted(forbidden_rule_ids.intersection(actual_rule_ids))
    if forbidden_present:
        errors.append(
            f"{case_name}: forbidden rule ids present expected_forbidden={sorted(forbidden_rule_ids)} "
            f"actual={actual_rule_ids} forbidden_present={forbidden_present}"
        )

    actual_severities = {
        finding["rule_id"]: finding["severity"]
        for finding in actual_findings
    }
    for rule_id, severity in expected.get("expected_severities", {}).items():
        if actual_severities.get(rule_id) != severity:
            errors.append(
                f"{case_name}: expected {rule_id} severity {severity}, got {actual_severities.get(rule_id)}"
            )

    expected_halted = expected.get("expected_halted", False)
    if rules_debug.get("halted") != expected_halted:
        errors.append(
            f"{case_name}: expected halted={expected_halted}, got {rules_debug.get('halted')}"
        )

    return errors


def main() -> int:
    all_errors: list[str] = []
    cases = discover_cases()
    with tempfile.TemporaryDirectory(prefix="material-guard-fixtures-") as temp_dir:
        output_parent = Path(temp_dir)
        for case_dir in cases:
            errors = check_case(case_dir, output_parent)
            if errors:
                all_errors.extend(errors)
            else:
                print(f"{case_dir.name}: ok")

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1
    print(f"fixture suite: {len(cases)} case(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
