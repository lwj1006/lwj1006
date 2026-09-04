from __future__ import annotations

import unittest
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fenjue.modes.photoset_template.mode import (
    _build_assigned_photoset_schedule,
    _load_used_shots,
    _mark_shot_used,
    _resolve_template_assignments,
    _select_random_unused_shots,
    _scheduled_template_starts,
    activate,
)


class PhotosetHistoryTests(unittest.TestCase):
    def test_random_shots_do_not_repeat_until_the_template_cycle_finishes(self) -> None:
        shots = tuple(SimpleNamespace(index=index) for index in range(1, 5))
        template = SimpleNamespace(template_id="900_A_3", shots=shots)
        history = {"900_A_3": [1, 2]}

        with (
            patch("fenjue.modes.photoset_template.mode.random.sample", side_effect=lambda pool, count: pool[:count]),
            patch("fenjue.modes.photoset_template.mode._save_used_shots"),
        ):
            remaining = _select_random_unused_shots(template, 4, history)
            self.assertEqual([shot.index for shot in remaining], [3, 4])
            _mark_shot_used(template, remaining[0], history)
            _mark_shot_used(template, remaining[1], history)
            next_cycle = _select_random_unused_shots(template, 2, history)

        self.assertEqual([shot.index for shot in next_cycle], [1, 2])
        self.assertEqual(history["900_A_3"], [])

    def test_shot_history_is_global_across_characters(self) -> None:
        shots = tuple(SimpleNamespace(index=index) for index in range(1, 4))
        template = SimpleNamespace(template_id="901_A_3", shots=shots)
        history = {"901_A_3": [1]}

        with patch("fenjue.modes.photoset_template.mode.random.sample", side_effect=lambda pool, count: pool[:count]):
            selected_for_another_character = _select_random_unused_shots(template, 2, history)

        self.assertEqual([shot.index for shot in selected_for_another_character], [2, 3])

    def test_numeric_count_equal_to_template_size_still_honors_history(self) -> None:
        shots = tuple(SimpleNamespace(index=index) for index in range(1, 4))
        template = SimpleNamespace(template_id="904_A_3", shots=shots)
        history = {"904_A_3": [1]}

        with patch("fenjue.modes.photoset_template.mode.random.sample", side_effect=lambda pool, count: pool[:count]):
            schedule = _build_assigned_photoset_schedule(
                (("千夏", template),),
                shots_per_template=3,
                used_shots_by_template=history,
            )

        self.assertEqual([shot.index for _, _, shot in schedule], [2, 3])

    def test_loading_one_template_preserves_other_template_history(self) -> None:
        template = SimpleNamespace(
            template_id="902_A_3",
            shots=(SimpleNamespace(index=1), SimpleNamespace(index=2)),
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            history_file = Path(temporary_directory) / "used_photoset_shots.json"
            history_file.write_text(
                json.dumps({"902_A_3": [1, 99], "903_A_3": [2]}, ensure_ascii=False),
                encoding="utf-8",
            )
            with patch("fenjue.modes.photoset_template.mode.USED_SHOT_FILE", history_file):
                history = _load_used_shots((template,))
                _mark_shot_used(template, template.shots[1], history)
                saved = json.loads(history_file.read_text(encoding="utf-8"))

        self.assertEqual(saved, {"902_A_3": [1, 2], "903_A_3": [2]})

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
            patch(
                "fenjue.modes.photoset_template.mode._load_used_shots",
                return_value={},
            ),
            patch("fenjue.modes.photoset_template.mode._mark_template_used") as mark_used,
            patch("fenjue.modes.photoset_template.mode._mark_shot_used") as mark_shot,
        ):
            activate(batch)
            batch.record_completed_run("千夏", 1)
            batch.record_completed_run("千夏", 2)
            batch.record_completed_run("爱芮", 3)
            batch.record_completed_run("爱芮", 4)

        self.assertEqual(mark_used.call_count, 2)
        self.assertEqual(mark_shot.call_count, 4)
        self.assertEqual(mark_used.call_args_list[0].args[:2], ("千夏", template_a))
        self.assertEqual(mark_used.call_args_list[1].args[:2], ("爱芮", template_b))


if __name__ == "__main__":
    unittest.main()
