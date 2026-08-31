from __future__ import annotations

import datetime as dt
import unittest
from pathlib import Path
from unittest.mock import patch

from fenjue.runtime import target_batch
from fenjue.runtime import batch
from fenjue.runtime.target_batch_prompts import PROMPT_SETS
from fenjue.vision.generation_limit import GenerationLimitDetection, GenerationLimitReached


class TargetBatchTests(unittest.TestCase):
    def test_prompt_selection_accepts_one_combination_range_and_all(self) -> None:
        self.assertEqual(target_batch.parse_prompt_selection("2"), (2,))
        self.assertEqual(target_batch.parse_prompt_selection("1,3,4"), (1, 3, 4))
        self.assertEqual(target_batch.parse_prompt_selection("1-3"), (1, 2, 3))
        self.assertEqual(target_batch.parse_prompt_selection("all"), (1, 2, 3, 4))

    def test_prompt_selection_rejects_out_of_range_values(self) -> None:
        with self.assertRaises(ValueError):
            target_batch.parse_prompt_selection("5")

    def test_same_image_runs_every_selected_prompt_before_move(self) -> None:
        source = Path("target/example.png")
        events: list[object] = []

        with (
            patch.object(target_batch, "upload_target_file", side_effect=lambda path: events.append(("upload", path))),
            patch.object(target_batch, "send_prompt", side_effect=lambda prompt: events.append(("send", prompt))),
            patch.object(target_batch, "take_screenshot", side_effect=lambda name: events.append(("shot", name))),
            patch.object(target_batch, "wait_for_generation", side_effect=lambda number: events.append(("wait", number))),
            patch.object(target_batch, "move_to_complete", side_effect=lambda path: events.append(("move", path)) or Path("complete/example.png")),
            patch.object(target_batch, "with_image_prompt_prefix", side_effect=lambda prompt: prompt),
        ):
            final_generation = target_batch.process_target_file(source, 1, (1, 3), 0)

        self.assertEqual(final_generation, 2)
        self.assertEqual([item for item in events if item[0] == "upload"], [("upload", source), ("upload", source)])
        self.assertEqual([item[1] for item in events if item[0] == "send"], [PROMPT_SETS[0], PROMPT_SETS[2]])
        self.assertEqual([item for item in events if item[0] == "wait"], [("wait", 1), ("wait", 2)])
        self.assertEqual(events[-1], ("move", source))

    def test_startup_refresh_never_clicks_the_send_button_coordinate(self) -> None:
        with (
            patch.object(batch.time, "sleep"),
            patch.object(batch, "focus_chatgpt_input") as focus_mock,
            patch.object(batch, "click_slow") as click_mock,
            patch.object(batch, "refresh_chatgpt_web_page") as refresh_mock,
        ):
            batch.startup_refresh_before_button_work()

        focus_mock.assert_called_once_with()
        click_mock.assert_not_called()
        refresh_mock.assert_called_once()

    def test_generation_limit_retries_only_current_prompt_before_move(self) -> None:
        source = Path("target/example.png")
        limit = GenerationLimitReached(
            GenerationLimitDetection(
                text="generation limit",
                delay_seconds=60,
                resume_at=dt.datetime.now() + dt.timedelta(minutes=1),
                source="test",
                screenshot_path=Path("limit.png"),
            )
        )
        events: list[object] = []

        with (
            patch.object(target_batch, "upload_target_file", side_effect=lambda path: events.append(("upload", path))),
            patch.object(target_batch, "send_prompt", side_effect=lambda prompt: events.append(("send", prompt))),
            patch.object(target_batch, "take_screenshot"),
            patch.object(target_batch, "wait_for_generation", side_effect=[limit, Path("done.png")]),
            patch.object(target_batch, "recover_after_generation_limit", side_effect=lambda error: events.append(("recover", error))),
            patch.object(target_batch, "move_to_complete", side_effect=lambda path: events.append(("move", path)) or Path("complete/example.png")),
            patch.object(target_batch, "with_image_prompt_prefix", side_effect=lambda prompt: prompt),
        ):
            final_generation = target_batch.process_target_file(source, 1, (2,), 0)

        self.assertEqual(final_generation, 1)
        self.assertEqual([item for item in events if item[0] == "upload"], [("upload", source), ("upload", source)])
        self.assertEqual([item[1] for item in events if item[0] == "send"], [PROMPT_SETS[1], PROMPT_SETS[1]])
        self.assertEqual(events[-1], ("move", source))


if __name__ == "__main__":
    unittest.main()
