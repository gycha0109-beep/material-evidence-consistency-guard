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
CASE03_DIR = SRC_ROOT / "fixtures" / "cases" / "03-ratio-conflict"
CASE04_DIR = SRC_ROOT / "fixtures" / "cases" / "04-product-target-mismatch"


def copy_case(source: Path, target: Path) -> Path:
    shutil.copytree(source, target)
    return target


class RatioRuleTest(unittest.TestCase):
    def test_case03_ratio_conflict_creates_r004_high(self) -> None:
        normalized = build_normalized_model(CASE03_DIR)

        result = run_gate_rules(CASE03_DIR, normalized)

        self.assertTrue(result["halted"])
        self.assertEqual(result["halt_reason"], "R-004 high: material ratio conflict")
        self.assertEqual(result["findings"][0]["rule_id"], "R-004")
        self.assertEqual(result["findings"][0]["severity"], "high")
        values = result["findings"][0]["values"]
        self.assertEqual(values["canonical_material"], "duck_down_cluster")
        self.assertIn("source_values", values)

    def test_case01_has_no_r004(self) -> None:
        normalized = build_normalized_model(CASE01_DIR)

        result = run_gate_rules(CASE01_DIR, normalized)

        self.assertFalse(result["halted"])
        self.assertNotIn("R-004", [finding["rule_id"] for finding in result["findings"]])

    def test_sku_mismatch_fixture_has_no_r004(self) -> None:
        normalized = build_normalized_model(CASE04_DIR)

        result = run_gate_rules(CASE04_DIR, normalized)

        self.assertTrue(result["halted"])
        self.assertEqual([finding["rule_id"] for finding in result["findings"]], ["R-003"])
        self.assertIn("R-004", result["skipped_rules"])

    def test_missing_report_has_no_r004(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(CASE01_DIR, Path(temp_dir) / "case")
            (case_dir / "test-report.md").unlink()

            result = run_gate_rules(case_dir, normalized_model=None)

            self.assertTrue(result["halted"])
            self.assertEqual([finding["rule_id"] for finding in result["findings"]], ["R-001"])
            self.assertIn("R-004", result["skipped_rules"])

    def test_ambiguous_alias_creates_review_not_high(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(CASE01_DIR, Path(temp_dir) / "case")
            detail_page = case_dir / "detail-page.md"
            detail_page.write_text(
                detail_page.read_text(encoding="utf-8").replace(
                    "충전재: 오리 솜털 80%, 오리 깃털 20%",
                    "충전재: down 80 / feather 20",
                ),
                encoding="utf-8",
            )
            normalized = build_normalized_model(case_dir)

            result = run_gate_rules(case_dir, normalized)

            severities = {finding["rule_id"]: finding["severity"] for finding in result["findings"]}
            self.assertEqual(severities.get("R-004"), "review")
            self.assertNotIn("high", severities.values())


if __name__ == "__main__":
    unittest.main()
