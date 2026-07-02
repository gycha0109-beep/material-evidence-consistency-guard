from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
RUN_GUARD = SRC_ROOT / "scripts" / "run_guard.py"
CASES_DIR = SRC_ROOT / "fixtures" / "cases"
FORBIDDEN = ["불법", "위반 확정", "판매 차단", "승인 불가"]


class MarkdownOutputsTest(unittest.TestCase):
    def run_case(self, case_name: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        output_dir = Path(temp_dir.name) / "out"
        result = subprocess.run(
            [
                sys.executable,
                str(RUN_GUARD),
                str(CASES_DIR / case_name),
                "--out",
                str(output_dir),
            ],
            cwd=SRC_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return output_dir

    def test_case05_markdown_files_exist_and_include_finding_ids(self) -> None:
        output_dir = self.run_case("05-detail-overclaim")
        report = (output_dir / "review-report.md").read_text(encoding="utf-8")
        queue = (output_dir / "human-review-queue.md").read_text(encoding="utf-8")

        self.assertIn("# Material Evidence Consistency Review", report)
        self.assertIn("## Run Summary", report)
        self.assertIn("## Scope Limitation", report)
        self.assertIn("F-R005-001", report)
        self.assertIn("R-005", report)
        self.assertIn("Finding ID", queue)
        self.assertIn("Rule ID", queue)
        self.assertIn("F-R005-001", queue)

    def test_forbidden_terms_are_not_used(self) -> None:
        output_dir = self.run_case("06-variant-scope-gap")
        combined = (
            (output_dir / "review-report.md").read_text(encoding="utf-8")
            + "\n"
            + (output_dir / "human-review-queue.md").read_text(encoding="utf-8")
        )

        for term in FORBIDDEN:
            self.assertNotIn(term, combined)

    def test_case01_has_no_open_findings_in_report(self) -> None:
        output_dir = self.run_case("01-pass-consistent")
        report = (output_dir / "review-report.md").read_text(encoding="utf-8")
        queue = (output_dir / "human-review-queue.md").read_text(encoding="utf-8")

        self.assertIn("No open findings from implemented rules.", report)
        self.assertIn("No open findings require manual queueing", queue)

    def test_queue_contains_required_fields_and_allowed_reviewer(self) -> None:
        output_dir = self.run_case("06-variant-scope-gap")
        queue = (output_dir / "human-review-queue.md").read_text(encoding="utf-8")

        self.assertIn("Why Human Review Is Required", queue)
        self.assertIn("Documents To Inspect", queue)
        self.assertIn("Suggested Reviewer", queue)
        self.assertIn("Decision Options", queue)
        self.assertRegex(queue, "상품등록 담당자|품질관리 담당자|상세페이지 콘텐츠 담당자")


if __name__ == "__main__":
    unittest.main()
