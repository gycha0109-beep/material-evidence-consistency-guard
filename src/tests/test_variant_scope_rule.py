from __future__ import annotations

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
CASE04_DIR = SRC_ROOT / "fixtures" / "cases" / "04-product-target-mismatch"
CASE06_DIR = SRC_ROOT / "fixtures" / "cases" / "06-variant-scope-gap"


def copy_case(source: Path, target: Path) -> Path:
    shutil.copytree(source, target)
    return target


class VariantScopeRuleTest(unittest.TestCase):
    def test_case06_variant_scope_gap_creates_r006_high(self) -> None:
        normalized = build_normalized_model(CASE06_DIR)

        result = run_gate_rules(CASE06_DIR, normalized)

        r006 = [finding for finding in result["findings"] if finding["rule_id"] == "R-006"]
        self.assertEqual(len(r006), 1)
        self.assertEqual(r006[0]["severity"], "high")
        self.assertEqual(r006[0]["values"]["tested_variant_scope"], "BLACK_ALL_SIZES")
        self.assertEqual(r006[0]["values"]["scope_status"], "partial")
        self.assertTrue(result["halted"])

    def test_case01_has_no_r006(self) -> None:
        normalized = build_normalized_model(CASE01_DIR)

        result = run_gate_rules(CASE01_DIR, normalized)

        self.assertNotIn("R-006", [finding["rule_id"] for finding in result["findings"]])

    def test_evidence_missing_or_sku_mismatch_prevents_r006(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_report_case = copy_case(CASE06_DIR, Path(temp_dir) / "missing-report")
            (missing_report_case / "test-report.md").unlink()

            r001_result = run_gate_rules(missing_report_case, normalized_model=None)
            self.assertEqual([finding["rule_id"] for finding in r001_result["findings"]], ["R-001"])
            self.assertIn("R-006", r001_result["skipped_rules"])

            normalized = build_normalized_model(CASE04_DIR)
            r003_result = run_gate_rules(CASE04_DIR, normalized)
            self.assertEqual([finding["rule_id"] for finding in r003_result["findings"]], ["R-003"])
            self.assertIn("R-006", r003_result["skipped_rules"])

    def test_unknown_scope_creates_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(CASE06_DIR, Path(temp_dir) / "case")
            report = case_dir / "test-report.md"
            report.write_text(
                report.read_text(encoding="utf-8").replace(
                    "tested_variant_scope: BLACK_ALL_SIZES",
                    "tested_variant_scope: SEASONAL_SAMPLE",
                ),
                encoding="utf-8",
            )
            normalized = build_normalized_model(case_dir)

            result = run_gate_rules(case_dir, normalized)

            r006 = [finding for finding in result["findings"] if finding["rule_id"] == "R-006"]
            self.assertEqual(len(r006), 1)
            self.assertEqual(r006[0]["severity"], "review")
            self.assertFalse(any(finding["rule_id"] == "R-006" and finding["severity"] == "high" for finding in result["findings"]))


if __name__ == "__main__":
    unittest.main()
