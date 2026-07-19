from __future__ import annotations

import datetime as dt
import ctypes
import time
from pathlib import Path
from typing import Callable

import pyautogui

from .contracts import ComposerLayout, Rect, ScreenState

try:
    import cv2
    import numpy as np
except ImportError as exc:  # pragma: no cover - exercised only on machines without OpenCV
    cv2 = None
    np = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


class VisionUnavailableError(RuntimeError):
    pass


class VisionTimeoutError(RuntimeError):
    pass


class OpenCVScreenInspector:
    """Find ChatGPT controls from pixels without browser DOM access.

    The first empty composer is located geometrically.  Its plus icon is then
    retained as an in-memory template so the same control can still be found
    after attachment cards change the composer's outer height.
    """

    def __init__(
        self,
        diagnostic_dir: Path,
        screenshot_provider: Callable[[], object] | None = None,
        plus_template_threshold: float = 0.78,
    ) -> None:
        if cv2 is None or np is None:
            raise VisionUnavailableError(
                "OpenCV visual automation requires cv2 and numpy. "
                f"Original import error: {_IMPORT_ERROR}"
            )
        self.diagnostic_dir = Path(diagnostic_dir)
        self.screenshot_provider = screenshot_provider or pyautogui.screenshot
        self.plus_template_threshold = float(plus_template_threshold)
        self.last_frame = None
        self.last_state: ScreenState | None = None
        self._plus_template = None

    def capture(self):
        image = self.screenshot_provider()
        rgb = np.asarray(image.convert("RGB"))
        frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        self.last_frame = frame
        return frame

    @staticmethod
    def _gray(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def _contours(gray):
        edges = cv2.Canny(gray, 15, 70)
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def _dedupe_rectangles(rectangles: list[Rect], tolerance: int = 4) -> list[Rect]:
        result: list[Rect] = []
        for rect in sorted(rectangles, key=lambda item: item.width * item.height, reverse=True):
            duplicate = any(
                abs(rect.x - known.x) <= tolerance
                and abs(rect.y - known.y) <= tolerance
                and abs(rect.width - known.width) <= tolerance * 2
                and abs(rect.height - known.height) <= tolerance * 2
                for known in result
            )
            if not duplicate:
                result.append(rect)
        return result

    def _composer_from_geometry(self, gray) -> tuple[Rect | None, float, list[str]]:
        screen_height, screen_width = gray.shape
        candidates: list[tuple[float, Rect]] = []
        diagnostics: list[str] = []
        for contour in self._contours(gray):
            x, y, width, height = cv2.boundingRect(contour)
            if not (max(280, int(screen_width * 0.14)) <= width <= int(screen_width * 0.70)):
                continue
            if not (34 <= height <= 240 and width / max(1, height) >= 2.0):
                continue
            if y < int(screen_height * 0.20) or y > screen_height - 25:
                continue
            control_top = y + max(0, height - 58)
            left_patch = gray[control_top:y + height, x:x + min(64, width)]
            dark = left_patch < 170
            dark_count = int(dark.sum())
            if not (20 <= dark_count <= 450):
                continue
            row_peak = int(dark.sum(axis=1).max(initial=0))
            col_peak = int(dark.sum(axis=0).max(initial=0))
            if row_peak < 6 or col_peak < 6:
                continue
            right_patch = gray[control_top:y + height, max(x, x + width - 60):x + width]
            right_dark_ratio = float((right_patch < 80).mean()) if right_patch.size else 0.0
            aspect_score = min(width / max(1.0, height) / 10.0, 1.0)
            cross_score = min(row_peak, col_peak) / max(row_peak, col_peak, 1)
            action_score = min(right_dark_ratio * 4.0, 1.0)
            score = 0.42 * aspect_score + 0.33 * cross_score + 0.25 * action_score
            candidates.append((score, Rect(x, y, width, height)))
        if not candidates:
            diagnostics.append("no geometric composer candidate")
            return None, 0.0, diagnostics
        score, rect = max(candidates, key=lambda item: item[0])
        diagnostics.append(f"geometric composer score={score:.3f}")
        return rect, min(1.0, score), diagnostics

    def _remember_plus_template(self, gray, composer: Rect) -> Rect:
        size = max(26, min(34, composer.height - 8))
        plus = Rect(
            composer.x + 7,
            max(composer.y, composer.bottom - size - 4),
            size,
            size,
        ).clipped(gray.shape[1], gray.shape[0])
        crop = gray[plus.y:plus.bottom, plus.x:plus.right]
        if crop.size and self._plus_template is None:
            self._plus_template = crop.copy()
        return plus

    def _plus_from_template(self, gray) -> tuple[Rect | None, float]:
        template = self._plus_template
        if template is None:
            return None, 0.0
        if gray.shape[0] < template.shape[0] or gray.shape[1] < template.shape[1]:
            return None, 0.0
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, maximum, _, location = cv2.minMaxLoc(result)
        if maximum < self.plus_template_threshold:
            return None, float(maximum)
        return Rect(location[0], location[1], template.shape[1], template.shape[0]), float(maximum)

    @staticmethod
    def _composer_from_bottom_action(gray) -> tuple[Rect | None, float]:
        """Cold-start fallback for a tall, internally scrolled draft composer."""
        screen_height, screen_width = gray.shape
        left = int(screen_width * 0.12)
        right = int(screen_width * 0.48)
        top = int(screen_height * 0.84)
        region = gray[top:screen_height, left:right]
        mask = (region < 85).astype("uint8") * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        actions: list[Rect] = []
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            if 25 <= width <= 48 and 25 <= height <= 48 and 0.72 <= width / max(1, height) <= 1.38:
                actions.append(Rect(left + x, top + y, width, height))
        if not actions:
            return None, 0.0
        action = max(actions, key=lambda item: item.x)
        composer_width = max(460, min(560, int(screen_width * 0.268)))
        composer_right = action.right + 5
        return Rect(
            max(0, composer_right - composer_width),
            max(0, action.center[1] - 23),
            composer_width,
            46,
        ), 0.82

    @staticmethod
    def _action_button(gray, plus: Rect, fallback_right: int | None = None) -> Rect | None:
        center_y = plus.center[1]
        left = plus.right + 180
        right = min(gray.shape[1], plus.x + 900 if fallback_right is None else fallback_right + 10)
        top = max(0, center_y - 28)
        bottom = min(gray.shape[0], center_y + 28)
        region = gray[top:bottom, left:right]
        if region.size == 0:
            return None
        mask = (region < 85).astype("uint8") * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates: list[Rect] = []
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            if 25 <= width <= 48 and 25 <= height <= 48 and 0.70 <= width / max(1, height) <= 1.35:
                candidates.append(Rect(left + x, top + y, width, height))
        return max(candidates, key=lambda rect: rect.x, default=None)

    @staticmethod
    def _classify_action(gray, action: Rect | None) -> str:
        if action is None:
            return "missing"
        crop = gray[action.y:action.bottom, action.x:action.right]
        if crop.size == 0:
            return "missing"
        margin_y = max(1, crop.shape[0] // 3)
        margin_x = max(1, crop.shape[1] // 3)
        center = crop[margin_y:crop.shape[0] - margin_y, margin_x:crop.shape[1] - margin_x]
        bright = (center > 220).astype("uint8") * 255
        contours, _ = cv2.findContours(bright, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            bounding = max(1, width * height)
            if 4 <= width <= 14 and 4 <= height <= 14 and 0.72 <= width / max(1, height) <= 1.38 and area / bounding >= 0.72:
                return "stop"
        return "action"

    @staticmethod
    def _model_controls(
        gray,
        composer: Rect | None,
        plus: Rect | None,
        action: Rect | None,
    ) -> tuple[Rect | None, Rect | None, Rect | None]:
        """Infer the image-model selector and its ``High`` popup row.

        ChatGPT anchors this compact selector immediately left of the voice /
        send control.  The popup itself is laid out in five fixed-height rows;
        ``High`` is the fourth row.  Returning geometry from the detected
        composer keeps this independent from absolute screen coordinates.
        The controller additionally requires a visual frame change before it
        treats the inferred popup row as clickable.
        """
        if composer is None or plus is None or action is None:
            return None, None, None
        selector = Rect(
            max(composer.x, action.x - 92),
            max(0, plus.center[1] - 18),
            min(64, max(36, action.x - composer.x - 40)),
            36,
        ).clipped(gray.shape[1], gray.shape[0])
        menu = Rect(
            max(0, action.x - 174),
            max(0, plus.center[1] - 177),
            138,
            160,
        ).clipped(gray.shape[1], gray.shape[0])
        high = Rect(
            menu.x + 8,
            max(menu.y, plus.center[1] - 87),
            max(30, menu.width - 16),
            30,
        ).clipped(gray.shape[1], gray.shape[0])
        return selector, menu, high

    def _attachment_menu(
        self,
        gray,
        composer: Rect | None,
    ) -> tuple[Rect | None, Rect | None, Rect | None]:
        if composer is None:
            return None, None, None
        # The first menu row has a persistent light-gray full-width highlight.
        # Detect that 24-36 px horizontal band directly.  Same-width message
        # bubbles are much taller, which avoids the failure mode where a
        # conversation card is mistaken for the popup outer contour.
        band_left = max(0, composer.x + 9)
        band_right = min(gray.shape[1], composer.right - 7)
        scan_top = max(0, composer.y - 550)
        scan_bottom = min(gray.shape[0], composer.bottom + 550)
        if band_right > band_left and scan_bottom > scan_top:
            coverage = (gray[scan_top:scan_bottom, band_left:band_right] < 250).mean(axis=1)
            indices = np.where(coverage >= 0.90)[0]
            groups: list[list[int]] = []
            for relative_y in indices:
                absolute_y = scan_top + int(relative_y)
                if not groups or absolute_y > groups[-1][-1] + 1:
                    groups.append([absolute_y])
                else:
                    groups[-1].append(absolute_y)
            bands = [group for group in groups if 24 <= len(group) <= 36]
            if bands:
                if composer.center[1] >= int(gray.shape[0] * 0.74):
                    eligible = [
                        group
                        for group in bands
                        if composer.y - 450 <= group[0] and group[-1] <= composer.y
                    ]
                    selected = max(eligible, key=lambda group: group[-1], default=None)
                else:
                    eligible = [group for group in bands if group[0] >= composer.bottom]
                    selected = min(eligible, key=lambda group: group[0], default=None)
                if selected is not None:
                    row_height = max(28, min(36, len(selected)))
                    row_y = selected[0]
                    add_file = Rect(band_left, row_y, band_right - band_left, row_height)
                    create_image = Rect(
                        band_left,
                        row_y + row_height + 1,
                        band_right - band_left,
                        row_height,
                    )
                    menu = Rect(
                        max(0, composer.x + 1),
                        max(0, row_y - 4),
                        max(1, composer.width - 2),
                        row_height * 9,
                    ).clipped(gray.shape[1], gray.shape[0])
                    return menu, add_file, create_image
        # Every current attachment popup exposes the shallow highlighted first
        # row above.  Falling back to a similarly sized conversation card is
        # destructive (it can click an old image/message), so fail closed and
        # let the controller retry instead of guessing.
        return None, None, None

    @staticmethod
    def _foreground_native_dialog() -> Rect | None:
        """Return the foreground Windows common-dialog bounds, never browser DOM."""
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return None
            class_name = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_name, len(class_name))
            if class_name.value != "#32770":
                return None

            class WinRect(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long),
                ]

            bounds = WinRect()
            if not user32.GetWindowRect(hwnd, ctypes.byref(bounds)):
                return None
            return Rect(
                int(bounds.left),
                int(bounds.top),
                int(bounds.right - bounds.left),
                int(bounds.bottom - bounds.top),
            )
        except (AttributeError, OSError):
            return None

    def _file_name_input(self, gray, dialog: Rect | None) -> Rect | None:
        if dialog is None:
            return None
        screen_height, screen_width = gray.shape
        dialog = dialog.clipped(screen_width, screen_height)
        candidates: list[Rect] = []
        for contour in self._contours(gray):
            x, y, width, height = cv2.boundingRect(contour)
            if width < max(260, int(dialog.width * 0.35)):
                continue
            if not (20 <= height <= 46):
                continue
            if not (
                dialog.x <= x
                and x + width <= dialog.right
                and dialog.y + int(dialog.height * 0.55) <= y <= dialog.bottom
            ):
                continue
            candidates.append(Rect(x, y, width, height))
        candidates = self._dedupe_rectangles(candidates)
        return max(candidates, key=lambda rect: (rect.y, rect.width), default=None)

    def _attachment_boxes(self, gray, composer: Rect | None) -> tuple[Rect, ...]:
        if composer is None:
            return ()
        if composer.height >= 130:
            # ChatGPT expands the last remaining card into a roughly 115 px
            # preview.  Counting its internal artwork contours reports two or
            # more fake cards, so model the single outer card directly.
            return (
                Rect(
                    composer.x + 8,
                    composer.y + 6,
                    min(115, composer.width - 20),
                    max(70, composer.height - 55),
                ),
            )
        if composer.height < 72:
            # A long prompt internally scrolls the composer and leaves only
            # the 42-46 px bottom control contour.  Recover the attachment row
            # from the same regular remove-X chain up to 360 px above it.
            # A single attachment also expands into a ~115 px card immediately
            # above that control row while geometry still reports only the
            # 46 px control contour.  Detect that tightly anchored card before
            # scanning older conversation thumbnails farther up the page.
            single_top = max(0, composer.y - 170)
            single_left = composer.x
            single_right = min(gray.shape[1], composer.x + 180)
            single_region = gray[single_top:composer.y, single_left:single_right]
            single_edges = cv2.Canny(single_region, 25, 90)
            single_contours, _ = cv2.findContours(
                single_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
            )
            single_candidates: list[Rect] = []
            for contour in single_contours:
                x, y, item_width, item_height = cv2.boundingRect(contour)
                if not (55 <= item_width <= 140 and 55 <= item_height <= 145):
                    continue
                if not (0.68 <= item_width / max(1, item_height) <= 1.45):
                    continue
                rect = Rect(single_left + x, single_top + y, item_width, item_height)
                if rect.x <= composer.x + 80 and 0 <= composer.y - rect.bottom <= 40:
                    single_candidates.append(rect)
            if single_candidates:
                return (
                    Rect(
                        composer.x + 8,
                        max(0, composer.y - 123),
                        min(115, composer.width - 20),
                        115,
                    ),
                )

            top = max(0, composer.y - 360)
            bottom = composer.y
            left = composer.x
            right = min(gray.shape[1], composer.x + 300)
            region = gray[top:bottom, left:right]
            mask = (region < 45).astype("uint8") * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            centers: list[tuple[int, int]] = []
            for contour in contours:
                x, y, item_width, item_height = cv2.boundingRect(contour)
                area = float(cv2.contourArea(contour))
                if not (11 <= item_width <= 26 and 10 <= item_height <= 24 and area >= 35):
                    continue
                center = (left + x + item_width // 2, top + y + item_height // 2)
                if composer.x + 25 <= center[0] <= composer.x + 270:
                    centers.append(center)
            rows: list[list[tuple[int, int]]] = []
            for center in sorted(centers, key=lambda item: (item[1], item[0])):
                for row in rows:
                    if abs(center[1] - row[0][1]) <= 10:
                        row.append(center)
                        break
                else:
                    rows.append([center])
            best_chain: list[tuple[int, int]] = []
            for row in rows:
                chain: list[tuple[int, int]] = []
                for center in sorted(row):
                    if not chain or 35 <= center[0] - chain[-1][0] <= 65:
                        chain.append(center)
                    elif len(chain) < 2:
                        chain = [center]
                if len(chain) > len(best_chain):
                    best_chain = chain
            if len(best_chain) >= 2:
                # A dark thumbnail can merge its black remove-X overlay into
                # the artwork, making that X exceed the contour-size filter.
                # Extend a reliable left-anchored chain only when the next
                # regularly spaced card-sized patch contains real image
                # variance and edge structure.  Blank prompt space therefore
                # cannot be promoted to an attachment.
                pitches = [
                    best_chain[index][0] - best_chain[index - 1][0]
                    for index in range(1, len(best_chain))
                ]
                pitch = int(round(float(np.median(pitches))))
                # A very pale first thumbnail can hide its remove-X just as a
                # dark trailing thumbnail can merge it into the artwork.  If
                # the detected chain starts one regular card pitch too far to
                # the right, validate the missing artwork and prepend it.
                expected_first_x = best_chain[0][0] - pitch
                if (
                    35 <= pitch <= 65
                    and composer.x + 25 <= expected_first_x <= composer.x + 75
                ):
                    inferred = Rect(
                        expected_first_x - 37, best_chain[0][1] - 10, 47, 47
                    ).clipped(gray.shape[1], gray.shape[0])
                    patch = gray[inferred.y:inferred.bottom, inferred.x:inferred.right]
                    edge_ratio = float((cv2.Canny(patch, 25, 90) > 0).mean()) if patch.size else 0.0
                    if patch.size and float(patch.std()) >= 25.0 and edge_ratio >= 0.08:
                        best_chain.insert(0, (expected_first_x, best_chain[0][1]))
                if best_chain[0][0] <= composer.x + 70:
                    while 35 <= pitch <= 65 and len(best_chain) < 4:
                        expected_x = best_chain[-1][0] + pitch
                        expected_y = int(round(float(np.median([item[1] for item in best_chain]))))
                        if expected_x > composer.x + 270:
                            break
                        inferred = Rect(expected_x - 37, expected_y - 10, 47, 47).clipped(
                            gray.shape[1], gray.shape[0]
                        )
                        patch = gray[inferred.y:inferred.bottom, inferred.x:inferred.right]
                        if patch.size == 0:
                            break
                        edge_ratio = float((cv2.Canny(patch, 25, 90) > 0).mean())
                        if float(patch.std()) < 25.0 or edge_ratio < 0.08:
                            break
                        best_chain.append((expected_x, expected_y))
                return tuple(
                    Rect(center_x - 37, center_y - 10, 47, 47)
                    for center_x, center_y in best_chain
                )
        if 72 <= composer.height < 130:
            # Compact attachment cards expose a dark remove-X overlay at a
            # regular ~51 px pitch.  The artwork itself can hide an outer card
            # contour, but these four overlays remain independently visible.
            top = composer.y
            bottom = min(gray.shape[0], composer.y + 32)
            left = composer.x
            right = min(gray.shape[1], composer.x + 300)
            strip = gray[top:bottom, left:right]
            mask = (strip < 45).astype("uint8") * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            centers: list[tuple[int, int]] = []
            for contour in contours:
                x, y, item_width, item_height = cv2.boundingRect(contour)
                area = float(cv2.contourArea(contour))
                if not (11 <= item_width <= 26 and 10 <= item_height <= 24 and area >= 35):
                    continue
                center = (left + x + item_width // 2, top + y + item_height // 2)
                if composer.x + 25 <= center[0] <= composer.x + 270:
                    centers.append(center)
            centers.sort()
            chain: list[tuple[int, int]] = []
            for center in centers:
                if not chain or 35 <= center[0] - chain[-1][0] <= 65:
                    chain.append(center)
                elif len(chain) < 2:
                    chain = [center]
            if len(chain) >= 2:
                # Apply the same dark-thumbnail recovery used by the long-
                # prompt layout.  In compact mode an X can merge into dark
                # artwork even though the 47 px attachment card is plainly
                # present.
                pitches = [
                    chain[index][0] - chain[index - 1][0]
                    for index in range(1, len(chain))
                ]
                pitch = int(round(float(np.median(pitches))))
                expected_first_x = chain[0][0] - pitch
                if (
                    35 <= pitch <= 65
                    and composer.x + 25 <= expected_first_x <= composer.x + 75
                ):
                    inferred = Rect(
                        expected_first_x - 37, chain[0][1] - 10, 47, 47
                    ).clipped(gray.shape[1], gray.shape[0])
                    patch = gray[inferred.y:inferred.bottom, inferred.x:inferred.right]
                    edge_ratio = float((cv2.Canny(patch, 25, 90) > 0).mean()) if patch.size else 0.0
                    if patch.size and float(patch.std()) >= 25.0 and edge_ratio >= 0.08:
                        chain.insert(0, (expected_first_x, chain[0][1]))
                if chain[0][0] <= composer.x + 70:
                    while 35 <= pitch <= 65 and len(chain) < 4:
                        expected_x = chain[-1][0] + pitch
                        expected_y = int(round(float(np.median([item[1] for item in chain]))))
                        if expected_x > composer.x + 270:
                            break
                        inferred = Rect(expected_x - 37, expected_y - 10, 47, 47).clipped(
                            gray.shape[1], gray.shape[0]
                        )
                        patch = gray[inferred.y:inferred.bottom, inferred.x:inferred.right]
                        if patch.size == 0:
                            break
                        edge_ratio = float((cv2.Canny(patch, 25, 90) > 0).mean())
                        if float(patch.std()) < 25.0 or edge_ratio < 0.08:
                            break
                        chain.append((expected_x, expected_y))
                return tuple(
                    # Choose the inferred right edge so the controller's
                    # fallback (right - 10) lands on this detected X center.
                    Rect(center_x - 37, composer.y + 5, 47, 47)
                    for center_x, _ in chain
                )
        # With an empty/short prompt the attachment strip is part of the outer
        # composer contour.  A long prompt makes the composer internally
        # scrollable and geometry then sees only its bottom control row; the
        # attachment strip can still be ~300 px above that row.  Search the
        # narrow composer column in both cases instead of treating the cards as
        # missing merely because the outer contour collapsed.
        top = composer.y + 2 if composer.height >= 72 else max(0, composer.y - 360)
        bottom = composer.bottom - 42
        left = composer.x + 2
        right = composer.right - 2
        if bottom <= top:
            return ()
        region = gray[top:bottom, left:right]
        edges = cv2.Canny(region, 25, 90)
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        candidates: list[Rect] = []
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            # ChatGPT enlarges the final remaining attachment card after its
            # siblings are removed, so accept both the compact strip cards and
            # the single-card presentation.
            if not (25 <= width <= 130 and 36 <= height <= 130):
                continue
            if not (0.62 <= width / max(1, height) <= 1.55):
                continue
            candidates.append(Rect(left + x, top + y, width, height))

        # Keep the strongest horizontal row.  This rejects similarly sized
        # controls or thumbnails elsewhere in the conversation column.
        rows: list[list[Rect]] = []
        for rect in sorted(candidates, key=lambda item: item.center[1]):
            for row in rows:
                if abs(rect.center[1] - row[0].center[1]) <= 12:
                    row.append(rect)
                    break
            else:
                rows.append([rect])
        if not rows:
            return ()
        rows = [row for row in rows if min(item.x for item in row) <= left + 40]
        if not rows:
            return ()
        candidates = max(
            rows,
            key=lambda row: (
                len({round(item.center[0] / 10) for item in row}),
                sum(item.width * item.height for item in row),
            ),
        )

        groups: list[list[Rect]] = []
        for rect in sorted(candidates, key=lambda item: item.center[0]):
            for group in groups:
                if abs(rect.center[0] - group[0].center[0]) <= 10:
                    group.append(rect)
                    break
            else:
                groups.append([rect])
        boxes = [
            max(group, key=lambda item: item.width * item.height)
            for group in groups
        ]
        boxes = sorted(boxes, key=lambda item: item.x)
        if len(boxes) == 1 and abs(boxes[0].bottom - composer.y) > 30:
            return ()
        return tuple(boxes)

    def inspect_frame(self, frame) -> ScreenState:
        gray = self._gray(frame)
        height, width = gray.shape
        diagnostics: list[str] = []

        composer, confidence, geometric_diagnostics = self._composer_from_geometry(gray)
        diagnostics.extend(geometric_diagnostics)
        plus = None
        if composer is not None:
            # Conversation cards and feedback widgets can satisfy the broad
            # rounded-rectangle geometry test.  Once the real composer plus
            # has been learned, a strong match substantially lower on screen
            # is authoritative and prevents those mid-page controls from
            # being classified as a fresh-chat composer.
            template_plus, template_score = self._plus_from_template(gray)
            if (
                template_plus is not None
                and template_plus.y >= int(height * 0.72)
                and template_plus.y > composer.y + 80
            ):
                template_action = self._action_button(gray, template_plus)
                if template_action is not None:
                    plus = template_plus
                    composer = Rect(
                        max(0, plus.x - 7),
                        max(0, plus.center[1] - 23),
                        template_action.right - max(0, plus.x - 7) + 5,
                        46,
                    )
                    confidence = template_score
                    diagnostics.append(f"lower plus template override={template_score:.3f}")
            if plus is None:
                plus = self._remember_plus_template(gray, composer)
        else:
            plus, template_score = self._plus_from_template(gray)
            if plus is not None:
                action = self._action_button(gray, plus)
                if action is not None:
                    composer = Rect(
                        max(0, plus.x - 7),
                        max(0, plus.center[1] - 23),
                        action.right - max(0, plus.x - 7) + 5,
                        46,
                    )
                    confidence = template_score
                    diagnostics.append(f"plus template score={template_score:.3f}")
            else:
                composer, confidence = self._composer_from_bottom_action(gray)
                if composer is not None:
                    plus = self._remember_plus_template(gray, composer)
                    diagnostics.append("bottom action cold-start fallback")

        action = self._action_button(gray, plus, composer.right if composer else None) if plus else None
        if composer is not None and action is None:
            action = Rect(composer.right - 39, composer.y + 4, 34, max(30, composer.height - 8))
        if composer is not None and plus is None:
            plus = Rect(composer.x + 7, composer.y + 6, 30, max(30, composer.height - 12))

        input_box = None
        input_ink_ratio = 0.0
        if composer is not None and plus is not None and action is not None:
            input_box = Rect(
                plus.right + 5,
                max(0, plus.center[1] - 18),
                max(20, action.x - plus.right - 10),
                36,
            ).clipped(width, height)
            crop = gray[input_box.y:input_box.bottom, input_box.x:input_box.right]
            input_ink_ratio = float((crop < 150).mean()) if crop.size else 0.0

        layout = ComposerLayout.MISSING
        if composer is not None:
            if composer.center[1] >= int(height * 0.74) and composer.width > composer.x * 2.5:
                layout = ComposerLayout.IMAGE_VIEWER
            elif composer.center[1] < int(height * 0.74):
                layout = ComposerLayout.NEW_CHAT_CENTERED
            else:
                layout = ComposerLayout.ACTIVE_CHAT_BOTTOM

        menu, add_file, create_image = self._attachment_menu(gray, composer)
        model_selector, model_menu, model_high = self._model_controls(gray, composer, plus, action)
        native_dialog = self._foreground_native_dialog()
        file_name_input = self._file_name_input(gray, native_dialog)
        attachment_boxes = self._attachment_boxes(gray, composer)
        viewer_close = None
        if layout == ComposerLayout.IMAGE_VIEWER:
            viewer_close = Rect(max(8, composer.x - 140), 120, 30, 30).clipped(width, height)
        state = ScreenState(
            screen_width=width,
            screen_height=height,
            layout=layout,
            composer=composer,
            plus_button=plus,
            input_box=input_box,
            action_button=action,
            attachment_menu=menu,
            add_file_row=add_file,
            create_image_row=create_image,
            model_selector=model_selector,
            model_menu=model_menu,
            model_high_row=model_high,
            file_name_input=file_name_input,
            viewer_close_button=viewer_close,
            attachment_boxes=attachment_boxes,
            attachment_count=len(attachment_boxes),
            action_kind=self._classify_action(gray, action),
            input_ink_ratio=input_ink_ratio,
            confidence=confidence,
            diagnostics=tuple(diagnostics),
        )
        self.last_frame = frame
        self.last_state = state
        return state

    def inspect(self) -> ScreenState:
        return self.inspect_frame(self.capture())

    def attachment_close_button(self, box: Rect) -> Rect | None:
        """Locate the dark remove-X overlay inside an attachment's top-right."""
        if self.last_frame is None:
            return None
        gray = self._gray(self.last_frame)
        height, width = gray.shape
        left = max(0, box.right - 30)
        right = min(width, box.right + 4)
        top = max(0, box.y - 5)
        bottom = min(height, box.y + 30)
        region = gray[top:bottom, left:right]
        if region.size == 0:
            return None
        mask = (region < 65).astype("uint8") * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates: list[tuple[float, Rect]] = []
        expected_x = box.right - 10
        expected_y = box.y + 10
        for contour in contours:
            x, y, item_width, item_height = cv2.boundingRect(contour)
            area = float(cv2.contourArea(contour))
            if not (10 <= item_width <= 26 and 10 <= item_height <= 26 and area >= 25):
                continue
            rect = Rect(left + x, top + y, item_width, item_height)
            distance = abs(rect.center[0] - expected_x) + abs(rect.center[1] - expected_y)
            candidates.append((area - distance * 2.0, rect))
        return max(candidates, key=lambda item: item[0])[1] if candidates else None

    def wait_for(
        self,
        predicate: Callable[[ScreenState], bool],
        timeout: float,
        poll_seconds: float = 0.75,
        label: str = "visual state",
    ) -> ScreenState:
        deadline = time.monotonic() + max(0.1, float(timeout))
        last_state: ScreenState | None = None
        while time.monotonic() < deadline:
            last_state = self.inspect()
            if predicate(last_state):
                return last_state
            time.sleep(max(0.1, float(poll_seconds)))
        path = self.save_diagnostic(f"timeout_{label.replace(' ', '_')}")
        raise VisionTimeoutError(
            f"Timed out waiting for {label}; diagnostic={path}; last_state={last_state}"
        )

    @staticmethod
    def frame_change_ratio(before, after, threshold: int = 18) -> float:
        if before is None or after is None or before.shape != after.shape:
            return 1.0
        difference = cv2.absdiff(before, after)
        changed = np.any(difference > threshold, axis=2)
        return float(changed.mean())

    @staticmethod
    def region_fingerprint(frame, rect: Rect | None) -> int:
        if frame is None or rect is None:
            return 0
        rect = rect.clipped(frame.shape[1], frame.shape[0])
        crop = frame[rect.y:rect.bottom, rect.x:rect.right]
        if crop.size == 0:
            return 0
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (16, 16), interpolation=cv2.INTER_AREA)
        average = float(small.mean())
        bits = small >= average
        value = 0
        for bit in bits.flatten():
            value = (value << 1) | int(bit)
        return value

    @staticmethod
    def fingerprint_distance(left: int, right: int) -> int:
        return int((left ^ right).bit_count())

    def save_diagnostic(self, label: str) -> str:
        self.diagnostic_dir.mkdir(parents=True, exist_ok=True)
        timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = self.diagnostic_dir / f"vision_{label}_{timestamp}.png"
        frame = self.last_frame if self.last_frame is not None else self.capture()
        cv2.imwrite(str(path), frame)
        return str(path)
