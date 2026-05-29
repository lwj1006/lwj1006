import ctypes
import datetime as dt
import json
import random
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PROJECT_DIR = Path(__file__).resolve().parent

import pyautogui
import pyperclip

from art_direction_options import (
    ART_DIRECTION_PLANS,
    OUTFIT_DIRECTIONS as CLOTHING_THEMES,
    choose_action_style,
    choose_plan_and_action,
    collect_cooldown_tags,
    propagation_profile_for,
)
from art_direction_templates import prompt_for_art_direction, prompt_template_name


# ChatGPT desktop batch automation.
# Adjust these coordinates if the ChatGPT window position/size changes.

REFERENCE_FILES = [
    # r"D:\workspace\1.jpeg",
    # r"D:\workspace\2.jpeg",
    # r"D:\workspace\3.jpg",
    # r"D:\workspace\4.png",
    # # r"D:\workspace\2.png",
    # r"D:\workspace\5.png",
    # r"D:\workspace\6.jpg",
    str(PROJECT_DIR / "assets" / "千夏.png"),
    str(PROJECT_DIR / "assets" / "南宫.png"),
    str(PROJECT_DIR / "assets" / "爱芮.jpeg"),
]

TOTAL_RUNS = 99

# Random character mode. Each run can upload one, two, or three character references.
CHARACTER_REFERENCES = {
    "南宫": [
        str(PROJECT_DIR / "assets" / "南宫.png"),
        str(PROJECT_DIR / "assets" / "南宫2.png"),
        str(PROJECT_DIR / "assets" / "南宫3.png"),
    ],
    "爱芮": [
        str(PROJECT_DIR / "assets" / "爱芮.png"),
        str(PROJECT_DIR / "assets" / "爱芮2.png"),
        str(PROJECT_DIR / "assets" / "爱芮3.png"),
        str(PROJECT_DIR / "assets" / "爱芮4.jpeg"),
        str(PROJECT_DIR / "assets" / "爱芮5.png"),
    ],
    "千夏": [
        str(PROJECT_DIR / "assets" / "千夏.png"),
        str(PROJECT_DIR / "assets" / "千夏1.jpg"),
        str(PROJECT_DIR / "assets" / "千夏2.png"),
        str(PROJECT_DIR / "assets" / "千夏3.png"),
        str(PROJECT_DIR / "assets" / "千夏4.jpg"),
        str(PROJECT_DIR / "assets" / "千夏5.png"),
    ],
    "丹": [
        str(PROJECT_DIR / "assets" / "dan.png"),
        str(PROJECT_DIR / "assets" / "dan2.png"),
        str(PROJECT_DIR / "assets" / "丹.png"),
    ],
    "星见雅": [
        str(PROJECT_DIR / "assets" / "星见雅1.png"),
        str(PROJECT_DIR / "assets" / "星见雅2.png"),
        str(PROJECT_DIR / "assets" / "星见雅3.png"),
    ],
    "仪玄": [
        str(PROJECT_DIR / "assets" / "仪玄1.png"),
        str(PROJECT_DIR / "assets" / "仪玄2.jpg"),
        str(PROJECT_DIR / "assets" / "仪玄3.png"),
    ],
}
MOUSOU_TENSHI_CHARACTERS = ["南宫", "爱芮", "千夏"]
# Art direction mode is single-character-first. Multi-character prompt logic is kept
# in the legacy templates, but the production batch does not use it by default.
GROUP_SIZE_WEIGHTS = [1]
CHARACTER_SEQUENCE = ["南宫", "爱芮", "千夏", "丹", "星见雅", "仪玄"]
RUNS_PER_CHARACTER_PER_THEME = 2
REFERENCE_FILES = CHARACTER_REFERENCES["丹"][:]
TOTAL_RUNS = 999

