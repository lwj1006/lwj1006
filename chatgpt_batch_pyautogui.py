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
    choose_compatible_action_style,
    choose_plan_and_action,
    collect_cooldown_tags,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
)

from art_direction_templates import (
    prompt_for_art_direction,
    prompt_template_name,
)
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
    str(PROJECT_DIR / "assets" / "千夏1.jpg"),
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
        str(PROJECT_DIR / "assets" / "千夏1.jpg"),
        str(PROJECT_DIR / "assets" / "千夏2.png"),
        str(PROJECT_DIR / "assets" / "千夏3.png"),
        str(PROJECT_DIR / "assets" / "千夏4.jpg"),
    ],
    "丹": [
        str(PROJECT_DIR / "assets" / "dan.png"),
        str(PROJECT_DIR / "assets" / "dan2.png"),
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
    "叶瞬光": [
        str(PROJECT_DIR / "assets" / "叶瞬光1.png"),
        str(PROJECT_DIR / "assets" / "叶瞬光2.png"),
        str(PROJECT_DIR / "assets" / "叶瞬光3.png"),
    ],
    "席德": [
        str(PROJECT_DIR / "assets" / "席德1.png"),
        str(PROJECT_DIR / "assets" / "席德2.png"),
    ],
    "橘福福": [
        str(PROJECT_DIR / "assets" / "橘福福2.jpeg"),
        str(PROJECT_DIR / "assets" / "橘福福3.png"),
    ],
    "柚叶": [
        str(PROJECT_DIR / "assets" / "柚叶1.png"),
        str(PROJECT_DIR / "assets" / "柚叶2.png"),
        str(PROJECT_DIR / "assets" / "柚叶3.png"),
    ],
    "爱丽丝": [
        str(PROJECT_DIR / "assets" / "爱丽丝1.png"),
        str(PROJECT_DIR / "assets" / "爱丽丝2.png"),
        str(PROJECT_DIR / "assets" / "爱丽丝3.png"),
    ],
    "普罗米娅": [
        str(PROJECT_DIR / "assets" / "普罗米娅1.png"),
        str(PROJECT_DIR / "assets" / "普罗米娅2.png"),
        str(PROJECT_DIR / "assets" / "普罗米娅3.png"),
    ],
    "薇薇安": [
        str(PROJECT_DIR / "assets" / "薇薇安1.png"),
        str(PROJECT_DIR / "assets" / "薇薇安2.png"),
        str(PROJECT_DIR / "assets" / "薇薇安3.png"),
    ],
    "安比": [
        str(PROJECT_DIR / "assets" / "安比1.png"),
        str(PROJECT_DIR / "assets" / "安比2.jpg"),
        str(PROJECT_DIR / "assets" / "安比3.png"),
    ],
    "可琳": [
        str(PROJECT_DIR / "assets" / "可琳1.png"),
        str(PROJECT_DIR / "assets" / "可琳2.png"),
    ],
    "艾莲": [
        str(PROJECT_DIR / "assets" / "艾莲1.png"),
        str(PROJECT_DIR / "assets" / "艾莲2.png"),
        str(PROJECT_DIR / "assets" / "艾莲3.png"),
    ],
    "琉音": [
        str(PROJECT_DIR / "assets" / "琉音1.png"),
        str(PROJECT_DIR / "assets" / "琉音2.png"),
    ],
    "耀嘉音": [
        str(PROJECT_DIR / "assets" / "耀嘉音1.png"),
        str(PROJECT_DIR / "assets" / "耀嘉音2.png"),
        str(PROJECT_DIR / "assets" / "耀嘉音3.png"),
    ],
}
MOUSOU_TENSHI_CHARACTERS = ["南宫", "爱芮", "千夏"]
# Art direction mode is single-character-first. Multi-character prompt logic is kept
# in the legacy templates, but the production batch does not use it by default.
GROUP_SIZE_WEIGHTS = [1]
CHARACTER_SEQUENCE = ["南宫", "爱芮", "千夏", "丹", "星见雅", "仪玄", "叶瞬光", "席德", "橘福福", "柚叶", "爱丽丝", "普罗米娅", "薇薇安", "安比", "可琳", "艾莲", "琉音", "耀嘉音"]
CHARACTERS_PER_BATCH = 3
REFERENCE_FILES = CHARACTER_REFERENCES["丹"][:]
TOTAL_RUNS = 999

CHECK_INTERVAL_SECONDS = 150
MAX_UPLOAD_SETTLE_SECONDS = 15
TEXT_BEFORE_SEND_SECONDS = 10
ECHO_COUNTDOWN_LAST_SECONDS = 20
SINGLE_CLICK_HOLD_SECONDS = 0.06
SEND_CLICK_HOLD_SECONDS = 0.14
SEND_RELEASE_SETTLE_SECONDS = 0.35
POST_CHARACTER_SELECTION_DELAY_SECONDS = 3
SEND_MOUSE_AWAY_OFFSET = (-220, -90)
WORK_REMINDER_INTERVAL = 10
WORK_REMINDER_TEXT = "不要做任何点评 生成图片就可以"
SAFE_SCREEN_MARGIN = 8
SAFETY_SHUTDOWN_TARGET_TIME = "12:00"
LOW_PROBABILITY_SCENE_OUTFIT_CHANCE = 0.08

