from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SRC_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from build_normalized_model import build_normalized_model  # noqa: E402
from run_rules import run_gate_rules  # noqa: E402


CASE01_DIR = SRC_ROOT / "fixtures" / "cases" / "01-pass-consistent"
CASE02_DIR = SRC_ROOT / "fixtures" / "cases" / "02-missing-evidence"
CASE03_DIR = SRC_ROOT / "fixtures" / "cases" / "03-report-extraction-failure"
OUTPUT_FILES = {
    "findings.json",
    "review-report.md",
    "evidence-map.json",
    "human-review-queue.md",
}


class GateRulesTest(unittest.TestCase):
    def copy_case(self, temp_dir: str) -> Path:
        case_dir = Path(temp_dir) / "case"
        shutil.copytree(CASE01_DIR, case_dir)
        return case_dir

    def test_high_risk_material_without_report_creates_r001_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = self.copy_case(temp_dir)
            (case_dir / "test-report.md").unlink()

            result = run_gate_rules(case_dir, normalized_model=None)

            self.assertTrue(result["halted"])
            self.assertEqual(result["findings"][0]["rule_id"], "R-001")
            self.assertEqual(len(result["findings"]), 1)
            self.assertEqual(result["halt_reason"], "missing_required_evidence")
            self.assertIn("R-002", result["skipped_rules"])

    def test_existing_report_with_missing_core_field_creates_r002_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = self.copy_case(temp_dir)
            report = case_dir / "test-report.md"
            report.write_text(
                report.read_text(encoding="utf-8").replace(
                    "tested_product_identifier: NW-DP-2026-01\n",
                    "",
                ),
                encoding="utf-8",
            )
            normalized = build_normalized_model(case_dir)

            result = run_gate_rules(case_dir, normalized)

            self.assertTrue(result["halted"])
            self.assertEqual(result["findings"][0]["rule_id"], "R-002")
            self.assertEqual(len(result["findings"]), 1)
            self.assertEqual(result["halt_reason"], "evidence_not_extractable_or_incomplete")
            self.assertIn("front_matter.tested_product_identifier", result["findings"][0]["message"])

    def test_gate_halts_for_r001_or_r002(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_report_case = self.copy_case(temp_dir)
            (missing_report_case / "test-report.md").unlink()

            r001_result = run_gate_rules(missing_report_case, normalized_model=None)

            incomplete_case = Path(temp_dir) / "case-incomplete"
            shutil.copytree(CASE01_DIR, incomplete_case)
            report = incomplete_case / "test-report.md"
            report.write_text(
                """---
report_id: TR-INCOMPLETE
issuer: Korea Textile Test Lab
issued_at: 2026-01-15
tested_product_name: 노르딕 오리 다운 파카
tested_product_identifier: NW-DP-2026-01
tested_variant_scope: BLACK_ALL_SIZES
---
""",
                encoding="utf-8",
            )
            r002_result = run_gate_rules(incomplete_case, build_normalized_model(incomplete_case))

            self.assertTrue(r001_result["halted"])
            self.assertTrue(r002_result["halted"])
            self.assertEqual(r001_result["halt_reason"], "missing_required_evidence")
            self.assertEqual(r002_result["halt_reason"], "evidence_not_extractable_or_incomplete")
            self.assertIn("R-003", r001_result["skipped_rules"])
            self.assertIn("R-003", r002_result["skipped_rules"])

    def test_case02_full_flow_creates_only_r001_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "case02"
            completed = __import__("subprocess").run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "run_guard.py"),
                    str(CASE02_DIR),
                    "--out",
                    str(output_dir),
                ],
                cwd=SRC_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            rules_debug = json.loads((output_dir / "rules-debug.json").read_text(encoding="utf-8"))
            rule_ids = [finding["rule_id"] for finding in rules_debug["findings"]]
            self.assertEqual(rule_ids, ["R-001"])
            self.assertEqual(rules_debug["findings"][0]["severity"], "blocker")
            self.assertTrue(rules_debug["halted"])
            self.assertEqual(rules_debug["halt_reason"], "missing_required_evidence")
            self.assertTrue(OUTPUT_FILES.issubset({path.name for path in output_dir.iterdir()}))

    def test_case03_full_flow_creates_only_r002_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "case03"
            completed = __import__("subprocess").run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "run_guard.py"),
                    str(CASE03_DIR),
                    "--out",
                    str(output_dir),
                ],
                cwd=SRC_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            rules_debug = json.loads((output_dir / "rules-debug.json").read_text(encoding="utf-8"))
            rule_ids = [finding["rule_id"] for finding in rules_debug["findings"]]
            self.assertEqual(rule_ids, ["R-002"])
            self.assertEqual(rules_debug["findings"][0]["severity"], "blocker")
            self.assertTrue(rules_debug["halted"])
            self.assertEqual(rules_debug["halt_reason"], "evidence_not_extractable_or_incomplete")
            self.assertTrue(OUTPUT_FILES.issubset({path.name for path in output_dir.iterdir()}))

    def test_case01_passes_gate(self) -> None:
        normalized = build_normalized_model(CASE01_DIR)

        result = run_gate_rules(CASE01_DIR, normalized)

        self.assertFalse(result["halted"])
        self.assertIsNone(result["halt_reason"])
        self.assertEqual(result["findings"], [])

    def test_run_guard_writes_rules_debug(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            run_guard = SCRIPTS_DIR / "run_guard.py"
            completed = __import__("subprocess").run(
                [
                    sys.executable,
                    str(run_guard),
                    str(CASE01_DIR),
                    "--out",
                    str(output_dir),
                ],
                cwd=SRC_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            rules_debug = json.loads((output_dir / "rules-debug.json").read_text(encoding="utf-8"))
            self.assertFalse(rules_debug["halted"])


if __name__ == "__main__":
    unittest.main()
