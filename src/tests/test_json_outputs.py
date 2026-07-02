from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SRC_ROOT / "scripts"
RUN_GUARD = SCRIPTS_DIR / "run_guard.py"
CASES_DIR = SRC_ROOT / "fixtures" / "cases"


class JsonOutputsTest(unittest.TestCase):
    def run_case(self, case_name: str) -> tuple[Path, dict, dict]:
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
        findings_path = output_dir / "findings.json"
        evidence_map_path = output_dir / "evidence-map.json"
        self.assertTrue(findings_path.is_file())
        self.assertTrue(evidence_map_path.is_file())
        return (
            output_dir,
            json.loads(findings_path.read_text(encoding="utf-8")),
            json.loads(evidence_map_path.read_text(encoding="utf-8")),
        )

    def test_case01_empty_findings_and_supported_evidence_map(self) -> None:
        _, findings, evidence_map = self.run_case("01-pass-consistent")

        self.assertEqual(findings["findings"], [])
        self.assertEqual(findings["summary"]["high"], 0)
        self.assertTrue(evidence_map["claims"])
        self.assertTrue(
            all(claim["support_status"] == "supported" for claim in evidence_map["claims"])
        )

    def test_case03_conflicting_evidence_map(self) -> None:
        _, findings, evidence_map = self.run_case("03-ratio-conflict")

        self.assertEqual(findings["summary"]["high"], 1)
        self.assertTrue(all(item["evidence_refs"] for item in findings["findings"]))
        self.assertIn("conflicting", {claim["support_status"] for claim in evidence_map["claims"]})

    def test_case05_outputs_human_review_context(self) -> None:
        _, findings, evidence_map = self.run_case("05-detail-overclaim")

        self.assertEqual(findings["findings"][0]["rule_id"], "R-005")
        self.assertIn("Confirm", findings["findings"][0]["human_action"])
        self.assertTrue(any("human review" in claim["review_reason"].lower() for claim in evidence_map["claims"]))

    def test_case06_variant_scope_conflict_is_mapped(self) -> None:
        _, findings, evidence_map = self.run_case("06-variant-scope-gap")

        rule_ids = {finding["rule_id"] for finding in findings["findings"]}
        self.assertIn("R-006", rule_ids)
        variant_claims = [
            claim for claim in evidence_map["claims"] if claim["claim_id"] == "variant-scope"
        ]
        self.assertEqual(variant_claims[0]["support_status"], "conflicting")


if __name__ == "__main__":
    unittest.main()