CHECK_INTERVAL_SECONDS = 150
MAX_UPLOAD_SETTLE_SECONDS = 15
TEXT_BEFORE_SEND_SECONDS = 10
ECHO_COUNTDOWN_LAST_SECONDS = 20
SINGLE_CLICK_HOLD_SECONDS = 0.06
SEND_CLICK_HOLD_SECONDS = 0.14
SEND_RELEASE_SETTLE_SECONDS = 0.35
SEND_MOUSE_AWAY_OFFSET = (-220, -90)
SAFE_SCREEN_MARGIN = 8
SAFETY_SHUTDOWN_TARGET_TIME = "12:00"

SCREENSHOT_DIR = PROJECT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
USE_RUNTIME_UPLOAD_COPIES = False
RUNTIME_UPLOAD_DIR = PROJECT_DIR / "runtime_uploads"
if USE_RUNTIME_UPLOAD_COPIES:
    RUNTIME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
FEEDBACK_DIR = PROJECT_DIR / "feedback"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
PROMPT_LOG_FILE = FEEDBACK_DIR / "prompt_log.jsonl"
FEEDBACK_LOG_FILE = FEEDBACK_DIR / "feedback_log.jsonl"
CHATGPT_IMAGES_URL = "https://chatgpt.com/images/"


COORDS = {
    # Main ChatGPT input area and Windows file picker positions.
    "plus_button": (778, 979),
    "add_photo_file_menu": (840, 712),
    "file_name_input": (760, 930),
    "send_button": (1404, 979),
}

CALIBRATION_FILE = PROJECT_DIR / "config" / "chatgpt_batch_coords.json"
USED_CLOTHING_THEMES_FILE = PROJECT_DIR / "config" / "used_clothing_themes.json"
CLOTHING_THEME_USAGE_LOG_FILE = PROJECT_DIR / "config" / "clothing_theme_usage_log.jsonl"


