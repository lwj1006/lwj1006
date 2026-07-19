from __future__ import annotations

import time
from pathlib import Path

import pyautogui
import pyperclip

from .contracts import ComposerLayout, Rect, ScreenState
from .opencv_inspector import OpenCVScreenInspector, VisionTimeoutError


DEFAULT_PRIME_PROMPT = "给你提示词，你来画。"


class VisionAutomationController:
    """Closed-loop browser operations backed by a pluggable screen inspector."""

    def __init__(self, batch_module, inspector: OpenCVScreenInspector) -> None:
        self.batch = batch_module
        self.inspector = inspector
        self.expected_attachment_count = 0
        # Transaction state is more trustworthy than card-like contours in a
        # completed generated image.  Only a live/failed upload transaction is
        # allowed to trigger destructive attachment cleanup.
        self.draft_attachments_pending = False

    def _click(self, rect: Rect, label: str) -> None:
        x, y = rect.center
        self.batch.debug_log(f"Vision: clicking {label} at ({x}, {y})")
        self.batch.click_slow(x, y, after=0.35)

    @staticmethod
    def _paste(text: str) -> None:
        pyperclip.copy(text)
        time.sleep(0.15)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.45)

    def wait_for_composer(
        self,
        layout: ComposerLayout | None = None,
        timeout: float = 30.0,
    ) -> ScreenState:
        return self.inspector.wait_for(
            lambda state: state.page_ready and (layout is None or state.layout == layout),
            timeout=timeout,
            label=f"composer {layout.value if layout else 'any'}",
        )

    def restore_chat_from_image_viewer(self, timeout: float = 30.0) -> ScreenState:
        state = self.inspector.inspect()
        if state.layout == ComposerLayout.IMAGE_VIEWER:
            if state.viewer_close_button is not None:
                self._click(state.viewer_close_button, "image viewer close X")
            else:
                print("Vision: image viewer close X unavailable; pressing Esc.", flush=True)
                pyautogui.press("esc")
            time.sleep(0.8)
        return self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=timeout)

    def _clear_visible_attachments(self, timeout: float = 15.0) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            state = self.inspector.inspect()
            if state.layout == ComposerLayout.IMAGE_VIEWER:
                print("Vision recovery: attachment cleanup entered image viewer; closing it.", flush=True)
                self.restore_chat_from_image_viewer(timeout=30)
                continue
            if state.attachment_count <= 0:
                time.sleep(1.0)
                confirmed = self.inspector.inspect()
                if confirmed.attachment_count <= 0:
                    return
                state = confirmed
            previous_count = state.attachment_count
            previous_composer_height = state.composer.height if state.composer is not None else 0
            box = state.attachment_boxes[-1]
            visual_close = self.inspector.attachment_close_button(box)
            if visual_close is not None:
                close = visual_close
            elif box.width > 65 or box.height > 65:
                if state.composer is not None and box.y - state.composer.y < 20:
                    # Directly modelled outer single-card rectangle.
                    close = Rect(box.right - 26, box.y + 2, 24, 24)
                else:
                    # Inner image contour: the X sits just above its top-right.
                    close = Rect(box.right - 26, max(0, box.y - 30), 24, 24)
            else:
                close = Rect(box.right - 18, box.y + 2, 16, 16)
            self._click(close, "attachment remove X")
            candidate = self.inspector.wait_for(
                lambda current: (
                    current.layout == ComposerLayout.IMAGE_VIEWER
                    or current.attachment_count < previous_count
                    or (
                        previous_count == 1
                        and previous_composer_height >= 130
                        and current.composer is not None
                        and current.composer.height < 100
                    )
                ),
                timeout=3.0,
                poll_seconds=0.25,
                label="attachment removal progress",
            )
            if candidate.layout == ComposerLayout.IMAGE_VIEWER:
                print("Vision recovery: removal click opened image viewer; closing it.", flush=True)
                self.restore_chat_from_image_viewer(timeout=30)
                continue
            if (
                previous_count == 1
                and previous_composer_height >= 130
                and candidate.composer is not None
                and candidate.composer.height < 100
            ):
                return
            if candidate.attachment_count >= previous_count:
                path = self.inspector.save_diagnostic("attachment_cleanup_no_progress")
                raise VisionTimeoutError(
                    "Attachment cleanup made no visual progress; "
                    f"count remained {candidate.attachment_count}; diagnostic={path}"
                )
            time.sleep(0.8)
        raise VisionTimeoutError("Could not clear partial attachments before upload retry.")

    def _clear_input_text(self) -> None:
        state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=15)
        if state.input_box is None:
            raise VisionTimeoutError("Cannot clear text without an active input box.")
        self._click(state.input_box, "input box before clear")
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        time.sleep(0.4)

    def _enter_text_and_send(self, text: str, required_layout: ComposerLayout) -> None:
        state = self.wait_for_composer(required_layout, timeout=30)
        assert state.input_box is not None
        before = self.inspector.last_frame.copy()
        self._click(state.input_box, "input box")
        self._paste(text)
        changed = self.inspector.wait_for(
            lambda candidate: (
                candidate.input_box is not None
                and self.inspector.frame_change_ratio(before, self.inspector.last_frame) > 0.001
            ),
            timeout=10,
            label="prompt text appearance",
        )
        if changed.action_button is None:
            raise VisionTimeoutError("Prompt changed the screen, but no action button was found.")
        self._click(changed.action_button, "send button")

    def prepare_session(self) -> None:
        """Prime only a genuinely new centered chat; otherwise reuse the active chat."""
        print("Vision automation: locating ChatGPT composer without DOM access.", flush=True)
        state = self.wait_for_composer(timeout=30)
        if state.layout == ComposerLayout.IMAGE_VIEWER:
            print("Vision automation: image viewer detected at startup; restoring chat.", flush=True)
            state = self.restore_chat_from_image_viewer(timeout=45)
        if state.layout == ComposerLayout.NEW_CHAT_CENTERED:
            print("Vision automation: new centered chat detected; sending the prime message.", flush=True)
            self._enter_text_and_send(DEFAULT_PRIME_PROMPT, ComposerLayout.NEW_CHAT_CENTERED)
            state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=90)
            self.inspector.wait_for(
                lambda candidate: candidate.layout == ComposerLayout.ACTIVE_CHAT_BOTTOM and candidate.action_kind != "stop",
                timeout=120,
                poll_seconds=1.0,
                label="prime response completion",
            )
        else:
            print("Vision automation: active bottom composer detected; prime message skipped.", flush=True)
        print(f"Vision automation ready: layout={state.layout.value}, confidence={state.confidence:.3f}", flush=True)

    def ensure_high_image_model(self) -> None:
        """Open the image-model popup and idempotently choose ``High``."""
        state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=20)
        if state.model_selector is None or state.model_menu is None:
            raise VisionTimeoutError("Image model selector geometry is unavailable.")
        before = self.inspector.last_frame.copy()
        menu_region = state.model_menu
        self._click(state.model_selector, "image model selector")
        opened = self.inspector.wait_for(
            lambda candidate: (
                candidate.model_high_row is not None
                and self.inspector.frame_change_ratio(
                    before[menu_region.y:menu_region.bottom, menu_region.x:menu_region.right],
                    self.inspector.last_frame[
                        menu_region.y:menu_region.bottom,
                        menu_region.x:menu_region.right,
                    ],
                ) > 0.01
            ),
            timeout=8,
            poll_seconds=0.25,
            label="image model menu opening",
        )
        assert opened.model_high_row is not None
        self._click(opened.model_high_row, "High image model")
        time.sleep(0.7)
        self.batch.debug_log("Vision: image model set to High")

    def _recover_failed_upload_cycle(self) -> None:
        """Return a failed upload/menu/dialog transaction to a clean composer."""
        pyautogui.press("esc")
        time.sleep(0.8)
        state = self.inspector.inspect()
        if state.layout == ComposerLayout.IMAGE_VIEWER:
            state = self.restore_chat_from_image_viewer(timeout=30)
        elif state.layout != ComposerLayout.ACTIVE_CHAT_BOTTOM:
            pyautogui.press("esc")
            state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=20)
        if self.draft_attachments_pending and state.attachment_count > 0:
            self._clear_visible_attachments(timeout=30)
        self._clear_input_text()
        self.draft_attachments_pending = False

    def upload_reference_images(self, reference_files: list[str]) -> list[str]:
        last_error: VisionTimeoutError | None = None
        for recovery_round in range(1, 4):
            try:
                return self._upload_reference_images_cycle(reference_files)
            except VisionTimeoutError as exc:
                last_error = exc
                print(
                    f"Vision upload recovery {recovery_round}/3 after: {exc}",
                    flush=True,
                )
                if recovery_round < 3:
                    self._recover_failed_upload_cycle()
        assert last_error is not None
        raise VisionTimeoutError(
            "Vision upload remained unrecoverable after 3 full transaction retries: "
            f"{last_error}"
        ) from last_error

    def _upload_reference_images_cycle(self, reference_files: list[str]) -> list[str]:
        upload_files = self.batch.prepare_upload_files(reference_files)
        self.batch.apply_upload_cooldown_if_needed(len(upload_files))
        expected_count = len(upload_files)
        self.batch.info_log(f"Vision upload: starting {expected_count} attachment(s)")
        for attempt in range(1, 4):
            self.batch.debug_log(f"Vision upload attempt {attempt}/3: expecting {expected_count} attachments")
            state = self.inspector.inspect()
            if state.layout == ComposerLayout.IMAGE_VIEWER:
                state = self.restore_chat_from_image_viewer(timeout=45)
            else:
                state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=45)
            if self.draft_attachments_pending and state.attachment_count:
                self._clear_visible_attachments()
                state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=15)
            self._clear_input_text()
            state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=15)
            if state.plus_button is None:
                raise VisionTimeoutError("Active composer found without a plus button.")

            self._click(state.plus_button, "attachment plus")
            menu_state = self.inspector.wait_for(
                lambda candidate: candidate.create_image_row is not None,
                timeout=12,
                label="attachment menu for create image",
            )
            assert menu_state.create_image_row is not None
            self._click(menu_state.create_image_row, "create image")

            image_mode_state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=20)
            self.ensure_high_image_model()
            image_mode_state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=20)
            if image_mode_state.plus_button is None:
                raise VisionTimeoutError("Image mode activated without a visible attachment plus button.")

            sequence_failed = False
            for ordinal, path in enumerate(upload_files, start=1):
                attachment_state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=20)
                if attachment_state.plus_button is None:
                    raise VisionTimeoutError("Attachment plus button disappeared during ordered upload.")
                self._click(
                    attachment_state.plus_button,
                    f"attachment plus for ordered file {ordinal}/{expected_count}",
                )
                menu_state = self.inspector.wait_for(
                    lambda candidate: candidate.add_file_row is not None,
                    timeout=12,
                    label=f"attachment menu for ordered file {ordinal}",
                )
                assert menu_state.add_file_row is not None
                self._click(menu_state.add_file_row, f"add ordered file {ordinal}/{expected_count}")

                dialog_state = self.inspector.wait_for(
                    lambda candidate: candidate.file_name_input is not None,
                    timeout=15,
                    label="Windows file-name input",
                )
                assert dialog_state.file_name_input is not None
                self._click(dialog_state.file_name_input, "Windows file-name input")
                pyautogui.hotkey("ctrl", "a")
                self._paste(f'"{path}"')
                self.draft_attachments_pending = True
                pyautogui.press("enter")

                dialog_closed = False
                for _ in range(12):
                    time.sleep(0.5)
                    candidate = self.inspector.inspect()
                    if candidate.layout == ComposerLayout.ACTIVE_CHAT_BOTTOM:
                        dialog_closed = True
                        break
                if not dialog_closed:
                    print(
                        f"Vision ordered upload: file {ordinal}/{expected_count} did not return to chat; retrying batch.",
                        flush=True,
                    )
                    pyautogui.press("esc")
                    time.sleep(0.8)
                    sequence_failed = True
                    break

                ordered_state = self.inspector.wait_for(
                    lambda candidate: (
                        candidate.layout == ComposerLayout.ACTIVE_CHAT_BOTTOM
                        and candidate.attachment_count == ordinal
                    ),
                    timeout=25,
                    poll_seconds=0.5,
                    label=f"ordered attachment {ordinal} of {expected_count}",
                )
                self.batch.debug_log(
                    f"Vision ordered upload: file {ordinal}/{expected_count} attached; "
                    f"visual count {ordered_state.attachment_count}/{expected_count}"
                )

            if sequence_failed:
                recovery = self.inspector.inspect()
                if recovery.layout == ComposerLayout.ACTIVE_CHAT_BOTTOM and recovery.attachment_count:
                    self._clear_visible_attachments(timeout=25)
                self.draft_attachments_pending = False
                continue

            self.batch.wait_with_echo(
                self.batch.upload_settle_seconds(expected_count),
                "Vision upload settle",
            )
            after_state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=20)
            self.batch.debug_log(
                f"Vision upload: attachment count {after_state.attachment_count}/{expected_count}"
            )
            if after_state.attachment_count == expected_count:
                self.expected_attachment_count = expected_count
                self.batch.record_uploaded_image_count(expected_count)
                self.batch.info_log(f"Vision upload: complete ({expected_count} attachment(s))")
                return upload_files
            if after_state.attachment_count:
                print(
                    f"Vision upload mismatch diagnostic: {self.inspector.save_diagnostic('upload_count_mismatch')}",
                    flush=True,
                )
                self._clear_visible_attachments()
            self._clear_input_text()
            self.draft_attachments_pending = False
        path = self.inspector.save_diagnostic("upload_failed_after_retries")
        raise VisionTimeoutError(
            f"Upload failed to produce {expected_count} attachments after 3 attempts; diagnostic={path}"
        )

    def send_prompt(self, prompt: str) -> None:
        last_error: VisionTimeoutError | None = None
        for attempt in range(1, 4):
            try:
                self._send_prompt_once(prompt)
                return
            except VisionTimeoutError as exc:
                last_error = exc
                print(f"Vision send recovery {attempt}/3 after: {exc}", flush=True)
                if attempt < 3:
                    pyautogui.press("esc")
                    time.sleep(0.8)
                    self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=20)
        assert last_error is not None
        raise VisionTimeoutError(
            f"Prompt send remained unrecoverable after 3 retries: {last_error}"
        ) from last_error

    def _send_prompt_once(self, prompt: str) -> None:
        state = self.wait_for_composer(ComposerLayout.ACTIVE_CHAT_BOTTOM, timeout=30)
        if state.input_box is None:
            raise VisionTimeoutError("Active composer found without an input box.")
        before = self.inspector.last_frame.copy()
        self._click(state.input_box, "active prompt input")
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        self._paste(prompt)
        self.batch.wait_with_echo(self.batch.TEXT_BEFORE_SEND_SECONDS, "Vision before send")

        ready = self.inspector.wait_for(
            lambda candidate: (
                candidate.layout == ComposerLayout.ACTIVE_CHAT_BOTTOM
                and candidate.action_button is not None
                and candidate.attachment_count == self.expected_attachment_count
                and self.inspector.frame_change_ratio(before, self.inspector.last_frame) > 0.001
            ),
            timeout=20,
            label="pasted prompt and send button",
        )
        assert ready.action_button is not None
        self._click(ready.action_button, "send button")
        self.inspector.wait_for(
            lambda candidate: (
                candidate.layout == ComposerLayout.ACTIVE_CHAT_BOTTOM
                and self.inspector.frame_change_ratio(before, self.inspector.last_frame) > 0.004
            ),
            timeout=20,
            label="sent message appearance",
        )
        self.expected_attachment_count = 0
        self.draft_attachments_pending = False

    def wait_for_generation(self, run_number: int) -> Path:
        poll_seconds = 5.0
        timeout = max(180, int(self.batch.CHECK_INTERVAL_SECONDS) * 2)
        minimum_wait = min(45, max(15, int(self.batch.CHECK_INTERVAL_SECONDS) // 4))
        started_at = time.monotonic()
        deadline = started_at + timeout
        observed_activity = False
        stable_cycles = 0
        previous_fingerprint = 0

        print(
            f"[{run_number:02d}] vision generation monitor: min={minimum_wait}s timeout={timeout}s",
            flush=True,
        )
        while time.monotonic() < deadline:
            state = self.inspector.inspect()
            if state.layout not in {ComposerLayout.ACTIVE_CHAT_BOTTOM, ComposerLayout.IMAGE_VIEWER} or state.composer is None:
                stable_cycles = 0
                time.sleep(poll_seconds)
                continue
            conversation = Rect(
                state.composer.x,
                0,
                state.composer.width,
                max(1, state.composer.y),
            )
            fingerprint = self.inspector.region_fingerprint(self.inspector.last_frame, conversation)
            distance = self.inspector.fingerprint_distance(previous_fingerprint, fingerprint) if previous_fingerprint else 0
            if state.layout == ComposerLayout.IMAGE_VIEWER or state.action_kind == "stop" or distance >= 3:
                observed_activity = True
            if observed_activity and state.action_kind != "stop" and distance <= 1:
                stable_cycles += 1
            else:
                stable_cycles = 0
            previous_fingerprint = fingerprint
            elapsed = time.monotonic() - started_at
            print(
                f"[{run_number:02d}] vision monitor: layout={state.layout.value} "
                f"action={state.action_kind} delta={distance} stable={stable_cycles}/3",
                flush=True,
            )
            if elapsed >= minimum_wait and observed_activity and stable_cycles >= 3:
                path = self.batch.take_screenshot(f"run_{run_number:02d}_vision_complete")
                print(f"[{run_number:02d}] vision completion screenshot: {path}", flush=True)
                if state.layout == ComposerLayout.IMAGE_VIEWER:
                    self.restore_chat_from_image_viewer(timeout=30)
                return path
            time.sleep(poll_seconds)

        path = self.inspector.save_diagnostic(f"run_{run_number:02d}_generation_timeout")
        raise VisionTimeoutError(
            f"Generation did not reach a visually stable completed state; diagnostic={path}"
        )
