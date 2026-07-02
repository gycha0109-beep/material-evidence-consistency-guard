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
CASE05_DIR = SRC_ROOT / "fixtures" / "cases" / "05-detail-overclaim"


def copy_case(source: Path, target: Path) -> Path:
    shutil.copytree(source, target)
    return target


class DetailClaimRuleTest(unittest.TestCase):
    def test_case05_detail_overclaim_creates_r005_high(self) -> None:
        normalized = build_normalized_model(CASE05_DIR)

        result = run_gate_rules(CASE05_DIR, normalized)

        self.assertTrue(result["halted"])
        self.assertEqual(result["halt_reason"], "R-005 high: detail page explicit claim exceeds evidence")
        self.assertEqual(result["findings"][0]["rule_id"], "R-005")
        self.assertEqual(result["findings"][0]["severity"], "high")
        self.assertIn("100% 오리 다운 충전재", result["findings"][0]["values"]["claim_raw_text"])
        self.assertIn("evidence_values", result["findings"][0]["values"])

    def test_qualitative_claim_without_numbers_has_no_r005(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(CASE01_DIR, Path(temp_dir) / "case")
            detail_page = case_dir / "detail-page.md"
            detail_page.write_text(
                detail_page.read_text(encoding="utf-8")
                + "\n- 프리미엄 보온성 우수 충전재\n",
                encoding="utf-8",
            )
            normalized = build_normalized_model(case_dir)

            result = run_gate_rules(case_dir, normalized)

            self.assertNotIn("R-005", [finding["rule_id"] for finding in result["findings"]])

    def test_r003_mismatch_prevents_r005(self) -> None:
        normalized = build_normalized_model(CASE04_DIR)

        result = run_gate_rules(CASE04_DIR, normalized)

        self.assertTrue(result["halted"])
        self.assertEqual([finding["rule_id"] for finding in result["findings"]], ["R-003"])
        self.assertIn("R-005", result["skipped_rules"])

    def test_ambiguous_alias_creates_review(self) -> None:
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

            r005 = [finding for finding in result["findings"] if finding["rule_id"] == "R-005"]
            self.assertEqual(len(r005), 1)
            self.assertEqual(r005[0]["severity"], "review")
            self.assertFalse(result["halted"])


if __name__ == "__main__":
    unittest.main()
