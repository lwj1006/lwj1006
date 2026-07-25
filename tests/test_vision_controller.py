from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from fenjue.vision.contracts import ComposerLayout, Rect, ScreenState
from fenjue.vision.controller import VisionAutomationController


def active_state(*, attachments: int = 0) -> ScreenState:
    boxes = tuple(Rect(110 + index * 50, 700, 45, 45) for index in range(attachments))
    return ScreenState(
        screen_width=1920,
        screen_height=1080,
        layout=ComposerLayout.ACTIVE_CHAT_BOTTOM,
        composer=Rect(700, 820, 560, 170 if attachments else 70),
        plus_button=Rect(710, 840, 30, 30),
        input_box=Rect(750, 830, 420, 50),
        action_button=Rect(1210, 840, 34, 34),
        model_selector=Rect(1110, 840, 60, 34),
        model_menu=Rect(1060, 650, 160, 180),
        model_high_row=Rect(1068, 730, 144, 42),
        attachment_boxes=boxes,
        attachment_count=attachments,
        action_kind="send",
        confidence=0.95,
    )


class FakeBatch:
    POST_CHARACTER_SELECTION_DELAY_SECONDS = 3
    STARTUP_REFRESH_SETTLE_SECONDS = 20
    TEXT_BEFORE_SEND_SECONDS = 20
    CHECK_INTERVAL_SECONDS = 400

    def __init__(self) -> None:
        self.clicks: list[tuple[int, int, float]] = []
        self.pastes: list[str] = []
        self.waits: list[tuple[int, str]] = []
        self.refreshes: list[tuple[str, int, str]] = []
        self.recorded_uploads: list[int] = []
        self.screenshots: list[str] = []

    def debug_log(self, _message: str) -> None:
        pass

    def info_log(self, _message: str) -> None:
        pass

    def click_slow(self, x: int, y: int, after: float = 1.0) -> None:
        self.clicks.append((x, y, after))

    def paste_text(self, text: str) -> None:
        self.pastes.append(text)

    def wait_with_echo(self, seconds: int, label: str, **_kwargs) -> None:
        self.waits.append((seconds, label))

    def refresh_chatgpt_web_page(self, reason: str, seconds: int, label: str) -> None:
        self.refreshes.append((reason, seconds, label))

    @staticmethod
    def prepare_upload_files(reference_files: list[str]) -> list[str]:
        return reference_files[:]

    @staticmethod
    def apply_upload_cooldown_if_needed(_count: int) -> None:
        pass

    @staticmethod
    def upload_settle_seconds(_count: int) -> int:
        return 15

    def record_uploaded_image_count(self, count: int) -> None:
        self.recorded_uploads.append(count)

    def take_screenshot(self, label: str) -> Path:
        self.screenshots.append(label)
        return Path(f"{label}.png")


class FakeInspector:
    def __init__(self) -> None:
        self.last_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        self.attachments_ready = 0
        self.wait_labels: list[str] = []
        self.focus_calls = 0

    def focus_chatgpt_window(self) -> tuple[str, str, str]:
        self.focus_calls += 1
        return ("Chrome_WidgetWin_1", "ChatGPT", "msedge.exe")

    def inspect(self) -> ScreenState:
        return active_state(attachments=self.attachments_ready)

    def wait_for(self, predicate, *, label: str, **_kwargs) -> ScreenState:
        self.wait_labels.append(label)
        if label == "composer (any layout)" and self.focus_calls == 0:
            raise AssertionError("Composer inspection started before the browser was focused.")
        if label == "attachment menu for create image":
            state = active_state()
            state = ScreenState(**{**state.__dict__, "create_image_row": Rect(700, 610, 300, 40)})
        elif label == "image model menu opening":
            self.last_frame.fill(255)
            state = ScreenState(screen_width=1920, screen_height=1080)
        elif label == "attachment menu for batch upload":
            state = active_state()
            state = ScreenState(**{**state.__dict__, "add_file_row": Rect(700, 560, 300, 40)})
        elif label == "Windows file-name input":
            state = active_state()
            state = ScreenState(**{**state.__dict__, "file_name_input": Rect(500, 800, 600, 30)})
        elif label.startswith("all "):
            self.attachments_ready = int(label.split()[1])
            state = active_state(attachments=self.attachments_ready)
        else:
            state = active_state(attachments=self.attachments_ready)
        if not predicate(state):
            raise AssertionError(f"Fake state did not satisfy wait label: {label}")
        return state

    @staticmethod
    def frame_change_ratio(_before, _after) -> float:
        return 1.0

    @staticmethod
    def region_fingerprint(_frame, _rect) -> int:
        return 123

    @staticmethod
    def fingerprint_distance(left: int, right: int) -> int:
        return abs(left - right)

    @staticmethod
    def save_diagnostic(label: str) -> str:
        return f"{label}.png"


