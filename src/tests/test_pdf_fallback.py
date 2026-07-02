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
from validate_input import validate_input  # noqa: E402


CASE01_DIR = SRC_ROOT / "fixtures" / "cases" / "01-pass-consistent"
CASE07_DIR = SRC_ROOT / "fixtures" / "cases" / "07-pdf-extraction-failure"


def copy_case(source: Path, target: Path) -> Path:
    shutil.copytree(source, target)
    return target


class PdfFallbackTest(unittest.TestCase):
    def test_markdown_takes_priority_over_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(CASE01_DIR, Path(temp_dir) / "case")
            (case_dir / "test-report.pdf").write_bytes(b"not a readable pdf")

            normalized = build_normalized_model(case_dir)

            self.assertEqual(normalized["evidence_document"]["document_status"], "parsed")
            self.assertEqual(
                normalized["evidence_document"]["tested_product"]["identifier"],
                "NW-DP-2026-01",
            )

    def test_no_pdf_or_markdown_uses_existing_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = copy_case(CASE01_DIR, Path(temp_dir) / "case")
            (case_dir / "test-report.md").unlink()

            result = validate_input(case_dir)

            self.assertFalse(result["ok"])
            self.assertIn("test-report.md or test-report.pdf", "\n".join(result["errors"]))

    def test_pdf_parsing_failure_becomes_r002(self) -> None:
        normalized = build_normalized_model(CASE07_DIR)

        result = run_gate_rules(CASE07_DIR, normalized)

        self.assertEqual(normalized["evidence_document"]["document_status"], "unreadable")
        self.assertTrue(result["halted"])
        self.assertEqual([finding["rule_id"] for finding in result["findings"]], ["R-002"])

    def test_pdf_parsing_failure_skips_downstream_rules(self) -> None:
        normalized = build_normalized_model(CASE07_DIR)

        result = run_gate_rules(CASE07_DIR, normalized)

        self.assertIn("R-003", result["skipped_rules"])
        self.assertIn("R-004", result["skipped_rules"])
        self.assertIn("R-005", result["skipped_rules"])
        self.assertIn("R-006", result["skipped_rules"])


if __name__ == "__main__":
    unittest.main()
