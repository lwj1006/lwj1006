from __future__ import annotations

import unittest
from unittest.mock import patch

from fenjue.modes.photoset_template.descriptions import (
    TEMPLATE_THEME_DEFINITIONS,
    template_ids_for_theme,
)
from fenjue.modes.photoset_template.library import list_template_ids
from fenjue.modes.photoset_template.mode import _split_template_selection


class PhotosetThemeSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.available = list_template_ids()

    def test_numeric_and_range_selection_are_unchanged(self) -> None:
        self.assertEqual(
            _split_template_selection("2,3,5-7", self.available),
            ["002_A_3", "003_A_3", "005_A_3", "006_A_3", "007_A_3"],
        )

    def test_theme_selection_shuffles_only_that_theme(self) -> None:
        expected = template_ids_for_theme("A", self.available)
        with patch(
            "fenjue.modes.photoset_template.mode.random.shuffle",
            side_effect=lambda values: values.reverse(),
        ):
            selected = _split_template_selection("A", self.available)

        self.assertEqual(selected, list(reversed(expected)))
        self.assertIn("009_A_3", selected)
        self.assertIn("182_A_3", selected)
        self.assertNotIn("300_A_3", selected)

    def test_overlapping_theme_pools_do_not_duplicate_templates(self) -> None:
        with patch("fenjue.modes.photoset_template.mode.random.shuffle"):
            selected = _split_template_selection("A,H,182,180-184", self.available)

        self.assertEqual(len(selected), len(set(selected)))
        self.assertEqual(selected.count("182_A_3"), 1)

    def test_deleted_templates_never_reenter_through_a_theme(self) -> None:
        for code in TEMPLATE_THEME_DEFINITIONS:
            selected = template_ids_for_theme(code, self.available)
            self.assertNotIn("023_A_3", selected)
            self.assertNotIn("024_A_3", selected)
            self.assertNotIn("043_A_3", selected)
            self.assertNotIn("046_A_3", selected)
            self.assertNotIn("207_A_3", selected)

    def test_every_theme_has_a_useful_pool(self) -> None:
        for code, (label, _keywords) in TEMPLATE_THEME_DEFINITIONS.items():
            with self.subTest(code=code, label=label):
                self.assertGreaterEqual(
                    len(template_ids_for_theme(code, self.available)),
                    5,
                )

    def test_every_available_template_is_classified(self) -> None:
        classified = {
            template_id
            for code in TEMPLATE_THEME_DEFINITIONS
            for template_id in template_ids_for_theme(code, self.available)
        }
        self.assertEqual(set(self.available) - classified, set())


if __name__ == "__main__":
    unittest.main()