def upload_settle_seconds(reference_count: int) -> int:
    """Wait 5s for one or two files, +5s for each additional pair, capped at 15s."""
    reference_count = max(1, int(reference_count))
    return min(MAX_UPLOAD_SETTLE_SECONDS, 5 + ((reference_count - 1) // 2) * 5)


def prepare_upload_files(reference_files: list[str] | None = None) -> list[str]:
    reference_files = reference_files or REFERENCE_FILES
    if not USE_RUNTIME_UPLOAD_COPIES:
        return [str(Path(source)) for source in reference_files]

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    upload_files: list[str] = []
    for index, source in enumerate(reference_files, start=1):
        source_path = Path(source)
        target = RUNTIME_UPLOAD_DIR / f"{source_path.stem}_upload_{timestamp}_{index}{source_path.suffix}"
        shutil.copy2(source_path, target)
        upload_files.append(str(target))
    return upload_files


def choose_character_group() -> tuple[str, list[str]]:
    group_size = random.choice(GROUP_SIZE_WEIGHTS)
    if group_size == 1:
        selected_names = random.sample(list(CHARACTER_REFERENCES.keys()), k=1)
    else:
        selected_names = random.sample(MOUSOU_TENSHI_CHARACTERS, k=min(group_size, len(MOUSOU_TENSHI_CHARACTERS)))
    character_label = "、".join(selected_names)
    reference_files = [
        file_path
        for name in selected_names
        for file_path in CHARACTER_REFERENCES[name]
    ]
    return character_label, reference_files


def reference_files_for_character(character_name: str) -> list[str]:
    return CHARACTER_REFERENCES[character_name][:]


def choose_art_plan_for_outfit(outfit_direction: str) -> dict:
    matching_plans = [
        plan for plan in ART_DIRECTION_PLANS
        if plan["outfit_direction"] == outfit_direction
    ]
    return random.choice(matching_plans or ART_DIRECTION_PLANS)


def load_calibrated_coords() -> None:
    global COORDS

    if not CALIBRATION_FILE.exists():
        calibrate_coords()
        return

    with CALIBRATION_FILE.open("r", encoding="utf-8") as f:
        saved = json.load(f)

    missing_keys = [key for key in COORDS if key not in saved]
    if missing_keys:
        print(f"Calibration file is missing coordinates: {missing_keys}")
        calibrate_coords()
        return

    for key in COORDS:
        if key in saved and len(saved[key]) == 2:
            COORDS[key] = (int(saved[key][0]), int(saved[key][1]))

    print(f"Loaded calibrated coordinates from {CALIBRATION_FILE}")
    print(f"Current coordinates: {COORDS}")


def save_calibrated_coords() -> None:
    CALIBRATION_FILE.write_text(
        json.dumps(COORDS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved calibrated coordinates to {CALIBRATION_FILE}")


def capture_mouse_position(label: str, seconds: int = 5) -> tuple[int, int]:
    print(f"{label}: move your mouse there within {seconds} seconds...")
    for remaining in range(seconds, 0, -1):
        print(f"  {remaining}...")
        time.sleep(1)
    pos = pyautogui.position()
    print(f"  captured {label}: ({pos.x}, {pos.y})")
    return (pos.x, pos.y)


def calibrate_coords() -> None:
    print("Calibration mode: keep ChatGPT visible at the position/size you will use.")
    print("Do not click during the countdown unless instructed.")

    COORDS["plus_button"] = capture_mouse_position(
        "Hover over the ChatGPT input-box plus button",
        seconds=5,
    )

    print("Opening the plus menu so you can hover over '添加照片和文件'.")
    click_slow(*COORDS["plus_button"], after=1.0)
    COORDS["add_photo_file_menu"] = capture_mouse_position(
        "Hover over the '添加照片和文件' menu item",
        seconds=5,
    )

    print("Opening the Windows file picker so you can hover over the file-name input box.")
    click_slow(*COORDS["add_photo_file_menu"], after=2.0)
    COORDS["file_name_input"] = capture_mouse_position(
        "Hover over the Windows file picker file-name input box",
        seconds=5,
    )

    print("Closing the file picker before capturing the send button.")
    pyautogui.press("esc")
    time.sleep(1)

    COORDS["send_button"] = capture_mouse_position(
        "Hover over the circular send button at the right side of the ChatGPT input box",
        seconds=5,
    )

    save_calibrated_coords()


MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def virtual_screen_bounds() -> tuple[int, int, int, int]:
    user32 = ctypes.windll.user32
    left = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
    top = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
    width = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    height = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    return left, top, left + width - 1, top + height - 1


def get_cursor_pos() -> tuple[int, int]:
    point = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def pointer_is_in_failsafe_corner() -> bool:
    x, y = get_cursor_pos()
    left, top, right, bottom = virtual_screen_bounds()
    return (
        (x <= left and y <= top)
        or (x <= left and y >= bottom)
        or (x >= right and y <= top)
        or (x >= right and y >= bottom)
    )


def wait_until_pointer_is_safe() -> None:
    warned = False
    while pointer_is_in_failsafe_corner():
        if not warned:
            print(
                "Mouse is in a virtual-screen corner. Move it away from the corner to continue.",
                flush=True,
            )
            warned = True
        time.sleep(1)


def clamp_to_virtual_screen(x: int, y: int) -> tuple[int, int]:
    left, top, right, bottom = virtual_screen_bounds()
    return (
        max(left + SAFE_SCREEN_MARGIN, min(right - SAFE_SCREEN_MARGIN, x)),
        max(top + SAFE_SCREEN_MARGIN, min(bottom - SAFE_SCREEN_MARGIN, y)),
    )


def guarded_move_to(x: int, y: int, duration: float = 0.25) -> None:
    wait_until_pointer_is_safe()
    x, y = clamp_to_virtual_screen(x, y)
    ctypes.windll.user32.SetCursorPos(int(x), int(y))
    if duration:
        time.sleep(duration)


def native_left_click() -> None:
    user32 = ctypes.windll.user32
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(SINGLE_CLICK_HOLD_SECONDS)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def native_left_click_with_hold(hold_seconds: float) -> None:
    user32 = ctypes.windll.user32
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(hold_seconds)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def click_slow(
    x: int,
    y: int,
    after: float = 1.0,
    move_away_offset: tuple[int, int] | None = None,
) -> None:
    guarded_move_to(x, y, duration=0.25)
    time.sleep(0.25)
    native_left_click()

    if move_away_offset is not None:
        away_x, away_y = clamp_to_virtual_screen(x + move_away_offset[0], y + move_away_offset[1])
        guarded_move_to(away_x, away_y, duration=0.15)

    time.sleep(after)


def click_send_button() -> None:
    x, y = COORDS["send_button"]
    guarded_move_to(x, y, duration=0.25)
    time.sleep(0.25)
    native_left_click_with_hold(SEND_CLICK_HOLD_SECONDS)
    time.sleep(SEND_RELEASE_SETTLE_SECONDS)

    away_x, away_y = clamp_to_virtual_screen(
        x + SEND_MOUSE_AWAY_OFFSET[0],
        y + SEND_MOUSE_AWAY_OFFSET[1],
    )
    guarded_move_to(away_x, away_y, duration=0.15)
    time.sleep(1.0)


def paste_text(text: str) -> None:
    pyperclip.copy(text)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)


def wait_with_echo(seconds: int, label: str) -> None:
    """Wait with a quiet countdown that only prints during the final seconds."""
    seconds = max(0, int(seconds))
    if seconds == 0:
        return

    print(f"{label}: waiting {seconds}s", flush=True)
    quiet_seconds = max(0, seconds - ECHO_COUNTDOWN_LAST_SECONDS)
    if quiet_seconds:
        time.sleep(quiet_seconds)

    for remaining in range(min(seconds, ECHO_COUNTDOWN_LAST_SECONDS), 0, -1):
        print(f"{label}: {remaining}s remaining", flush=True)
        time.sleep(1)


def upload_reference_images(reference_files: list[str]) -> list[str]:
    print("Upload: opening plus menu", flush=True)
    # Use the ChatGPT input plus menu instead of Ctrl+U.
    click_slow(*COORDS["plus_button"], after=1.0)
    print("Upload: choosing add photo/file menu item", flush=True)
    click_slow(*COORDS["add_photo_file_menu"], after=2.0)

    upload_files = prepare_upload_files(reference_files)
    file_list = " ".join(f'"{p}"' for p in upload_files)
    time.sleep(0.25)

    print("Upload: focusing file-name input", flush=True)
    click_slow(*COORDS["file_name_input"], after=0.3)
    print(f"Upload: selecting reference files: {file_list}", flush=True)
    paste_text(file_list)
    pyautogui.press("enter")

    # Wait for ChatGPT to attach/process thumbnails before typing text.
    wait_with_echo(upload_settle_seconds(len(upload_files)), "Upload settle")
    return upload_files


def send_prompt(prompt: str) -> None:
    print("Prompt: pasting text", flush=True)
    paste_text(prompt)

    # Upload completion can leave the send button inactive briefly.
    wait_with_echo(TEXT_BEFORE_SEND_SECONDS, "Before send")
    print("Prompt: clicking send button", flush=True)
    click_send_button()


def take_screenshot(label: str) -> Path:
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"{label}_{timestamp}.png"
    pyautogui.screenshot(str(path))
    return path


def wait_for_generation(run_number: int) -> Path:
    # The script cannot visually understand completion by itself without OCR/CV.
    # It captures a check screenshot every 30 seconds, then assumes the generation
    # is complete after one interval, matching the manual workflow used here.
    wait_with_echo(CHECK_INTERVAL_SECONDS, f"[{run_number:02d}] generation check")
    path = take_screenshot(f"run_{run_number:02d}_check")
    print(f"[{run_number:02d}] check screenshot: {path}")
    return path


def open_images_page_for_review() -> None:
    print(f"Review: opening {CHATGPT_IMAGES_URL}", flush=True)
    webbrowser.open(CHATGPT_IMAGES_URL, new=0, autoraise=True)
    time.sleep(3)


def append_jsonl(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_json_safe(entry), ensure_ascii=False) + "\n")


def _json_safe(value):
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, set):
        return sorted(_json_safe(item) for item in value)
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def log_prompt(
    run_number: int,
    character_name: str,
    reference_files: list[str],
    uploaded_files: list[str],
    theme: str,
    scene: str,
    pose: str,
    lighting: str,
    mood: str,
    prompt_name: str,
    prompt: str,
    propagation_profile: dict | None = None,
) -> str:
    run_id = dt.datetime.now().strftime(f"%Y%m%d_%H%M%S_run_{run_number:03d}")
    append_jsonl(
        PROMPT_LOG_FILE,
        {
            "run_id": run_id,
            "time": dt.datetime.now().isoformat(timespec="seconds"),
            "run_number": run_number,
            "character": character_name,
            "reference_files": reference_files,
            "uploaded_files": uploaded_files,
            "theme": theme,
            "scene": scene,
            "pose": pose,
            "lighting": lighting,
            "mood": mood,
            "prompt_template": prompt_name,
            "propagation_profile": propagation_profile,
            "prompt": prompt,
        },
    )
    print(f"[{run_number:02d}] prompt log -> {PROMPT_LOG_FILE}", flush=True)
    return run_id


def log_feedback_placeholder(
    run_id: str,
    run_number: int,
    character_name: str,
    screenshot_path: Path,
) -> None:
    append_jsonl(
        FEEDBACK_LOG_FILE,
        {
            "run_id": run_id,
            "time": dt.datetime.now().isoformat(timespec="seconds"),
            "run_number": run_number,
            "character": character_name,
            "screenshot_path": str(screenshot_path),
            "status": "needs_artist_review",
            "composition": "",
            "character_identity": "",
            "clothing_match": "",
            "scene_match": "",
            "orientation": "",
            "issues": ["占位记录：必须结合 prompt_log 和最新图片人工复核后补写，不代表已完成 feedback"],
            "next_prompt_adjustment": "等待画师复核",
        },
    )
    print(f"[{run_number:02d}] feedback placeholder -> {FEEDBACK_LOG_FILE}", flush=True)



def load_used_clothing_themes() -> list[str]:
    if not USED_CLOTHING_THEMES_FILE.exists():
        return []

    try:
        data = json.loads(USED_CLOTHING_THEMES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Used clothing theme file is invalid; starting a new cycle: {USED_CLOTHING_THEMES_FILE}")
        return []

    if not isinstance(data, list):
        return []

    valid_themes = set(CLOTHING_THEMES)
    return [theme for theme in data if isinstance(theme, str) and theme in valid_themes]


def save_used_clothing_themes(used_themes: list[str]) -> None:
    USED_CLOTHING_THEMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    USED_CLOTHING_THEMES_FILE.write_text(
        json.dumps(used_themes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def choose_unused_clothing_theme(used_themes: list[str]) -> str:
    valid_used = [theme for theme in used_themes if theme in CLOTHING_THEMES]
    used_themes[:] = valid_used

    available = [theme for theme in CLOTHING_THEMES if theme not in used_themes]
    if not available:
        print(
            "All clothing themes have been used in the current cycle. Clearing current-cycle history and starting a new cycle.",
            flush=True,
        )
        print(f"Permanent clothing usage log is kept at: {CLOTHING_THEME_USAGE_LOG_FILE}", flush=True)
        used_themes.clear()
        save_used_clothing_themes(used_themes)
        available = CLOTHING_THEMES[:]

    return random.choice(available)



def append_clothing_theme_usage_log(theme: str, used_count: int) -> None:
    CLOTHING_THEME_USAGE_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "time": dt.datetime.now().isoformat(timespec="seconds"),
        "theme": theme,
        "cycle_used_count": used_count,
        "cycle_total": len(CLOTHING_THEMES),
    }
    with CLOTHING_THEME_USAGE_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def mark_clothing_theme_used(theme: str, used_themes: list[str]) -> None:
    if theme not in CLOTHING_THEMES:
        return
    if theme not in used_themes:
        used_themes.append(theme)
    save_used_clothing_themes(used_themes)
    append_clothing_theme_usage_log(theme, len(used_themes))
    print(
        f"Clothing theme current cycle: {len(used_themes)}/{len(CLOTHING_THEMES)} used -> {USED_CLOTHING_THEMES_FILE}",
        flush=True,
    )
    print(f"Clothing theme permanent log -> {CLOTHING_THEME_USAGE_LOG_FILE}", flush=True)

def schedule_safety_shutdown() -> None:
    now = dt.datetime.now()
    target_hour, target_minute = [int(part) for part in SAFETY_SHUTDOWN_TARGET_TIME.split(":", 1)]
    target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if target <= now:
        target += dt.timedelta(days=1)
    seconds = max(60, int((target - now).total_seconds()))

    subprocess.run(["shutdown.exe", "/a"], check=False)
    subprocess.run(
        [
            "shutdown.exe",
            "/s",
            "/t",
            str(seconds),
            "/c",
            "ChatGPT batch safety shutdown at 12:00",
        ],
        check=False,
    )
    print(f"Safety shutdown scheduled for {target:%Y-%m-%d %H:%M:%S}")


def shutdown_now() -> None:
    subprocess.run(
        [
            "shutdown.exe",
            "/s",
            "/t",
            "30",
            "/c",
            "ChatGPT batch completed",
        ],
        check=False,
    )


def main() -> None:
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.15

    if "--calibrate" in sys.argv or not CALIBRATION_FILE.exists():
        calibrate_coords()
    else:
        load_calibrated_coords()

    all_reference_files = [
        path
        for reference_files in CHARACTER_REFERENCES.values()
        for path in reference_files
    ]
    missing = [p for p in all_reference_files if not Path(p).exists()]
    if missing:
        raise FileNotFoundError(f"Missing reference files: {missing}")

    print("Keep ChatGPT desktop open, unlocked, and focused.")
    print("Press Ctrl+C in this terminal to abort. Moving the mouse to a virtual-screen corner pauses the next click.")
    if "--shutdown" in sys.argv:
        schedule_safety_shutdown()
    else:
        print("Safety shutdown is disabled for this feedback run. Use --shutdown to enable it.")
    time.sleep(3)

    print(
        f"Fenjue 3.0 social anime character pipeline active: {len(ART_DIRECTION_PLANS)} viral character plans available. "
        "Priority: thumbnail impact, character personality, fantasy symbols, and viewer interaction.",
        flush=True,
    )

    total_runs = TOTAL_RUNS
    if "--runs" in sys.argv:
        runs_index = sys.argv.index("--runs")
        if runs_index + 1 >= len(sys.argv):
            raise ValueError("--runs requires a number")
        total_runs = int(sys.argv[runs_index + 1])

    recent_visual_tags: list[str] = []
    used_clothing_themes = load_used_clothing_themes()
    run_number = 1
    stop_requested = False

    while run_number <= total_runs and not stop_requested:
        theme = choose_unused_clothing_theme(used_clothing_themes)
        theme_completed = True
        theme_total_runs = len(CHARACTER_SEQUENCE) * RUNS_PER_CHARACTER_PER_THEME
        print("=" * 72, flush=True)
        print(
            f"Theme batch selected: {theme} "
            f"({theme_total_runs} runs: {len(CHARACTER_SEQUENCE)} characters x {RUNS_PER_CHARACTER_PER_THEME})",
            flush=True,
        )

        for character_name in CHARACTER_SEQUENCE:
            if stop_requested:
                break

            for character_repeat in range(1, RUNS_PER_CHARACTER_PER_THEME + 1):
                if run_number > total_runs:
                    theme_completed = False
                    break

                reference_files = reference_files_for_character(character_name)
                art_plan = choose_art_plan_for_outfit(theme)
                action_style = choose_action_style(character_name, recent_visual_tags)
                propagation_profile = propagation_profile_for(character_name)
                scene = art_plan["spatial_structure"]
                pose = action_style["body_silhouette"]
                lighting = art_plan["lighting_behavior"]
                mood = art_plan["color_strategy"]
                template_index = 0
                concept = art_plan["graphic_concept"]
                prompt_name = prompt_template_name(template_index)
                prompt = prompt_for_art_direction(character_name, art_plan, action_style)

                print("=" * 72, flush=True)
                print(f"[{run_number:02d}/{total_runs}] Starting run", flush=True)
                print(f"[{run_number:02d}] theme repeat: {character_name} {character_repeat}/{RUNS_PER_CHARACTER_PER_THEME}", flush=True)
                print(f"[{run_number:02d}] character: {character_name}", flush=True)
                print(f"[{run_number:02d}] references: {reference_files}", flush=True)
                print(f"[{run_number:02d}] clothing theme: {theme}", flush=True)
                print(f"[{run_number:02d}] scene: {scene}", flush=True)
                print(f"[{run_number:02d}] pose: {pose}", flush=True)
                print(f"[{run_number:02d}] lighting: {lighting}", flush=True)
                print(f"[{run_number:02d}] mood: {mood}", flush=True)
                print(f"[{run_number:02d}] art plan: {art_plan['name']}", flush=True)
                print(f"[{run_number:02d}] action style: {action_style['name']}", flush=True)
                print(f"[{run_number:02d}] propagation: {propagation_profile['propagation_translation']}", flush=True)
                print(f"[{run_number:02d}] graphic concept: {concept}", flush=True)
                print(f"[{run_number:02d}] visual device: {art_plan['visual_device']}", flush=True)
                print(f"[{run_number:02d}] material language: {art_plan['material_language']}", flush=True)
                print(f"[{run_number:02d}] recent cooldown tags: {recent_visual_tags}", flush=True)
                print(f"[{run_number:02d}] prompt template: {prompt_name}", flush=True)
                # print(f"[{run_number:02d}] prompt: {prompt}", flush=True)

                uploaded_files = upload_reference_images(reference_files)
                run_id = log_prompt(
                    run_number,
                    character_name,
                    reference_files,
                    uploaded_files,
                    theme,
                    scene,
                    pose,
                    lighting,
                    mood,
                    prompt_name,
                    prompt,
                    propagation_profile,
                )
                send_prompt(prompt)
                take_screenshot(f"run_{run_number:02d}_sent")
                screenshot_path = wait_for_generation(run_number)
                log_feedback_placeholder(run_id, run_number, character_name, screenshot_path)
                recent_visual_tags.extend(collect_cooldown_tags(art_plan, action_style))
                recent_visual_tags = recent_visual_tags[-12:]
                if "--once" in sys.argv or "--review-url" in sys.argv:
                    open_images_page_for_review()

                if "--once" in sys.argv:
                    print("--once completed. Review feedback, adjust prompts if needed, then run again.")
                    theme_completed = False
                    stop_requested = True
                    break

                run_number += 1

            if run_number > total_runs:
                break

        if theme_completed and not stop_requested:
            mark_clothing_theme_used(theme, used_clothing_themes)
        else:
            print(
                f"Theme batch not completed; not marking theme as used: {theme}",
                flush=True,
            )

    print("All runs completed. Safety shutdown remains scheduled.")


if __name__ == "__main__":
    main()