SCREENSHOT_DIR = PROJECT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
USE_RUNTIME_UPLOAD_COPIES = False
RUNTIME_UPLOAD_DIR = PROJECT_DIR / "runtime_uploads"
if USE_RUNTIME_UPLOAD_COPIES:
    RUNTIME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
FEEDBACK_DIR = PROJECT_DIR / "feedback"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

LOW_PROBABILITY_BRAND_THEMES = [
    theme for theme in CLOTHING_THEMES
    if "Adidas-inspired" in theme or "Yonex-inspired" in theme
]
STRONG_SCENE_ONLY_CLOTHING_THEMES = [
    theme for theme in CLOTHING_THEMES
    if theme in LOW_PROBABILITY_BRAND_THEMES
    or "dark-hosiery" in theme
    or "maid remix" in theme
    or "bridal dress" in theme
]
REGULAR_CLOTHING_THEMES = [
    theme for theme in CLOTHING_THEMES
    if theme not in STRONG_SCENE_ONLY_CLOTHING_THEMES
]
REFERENCE_OUTFIT = "reference-faithful outfit with small fashionable variation"
LIGHT_NOVEL_OUTFIT = "clean light-novel casual outfit, character palette stays recognizable"
YOUNG_CASUAL_OUTFIT = "young casual tops: white short T-shirt, cropped hoodie, sleeveless tank, or off-shoulder knit"
SOFT_DATE_OUTFIT = "soft date outfit: fitted cardigan, simple camisole or blouse, A-line skirt, small shoulder bag, clean and youthful"
CAFE_MAID_OUTFIT = "cafe maid remix outfit, neat apron, ribbons, cute and clean"
BRIDAL_OUTFIT = "romantic flower bridal dress, elegant veil or bouquet, clean and elegant"
FLOWER_FANTASY_OUTFIT = "elegant flower-field fantasy outfit, simplified layers, no weapon requirement"
DARK_HOSIERY_OUTFIT = "rare refined dark-hosiery fashion outfit, restrained and non-fetishized"
YOUTHFUL_CASUAL_OUTFIT = "clean youthful casual outfit, blouse or light cardigan, no stocking emphasis"
PICNIC_OUTFIT = "fresh picnic outfit, short jacket or light cardigan, clear color blocks"
BAKERY_CAFE_OUTFIT = "soft bakery or cafe casual outfit, warm and simple"
SUNNY_STUDIO_OUTFIT = "minimal sunny studio outfit, face and hair identity as the main focus"
PURE_WHITE_OUTFIT = "clean pure-white studio outfit, simple silhouette, character colors as the only accent"
FAIRY_FLOATING_OUTFIT = "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling"
WHITE_SUNDRESS_STRAW_HAT_OUTFIT = "pure white sundress with a straw hat, fresh summer date mood"
BLUE_GINGHAM_DENIM_OUTFIT = "medium-short blue-and-white gingham shirt over a white tank top, denim shorts; shirt worn either tied into a small front-bottom bow or open and unbuttoned"
LIGHT_BLUE_WINDBREAKER_OUTFIT = "soft light-blue windbreaker jacket, white low-neck tank top, athletic shorts, round-frame glasses"
ASYMMETRIC_WHITE_T_OUTFIT = "thin white off-shoulder long T-shirt, green camisole inner layer visible at neckline, shorts"
LACE_OFF_SHOULDER_DRESS_OUTFIT = "lace off-shoulder dress with puff sleeves, clean romantic styling"
BASEBALL_SPECTATOR_OUTFIT = "baseball stadium spectator outfit, casual sporty top, shorts or skirt, cap or small cheering accessory"
BRIGHT_RED_SHORT_DRESS_OUTFIT = "bright red short one-piece dress, youthful clean date styling"
FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT = "five-sleeve white light-sport T-shirt with gray shorts or denim shorts"
SAFE_DAILY_CLOTHING_POOL = [
    LIGHT_NOVEL_OUTFIT,
    YOUNG_CASUAL_OUTFIT,
    SOFT_DATE_OUTFIT,
    YOUTHFUL_CASUAL_OUTFIT,
    PICNIC_OUTFIT,
    BAKERY_CAFE_OUTFIT,
    SUNNY_STUDIO_OUTFIT,
    PURE_WHITE_OUTFIT,
    WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
    BLUE_GINGHAM_DENIM_OUTFIT,
    LIGHT_BLUE_WINDBREAKER_OUTFIT,
    ASYMMETRIC_WHITE_T_OUTFIT,
    BRIGHT_RED_SHORT_DRESS_OUTFIT,
    FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
]
PLAN_COMPATIBLE_CLOTHING_THEMES = {
    "trend_mirror_studio": [
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        LIGHT_BLUE_WINDBREAKER_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
        *LOW_PROBABILITY_BRAND_THEMES,
    ],
    "capsule_toy_corner": [
        LIGHT_NOVEL_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "graphic_poster_studio": [
        LIGHT_NOVEL_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "afternoon_cafe_negative_space": [
        BAKERY_CAFE_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "small_bakery_morning": [
        BAKERY_CAFE_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
    ],
    "bookstore_cafe_corner": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        BAKERY_CAFE_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "library_corner_sunset_silence": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "balcony_breeze_half_out_frame": [
        LIGHT_NOVEL_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "summer_courtyard_soft_shadow": [
        PICNIC_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BASEBALL_SPECTATOR_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
    ],
    "open_grassland_breeze": [
        PICNIC_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BASEBALL_SPECTATOR_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
    ],
    "greenhouse_terrace_reflection": [
        FLOWER_FANTASY_OUTFIT,
        SOFT_DATE_OUTFIT,
        BRIDAL_OUTFIT,
        FAIRY_FLOATING_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "flower_sea_afternoon": [
        FLOWER_FANTASY_OUTFIT,
        SOFT_DATE_OUTFIT,
        BRIDAL_OUTFIT,
        FAIRY_FLOATING_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "garden_tea_table": [
        FLOWER_FANTASY_OUTFIT,
        SOFT_DATE_OUTFIT,
        BAKERY_CAFE_OUTFIT,
        FAIRY_FLOATING_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "flower_bridal_garden": [
        BRIDAL_OUTFIT,
        FLOWER_FANTASY_OUTFIT,
        FAIRY_FLOATING_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "dessert_shop_mirror_glance": [
        BAKERY_CAFE_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "city_date_window_stroll": [
        SOFT_DATE_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        LIGHT_BLUE_WINDBREAKER_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BASEBALL_SPECTATOR_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
        *LOW_PROBABILITY_BRAND_THEMES,
    ],
    "park_date_riverside_breeze": [
        SOFT_DATE_OUTFIT,
        PICNIC_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        LIGHT_BLUE_WINDBREAKER_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        BASEBALL_SPECTATOR_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
        *LOW_PROBABILITY_BRAND_THEMES,
    ],
    "pastel_room_sweets": [
        SUNNY_STUDIO_OUTFIT,
        BAKERY_CAFE_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "cafe_maid_afternoon": [
        CAFE_MAID_OUTFIT,
        BAKERY_CAFE_OUTFIT,
    ],
    "sunny_seaside_train": [
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        PICNIC_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        LIGHT_BLUE_WINDBREAKER_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        BASEBALL_SPECTATOR_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
        *LOW_PROBABILITY_BRAND_THEMES,
    ],
    "white_room_floor_window": [
        *CLOTHING_THEMES,
    ],
    "pure_white_character_focus": [
        *CLOTHING_THEMES,
    ],
    "zero_gravity_fairy_room": [
        FAIRY_FLOATING_OUTFIT,
        FLOWER_FANTASY_OUTFIT,
        BRIDAL_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "zero_gravity_fairy_garden": [
        FAIRY_FLOATING_OUTFIT,
        FLOWER_FANTASY_OUTFIT,
        BRIDAL_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "guofeng_decorative_kv": [
        REFERENCE_OUTFIT,
        FLOWER_FANTASY_OUTFIT,
        SOFT_DATE_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "overhead_deep_perspective_space": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
    ],
    "low_angle_foreground_depth": [
        PICNIC_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        LIGHT_BLUE_WINDBREAKER_OUTFIT,
        BASEBALL_SPECTATOR_OUTFIT,
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
    ],
    "far_shot_small_figure_room": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "telephoto_layered_interior": [
        BAKERY_CAFE_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
    ],
    "black_stockings_tea_room": [
        DARK_HOSIERY_OUTFIT,
    ],
}
LOW_PROBABILITY_SCENE_ONLY_CLOTHING_BY_PLAN = {
    "trend_mirror_studio": LOW_PROBABILITY_BRAND_THEMES,
    "city_date_window_stroll": LOW_PROBABILITY_BRAND_THEMES,
    "park_date_riverside_breeze": LOW_PROBABILITY_BRAND_THEMES,
    "sunny_seaside_train": LOW_PROBABILITY_BRAND_THEMES,
}
SCENE_CATEGORY_OPTIONS = [
    {
        "key": "studio_mirror",
        "label": "练习室 / 镜子棚拍",
        "plan_names": ["trend_mirror_studio", "graphic_poster_studio"],
    },
    {
        "key": "cafe_bakery_sweets",
        "label": "咖啡 / 烘焙 / 甜品",
        "plan_names": [
            "afternoon_cafe_negative_space",
            "small_bakery_morning",
            "bookstore_cafe_corner",
            "dessert_shop_mirror_glance",
            "pastel_room_sweets",
        ],
    },
    {
        "key": "dream_garden_floating",
        "label": "梦幻 / 花园 / 漂浮",
        "plan_names": [
            "summer_courtyard_soft_shadow",
            "open_grassland_breeze",
            "greenhouse_terrace_reflection",
            "flower_sea_afternoon",
            "garden_tea_table",
            "flower_bridal_garden",
            "park_date_riverside_breeze",
            "zero_gravity_fairy_room",
            "zero_gravity_fairy_garden",
        ],
    },
    {
        "key": "pure_white_minimal",
        "label": "纯白 / 极简棚拍",
        "plan_names": ["white_room_floor_window", "pure_white_character_focus"],
    },
    {
        "key": "distance_perspective_interior",
        "label": "远景 / 透视 / 室内构图",
        "plan_names": [
            "city_date_window_stroll",
            "sunny_seaside_train",
            "library_corner_sunset_silence",
            "balcony_breeze_half_out_frame",
            "overhead_deep_perspective_space",
            "low_angle_foreground_depth",
            "far_shot_small_figure_room",
            "telephoto_layered_interior",
        ],
    },
    {
        "key": "special_limited",
        "label": "特殊限定",
        "plan_names": ["capsule_toy_corner", "cafe_maid_afternoon", "black_stockings_tea_room", "guofeng_decorative_kv"],
    },
]
PROMPT_LOG_FILE = FEEDBACK_DIR / "prompt_log.jsonl"
FEEDBACK_LOG_FILE = FEEDBACK_DIR / "feedback_log.jsonl"
SHARED_FEEDBACK_DIR = Path(r"\\vmware-host\Shared Folders\develop\feedback")
SHARED_LOG_MIRRORS = {
    "prompt_log.jsonl": "vm_prompt_log.jsonl",
    "feedback_log.jsonl": "vm_feedback_log.jsonl",
}
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
USED_CHARACTER_CLOTHING_THEMES_FILE = PROJECT_DIR / "config" / "used_character_clothing_themes.json"
USED_CHARACTER_ART_PLANS_FILE = PROJECT_DIR / "config" / "used_character_art_plans.json"
USED_CHARACTER_BATCH_FILE = PROJECT_DIR / "config" / "used_character_batches.json"
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


def validate_reference_files_for_characters(character_names: list[str]) -> None:
    reference_files = [
        path
        for character_name in character_names
        for path in CHARACTER_REFERENCES[character_name]
    ]
    missing = [path for path in reference_files if not Path(path).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing reference files for {'、'.join(character_names)}: {missing}"
        )


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
    CALIBRATION_FILE.parent.mkdir(parents=True, exist_ok=True)
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


def send_work_reminder(completed_run_number: int) -> None:
    print(
        f"[{completed_run_number:02d}] reminder: sending plain text work reminder, no upload and no image prompt",
        flush=True,
    )
    send_prompt(WORK_REMINDER_TEXT)
    wait_with_echo(CHECK_INTERVAL_SECONDS, f"[{completed_run_number:02d}] reminder settle")


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
    safe_entry = _json_safe(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(safe_entry, ensure_ascii=False) + "\n")
    mirror_jsonl_to_shared(path, safe_entry)


def mirror_jsonl_to_shared(path: Path, entry: dict) -> None:
    mirror_name = SHARED_LOG_MIRRORS.get(path.name)
    if not mirror_name:
        return
    try:
        if not SHARED_FEEDBACK_DIR.exists():
            return
        mirror_path = SHARED_FEEDBACK_DIR / mirror_name
        with mirror_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"Shared log mirror skipped: {exc}", flush=True)


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
    required_identity_tokens: list[str] | None = None,
    viewer_distance: str = "",
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
            "required_identity_tokens": required_identity_tokens or [],
            "viewer_distance": viewer_distance,
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
    valid_used = [theme for theme in used_themes if theme in REGULAR_CLOTHING_THEMES]
    used_themes[:] = valid_used

    available = [theme for theme in REGULAR_CLOTHING_THEMES if theme not in used_themes]
    if not available:
        print(
            "All clothing themes have been used in the current cycle. Clearing current-cycle history and starting a new cycle.",
            flush=True,
        )
        print(f"Permanent clothing usage log is kept at: {CLOTHING_THEME_USAGE_LOG_FILE}", flush=True)
        used_themes.clear()
        save_used_clothing_themes(used_themes)
        available = REGULAR_CLOTHING_THEMES[:]

    return random.choice(available)


def choose_character_clothing_theme(
    character_name: str,
    used_by_character: dict[str, list[str]],
    batch_used_themes: set[str] | None = None,
) -> str:
    batch_used_themes = batch_used_themes or set()
    used_themes = used_by_character.setdefault(character_name, [])
    valid_used = [theme for theme in used_themes if theme in REGULAR_CLOTHING_THEMES]
    used_by_character[character_name] = valid_used
    used_set = set(valid_used)

    available = [
        theme for theme in REGULAR_CLOTHING_THEMES
        if theme not in used_set and theme not in batch_used_themes
    ]
    if not available:
        print(f"{character_name} regular clothing theme cycle complete; clearing per-character theme history.", flush=True)
        used_by_character[character_name] = []
        save_used_character_clothing_themes(used_by_character)
        available = [
            theme for theme in REGULAR_CLOTHING_THEMES
            if theme not in batch_used_themes
        ] or REGULAR_CLOTHING_THEMES[:]

    return random.choice(available)


def choose_compatible_clothing_theme(
    character_name: str,
    art_plan: dict,
    used_by_character: dict[str, list[str]],
    batch_used_themes: set[str] | None = None,
) -> str:
    compatible_themes = [
        theme for theme in PLAN_COMPATIBLE_CLOTHING_THEMES.get(art_plan["name"], [])
        if theme in CLOTHING_THEMES
    ]
    if not compatible_themes:
        compatible_themes = SAFE_DAILY_CLOTHING_POOL[:]

    batch_used_themes = batch_used_themes or set()
    regular_compatible = [
        theme for theme in compatible_themes
        if theme in REGULAR_CLOTHING_THEMES
    ]
    scene_only_compatible = [
        theme for theme in compatible_themes
        if theme in STRONG_SCENE_ONLY_CLOTHING_THEMES
    ]
    low_probability_scene_themes = [
        theme for theme in LOW_PROBABILITY_SCENE_ONLY_CLOTHING_BY_PLAN.get(art_plan["name"], [])
        if theme in compatible_themes
    ]

    if (
        low_probability_scene_themes
        and random.random() < LOW_PROBABILITY_SCENE_OUTFIT_CHANCE
    ):
        return random.choice(low_probability_scene_themes)

    used_themes = used_by_character.setdefault(character_name, [])
    valid_used = [
        theme for theme in used_themes
        if theme in REGULAR_CLOTHING_THEMES
    ]
    used_by_character[character_name] = valid_used
    used_set = set(valid_used)

    available = [
        theme for theme in regular_compatible
        if theme not in used_set and theme not in batch_used_themes
    ]
    if available:
        return random.choice(available)

    available = [
        theme for theme in regular_compatible
        if theme not in batch_used_themes
    ]
    if available:
        return random.choice(available)

    if regular_compatible:
        return random.choice(regular_compatible)

    if scene_only_compatible:
        return random.choice(scene_only_compatible)

    return random.choice(SAFE_DAILY_CLOTHING_POOL)



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


def load_used_character_clothing_themes() -> dict[str, list[str]]:
    if not USED_CHARACTER_CLOTHING_THEMES_FILE.exists():
        return {}

    try:
        data = json.loads(USED_CHARACTER_CLOTHING_THEMES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Used character clothing theme file is invalid; starting fresh: {USED_CHARACTER_CLOTHING_THEMES_FILE}")
        return {}

    if not isinstance(data, dict):
        return {}

    valid_themes = set(CLOTHING_THEMES)
    normalized: dict[str, list[str]] = {}
    for character_name, themes in data.items():
        if not isinstance(character_name, str) or not isinstance(themes, list):
            continue
        normalized[character_name] = [
            theme for theme in themes
            if isinstance(theme, str) and theme in valid_themes
        ]
    return normalized


def save_used_character_clothing_themes(used_by_character: dict[str, list[str]]) -> None:
    USED_CHARACTER_CLOTHING_THEMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    USED_CHARACTER_CLOTHING_THEMES_FILE.write_text(
        json.dumps(used_by_character, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_used_character_art_plans() -> dict[str, list[str]]:
    if not USED_CHARACTER_ART_PLANS_FILE.exists():
        return {}

    try:
        data = json.loads(USED_CHARACTER_ART_PLANS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Used character art-plan file is invalid; starting fresh: {USED_CHARACTER_ART_PLANS_FILE}")
        return {}

    if not isinstance(data, dict):
        return {}

    valid_plans = {plan["name"] for plan in ART_DIRECTION_PLANS}
    normalized: dict[str, list[str]] = {}
    for character_name, plan_names in data.items():
        if not isinstance(character_name, str) or not isinstance(plan_names, list):
            continue
        normalized[character_name] = [
            plan_name for plan_name in plan_names
            if isinstance(plan_name, str) and plan_name in valid_plans
        ]
    return normalized


def save_used_character_art_plans(used_by_character: dict[str, list[str]]) -> None:
    USED_CHARACTER_ART_PLANS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USED_CHARACTER_ART_PLANS_FILE.write_text(
        json.dumps(used_by_character, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_used_character_batch() -> list[str]:
    if not USED_CHARACTER_BATCH_FILE.exists():
        return []

    try:
        data = json.loads(USED_CHARACTER_BATCH_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Used character batch file is invalid; starting fresh: {USED_CHARACTER_BATCH_FILE}")
        return []

    if not isinstance(data, list):
        return []

    valid_characters = set(CHARACTER_SEQUENCE)
    return [name for name in data if isinstance(name, str) and name in valid_characters]


def save_used_character_batch(used_characters: list[str]) -> None:
    USED_CHARACTER_BATCH_FILE.parent.mkdir(parents=True, exist_ok=True)
    USED_CHARACTER_BATCH_FILE.write_text(
        json.dumps(used_characters, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def choose_character_batch(used_characters: list[str]) -> list[str]:
    valid_used = [name for name in used_characters if name in CHARACTER_SEQUENCE]
    used_characters[:] = valid_used

    available = [name for name in CHARACTER_SEQUENCE if name not in used_characters]
    if not available:
        print(
            "All characters have appeared in the current character cycle. Clearing character-cycle history.",
            flush=True,
        )
        used_characters.clear()
        save_used_character_batch(used_characters)
        available = CHARACTER_SEQUENCE[:]

    batch_size = min(CHARACTERS_PER_BATCH, len(available))
    selected = random.sample(available, k=batch_size)
    print(
        f"Character cycle: {len(used_characters)}/{len(CHARACTER_SEQUENCE)} used before this batch -> "
        f"{USED_CHARACTER_BATCH_FILE}",
        flush=True,
    )
    return selected


def _parse_character_selection(raw_choice: str) -> list[str] | None:
    choice = raw_choice.strip()
    if not choice or choice.lower() in {"r", "random", "all", "all-random", "全随机", "随机"}:
        return None

    selected: list[str] = []
    if choice.isdigit():
        tokens = [choice]
    else:
        normalized = choice.replace("，", ",").replace("、", ",").replace(" ", ",")
        tokens = [token.strip() for token in normalized.split(",") if token.strip()]

    name_to_character = {name.lower(): name for name in CHARACTER_SEQUENCE}
    for token in tokens:
        character_names: list[str] = []
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            if not start_text.isdigit() or not end_text.isdigit():
                raise ValueError(f"Unknown character selection: {token!r}")
            start_index = int(start_text)
            end_index = int(end_text)
            if start_index > end_index:
                raise ValueError(f"Character range must be ascending: {token!r}")
            if start_index < 1 or end_index > len(CHARACTER_SEQUENCE):
                raise ValueError(f"Character range out of bounds: {token!r}")
            character_names = CHARACTER_SEQUENCE[start_index - 1:end_index]
        elif token.isdigit():
            index = int(token)
            if 1 <= index <= len(CHARACTER_SEQUENCE):
                character_names = [CHARACTER_SEQUENCE[index - 1]]
        else:
            character_name = name_to_character.get(token.lower())
            if character_name:
                character_names = [character_name]

        if not character_names:
            raise ValueError(f"Unknown character selection: {token!r}")
        for character_name in character_names:
            if character_name not in selected:
                selected.append(character_name)

    if not selected:
        raise ValueError("No valid characters selected")
    return selected


def prompt_character_selection() -> list[str] | None:
    print("=" * 72, flush=True)
    print("Choose characters for this run:", flush=True)
    for index, character_name in enumerate(CHARACTER_SEQUENCE, start=1):
        print(f"  {index}. {character_name}", flush=True)
    print("Input examples: Enter/r/random = full random cycle; 1 2 3 = characters 1,2,3; 10-15 = characters 10 through 15; 16 17 18 = characters 16,17,18; names are also OK.", flush=True)

    while True:
        raw_choice = input("Character selection: ")
        try:
            selected = _parse_character_selection(raw_choice)
        except ValueError as exc:
            print(f"{exc}. Please try again.", flush=True)
            continue

        if selected is None:
            print("Character mode: full random cycle.", flush=True)
        else:
            print(f"Character mode: fixed selection -> {'、'.join(selected)}", flush=True)
        return selected


def _parse_scene_category_selection(raw_choice: str) -> list[str] | None:
    choice = raw_choice.strip()
    if not choice or choice.lower() in {"r", "random", "all", "all-random", "全随机", "随机"}:
        return None

    if choice.isdigit() and all(char != "0" for char in choice):
        tokens = list(choice)
    else:
        normalized = choice.replace("，", ",").replace("、", ",").replace(" ", ",")
        tokens = [token.strip() for token in normalized.split(",") if token.strip()]

    selected_plan_names: list[str] = []
    key_to_option = {option["key"].lower(): option for option in SCENE_CATEGORY_OPTIONS}
    label_to_option = {option["label"].lower(): option for option in SCENE_CATEGORY_OPTIONS}
    for token in tokens:
        option = None
        if token.isdigit():
            index = int(token)
            if 1 <= index <= len(SCENE_CATEGORY_OPTIONS):
                option = SCENE_CATEGORY_OPTIONS[index - 1]
        else:
            option = key_to_option.get(token.lower()) or label_to_option.get(token.lower())

        if not option:
            raise ValueError(f"Unknown scene selection: {token!r}")
        for plan_name in option["plan_names"]:
            if plan_name not in selected_plan_names:
                selected_plan_names.append(plan_name)

    if not selected_plan_names:
        raise ValueError("No valid scenes selected")
    return selected_plan_names


def prompt_scene_category_selection() -> list[str] | None:
    print("=" * 72, flush=True)
    print("Choose scene category for this run:", flush=True)
    for index, option in enumerate(SCENE_CATEGORY_OPTIONS, start=1):
        print(f"  {index}. {option['label']}", flush=True)
    print("Input examples: Enter/r/random = all scenes; 1 = category 1; 135 = categories 1,3,5.", flush=True)
    print("Clothing is still chosen automatically from the selected scene's compatible pool.", flush=True)

    while True:
        raw_choice = input("Scene selection: ")
        try:
            selected_plan_names = _parse_scene_category_selection(raw_choice)
        except ValueError as exc:
            print(f"{exc}. Please try again.", flush=True)
            continue

        if selected_plan_names is None:
            print("Scene mode: full random art-plan cycle.", flush=True)
        else:
            selected_labels = [
                option["label"]
                for option in SCENE_CATEGORY_OPTIONS
                if any(plan_name in selected_plan_names for plan_name in option["plan_names"])
            ]
            print(f"Scene mode: fixed category -> {'、'.join(selected_labels)}", flush=True)
        return selected_plan_names


def mark_character_batch_used(selected_characters: list[str], used_characters: list[str]) -> None:
    for character_name in selected_characters:
        if character_name in CHARACTER_SEQUENCE and character_name not in used_characters:
            used_characters.append(character_name)
    save_used_character_batch(used_characters)
    print(
        f"Character cycle after batch: {len(used_characters)}/{len(CHARACTER_SEQUENCE)} used -> "
        f"{USED_CHARACTER_BATCH_FILE}",
        flush=True,
    )


def choose_character_plan_and_action(
    character_name: str,
    recent_visual_tags: list[str],
    used_themes_by_character: dict[str, list[str]],
    used_plans_by_character: dict[str, list[str]],
    batch_used_themes: set[str] | None = None,
    batch_used_plans: set[str] | None = None,
    allowed_plan_names: list[str] | None = None,
) -> tuple[dict, dict]:
    batch_used_themes = batch_used_themes or set()
    batch_used_plans = batch_used_plans or set()

    valid_plan_names = {plan["name"] for plan in ART_DIRECTION_PLANS}
    if allowed_plan_names:
        valid_plan_names &= set(allowed_plan_names)
    plan_pool = [
        plan for plan in ART_DIRECTION_PLANS
        if plan["name"] in valid_plan_names
    ]
    if not plan_pool:
        plan_pool = ART_DIRECTION_PLANS[:]
        valid_plan_names = {plan["name"] for plan in plan_pool}

    used_plans = used_plans_by_character.setdefault(character_name, [])
    valid_used_plans = [
        plan_name for plan_name in used_plans
        if plan_name in valid_plan_names
    ]
    used_plans_by_character[character_name] = valid_used_plans
    used_plan_set = set(valid_used_plans)

    if len(used_plan_set) >= len(plan_pool):
        print(f"{character_name} art-plan cycle complete; clearing per-character plan history.", flush=True)
        used_plans_by_character[character_name] = []
        used_plan_set = set()
        save_used_character_art_plans(used_plans_by_character)

    best_unused_plan: tuple[dict, dict] | None = None
    fallback: tuple[dict, dict] | None = None
    for _ in range(180):
        art_plan, action_style = choose_plan_and_action(character_name, recent_visual_tags)
        if art_plan["name"] not in valid_plan_names:
            continue
        if fallback is None:
            fallback = (art_plan, action_style)
        plan_name = art_plan["name"]
        plan_is_unused = plan_name not in used_plan_set and plan_name not in batch_used_plans

        if plan_is_unused:
            return art_plan, action_style
        if plan_is_unused and best_unused_plan is None:
            best_unused_plan = (art_plan, action_style)

    unused_plans = [
        plan for plan in plan_pool
        if plan["name"] not in used_plan_set and plan["name"] not in batch_used_plans
    ]
    if unused_plans:
        art_plan = random.choice(unused_plans)
        action_style = choose_compatible_action_style(character_name, recent_visual_tags, art_plan)
        print(f"{character_name} selected from explicit unused art-plan pool after random attempts.", flush=True)
        return dict(art_plan), action_style

    if best_unused_plan is not None:
        print(f"{character_name} selected an unused art plan after random attempts.", flush=True)
        return best_unused_plan
    if fallback is not None:
        print(f"{character_name} could not find a fresh art plan; using character-safe fallback plan.", flush=True)
        return fallback

    art_plan = random.choice(plan_pool)
    action_style = choose_compatible_action_style(character_name, recent_visual_tags, art_plan)
    return dict(art_plan), action_style


def mark_character_clothing_theme_used(
    character_name: str,
    theme: str,
    used_by_character: dict[str, list[str]],
) -> None:
    if theme not in REGULAR_CLOTHING_THEMES:
        append_clothing_theme_usage_log(f"{character_name}: {theme} (scene-only strong outfit, not cycle-counted)", 0)
        return
    used_themes = used_by_character.setdefault(character_name, [])
    if theme not in used_themes:
        used_themes.append(theme)
    save_used_character_clothing_themes(used_by_character)
    append_clothing_theme_usage_log(f"{character_name}: {theme}", len(used_themes))
    print(
        f"{character_name} clothing theme current cycle: {len(used_themes)}/{len(REGULAR_CLOTHING_THEMES)} used -> "
        f"{USED_CHARACTER_CLOTHING_THEMES_FILE}",
        flush=True,
    )


def mark_character_art_plan_used(
    character_name: str,
    plan_name: str,
    used_by_character: dict[str, list[str]],
) -> None:
    valid_plan_names = {plan["name"] for plan in ART_DIRECTION_PLANS}
    if plan_name not in valid_plan_names:
        return
    used_plans = used_by_character.setdefault(character_name, [])
    if plan_name not in used_plans:
        used_plans.append(plan_name)
    save_used_character_art_plans(used_by_character)
    print(
        f"{character_name} art-plan current cycle: {len(used_plans)}/{len(ART_DIRECTION_PLANS)} used -> "
        f"{USED_CHARACTER_ART_PLANS_FILE}",
        flush=True,
    )


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

    print("Keep ChatGPT desktop open, unlocked, and focused.")
    print("Press Ctrl+C in this terminal to abort. Moving the mouse to a virtual-screen corner pauses the next click.")
    if "--shutdown" in sys.argv:
        schedule_safety_shutdown()
    else:
        print("Safety shutdown is disabled for this feedback run. Use --shutdown to enable it.")
    time.sleep(3)

    print(
        f"Fenjue stable compact anime pipeline active: {len(ART_DIRECTION_PLANS)} art direction plans available. "
        "Priority: character identity, clean composition, stable anatomy, and consistent illustration quality.",
        flush=True,
    )

    total_runs = TOTAL_RUNS
    if "--runs" in sys.argv:
        runs_index = sys.argv.index("--runs")
        if runs_index + 1 >= len(sys.argv):
            raise ValueError("--runs requires a number")
        total_runs = int(sys.argv[runs_index + 1])

    recent_visual_tags: list[str] = []
    used_by_character = load_used_character_clothing_themes()
    used_plans_by_character = load_used_character_art_plans()
    used_character_batch = load_used_character_batch()
    fixed_character_selection = prompt_character_selection()
    fixed_scene_plan_names = prompt_scene_category_selection()
    print(
        f"Starting in {POST_CHARACTER_SELECTION_DELAY_SECONDS} seconds; keep the mouse clear of the target area.",
        flush=True,
    )
    time.sleep(POST_CHARACTER_SELECTION_DELAY_SECONDS)
    run_number = 1
    stop_requested = False

    while run_number <= total_runs and not stop_requested:
        random_character_mode = fixed_character_selection is None
        selected_characters = (
            choose_character_batch(used_character_batch)
            if random_character_mode
            else fixed_character_selection[:]
        )
        batch_completed_characters: list[str] = []
        batch_used_themes: set[str] = set()
        batch_used_plans: set[str] = set()
        validate_reference_files_for_characters(selected_characters)
        print("=" * 72, flush=True)
        print(
            f"Character-first batch selected ({len(selected_characters)} characters x 1, "
            f"{'random cycle' if random_character_mode else 'fixed selection'}): "
            f"{'、'.join(selected_characters)}",
            flush=True,
        )
        print(
            "Scene category: "
            + ("full random" if fixed_scene_plan_names is None else f"{len(fixed_scene_plan_names)} allowed art plans"),
            flush=True,
        )

        for character_name in selected_characters:
            if run_number > total_runs:
                break

            reference_files = reference_files_for_character(character_name)
            art_plan, action_style = choose_character_plan_and_action(
                character_name,
                recent_visual_tags,
                used_by_character,
                used_plans_by_character,
                batch_used_themes,
                batch_used_plans,
                fixed_scene_plan_names,
            )
            propagation_profile = propagation_profile_for(character_name)
            required_identity_tokens = required_identity_tokens_for(character_name)
            viewer_distance = viewer_distance_for(character_name)
            theme = choose_compatible_clothing_theme(
                character_name,
                art_plan,
                used_by_character,
                batch_used_themes,
            )
            plan_name = art_plan["name"]
            batch_used_themes.add(theme)
            batch_used_plans.add(plan_name)
            scene = art_plan["spatial_structure"]
            pose = action_style["body_silhouette"]
            lighting = art_plan["lighting_behavior"]
            mood = art_plan["color_strategy"]
            template_index = 0
            concept = art_plan["graphic_concept"]
            prompt_name = prompt_template_name(template_index)
            prompt = prompt_for_art_direction(
                character_name,
                art_plan,
                action_style,
                outfit_direction=theme,
            )

            print("=" * 72, flush=True)
            print(f"[{run_number:02d}/{total_runs}] Starting run", flush=True)
            print(f"[{run_number:02d}] batch character: {character_name}", flush=True)
            print(f"[{run_number:02d}] character: {character_name}", flush=True)
            print(f"[{run_number:02d}] references: {reference_files}", flush=True)
            print(f"[{run_number:02d}] clothing theme: {theme}", flush=True)
            print(f"[{run_number:02d}] scene: {scene}", flush=True)
            print(f"[{run_number:02d}] pose: {pose}", flush=True)
            print(f"[{run_number:02d}] lighting: {lighting}", flush=True)
            print(f"[{run_number:02d}] mood: {mood}", flush=True)
            print(f"[{run_number:02d}] art plan: {plan_name}", flush=True)
            print(f"[{run_number:02d}] action style: {action_style['name']}", flush=True)
            print(f"[{run_number:02d}] propagation: {propagation_profile['propagation_translation']}", flush=True)
            print(f"[{run_number:02d}] viewer distance: {viewer_distance}", flush=True)
            print(f"[{run_number:02d}] required identity tokens: {required_identity_tokens}", flush=True)
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
                required_identity_tokens,
                viewer_distance,
            )
            send_prompt(prompt)
            take_screenshot(f"run_{run_number:02d}_sent")
            screenshot_path = wait_for_generation(run_number)
            log_feedback_placeholder(run_id, run_number, character_name, screenshot_path)
            mark_character_clothing_theme_used(character_name, theme, used_by_character)
            mark_character_art_plan_used(character_name, plan_name, used_plans_by_character)
            batch_completed_characters.append(character_name)
            recent_visual_tags.extend(collect_cooldown_tags(art_plan, action_style))
            recent_visual_tags = recent_visual_tags[-12:]

            if run_number % WORK_REMINDER_INTERVAL == 0 and run_number < total_runs:
                send_work_reminder(run_number)

            if "--once" in sys.argv or "--review-url" in sys.argv:
                open_images_page_for_review()

            if "--once" in sys.argv:
                print("--once completed. Review feedback, adjust prompts if needed, then run again.")
                stop_requested = True
                break

            run_number += 1

        if batch_completed_characters:
            if random_character_mode:
                mark_character_batch_used(batch_completed_characters, used_character_batch)

    print("All runs completed. Safety shutdown remains scheduled.")


if __name__ == "__main__":
    main()


