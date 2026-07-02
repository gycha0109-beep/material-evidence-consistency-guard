from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SRC_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from build_normalized_model import build_normalized_model  # noqa: E402


CASE01_DIR = SRC_ROOT / "fixtures" / "cases" / "01-pass-consistent"


class NormalizerTest(unittest.TestCase):
    def test_case01_normalizes_core_values(self) -> None:
        model = build_normalized_model(CASE01_DIR)

        self.assertEqual(model["product"]["product_id"], "MUS-OUTER-00031")
        self.assertEqual(model["product"]["internal_sku"], "NW-DP-2026-01")
        self.assertEqual(len(model["variants"]), 2)
        self.assertEqual(
            [variant["option_name"] for variant in model["variants"]],
            ["블랙 / M", "블랙 / L"],
        )

        fill_materials = model["variants"][0]["material_components"][1]["materials"]
        self.assertEqual(fill_materials[0]["normalized_material"]["value"], "duck_down_cluster")
        self.assertEqual(fill_materials[0]["percentage"], 80.0)
        self.assertEqual(fill_materials[1]["normalized_material"]["value"], "duck_feather")
        self.assertEqual(fill_materials[1]["percentage"], 20.0)

        evidence = model["evidence_document"]
        self.assertEqual(evidence["document_status"], "parsed")
        self.assertEqual(evidence["tested_product"]["identifier"], "NW-DP-2026-01")
        self.assertEqual(evidence["tested_product"]["variant_scope"], "BLACK_ALL_SIZES")
        self.assertEqual(evidence["tested_materials"][1]["percentage"], 80.0)

    def test_unknown_and_ambiguous_status_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = Path(temp_dir) / "case"
            shutil.copytree(CASE01_DIR, case_dir)
            detail_page = case_dir / "detail-page.md"
            detail_page.write_text(
                detail_page.read_text(encoding="utf-8")
                + "\n- ambiguous fixture line: down 5%\n",
                encoding="utf-8",
            )

            model = build_normalized_model(case_dir)

            statuses = {item["status"] for item in model["uncertainties"]}
            self.assertIn("unknown", statuses)
            self.assertIn("ambiguous", statuses)
            ambiguous = [
                item
                for item in model["uncertainties"]
                if item["status"] == "ambiguous"
            ]
            self.assertTrue(any("detail_claims" in item["field"] for item in ambiguous))

    def test_run_guard_writes_normalized_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "run_guard.py"),
                    str(CASE01_DIR),
                    "--out",
                    str(output_dir),
                ],
                cwd=SRC_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            normalized_path = output_dir / "normalized.json"
            self.assertTrue(normalized_path.is_file())
            normalized = json.loads(normalized_path.read_text(encoding="utf-8"))
            self.assertEqual(normalized["product"]["product_id"], "MUS-OUTER-00031")


if __name__ == "__main__":
    unittest.main()
