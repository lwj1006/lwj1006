from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from unittest.mock import patch

from fenjue.vision.contracts import ComposerLayout, Rect
from fenjue.vision.opencv_inspector import OpenCVScreenInspector


def synthetic_chatgpt_frame(theme: str) -> np.ndarray:
    if theme == "light":
        page, composer, border, ink, action = 255, 250, 220, 35, 10
    else:
        page, composer, border, ink, action = 0, 33, 58, 235, 248

    frame = np.full((1080, 1920, 3), page, dtype=np.uint8)
    left, top, right, bottom = 500, 900, 1200, 970
    cv2.rectangle(frame, (left, top), (right, bottom), (composer,) * 3, -1)
    cv2.rectangle(frame, (left, top), (right, bottom), (border,) * 3, 2)

    plus_x, plus_y = 522, 935
    cv2.line(frame, (plus_x - 9, plus_y), (plus_x + 9, plus_y), (ink,) * 3, 3)
    cv2.line(frame, (plus_x, plus_y - 9), (plus_x, plus_y + 9), (ink,) * 3, 3)

    action_x, action_y = 1170, 935
    cv2.circle(frame, (action_x, action_y), 19, (action,) * 3, -1)
    arrow_ink = 250 if action < 128 else 10
    points = np.array(
        [[action_x, action_y - 9], [action_x - 8, action_y + 4], [action_x + 8, action_y + 4]],
        dtype=np.int32,
    )
    cv2.fillConvexPoly(frame, points, (arrow_ink,) * 3)
    return frame


def synthetic_narrow_centered_frame() -> np.ndarray:
    frame = np.full((758, 782, 3), 255, dtype=np.uint8)
    left, top, right, bottom = 95, 316, 738, 438
    cv2.rectangle(frame, (left, top), (right, bottom), (250, 250, 250), -1)
    cv2.rectangle(frame, (left, top), (right, bottom), (220, 220, 220), 2)
    cv2.line(frame, (114, 414), (132, 414), (35, 35, 35), 3)
    cv2.line(frame, (123, 405), (123, 423), (35, 35, 35), 3)
    cv2.circle(frame, (710, 414), 19, (10, 10, 10), -1)
    return frame


def synthetic_fullscreen_active_frame() -> np.ndarray:
    frame = np.full((768, 1024, 3), 255, dtype=np.uint8)
    left, top, right, bottom = 217, 638, 856, 692
    cv2.rectangle(frame, (left, top), (right, bottom), (250, 250, 250), -1)
    cv2.rectangle(frame, (left, top), (right, bottom), (220, 220, 220), 2)
    cv2.line(frame, (224, 654), (242, 654), (35, 35, 35), 3)
    cv2.line(frame, (233, 645), (233, 663), (35, 35, 35), 3)
    cv2.circle(frame, (828, 665), 19, (10, 10, 10), -1)
    return frame


def synthetic_compact_file_dialog() -> tuple[np.ndarray, Rect]:
    frame = np.full((768, 1024, 3), 245, dtype=np.uint8)
    dialog = Rect(7, 1, 611, 471)
    cv2.rectangle(frame, (200, 398), (400, 425), (255, 255, 255), -1)
    cv2.rectangle(frame, (200, 398), (400, 425), (160, 160, 160), 1)
    cv2.rectangle(frame, (412, 398), (600, 425), (255, 255, 255), -1)
    cv2.rectangle(frame, (412, 398), (600, 425), (160, 160, 160), 1)
    return frame, dialog


class OpenCVInspectorThemeTests(unittest.TestCase):
    def test_light_theme_composer_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(Path(directory))
            state = inspector.inspect_frame(synthetic_chatgpt_frame("light"))

        self.assertEqual(state.layout, ComposerLayout.ACTIVE_CHAT_BOTTOM)
        self.assertIsNotNone(state.plus_button)
        self.assertIsNotNone(state.input_box)
        self.assertIsNotNone(state.action_button)

    def test_dark_theme_composer_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(Path(directory))
            state = inspector.inspect_frame(synthetic_chatgpt_frame("dark"))

        self.assertEqual(state.layout, ComposerLayout.ACTIVE_CHAT_BOTTOM)
        self.assertIsNotNone(state.plus_button)
        self.assertIsNotNone(state.input_box)
        self.assertIsNotNone(state.action_button)

    def test_narrow_centered_composer_can_fill_most_of_window(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(Path(directory))
            state = inspector.inspect_frame(synthetic_narrow_centered_frame())

        self.assertEqual(state.layout, ComposerLayout.NEW_CHAT_CENTERED)
        self.assertIsNotNone(state.plus_button)

    def test_fullscreen_bottom_composer_is_not_misclassified_as_image_viewer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(Path(directory))
            state = inspector.inspect_frame(synthetic_fullscreen_active_frame())

        self.assertEqual(state.layout, ComposerLayout.ACTIVE_CHAT_BOTTOM)
        self.assertIsNone(state.viewer_close_button)
        self.assertIsNotNone(state.action_button)

    def test_compact_windows_file_name_input_is_detected(self) -> None:
        frame, dialog = synthetic_compact_file_dialog()
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(Path(directory))
            field = inspector._file_name_input(
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                dialog,
            )

        self.assertIsNotNone(field)
        assert field is not None
        self.assertLess(field.center[0], dialog.x + dialog.width // 2 + 100)
        self.assertGreaterEqual(field.width, 190)

    def test_theme_change_refreshes_learned_plus_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(Path(directory))
            inspector.inspect_frame(synthetic_chatgpt_frame("dark"))
            dark_template = inspector._plus_template.copy()
            state = inspector.inspect_frame(synthetic_chatgpt_frame("light"))

        self.assertEqual(state.layout, ComposerLayout.ACTIVE_CHAT_BOTTOM)
        self.assertFalse(np.array_equal(dark_template, inspector._plus_template))

    def test_non_browser_foreground_is_rejected_before_clicks(self) -> None:
        rgb = cv2.cvtColor(synthetic_chatgpt_frame("light"), cv2.COLOR_BGR2RGB)
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(
                Path(directory),
                screenshot_provider=lambda: Image.fromarray(rgb),
            )
            with patch.object(
                inspector,
                "_foreground_window_context",
                return_value=("GameWindow", "A Game", "game.exe"),
            ):
                state = inspector.inspect()

        self.assertEqual(state.layout, ComposerLayout.MISSING)
        self.assertIsNone(state.plus_button)
        self.assertTrue(any("foreground rejected" in item for item in state.diagnostics))

    def test_browser_foreground_keeps_visual_state(self) -> None:
        rgb = cv2.cvtColor(synthetic_chatgpt_frame("light"), cv2.COLOR_BGR2RGB)
        with tempfile.TemporaryDirectory() as directory:
            inspector = OpenCVScreenInspector(
                Path(directory),
                screenshot_provider=lambda: Image.fromarray(rgb),
            )
            with patch.object(
                inspector,
                "_foreground_window_context",
                return_value=("Chrome_WidgetWin_1", "ChatGPT", "msedge.exe"),
            ):
                state = inspector.inspect()

        self.assertEqual(state.layout, ComposerLayout.ACTIVE_CHAT_BOTTOM)
        self.assertIsNotNone(state.plus_button)


if __name__ == "__main__":
    unittest.main()
