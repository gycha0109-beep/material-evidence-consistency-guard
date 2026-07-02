from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SRC_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_input import validate_input  # noqa: E402


FIXTURE_DIR = SRC_ROOT / "fixtures" / "cases" / "01-pass-consistent"
CASE02_DIR = SRC_ROOT / "fixtures" / "cases" / "02-missing-evidence"


class ValidateInputTest(unittest.TestCase):
    def copy_fixture(self, temp_dir: str) -> Path:
        target = Path(temp_dir) / "case"
        shutil.copytree(FIXTURE_DIR, target)
        return target

    def test_valid_fixture_passes(self) -> None:
        result = validate_input(FIXTURE_DIR)

        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["evidence_input_status"], "markdown")

    def test_missing_test_report_is_absent_evidence_status(self) -> None:
        result = validate_input(CASE02_DIR)

        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["evidence_input_status"], "absent")

    def test_missing_required_file_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = self.copy_fixture(temp_dir)
            (case_dir / "product-notice.json").unlink()

            result = validate_input(case_dir)

            self.assertFalse(result["ok"])
            self.assertIn("product-notice.json: required file is missing", result["errors"])

    def test_missing_test_report_with_required_file_missing_still_fails_structural_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = self.copy_fixture(temp_dir)
            (case_dir / "test-report.md").unlink()
            (case_dir / "detail-page.md").unlink()

            result = validate_input(case_dir)

            self.assertFalse(result["ok"])
            self.assertEqual(result["evidence_input_status"], "absent")
            self.assertIn("detail-page.md: required file is missing", result["errors"])

    def test_missing_product_draft_key_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = self.copy_fixture(temp_dir)
            (case_dir / "product-draft.json").write_text(
                """{
  "product_id": "demo-product-001",
  "product_name": "Demo Consistent Product",
  "variants": [],
  "material_components": []
}
""",
                encoding="utf-8",
            )

            result = validate_input(case_dir)

            self.assertFalse(result["ok"])
            self.assertIn(
                "product-draft.json: missing required key 'high_risk_materials'",
                result["errors"],
            )

    def test_missing_detail_page_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = self.copy_fixture(temp_dir)
            (case_dir / "detail-page.md").write_text(
                """## Product Identity

## Material Claims

## Fill Claims

## Certification Or Evidence Claims
""",
                encoding="utf-8",
            )

            result = validate_input(case_dir)

            self.assertFalse(result["ok"])
            self.assertIn(
                "detail-page.md: missing required section '## Care Or Safety Claims'",
                result["errors"],
            )

    def test_missing_validation_policy_key_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = self.copy_fixture(temp_dir)
            (case_dir / "validation-policy.yml").write_text(
                """high_risk_materials: []
material_aliases: {}
required_evidence_rules: []
""",
                encoding="utf-8",
            )

            result = validate_input(case_dir)

            self.assertFalse(result["ok"])
            self.assertIn(
                "validation-policy.yml: missing required key 'ratio_tolerance'",
                result["errors"],
            )


if __name__ == "__main__":
    unittest.main()
