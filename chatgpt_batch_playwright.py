import argparse
import asyncio
import datetime as dt
import json
import random
import sys
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PROJECT_DIR = Path(__file__).resolve().parent
FEEDBACK_DIR = PROJECT_DIR / "feedback"
PROMPT_LOG_FILE = FEEDBACK_DIR / "prompt_log.jsonl"
FEEDBACK_LOG_FILE = FEEDBACK_DIR / "feedback_log.jsonl"
SCREENSHOT_DIR = PROJECT_DIR / "screenshots"
PLAYWRIGHT_PROFILE_DIR = PROJECT_DIR / "playwright-profile"
CHATGPT_IMAGES_URL = "https://chatgpt.com/images/"

TOTAL_RUNS = 30
CHECK_INTERVAL_SECONDS = 150
GROUP_SIZE_WEIGHTS = [1]
MOUSOU_TENSHI_CHARACTERS = ["南宫", "爱芮", "千夏"]

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

from art_direction_options import (  # noqa: E402
    ART_DIRECTION_PLANS,
    choose_plan_and_action,
    collect_cooldown_tags,
    propagation_profile_for,
)
from art_direction_templates import prompt_for_art_direction, prompt_template_name  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ChatGPT image batch automation through Playwright. Does not control the real mouse or keyboard.",
    )
    parser.add_argument("--runs", type=int, default=TOTAL_RUNS)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--headless", action="store_true", help="Run browser without a visible window.")
    parser.add_argument("--profile", type=Path, default=PLAYWRIGHT_PROFILE_DIR)
    parser.add_argument("--url", default=CHATGPT_IMAGES_URL)
    parser.add_argument("--dry-run", action="store_true", help="Build and log prompts but do not send to ChatGPT.")
    parser.add_argument("--login-only", action="store_true", help="Open ChatGPT and save login state, without running a batch.")
    parser.add_argument(
        "--login-wait",
        type=int,
        default=180,
        help="Seconds to wait for manual login if the ChatGPT composer is not available.",
    )
    parser.add_argument(
        "--generation-wait",
        type=int,
        default=CHECK_INTERVAL_SECONDS,
        help="Seconds to wait after sending each prompt before taking a review screenshot.",
    )
    return parser.parse_args()


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


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, set):
        return sorted(_json_safe(item) for item in value)
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def append_jsonl(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_json_safe(entry), ensure_ascii=False) + "\n")


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
            "executor": "playwright",
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
            "executor": "playwright",
            "run_number": run_number,
            "character": character_name,
            "screenshot_path": str(screenshot_path),
            "status": "needs_artist_review",
            "issues": ["占位记录：等待人工复核最新图片后补写。"],
            "next_prompt_adjustment": "等待画师复核",
        },
    )


def validate_reference_files() -> None:
    all_reference_files = [
        path
        for reference_files in CHARACTER_REFERENCES.values()
        for path in reference_files
    ]
    missing = [p for p in all_reference_files if not Path(p).exists()]
    if missing:
        raise FileNotFoundError(f"Missing reference files: {missing}")


async def wait_with_echo(seconds: int, label: str) -> None:
    for remaining in range(seconds, 0, -1):
        if remaining <= 20 or remaining % 30 == 0:
            print(f"{label}: {remaining}s remaining", flush=True)
        await asyncio.sleep(1)


async def first_available(page, selectors: list[str], timeout: int = 1500):
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            await locator.wait_for(state="attached", timeout=timeout)
            return locator
        except Exception:
            continue
    return None


async def composer_locator(page):
    selectors = [
        "#prompt-textarea",
        "div.ProseMirror[contenteditable='true']",
        "div[contenteditable='true'][data-lexical-editor='true']",
        "textarea[placeholder*='Message']",
        "textarea[placeholder*='Send']",
        "textarea",
    ]
    return await first_available(page, selectors, timeout=2000)


async def wait_for_composer(page, login_wait_seconds: int):
    composer = await composer_locator(page)
    if composer:
        return composer

    print("Composer not found. If the browser asks for login, complete it in the Playwright window.", flush=True)
    deadline = dt.datetime.now() + dt.timedelta(seconds=login_wait_seconds)
    while dt.datetime.now() < deadline:
        composer = await composer_locator(page)
        if composer:
            return composer
        await asyncio.sleep(2)

    raise RuntimeError("ChatGPT composer was not found. Login may not be complete, or the page selectors changed.")


