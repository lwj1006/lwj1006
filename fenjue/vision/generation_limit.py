from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import pyautogui
import pyperclip


RESET_SAFETY_BUFFER_SECONDS = 90
_OCR_SCRIPT = Path(__file__).with_name("windows_ocr.ps1")


@dataclass(frozen=True)
class GenerationLimitDetection:
    text: str
    delay_seconds: int | None
    resume_at: dt.datetime | None
    source: str
    screenshot_path: Path


class GenerationLimitReached(RuntimeError):
    def __init__(self, detection: GenerationLimitDetection) -> None:
        self.detection = detection
        if detection.resume_at is None:
            detail = "reset time could not be parsed"
        else:
            detail = f"resume at {detection.resume_at:%Y-%m-%d %H:%M:%S}"
        super().__init__(f"ChatGPT image generation limit detected; {detail}")


def is_generation_limit_text(text: str) -> bool:
    folded = " ".join(str(text).casefold().split())
    compact = re.sub(r"\s+", "", str(text))
    english = (
        "plus plan limit" in folded
        or (
            ("image generation" in folded or "images" in folded)
            and "limit" in folded
            and ("reset" in folded or "used up" in folded or "hit" in folded)
        )
    )
    chinese = (
        ("图片生成" in compact or "图像生成" in compact)
        and (
            "次数已用完" in compact
            or "已用完" in compact
            or "恢复更多次数" in compact
            or "套餐限制" in compact
        )
    )
    return english or chinese


def parse_reset_delay_seconds(text: str) -> int | None:
    folded = " ".join(str(text).casefold().split())
    compact = re.sub(r"\s+", "", str(text))

    hours = 0
    minutes = 0
    matched = False
    hour_match = re.search(r"(\d+)\s*(?:hours?|hrs?)\b", folded)
    minute_match = re.search(r"(\d+)\s*(?:minutes?|mins?)\b", folded)
    if hour_match:
        hours = int(hour_match.group(1))
        matched = True
    if minute_match:
        minutes = int(minute_match.group(1))
        matched = True

    if not matched:
        hour_match = re.search(r"(\d+)(?:小时|小時|时|時)", compact)
        minute_match = re.search(r"(\d+)(?:分钟|分鐘|分种|分鈡)", compact)
        if hour_match:
            hours = int(hour_match.group(1))
            matched = True
        if minute_match:
            minutes = int(minute_match.group(1))
            matched = True

    if not matched:
        return None
    delay = hours * 3600 + minutes * 60
    return delay if delay > 0 else None


def _run_windows_ocr(screenshot_path: Path) -> dict:
    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(_OCR_SCRIPT),
            "-Path",
            str(screenshot_path),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    return json.loads(result.stdout.lstrip("\ufeff").strip())


def _line_score(text: str) -> int:
    folded = str(text).casefold()
    compact = re.sub(r"\s+", "", str(text))
    score = 0
    for token, weight in (
        ("plus plan limit", 12),
        ("limit", 7),
        ("reset", 6),
        ("image generation", 5),
        ("minutes", 4),
        ("hours", 4),
    ):
        if token in folded:
            score += weight
    for token, weight in (
        ("次数已用完", 12),
        ("图片生成", 6),
        ("图像生成", 6),
        ("恢复", 5),
        ("分钟", 4),
        ("小时", 4),
    ):
        if token in compact:
            score += weight
    return score


def _copy_limit_paragraph(lines: list[dict]) -> str:
    candidates = sorted(lines, key=lambda line: _line_score(line.get("text", "")), reverse=True)
    for line in candidates[:4]:
        if _line_score(line.get("text", "")) <= 0:
            continue
        x = int(line.get("x", 0)) + max(2, int(line.get("width", 0)) // 2)
        y = int(line.get("y", 0)) + max(2, int(line.get("height", 0)) // 2)
        pyperclip.copy("")
        pyautogui.click(x, y, clicks=3, interval=0.08)
        time.sleep(0.25)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.35)
        copied = pyperclip.paste().strip()
        pyautogui.press("esc")
        if is_generation_limit_text(copied):
            return copied
    return ""


def detect_generation_limit(screenshot_path: Path) -> GenerationLimitDetection | None:
    screenshot_path = Path(screenshot_path).resolve()
    try:
        payload = _run_windows_ocr(screenshot_path)
    except (OSError, subprocess.SubprocessError, ValueError, json.JSONDecodeError) as exc:
        print(f"[WARN] Image limit OCR check unavailable: {exc}", flush=True)
        return None

    ocr_text = str(payload.get("text", ""))
    if not is_generation_limit_text(ocr_text):
        return None

    copied_text = _copy_limit_paragraph(list(payload.get("lines", [])))
    authoritative_text = copied_text or ocr_text
    delay_seconds = parse_reset_delay_seconds(authoritative_text)
    if delay_seconds is None and copied_text:
        delay_seconds = parse_reset_delay_seconds(ocr_text)

    resume_at = None
    if delay_seconds is not None:
        resume_at = dt.datetime.now() + dt.timedelta(
            seconds=delay_seconds + RESET_SAFETY_BUFFER_SECONDS
        )
    return GenerationLimitDetection(
        text=authoritative_text,
        delay_seconds=delay_seconds,
        resume_at=resume_at,
        source="clipboard" if copied_text else "windows-ocr",
        screenshot_path=screenshot_path,
    )
