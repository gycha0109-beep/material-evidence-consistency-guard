from __future__ import annotations

import sys
import unittest
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SRC_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from normalize_inputs import material_match, normalize_material, normalize_percentage  # noqa: E402


class TaxonomyTest(unittest.TestCase):
    def test_clear_alias_maps_to_canonical_material(self) -> None:
        self.assertEqual(
            normalize_material("\uc624\ub9ac \uc19c\ud138"),
            {"status": "canonical", "value": "duck_down_cluster"},
        )
        self.assertEqual(
            normalize_material("\uc624\ub9ac\uae43\ud138"),
            {"status": "canonical", "value": "duck_feather"},
        )
        self.assertEqual(
            normalize_material("\uc624\ub9ac \uae43\ud138"),
            {"status": "canonical", "value": "duck_feather"},
        )
        self.assertEqual(
            normalize_material("\uce90\uc2dc\ubbf8\uc5b4"),
            {"status": "canonical", "value": "cashmere"},
        )

    def test_ambiguous_alias_stays_ambiguous(self) -> None:
        self.assertEqual(
            normalize_material("down"),
            {"status": "ambiguous", "value": "down"},
        )
        self.assertEqual(
            normalize_material("\uae43\ud138"),
            {"status": "ambiguous", "value": "\uae43\ud138"},
        )

    def test_percentage_parsing(self) -> None:
        self.assertEqual(normalize_percentage("80%"), 80.0)
        self.assertEqual(normalize_percentage(80), 80.0)
        self.assertEqual(normalize_percentage("80.0"), 80.0)

    def test_same_material_matches(self) -> None:
        result = material_match("\uc624\ub9ac \uc19c\ud138", "duck_down_cluster")

        self.assertEqual(result["status"], "compared")
        self.assertTrue(result["matched"])

    def test_different_material_mismatches(self) -> None:
        result = material_match("\uc624\ub9ac \uc19c\ud138", "goose_down_cluster")

        self.assertEqual(result["status"], "compared")
        self.assertFalse(result["matched"])

    def test_ambiguous_material_is_not_mismatch(self) -> None:
        result = material_match("down", "duck_down_cluster")

        self.assertEqual(result["status"], "ambiguous")
        self.assertIsNone(result["matched"])


if __name__ == "__main__":
    unittest.main()