async def upload_reference_images(page, reference_files: list[str]) -> list[str]:
    upload_files = [str(Path(path)) for path in reference_files]
    print(f"Upload: attaching reference files: {' '.join(upload_files)}", flush=True)

    file_input = page.locator("input[type='file']").first
    try:
        await file_input.set_input_files(upload_files, timeout=3000)
        return upload_files
    except Exception:
        pass

    attach_button = await first_available(
        page,
        [
            "button[data-testid='composer-plus-btn']",
            "button[aria-label*='Attach']",
            "button[aria-label*='Upload']",
            "button[aria-label*='添加']",
            "button[aria-label*='上传']",
            "button:has-text('添加照片')",
            "button:has-text('Upload')",
        ],
        timeout=1000,
    )
    if not attach_button:
        raise RuntimeError("Could not find ChatGPT attach/upload button.")

    try:
        async with page.expect_file_chooser(timeout=8000) as file_chooser_info:
            await attach_button.click()
        file_chooser = await file_chooser_info.value
    except Exception:
        await attach_button.click()
        menu_item = await first_available(
            page,
            [
                "div[role='menuitem']:has-text('Upload')",
                "div[role='menuitem']:has-text('上传')",
                "div[role='menuitem']:has-text('添加照片')",
                "button:has-text('Upload')",
                "button:has-text('上传')",
                "button:has-text('添加照片')",
            ],
            timeout=2000,
        )
        if not menu_item:
            raise RuntimeError("Could not find ChatGPT upload menu item after opening the attach menu.")
        async with page.expect_file_chooser(timeout=8000) as file_chooser_info:
            await menu_item.click()
        file_chooser = await file_chooser_info.value

    await file_chooser.set_files(upload_files)
    return upload_files


async def fill_prompt(page, prompt: str) -> None:
    composer = await wait_for_composer(page, login_wait_seconds=30)
    await composer.click()
    try:
        await composer.fill(prompt)
    except Exception:
        await page.keyboard.insert_text(prompt)


async def click_send(page) -> None:
    send_button = await first_available(
        page,
        [
            "button[data-testid='send-button']",
            "button[aria-label*='Send']",
            "button[aria-label*='发送']",
            "button:has(svg):near(#prompt-textarea)",
        ],
        timeout=2000,
    )
    if not send_button:
        raise RuntimeError("Could not find ChatGPT send button.")
    await send_button.click()


async def take_screenshot(page, label: str) -> Path:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"{label}_{timestamp}.png"
    await page.screenshot(path=str(path), full_page=False)
    return path


async def run_batch(args: argparse.Namespace) -> None:
    try:
        from playwright.async_api import async_playwright
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Playwright is not installed.\n"
            "Install it with:\n"
            "  python -m pip install playwright\n"
            "  python -m playwright install chromium\n"
        ) from exc

    validate_reference_files()
    args.profile.mkdir(parents=True, exist_ok=True)

    print(
        f"Fenjue 3.0 Playwright executor active: {len(ART_DIRECTION_PLANS)} viral character plans available.",
        flush=True,
    )
    print("This executor controls only its browser context, not your real mouse or keyboard.", flush=True)

    recent_visual_tags: list[str] = []
    total_runs = 1 if args.once else args.runs

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(args.profile),
            headless=args.headless,
            viewport={"width": 1440, "height": 1000},
            accept_downloads=True,
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(args.url, wait_until="domcontentloaded")
        await wait_for_composer(page, args.login_wait)

        if args.login_only:
            print("Login state is ready and saved in the Playwright profile.", flush=True)
            print("You can close the browser window now, or press Ctrl+C in this terminal.", flush=True)
            while True:
                await asyncio.sleep(5)

        for run_number in range(1, total_runs + 1):
            character_name, reference_files = choose_character_group()
            art_plan, action_style = choose_plan_and_action(character_name, recent_visual_tags)
            propagation_profile = propagation_profile_for(character_name)
            theme = art_plan["outfit_direction"]
            scene = art_plan["spatial_structure"]
            pose = action_style["body_silhouette"]
            lighting = art_plan["lighting_behavior"]
            mood = art_plan["color_strategy"]
            prompt_name = prompt_template_name(0)
            prompt = prompt_for_art_direction(character_name, art_plan, action_style)

            print("=" * 72, flush=True)
            print(f"[{run_number:02d}/{total_runs}] character: {character_name}", flush=True)
            print(f"[{run_number:02d}] art plan: {art_plan['name']}", flush=True)
            print(f"[{run_number:02d}] action style: {action_style['name']}", flush=True)
            print(f"[{run_number:02d}] references: {reference_files}", flush=True)
            print(f"[{run_number:02d}] visual device: {art_plan['visual_device']}", flush=True)

            uploaded_files: list[str] = []
            if not args.dry_run:
                await wait_for_composer(page, args.login_wait)
                uploaded_files = await upload_reference_images(page, reference_files)
                await wait_with_echo(8, "Upload settle")

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

            if not args.dry_run:
                await fill_prompt(page, prompt)
                await wait_with_echo(5, "Before send")
                await click_send(page)
                sent_screenshot = await take_screenshot(page, f"playwright_run_{run_number:02d}_sent")
                print(f"[{run_number:02d}] sent screenshot: {sent_screenshot}", flush=True)
                await wait_with_echo(args.generation_wait, f"[{run_number:02d}] generation check")
                screenshot_path = await take_screenshot(page, f"playwright_run_{run_number:02d}_check")
                log_feedback_placeholder(run_id, run_number, character_name, screenshot_path)
                print(f"[{run_number:02d}] review screenshot: {screenshot_path}", flush=True)

            recent_visual_tags.extend(collect_cooldown_tags(art_plan, action_style))
            recent_visual_tags = recent_visual_tags[-12:]

        await context.close()


def main() -> None:
    args = parse_args()
    asyncio.run(run_batch(args))


if __name__ == "__main__":
    main()
