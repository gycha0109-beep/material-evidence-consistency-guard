from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SRC_ROOT / "scripts" / "run_guard.py"
FIXTURE_DIR = SRC_ROOT / "fixtures" / "cases" / "01-pass-consistent"


class CliContractTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=SRC_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_success_creates_run_meta(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"

            result = self.run_cli(str(FIXTURE_DIR), "--out", str(output_dir))

            self.assertEqual(result.returncode, 0, result.stderr)
            run_meta_path = output_dir / "run-meta.json"
            self.assertTrue(run_meta_path.is_file())

            run_meta = json.loads(run_meta_path.read_text(encoding="utf-8"))
            self.assertEqual(run_meta["input_dir"], str(FIXTURE_DIR))
            self.assertEqual(run_meta["output_dir"], str(output_dir))
            self.assertEqual(run_meta["status"], "initialized")
            self.assertEqual(run_meta["tool_version"], "0.1.0")
            self.assertIn("generated_at", run_meta)

    def test_missing_input_directory_fails_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_input = Path(temp_dir) / "missing"
            output_dir = Path(temp_dir) / "out"

            result = self.run_cli(str(missing_input), "--out", str(output_dir))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("input directory does not exist", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse(output_dir.exists())

    def test_existing_output_directory_without_overwrite_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            output_dir.mkdir()

            result = self.run_cli(str(FIXTURE_DIR), "--out", str(output_dir))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output directory already exists", result.stderr)
            self.assertIn("--overwrite", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse((output_dir / "run-meta.json").exists())

    def test_existing_output_directory_with_overwrite_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            output_dir.mkdir()

            result = self.run_cli(
                str(FIXTURE_DIR),
                "--out",
                str(output_dir),
                "--overwrite",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_dir / "run-meta.json").is_file())

    def test_help_succeeds(self) -> None:
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage:", result.stdout)
        self.assertIn("--overwrite", result.stdout)


if __name__ == "__main__":
    unittest.main()
