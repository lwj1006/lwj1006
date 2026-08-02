from __future__ import annotations

import datetime as dt
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fenjue.modes.photoset_template.mode import activate
from fenjue.modes.photoset_template.session import (
    PhotosetSessionError,
    advance_session,
    load_session,
    mark_resume_started,
    resumable_mode,
    resume_requested,
    save_new_session,
)


class PhotosetResumeSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.session_path = Path(self.temporary_directory.name) / "photoset_resume_session.json"
        self.schedule = [
            {"character": "仪玄", "template_id": "429_A_3", "shot_index": 1},
            {"character": "仪玄", "template_id": "429_A_3", "shot_index": 2},
            {"character": "星见雅", "template_id": "430_A_3", "shot_index": 3},
            {"character": "星见雅", "template_id": "430_A_3", "shot_index": 4},
        ]

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_bare_l_requests_resume(self) -> None:
        self.assertTrue(resume_requested(["L", "--vision"]))
        self.assertTrue(resume_requested(["--resume-session"]))
        self.assertFalse(resume_requested(["E", "--vision"]))

    def test_new_session_preserves_exact_expanded_queue(self) -> None:
        start = dt.datetime(2026, 8, 2, 11, 25)
        save_new_session("E", self.schedule, start, self.session_path)

        state = load_session(self.session_path)

        self.assertEqual(state["mode"], "E")
        self.assertEqual(state["next_index"], 0)
        self.assertEqual(state["scheduled_start"], "2026-08-02T11:25")
        self.assertEqual(state["schedule"], self.schedule)

    def test_progress_points_to_first_unfinished_image(self) -> None:
        save_new_session("E2", self.schedule, None, self.session_path)
        advance_session(3, self.session_path)

        state = load_session(self.session_path)

        self.assertEqual(resumable_mode(self.session_path), "E2")
        self.assertEqual(state["next_index"], 3)
        self.assertEqual(state["schedule"][state["next_index"]], self.schedule[3])

    def test_progress_never_moves_backwards_after_retry(self) -> None:
        save_new_session("E", self.schedule, None, self.session_path)
        advance_session(3, self.session_path)
        advance_session(2, self.session_path)

        self.assertEqual(load_session(self.session_path)["next_index"], 3)

    def test_resuming_does_not_reset_progress(self) -> None:
        save_new_session("E", self.schedule, None, self.session_path)
        advance_session(2, self.session_path)
        mark_resume_started(dt.datetime(2026, 8, 3, 9, 10), self.session_path)

        state = load_session(self.session_path)

        self.assertEqual(state["next_index"], 2)
        self.assertEqual(state["scheduled_start"], "2026-08-03T09:10")

    def test_completed_session_is_not_resumable(self) -> None:
        save_new_session("E", self.schedule, None, self.session_path)
        advance_session(len(self.schedule), self.session_path)

        with self.assertRaises(PhotosetSessionError):
            resumable_mode(self.session_path)

    def test_new_selection_does_not_overwrite_until_start_is_confirmed(self) -> None:
        shot = SimpleNamespace(index=1)
        template = SimpleNamespace(template_id="429_A_3", shots=(shot,))
        batch = SimpleNamespace(
            ACTIVE_PROMPT_MODE="E",
            reference_files_for_character=lambda _character: [],
        )

        with (
            patch("fenjue.modes.photoset_template.mode._choose_templates", return_value=(template,)),
            patch("fenjue.modes.photoset_template.mode._choose_characters", return_value=("仪玄",)),
            patch("fenjue.modes.photoset_template.mode._choose_shots_per_template", return_value=None),
            patch("fenjue.modes.photoset_template.mode.list_template_ids", return_value=["429_A_3"]),
            patch("fenjue.modes.photoset_template.mode._load_used_templates", return_value={}),
            patch("fenjue.modes.photoset_template.mode.save_new_session", return_value=self.session_path) as save,
        ):
            activate(batch, args=["E"])
            save.assert_not_called()
            batch.confirm_run_session(None)

        save.assert_called_once()
        self.assertEqual(save.call_args.args[0], "E")
        self.assertEqual(save.call_args.args[1][0]["shot_index"], 1)

    def test_resume_activation_uses_saved_queue_without_reopening_choices(self) -> None:
        shot_429_1 = SimpleNamespace(index=1)
        shot_429_2 = SimpleNamespace(index=2)
        shot_430_3 = SimpleNamespace(index=3)
        shot_430_4 = SimpleNamespace(index=4)
        template_429 = SimpleNamespace(template_id="429_A_3", shots=(shot_429_1, shot_429_2))
        template_430 = SimpleNamespace(template_id="430_A_3", shots=(shot_430_3, shot_430_4))
        restored_schedule = (
            ("仪玄", template_429, shot_429_1),
            ("仪玄", template_429, shot_429_2),
            ("星见雅", template_430, shot_430_3),
            ("星见雅", template_430, shot_430_4),
        )
        state = {
            "mode": "E",
            "next_index": 3,
            "schedule": self.schedule,
        }
        batch = SimpleNamespace(
            ACTIVE_PROMPT_MODE="E",
            reference_files_for_character=lambda _character: [],
        )

        with (
            patch("fenjue.modes.photoset_template.mode.list_template_ids", return_value=["429_A_3", "430_A_3"]),
            patch("fenjue.modes.photoset_template.mode._load_used_templates", return_value={}),
            patch("fenjue.modes.photoset_template.mode.load_session", return_value=state),
            patch("fenjue.modes.photoset_template.mode._restore_saved_schedule", return_value=restored_schedule),
            patch("fenjue.modes.photoset_template.mode._choose_templates") as choose_templates,
            patch("fenjue.modes.photoset_template.mode.mark_resume_started", return_value=self.session_path) as resume_start,
            patch("fenjue.modes.photoset_template.mode.advance_session", return_value=self.session_path) as advance,
        ):
            activate(batch, args=["L", "--vision"])
            choose_templates.assert_not_called()
            self.assertEqual(batch.TOTAL_RUNS, 1)
            self.assertEqual(batch.resolve_run_character("ignored", 1), "星见雅")
            resume_start.assert_not_called()
            batch.confirm_run_session(None)
            batch.record_run_session_progress(1)

        resume_start.assert_called_once_with(None)
        advance.assert_called_once_with(4)


if __name__ == "__main__":
    unittest.main()
