from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]


class FixtureSuiteTest(unittest.TestCase):
    def test_fixture_suite_matches_expected_findings(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/run_fixture_suite.py"],
            cwd=SRC_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("fixture suite: 8 case(s) passed", completed.stdout)


if __name__ == "__main__":
    unittest.main()
