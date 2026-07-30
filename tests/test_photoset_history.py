from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fenjue.modes.photoset_template.mode import (
    _resolve_template_assignments,
    _scheduled_template_starts,
    activate,
)


class PhotosetHistoryTests(unittest.TestCase):
    def test_only_first_scheduled_shot_marks_template_used(self) -> None:
        template_a = object()
        template_b = object()
        schedule = (
            ("千夏", template_a, object()),
            ("千夏", template_a, object()),
            ("千夏", template_a, object()),
            ("爱芮", template_b, object()),
            ("爱芮", template_b, object()),
        )

        self.assertTrue(_scheduled_template_starts(schedule, 0))
        self.assertFalse(_scheduled_template_starts(schedule, 1))
        self.assertFalse(_scheduled_template_starts(schedule, 2))
        self.assertTrue(_scheduled_template_starts(schedule, 3))
        self.assertFalse(_scheduled_template_starts(schedule, 4))

    def test_same_template_starts_again_for_a_different_character(self) -> None:
        template = object()
        schedule = (
            ("千夏", template, object()),
            ("千夏", template, object()),
            ("爱芮", template, object()),
        )

        self.assertTrue(_scheduled_template_starts(schedule, 0))
        self.assertFalse(_scheduled_template_starts(schedule, 1))
        self.assertTrue(_scheduled_template_starts(schedule, 2))

    def test_invalid_schedule_index_is_not_a_start(self) -> None:
        schedule = (("千夏", object(), object()),)

        self.assertFalse(_scheduled_template_starts(schedule, -1))
        self.assertFalse(_scheduled_template_starts(schedule, 1))

    def test_range_and_global_random_share_the_same_character_history(self) -> None:
        template_122 = SimpleNamespace(template_id="122_A_3")
        template_123 = SimpleNamespace(template_id="123_A_3")
        history = {"千夏": ["122_A_3"]}

        assignments = _resolve_template_assignments(
            (template_122, template_123),
            ("千夏",),
            history,
            ["122_A_3", "123_A_3", "300_A_3"],
        )

        self.assertEqual(assignments, (("千夏", template_123),))
        self.assertEqual(history["千夏"], ["122_A_3"])

    def test_exhausted_range_does_not_reset_global_history(self) -> None:
        template_122 = SimpleNamespace(template_id="122_A_3")
        history = {"千夏": ["122_A_3"]}

        assignments = _resolve_template_assignments(
            (template_122,),
            ("千夏",),
            history,
            ["122_A_3", "300_A_3"],
        )

        self.assertEqual(assignments, ())
        self.assertEqual(history["千夏"], ["122_A_3"])

    def test_runtime_records_each_template_after_its_first_successful_image(self) -> None:
        template_a = SimpleNamespace(template_id="002_A_3", shots=(object(), object()))
        template_b = SimpleNamespace(template_id="003_A_3", shots=(object(), object()))
        batch = SimpleNamespace(reference_files_for_character=lambda _character: [])

        with (
            patch(
                "fenjue.modes.photoset_template.mode._choose_templates",
                return_value=(template_a, template_b),
            ),
            patch(
                "fenjue.modes.photoset_template.mode._choose_characters",
                return_value=("千夏", "爱芮"),
            ),
            patch(
                "fenjue.modes.photoset_template.mode._choose_shots_per_template",
                return_value=None,
            ),
            patch(
                "fenjue.modes.photoset_template.mode.list_template_ids",
                return_value=["002_A_3", "003_A_3"],
            ),
            patch(
                "fenjue.modes.photoset_template.mode._load_used_templates",
                return_value={},
            ),
            patch("fenjue.modes.photoset_template.mode._mark_template_used") as mark_used,
        ):
            activate(batch)
            batch.record_completed_run("千夏", 1)
            batch.record_completed_run("千夏", 2)
            batch.record_completed_run("爱芮", 3)
            batch.record_completed_run("爱芮", 4)

        self.assertEqual(mark_used.call_count, 2)
        self.assertEqual(mark_used.call_args_list[0].args[:2], ("千夏", template_a))
        self.assertEqual(mark_used.call_args_list[1].args[:2], ("爱芮", template_b))


if __name__ == "__main__":
    unittest.main()
