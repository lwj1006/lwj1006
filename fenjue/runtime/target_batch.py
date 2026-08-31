"""Batch-send one dynamic target image through selected fixed prompts.

Put images into ../target. The script runs every selected prompt against the same
target file, then moves that file into ../complete only after all selected runs finish.
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

import pyautogui

from fenjue.runtime.batch import (
    COORDS,
    PROJECT_DIR,
    calibrate_coords,
    click_slow,
    load_calibrated_coords,
    paste_text,
    apply_upload_cooldown_if_needed,
    record_uploaded_image_count,
    recover_after_generation_limit,
    send_prompt,
    startup_refresh_before_button_work,
    take_screenshot,
    upload_settle_seconds,
    wait_for_generation,
    wait_with_echo,
    with_image_prompt_prefix,
)
from fenjue.runtime.target_batch_prompts import PROMPT_SETS
from fenjue.vision.generation_limit import GenerationLimitReached

WORKSPACE_DIR = PROJECT_DIR.parent
TARGET_DIR = WORKSPACE_DIR / "target"
COMPLETE_DIR = WORKSPACE_DIR / "complete"
TARGET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
MAX_TARGET_RUNS: int | None = None

PROMPT_SET_LABELS = (
    "Extreme close-up / low-angle negative space",
    "Extreme close-up / flowing-hair frame",
    "Knee-up / standing cinematic portrait",
    "Waist-up / intimate cinematic portrait",
)


def parse_prompt_selection(raw: str) -> tuple[int, ...]:
    normalized = raw.strip().lower()
    if normalized in {"all", "a", "全部", "全选"}:
        return tuple(range(1, len(PROMPT_SETS) + 1))
    if not normalized:
        raise ValueError("Prompt selection cannot be empty.")

    selected: list[int] = []
    tokens = normalized.replace("，", ",").replace("+", ",").replace(" ", ",").split(",")
    for token in (item for item in tokens if item):
        if "-" in token:
            parts = token.split("-", 1)
            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                raise ValueError(f"Invalid prompt range: {token}")
            start, end = (int(part) for part in parts)
            if start > end:
                start, end = end, start
            values = range(start, end + 1)
        elif token.isdigit():
            values = (int(token),)
        else:
            raise ValueError(f"Invalid prompt selection: {token}")

        for value in values:
            if not 1 <= value <= len(PROMPT_SETS):
                raise ValueError(f"Prompt set must be between 1 and {len(PROMPT_SETS)}: {value}")
            if value not in selected:
                selected.append(value)
    if not selected:
        raise ValueError("Select at least one prompt set.")
    return tuple(selected)


def choose_prompt_sets() -> tuple[int, ...]:
    print("Available D-mode prompt sets:", flush=True)
    for index, label in enumerate(PROMPT_SET_LABELS, start=1):
        print(f"  [{index}] {label}", flush=True)
    print("Choose one set (2), a combination (1,3,4), a range (1-3), or all.", flush=True)
    while True:
        raw = input("Prompt sets: ")
        try:
            return parse_prompt_selection(raw)
        except ValueError as exc:
            print(f"Invalid selection: {exc}", flush=True)


def ensure_target_dirs() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    COMPLETE_DIR.mkdir(parents=True, exist_ok=True)


def iter_target_files() -> list[Path]:
    ensure_target_dirs()
    files = [
        path
        for path in TARGET_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in TARGET_EXTENSIONS
    ]
    return sorted(files, key=lambda path: (path.stat().st_mtime, path.name.lower()))


def next_target_file() -> Path | None:
    files = iter_target_files()
    if not files:
        return None
    return files[0]


def unique_complete_path(source: Path) -> Path:
    candidate = COMPLETE_DIR / source.name
    if not candidate.exists():
        return candidate

    stem = source.stem
    suffix = source.suffix
    index = 2
    while True:
        candidate = COMPLETE_DIR / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def move_to_complete(source: Path) -> Path:
    ensure_target_dirs()
    destination = unique_complete_path(source)
    shutil.move(str(source), str(destination))
    return destination


def upload_target_file(path: Path) -> None:
    print(f"Upload target: {path}", flush=True)
    apply_upload_cooldown_if_needed(1)
    print("Upload: opening plus menu", flush=True)
    click_slow(*COORDS["plus_button"], after=1.0)
    print("Upload: choosing add photo/file menu item", flush=True)
    click_slow(*COORDS["add_photo_file_menu"], after=2.0)

    print("Upload: focusing file-name input", flush=True)
    click_slow(*COORDS["file_name_input"], after=0.3)
    paste_text(f'"{path}"')
    pyautogui.press("enter")

    wait_with_echo(upload_settle_seconds(1), "Upload settle")
    record_uploaded_image_count(1)


def process_target_file(
    path: Path,
    image_number: int,
    selected_prompt_sets: tuple[int, ...],
    generation_number: int,
) -> int:
    print("=" * 72, flush=True)
    print(f"[Image {image_number:02d}] Starting target file: {path.name}", flush=True)

    for prompt_set_number in selected_prompt_sets:
        generation_number += 1
        attempt = 1
        while True:
            print(
                f"[Image {image_number:02d}] prompt set {prompt_set_number} "
                f"({generation_number:02d} total), attempt {attempt}",
                flush=True,
            )
            upload_target_file(path)
            send_prompt(with_image_prompt_prefix(PROMPT_SETS[prompt_set_number - 1]))
            take_screenshot(
                f"target_{image_number:02d}_prompt_{prompt_set_number}_attempt_{attempt}_sent"
            )
            try:
                wait_for_generation(generation_number)
                break
            except GenerationLimitReached as error:
                print(
                    f"[Image {image_number:02d}] prompt set {prompt_set_number} hit the "
                    "generation limit; preserving this image and prompt position.",
                    flush=True,
                )
                recover_after_generation_limit(error)
                attempt += 1

    moved_to = move_to_complete(path)
    print(f"[Image {image_number:02d}] moved to complete: {moved_to}", flush=True)
    return generation_number


def main() -> None:
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.15

    ensure_target_dirs()
    selected_prompt_sets = choose_prompt_sets()

    if "--calibrate" in sys.argv:
        calibrate_coords()
    else:
        load_calibrated_coords()

    print(f"Target dir: {TARGET_DIR}", flush=True)
    print(f"Complete dir: {COMPLETE_DIR}", flush=True)
    print(f"Selected prompt sets: {', '.join(map(str, selected_prompt_sets))}", flush=True)
    print("Each target file runs through every selected prompt before it is moved.", flush=True)
    startup_refresh_before_button_work()

    image_number = 1
    generation_number = 0
    while True:
        if MAX_TARGET_RUNS is not None and image_number > MAX_TARGET_RUNS:
            print(f"Reached MAX_TARGET_RUNS={MAX_TARGET_RUNS}.", flush=True)
            return

        target_file = next_target_file()
        if target_file is None:
            print("No target files left. Done.", flush=True)
            return

        generation_number = process_target_file(
            target_file,
            image_number,
            selected_prompt_sets,
            generation_number,
        )
        image_number += 1


if __name__ == "__main__":
    main()
