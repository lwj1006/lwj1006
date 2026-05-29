"""Batch-send one dynamic target image at a time to ChatGPT.

Put images into ./target. The script uploads exactly one target file per run item,
sends the fixed prompt, then moves that file into ./complete after the prompt is sent.
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

import pyautogui

from chatgpt_batch_pyautogui import (
    COORDS,
    PROJECT_DIR,
    UPLOAD_SETTLE_SECONDS,
    calibrate_coords,
    click_slow,
    load_calibrated_coords,
    paste_text,
    send_prompt,
    take_screenshot,
    wait_for_generation,
    wait_with_echo,
)

TARGET_DIR = PROJECT_DIR / "target"
COMPLETE_DIR = PROJECT_DIR / "complete"
TARGET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
MAX_TARGET_RUNS: int | None = None

FIXED_PROMPT = """
杰作级，最高画质，

仅将上传图片作为角色身份参考，
保留原角色的人物特征、发型、服装、姿势与整体构图，

如果参考图中出现爱芮：必须保留她的高饱和粉色偏高双马尾，双马尾长度为短到中短，集中在头部两侧，呈明显外翘、蓬松、卷曲短束结构；不要画成普通长卷双马尾，不要让双马尾垂到胸口或腰部。额前必须保留清楚的黑色挑染刘海；保留黑色蝴蝶结、耳机式头戴发饰、爱心头饰、粉色机械小翅膀和小恶魔偶像气质。

重新诠释为轻量手绘感二次元插画风格，

柔和淡彩二次元插画，
轻小说插画美术风格，
可爱萌系 anime 风格，

干净的动漫线稿，
纤细草稿感轮廓线，
细腻手绘线条，
以线稿为核心的插画表现，
轻盈线条感，
空气感线稿氛围，

简化版二次元渲染，
降低细节复杂度，
减少材质纹理表现，
柔和二维动画感，
插画化完成效果，

简单赛璐璐上色，
柔和扁平化配色，但不要过淡，
简化阴影结构，

柔和但鲜明的二次元色彩，
清晰颜色分区，
保留角色原本的人物固有色识别度，例如发色、眼睛颜色、发饰、翅膀与代表性小元素，
服装主色不必固定沿用原角色配色，可以根据画面主题与整体色彩关系重新分配，
三位角色可以穿适合当前画面的统一系列服装配色，而不是爱芮只能全粉、南宫羽只能全黑、千夏只能薄荷绿，
角色代表色只需要作为局部点缀或识别线索保留，例如饰边、领结、腰带、小挂饰、图案或发饰，
保留视觉重点颜色，但不要让角色代表色完全支配整套服装，
服装设计保持简洁清爽，不要堆叠过多配饰、复杂花纹、碎小挂件、徽章、文字、蕾丝层、飘带或多层结构，
明亮清新的 anime 配色方案，

使用手绘感的低到中等饱和度颜色，
像水彩、彩铅和淡马克笔混合出的柔和颜色，
保持淡彩氛围，但避免整体低饱和、发白、灰雾化或过度粉彩化，
角色主色要清楚但不刺眼，
服装颜色要比背景更明确，但允许与角色固有色不同；不要高饱和霓虹感，
轻微粉嫩感只用于局部点缀，
温暖奶油肌肤色，

大而柔和的动漫眼睛，
轻微脸红，
温柔自然的表情，
年轻可爱的氛围，

高画面洁净度，
极低渲染噪点，
干净清爽构图，

如果原图存在明显作画 bug，例如多余的手、三只手、手指数量错误、手部明显畸形或肢体穿插，可以顺手修正为自然合理的手部与肢体结构；不强制大幅修改原图姿势与构图。

避免半写实动漫风，
避免游戏宣传图风格，
避免高厚涂渲染，
避免油画感，
避免厚重笔触，
避免油亮皮肤，
避免电影级光影，
避免戏剧化阴影，
避免真实渲染，
避免3D感，
避免厚重材质，
避免过度细节，
避免杂乱画面，
避免整体颜色太淡，
避免画面发白，
避免低饱和雾化，
避免服装主色被冲淡，
避免三人服装配色被固定成各自代表色的大面积套用，
避免爱芮整套服装总是粉色、南宫羽整套服装总是黑色、千夏整套服装总是薄荷绿，
避免服装过于花哨导致画面杂乱，
避免复杂图案、过多小饰品、过多挂件和过密装饰线，
避免AI感高饱和糖果色，
避免过强对比和霓虹配色
""".strip()


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
    print("Upload: opening plus menu", flush=True)
    click_slow(*COORDS["plus_button"], after=1.0)
    print("Upload: choosing add photo/file menu item", flush=True)
    click_slow(*COORDS["add_photo_file_menu"], after=2.0)

    print("Upload: focusing file-name input", flush=True)
    click_slow(*COORDS["file_name_input"], after=0.3)
    paste_text(f'"{path}"')
    pyautogui.press("enter")

    wait_with_echo(UPLOAD_SETTLE_SECONDS, "Upload settle")


def process_target_file(path: Path, run_number: int) -> None:
    print("=" * 72, flush=True)
    print(f"[{run_number:02d}] Starting target file", flush=True)
    print(f"[{run_number:02d}] file: {path.name}", flush=True)

    upload_target_file(path)
    send_prompt(FIXED_PROMPT)
    take_screenshot(f"target_{run_number:02d}_sent")

    moved_to = move_to_complete(path)
    print(f"[{run_number:02d}] moved to complete: {moved_to}", flush=True)

    wait_for_generation(run_number)


def main() -> None:
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.15

    ensure_target_dirs()

    if "--calibrate" in sys.argv:
        calibrate_coords()
    else:
        load_calibrated_coords()

    print(f"Target dir: {TARGET_DIR}", flush=True)
    print(f"Complete dir: {COMPLETE_DIR}", flush=True)
    print("This script uploads exactly one target file per prompt.", flush=True)
    time.sleep(2)

    run_number = 1
    while True:
        if MAX_TARGET_RUNS is not None and run_number > MAX_TARGET_RUNS:
            print(f"Reached MAX_TARGET_RUNS={MAX_TARGET_RUNS}.", flush=True)
            return

        target_file = next_target_file()
        if target_file is None:
            print("No target files left. Done.", flush=True)
            return

        process_target_file(target_file, run_number)
        run_number += 1


if __name__ == "__main__":
    main()
