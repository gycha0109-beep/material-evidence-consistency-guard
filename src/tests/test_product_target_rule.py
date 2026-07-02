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


def copy_case(target: Path) -> Path:
    shutil.copytree(CASE01_DIR, target)
    return target


class ProductTargetRuleTest(unittest.TestCase):
    def test_sku_mismatch_creates_r003_high_and_halts_lower_rules(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(Path(temp_dir) / "case")
            report = case_dir / "test-report.md"
            report.write_text(
                report.read_text(encoding="utf-8").replace(
                    "tested_product_identifier: NW-DP-2026-01",
                    "tested_product_identifier: UW-GV-02",
                ),
                encoding="utf-8",
            )
            normalized = build_normalized_model(case_dir)

            result = run_gate_rules(case_dir, normalized)

            self.assertTrue(result["halted"])
            self.assertEqual(result["halt_reason"], "R-003 high: test report target product mismatch")
            self.assertEqual(result["findings"][0]["rule_id"], "R-003")
            self.assertEqual(result["findings"][0]["severity"], "high")
            self.assertEqual(result["findings"][0]["values"]["product.internal_sku"], "NW-DP-2026-01")
            self.assertEqual(
                result["findings"][0]["values"]["evidence_document.tested_product.identifier"],
                "UW-GV-02",
            )
            self.assertIn("R-004", result["skipped_rules"])

    def test_case01_matches(self) -> None:
        normalized = build_normalized_model(CASE01_DIR)

        result = run_gate_rules(CASE01_DIR, normalized)

        self.assertFalse(result["halted"])
        self.assertEqual(result["findings"], [])

    def test_same_sku_with_name_difference_is_not_high(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(Path(temp_dir) / "case")
            report = case_dir / "test-report.md"
            report.write_text(
                report.read_text(encoding="utf-8").replace(
                    "tested_product_name: 노르딕 오리 다운 파카",
                    "tested_product_name: 노르딕 파카",
                ),
                encoding="utf-8",
            )
            normalized = build_normalized_model(case_dir)

            result = run_gate_rules(case_dir, normalized)

            self.assertFalse(result["halted"])
            self.assertNotIn("high", {finding["severity"] for finding in result["findings"]})

    def test_r001_prevents_r003(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(Path(temp_dir) / "case")
            (case_dir / "test-report.md").unlink()

            result = run_gate_rules(case_dir, normalized_model=None)

            self.assertTrue(result["halted"])
            self.assertEqual([finding["rule_id"] for finding in result["findings"]], ["R-001"])
            self.assertIn("R-003", result["skipped_rules"])

    def test_r002_prevents_r003(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(Path(temp_dir) / "case")
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
            self.assertEqual([finding["rule_id"] for finding in result["findings"]], ["R-002"])
            self.assertIn("R-003", result["skipped_rules"])


if __name__ == "__main__":
    unittest.main()