class VisionControllerTests(unittest.TestCase):
    def test_startup_uses_legacy_refresh_cadence(self) -> None:
        batch = FakeBatch()
        inspector = FakeInspector()
        controller = VisionAutomationController(batch, inspector)

        with patch("fenjue.vision.controller.time.sleep") as sleep:
            controller.prepare_session()

        sleep.assert_any_call(3)
        self.assertEqual(
            batch.refreshes,
            [("Vision startup refresh", 20, "Vision startup refresh settle")],
        )
        self.assertEqual(inspector.focus_calls, 1)
        self.assertEqual(batch.clicks, [])

    def test_upload_selects_all_files_in_one_dialog(self) -> None:
        batch = FakeBatch()
        inspector = FakeInspector()
        controller = VisionAutomationController(batch, inspector)
        files = [r"C:\refs\a.png", r"C:\refs\b.jpg", r"C:\refs\c.jpeg"]

        with (
            patch("fenjue.vision.controller.time.sleep"),
            patch("fenjue.vision.controller.pyautogui.hotkey") as hotkey,
            patch("fenjue.vision.controller.pyautogui.press") as press,
        ):
            uploaded = controller._upload_reference_images_cycle(files)

        self.assertEqual(uploaded, files)
        self.assertEqual(batch.pastes, ['"C:\\refs\\a.png" "C:\\refs\\b.jpg" "C:\\refs\\c.jpeg"'])
        self.assertEqual(press.call_count, 2)
        press.assert_any_call("enter")
        self.assertEqual(hotkey.call_count, 2)
        self.assertEqual(batch.waits, [(15, "Vision upload settle")])
        self.assertEqual(batch.recorded_uploads, [3])
        self.assertIn("all 3 reference attachments", inspector.wait_labels)
        self.assertEqual(
            inspector.wait_labels.count("attachment menu for batch upload"),
            1,
        )
        self.assertNotIn("attachment menu for create image", inspector.wait_labels)
        self.assertEqual(inspector.wait_labels.count("Windows file-name input"), 1)
        self.assertTrue(
            any(
                x == 1140 and y == 751
                for x, y, _after in batch.clicks
            )
        )

    def test_upload_recovery_refreshes_without_clicking_attachment_cards(self) -> None:
        batch = FakeBatch()
        inspector = FakeInspector()
        inspector.attachments_ready = 2
        controller = VisionAutomationController(batch, inspector)
        controller.draft_attachments_pending = True
        controller.expected_attachment_count = 2

        with (
            patch("fenjue.vision.controller.time.sleep"),
            patch("fenjue.vision.controller.pyautogui.press"),
        ):
            controller._recover_failed_upload_cycle()

        self.assertFalse(hasattr(controller, "_clear_visible_attachments"))
        self.assertIn(
            (
                "Vision upload recovery refresh",
                20,
                "Vision upload recovery refresh settle",
            ),
            batch.refreshes,
        )
        self.assertFalse(controller.draft_attachments_pending)
        self.assertEqual(controller.expected_attachment_count, 0)

    def test_generation_never_finishes_before_legacy_wait(self) -> None:
        batch = FakeBatch()
        inspector = FakeInspector()
        controller = VisionAutomationController(batch, inspector)

        with patch("fenjue.vision.controller.time.sleep"):
            screenshot = controller.wait_for_generation(7)

        self.assertEqual(batch.waits, [(400, "[07] vision generation baseline")])
        self.assertEqual(screenshot, Path("run_07_vision_complete.png"))
        self.assertEqual(batch.screenshots, ["run_07_vision_complete"])


if __name__ == "__main__":
    unittest.main()
