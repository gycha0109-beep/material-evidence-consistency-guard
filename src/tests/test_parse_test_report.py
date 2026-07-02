from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SRC_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from normalize_inputs import load_policy  # noqa: E402
from parse_test_report import parse_test_report  # noqa: E402


CASE01_REPORT = SRC_ROOT / "fixtures" / "cases" / "01-pass-consistent" / "test-report.md"


def write_report(directory: str, content: str) -> Path:
    path = Path(directory) / "test-report.md"
    path.write_text(content, encoding="utf-8")
    return path


class ParseTestReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_policy()

    def test_case01_parses(self) -> None:
        result = parse_test_report(CASE01_REPORT, self.policy)

        self.assertEqual(result["document_status"], "parsed")
        self.assertEqual(result["report_id"], "TR-CASE01-2026-0001")
        self.assertEqual(result["issuer"], "Korea Textile Test Lab")
        self.assertEqual(result["issued_at"], "2026-01-15")
        self.assertEqual(result["tested_product"]["name"], "노르딕 오리 다운 파카")
        self.assertEqual(result["tested_product"]["identifier"], "NW-DP-2026-01")
        self.assertEqual(result["tested_product"]["variant_scope"], "BLACK_ALL_SIZES")
        self.assertEqual(len(result["tested_materials"]), 3)
        self.assertEqual(result["missing_fields"], [])

    def test_missing_tested_product_identifier_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = write_report(
                temp_dir,
                """---
report_id: TR-MISSING-ID
issuer: Korea Textile Test Lab
issued_at: 2026-01-15
tested_product_name: 노르딕 오리 다운 파카
tested_variant_scope: BLACK_ALL_SIZES
---

## Tested Materials

- component: 충전재
  material: 오리 솜털
  percentage: 80%
""",
            )

            result = parse_test_report(report, self.policy)

            self.assertEqual(result["document_status"], "incomplete")
            self.assertIsNone(result["tested_product"]["identifier"])
            self.assertIn("front_matter.tested_product_identifier", result["missing_fields"])

    def test_missing_tested_materials_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = write_report(
                temp_dir,
                """---
report_id: TR-NO-MATERIALS
issuer: Korea Textile Test Lab
issued_at: 2026-01-15
tested_product_name: 노르딕 오리 다운 파카
tested_product_identifier: NW-DP-2026-01
tested_variant_scope: BLACK_ALL_SIZES
---

## Tested Results

- note: no material rows
""",
            )

            result = parse_test_report(report, self.policy)

            self.assertEqual(result["document_status"], "incomplete")
            self.assertIn("tested_materials", result["missing_fields"])

    def test_percentage_format_is_converted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = write_report(
                temp_dir,
                """---
report_id: TR-PCT
issuer: Korea Textile Test Lab
issued_at: 2026-01-15
tested_product_name: 노르딕 오리 다운 파카
tested_product_identifier: NW-DP-2026-01
tested_variant_scope: BLACK_ALL_SIZES
---

## Tested Materials

- component: 충전재
  material: 오리 솜털
  percentage: 80.0
""",
            )

            result = parse_test_report(report, self.policy)

            self.assertEqual(result["document_status"], "parsed")
            self.assertEqual(result["tested_materials"][0]["percentage"], 80.0)

    def test_ambiguous_material_alias_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = write_report(
                temp_dir,
                """---
report_id: TR-AMBIGUOUS
issuer: Korea Textile Test Lab
issued_at: 2026-01-15
tested_product_name: 노르딕 오리 다운 파카
tested_product_identifier: NW-DP-2026-01
tested_variant_scope: BLACK_ALL_SIZES
---

## Tested Materials

- component: 충전재
  material: down
  percentage: 80%
""",
            )

            result = parse_test_report(report, self.policy)

            self.assertEqual(result["document_status"], "parsed")
            self.assertEqual(
                result["tested_materials"][0]["normalized_material"],
                {"status": "ambiguous", "value": "down"},
            )


if __name__ == "__main__":
    unittest.main()
