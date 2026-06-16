import ctypes
import datetime as dt
import json
import os
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

import art_direction_options as art_options
from art_direction_options import (
    ART_DIRECTION_PLANS,
    OUTFIT_DIRECTIONS as CLOTHING_THEMES,
    choose_compatible_action_style,
    choose_composition_plan,
    choose_shot_scale,
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
from yang_mi_outfits import YANG_MI_COLOR_FREE_THEMES, YANG_MI_ORIGINAL_COLOR_THEMES
from zhang_wonyoung_outfits import ZHANG_WONYOUNG_COLOR_FREE_THEMES, ZHANG_WONYOUNG_ORIGINAL_COLOR_THEMES
from zhang_ruonan_outfits import ZHANG_RUONAN_COLOR_FREE_THEMES, ZHANG_RUONAN_ORIGINAL_COLOR_THEMES
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
    ],
    "千夏": [
        str(PROJECT_DIR / "assets" / "千夏1.png"),
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
        str(PROJECT_DIR / "assets" / "橘福福1.png"),
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
    "柏妮思": [
        str(PROJECT_DIR / "assets" / "柏妮思1.png"),
        str(PROJECT_DIR / "assets" / "柏妮思2.png"),
    ],
    "妮可": [
        str(PROJECT_DIR / "assets" / "妮可1.png"),
        str(PROJECT_DIR / "assets" / "妮可2.png"),
        str(PROJECT_DIR / "assets" / "妮可3.png"),
    ],
    "简": [
        str(PROJECT_DIR / "assets" / "简1.png"),
        str(PROJECT_DIR / "assets" / "简2.png"),
        str(PROJECT_DIR / "assets" / "简3.png"),
    ],
    "月城柳": [
        str(PROJECT_DIR / "assets" / "柳1.png"),
        str(PROJECT_DIR / "assets" / "柳2.png"),
    ],
    "青衣": [
        str(PROJECT_DIR / "assets" / "青衣1.png"),
        str(PROJECT_DIR / "assets" / "青衣2.png"),
    ],
    "伊芙琳": [
        str(PROJECT_DIR / "assets" / "伊芙琳1.png"),
        str(PROJECT_DIR / "assets" / "伊芙琳2.png"),
    ],
    "朱鸢": [
        str(PROJECT_DIR / "assets" / "朱鸢1.png"),
        str(PROJECT_DIR / "assets" / "朱鸢2.png"),
    ],
    "卢西娅": [
        str(PROJECT_DIR / "assets" / "卢西娅1.png"),
        str(PROJECT_DIR / "assets" / "卢西娅2.png"),
    ],
    "维琳娜": [
        str(PROJECT_DIR / "assets" / "维琳娜1.jpeg"),
        str(PROJECT_DIR / "assets" / "维琳娜2.png"),
        str(PROJECT_DIR / "assets" / "维琳娜3.jpeg"),
    ],
}
MOUSOU_TENSHI_CHARACTERS = ["南宫", "爱芮", "千夏"]
# Art direction mode is single-character-first. Multi-character prompt logic is kept
# in the legacy templates, but the production batch does not use it by default.
GROUP_SIZE_WEIGHTS = [1]
CHARACTER_SEQUENCE = ["南宫", "爱芮", "千夏", "丹", "星见雅", "仪玄", "叶瞬光", "席德", "橘福福", "柚叶", "爱丽丝", "普罗米娅", "薇薇安", "安比", "可琳", "艾莲", "琉音", "耀嘉音", "柏妮思", "妮可", "简", "月城柳", "青衣", "伊芙琳", "朱鸢", "卢西娅", "维琳娜"]
CHARACTERS_PER_BATCH = 3
REFERENCE_FILES = CHARACTER_REFERENCES["丹"][:]
TOTAL_RUNS = 999

CHECK_INTERVAL_SECONDS = 120
MAX_UPLOAD_SETTLE_SECONDS = 15
TEXT_BEFORE_SEND_SECONDS = 10
ECHO_COUNTDOWN_LAST_SECONDS = 20
SINGLE_CLICK_HOLD_SECONDS = 0.06
SEND_CLICK_HOLD_SECONDS = 0.14
SEND_RELEASE_SETTLE_SECONDS = 0.35
POST_CHARACTER_SELECTION_DELAY_SECONDS = 3
SEND_MOUSE_AWAY_OFFSET = (-220, -90)
WORK_REMINDER_INTERVAL = 14
WORK_REMINDER_TEXT = "REMINDER: This is still an image-generation-only batch. Do not explain or comment. Generate the image directly."
IMAGE_PROMPT_PREFIX = "【根据以下提示词完成图片的生成】"
SAFE_SCREEN_MARGIN = 8
SAFETY_SHUTDOWN_TARGET_TIME = "12:00"
LOW_PROBABILITY_SCENE_OUTFIT_CHANCE = 0.08
RUNTIME_CONFIG_PATH = PROJECT_DIR / "config" / "runtime_art_direction.json"
RUNTIME_GIT_PULL_INTERVAL_SECONDS = 300
RUNTIME_GIT_PULL_TIMEOUT_SECONDS = 60
DEFAULT_BLACK_HOSIERY_CHANCE = 0.23
CHARACTER_BLACK_HOSIERY_CHANCES = {
    "艾莲": 0.47,
}
BLACK_HOSIERY_ACCENT = (
    "paired with refined semi-opaque black tights or stockings as a subtle styling accent, "
    "balanced with the selected outfit, restrained and non-fetishized"
)
BLACK_HOSIERY_INCOMPATIBLE_KEYWORDS = (
    "swim",
    "beach",
    "resort",
    "bridal",
    "wedding",
    "activewear",
    "athletic",
    "running",
    "sport",
    "sporty",
    "yoga",
    "pilates",
    "shorts",
    "denim shorts",
    "jogger pants",
    "long pants",
    "wide-leg trousers",
    "wide leg trousers",
    "trousers",
    "loose jeans",
    "jeans",
    "denim overalls",
    "overalls",
    "flare pants",
    "yoga pants",
    "no stocking emphasis",
    "sailor",
    "barefoot",
)
BLACK_HOSIERY_INCOMPATIBLE_PLAN_NAMES = {
    "beach_wind_open_sand",
    "flower_bridal_garden",
}

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
CONDITIONAL_SCENE_ONLY_CLOTHING_THEMES = {
    "minimal one-piece swimsuit, modest scoop neckline, standard leg openings, clean fitted silhouette, thin straps wrapping around the upper thighs",
    "straight-neck tailored mini dress, clean neckline, asymmetric hem, long flowing side panels forming a dramatic trailing train, opaque satin opera gloves, pointed high heels",
    "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
    "retro athletic cheer set, sleeveless high-neck cropped athletic top with large number graphic, matching standard-waist athletic shorts, side stripes, piping and drawstring, semi-opaque polka-dot tights",
    "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
    "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
    "striped swim top under loose cover shirt, clean beach resort style",
    "satin lounge slip dress, lace panel, halter neck, side tie ribbon, relaxed resort-home mood",
    "long-sleeve cropped active top, high-waist flare yoga pants, soft pilates outfit",
    "simple camisole, high-waist flare pants, balletcore pilates fashion",
    "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
    "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit",
    "waist-shaped mini dress, lace panels, bell sleeves, boots, idol stagewear",
    "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt",
    "racing crop jacket, motorsport sponsor top, performance event costume",
    "ruffled chiffon mini dress, tiered fairy dress, idol rehearsal outfit",
    "straight-neck maxi dress, simple straight bodice, loose flowing resort silhouette",
    "spaghetti-strap lightly fitted mini dress, clean silhouette, minimalist cocktail eveningwear",
}
SCENE_ONLY_COMPATIBLE_OUTFIT_CHANCE = 0.18
STRONG_SCENE_ONLY_CLOTHING_THEMES = [
    theme for theme in CLOTHING_THEMES
    if theme in LOW_PROBABILITY_BRAND_THEMES
    or theme in CONDITIONAL_SCENE_ONLY_CLOTHING_THEMES
    or "black hosiery" in theme
    or "maid remix" in theme
    or "bridal dress" in theme
]
REGULAR_CLOTHING_THEMES = [
    theme for theme in CLOTHING_THEMES
    if theme not in STRONG_SCENE_ONLY_CLOTHING_THEMES
]
REFERENCE_OUTFIT = "character-signature outfit with a small fashionable variation"
LIGHT_NOVEL_OUTFIT = "clean light-novel casual outfit, character palette stays recognizable"
YOUNG_CASUAL_OUTFIT = "young casual top: sleeveless tank with cropped casual layering, clean youthful styling"
SOFT_DATE_OUTFIT = "soft date outfit: cardigan, camisole or blouse, A-line skirt, small shoulder bag, clean and youthful"
CAFE_MAID_OUTFIT = "cafe maid remix outfit, neat apron, ribbons, cute and clean"
BRIDAL_OUTFIT = "romantic flower bridal dress, elegant veil or bouquet, clean and elegant"
FLOWER_FANTASY_OUTFIT = "elegant flower-field fantasy outfit, simplified layers, no weapon requirement"
YOUTHFUL_CASUAL_OUTFIT = "clean youthful casual outfit, blouse or light cardigan, no stocking emphasis"
PICNIC_OUTFIT = "fresh picnic outfit, short jacket or light cardigan, clear layered pieces"
SUNNY_STUDIO_OUTFIT = "minimal sunny studio outfit, face and hair identity as the main focus"
PURE_WHITE_OUTFIT = "clean minimal studio outfit, simple silhouette, palette selected to support character identity"
FAIRY_FLOATING_OUTFIT = "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling"
WHITE_SUNDRESS_STRAW_HAT_OUTFIT = "fresh sundress with a straw hat, summer date mood"
BLUE_GINGHAM_DENIM_OUTFIT = "medium-short gingham shirt over a tank top, denim shorts; shirt tied into a small front-bottom bow"
LIGHT_BLUE_WINDBREAKER_OUTFIT = "soft windbreaker jacket, modest crew-neck tank top, athletic shorts, round-frame glasses"
ASYMMETRIC_WHITE_T_OUTFIT = "thin off-shoulder long T-shirt, camisole inner layer visible at neckline, shorts"
LACE_OFF_SHOULDER_DRESS_OUTFIT = "lace off-shoulder dress with puff sleeves, clean romantic styling"
BRIGHT_RED_SHORT_DRESS_OUTFIT = "short one-piece dress, youthful clean date styling"
FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT = "elbow-length sleeve light-sport T-shirt with tailored denim shorts"
CLOTHING_DISPLAY_LABELS = {
    REFERENCE_OUTFIT: "参考图服装微调",
    LIGHT_NOVEL_OUTFIT: "轻小说日常",
    YOUNG_CASUAL_OUTFIT: "年轻休闲上衣",
    SOFT_DATE_OUTFIT: "柔和约会装",
    CAFE_MAID_OUTFIT: "咖啡女仆改良",
    BRIDAL_OUTFIT: "花园婚纱",
    FLOWER_FANTASY_OUTFIT: "花田幻想礼服",
    YOUTHFUL_CASUAL_OUTFIT: "清爽少女日常",
    PICNIC_OUTFIT: "野餐层次穿搭",
    "soft casual outfit with warm simple styling": "温柔简洁日常",
    SUNNY_STUDIO_OUTFIT: "晴光棚拍简装",
    PURE_WHITE_OUTFIT: "极简棚拍造型",
    FAIRY_FLOATING_OUTFIT: "漂浮童话纱裙",
    WHITE_SUNDRESS_STRAW_HAT_OUTFIT: "夏日草帽连衣裙",
    BLUE_GINGHAM_DENIM_OUTFIT: "格纹衬衫牛仔短裤",
    LIGHT_BLUE_WINDBREAKER_OUTFIT: "运动风防晒外套",
    ASYMMETRIC_WHITE_T_OUTFIT: "露肩长T叠穿",
    LACE_OFF_SHOULDER_DRESS_OUTFIT: "蕾丝露肩裙",
    BRIGHT_RED_SHORT_DRESS_OUTFIT: "短款连衣裙",
    FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT: "轻运动T恤短裤",
    "sailor dress, short sleeves, bow and trim, fitted knee-length summer school-date style": "水手学院连衣裙",
    "simple camisole, lightweight opaque chiffon off-shoulder sleeves, high-waisted denim shorts, clean summer date style": "吊带透袖牛仔短裤",
    "strap maxi dress, fitted waist, flowing full skirt, elegant lightweight summer style": "吊带长裙",
    "tank top, oversized cropped hoodie, loose jeans, relaxed casual style": "背心短款帽衫牛仔裤",
    "sleeveless top, denim overalls, youthful clean casual style": "无袖上衣牛仔背带裤",
    "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style": "高领蕾丝婚纱",
    "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit": "短卫衣舞台短裙",
    "academy pinafore dress, shirt, ribbon tie, round glasses, preppy school style": "学院背心裙",
    "oversized sweater, loose sleeves, cozy homewear, soft casual style": "宽松毛衣居家风",
    "waist-shaped mini dress, lace panels, bell sleeves, boots, idol stagewear": "蕾丝舞台裙",
    "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style": "雪纺仙女礼服",
    "waist-shaped dress, off-shoulder cut, uneven skirt, romantic cottagecore style": "田园连衣裙",
    "lace dress, ribbon waist, airy garden fairy style": "蕾丝花园裙",
    "striped swim top under loose cover shirt, clean beach resort style": "沙滩罩衫度假装",
    "satin lounge slip dress, lace panel, halter neck, side tie ribbon, relaxed resort-home mood": "缎面蕾丝家居裙",
    "athleisure activewear set, athletic tank, lightweight sun jacket, running shorts, summer sport mood": "运动防晒套装",
    "layered striped knit top, wrap skirt, preppy luxury styling": "层叠针织半裙",
    "striped tank top, pleated mini skirt, tennis-girl summer casual style": "美式网球学院风",
    "ribbed tank top, satin shorts, minimal summer lounge style": "罗纹背心缎面短裤",
    "long-sleeve cropped active top, high-waist flare yoga pants, soft pilates outfit": "瑜伽训练套装",
    "simple camisole, high-waist flare pants, balletcore pilates fashion": "芭蕾普拉提风",
    "straight-neck maxi dress, simple straight bodice, loose flowing resort silhouette": "直领度假长裙",
    "straight-neck opaque top with oversized cardigan worn off shoulders, relaxed knit loungewear style": "直领开衫居家风",
    "cropped graphic T-shirt, abstract graphic chest print, high-waisted jogger pants, casual streetwear": "印花短T运动长裤",
    "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt": "幻想风礼服",
    "spaghetti-strap lightly fitted mini dress, clean silhouette, minimalist cocktail eveningwear": "吊带小礼裙",
    "cropped athletic top, fitted short sleeves, plain hem band, clean activewear style": "短款运动上衣",
    "knit halter dress, textured fabric, clean upper-body fit, soft draped summer silhouette": "针织挂脖连衣裙",
    "straight-neck tailored mini dress, clean neckline, asymmetric hem, long flowing side panels forming a dramatic trailing train, opaque satin opera gloves, pointed high heels": "不对称拖尾迷你礼服",
    "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots": "挂脖荷叶边高低摆礼服",
    "minimal one-piece swimsuit, modest scoop neckline, standard leg openings, clean fitted silhouette, thin straps wrapping around the upper thighs": "连体泳装腿部绑带",
    "retro athletic cheer set, sleeveless high-neck cropped athletic top with large number graphic, matching standard-waist athletic shorts, side stripes, piping and drawstring, semi-opaque polka-dot tights": "复古运动啦啦队套装",
    "sleeveless halter-neck blouse, soft draped fabric, scarf-like neck tie detail, loose flowing silhouette, high-waisted wide-leg trousers": "挂脖飘带上衣长裤",
    "sleeveless high-neck blouse, delicate floral embroidery, lightly textured opaque fabric, softly gathered neckline, subtle ruffled shoulder trim": "刺绣无袖高领上衣",
    "racing crop jacket, motorsport sponsor top, performance event costume": "赛车活动服",
    "lace mini dress, ribbon neck detail, romantic feminine style": "蕾丝短裙",
    "light knit cardigan, soft layered outerwear": "针织开衫",
    "striped lounge pants, casual wide-leg pants": "条纹阔腿裤",
    "athletic crop tank, fitness camisole": "运动背心",
    "high-waist denim mini skirt, casual sporty skirt": "牛仔短裙",
    "ruffled chiffon mini dress, tiered fairy dress, idol rehearsal outfit": "荷叶边蛋糕裙",
    "oversized zip hoodie, casual rehearsal outerwear": "宽松拉链卫衣",
    "chiffon spaghetti-strap maxi dress, flowing skirt, light luxury feminine dating fashion": "青稞雪纺吊带长裙",
    "layered chiffon dress, soft draped layers, gentle girlfriend city-date fashion": "青稞层叠雪纺裙",
    "satin wrap dress, gentle waist definition, quiet luxury weekend date styling": "青稞缎面裹身裙",
    "clean fitted shirt dress, minimal luxury urban lifestyle fashion": "青稞修身衬衫裙",
    "short-sleeve blouse dress, soft mature dating fashion, natural social-media outfit": "青稞短袖衬衫裙",
    "floral tailored top with high-waist skirt, soft romantic rich-girl styling": "青稞碎花上衣半裙",
    "lace tailored blouse with delicate panel detail, clean refined feminine fashion": "青稞蕾丝精致上衣",
    "off-shoulder floral tailored top with elegant shoulder line, light luxury dating style": "青稞露肩碎花上衣",
    "off-shoulder cable-knit sweater, soft knit, gentle girlfriend styling": "青稞露肩绞花针织",
    "ribbed off-shoulder knit sweater, clean rich-girl casual fashion": "青稞罗纹露肩针织",
    "off-shoulder mini dress, refined slim silhouette, weekend city date fashion": "青稞露肩短裙",
    "pleated mini skirt with fitted blouse, soft intellectual date styling": "青稞衬衫百褶短裙",
    "layered tulle skirt with lightweight blouse, romantic urban lifestyle outfit": "青稞薄纱半裙",
    "high-waist straight-leg jeans with fitted blouse, elegant city walk styling": "青稞衬衫直筒牛仔裤",
    "shoulder-draped striped sweater over fitted blouse, clean rich-girl lifestyle fashion": "青稞披肩针织衬衫",
}

QINGKE_LIGHT_LUXURY_THEMES = [
    "chiffon spaghetti-strap maxi dress, flowing skirt, light luxury feminine dating fashion",
    "layered chiffon dress, soft draped layers, gentle girlfriend city-date fashion",
    "satin wrap dress, gentle waist definition, quiet luxury weekend date styling",
    "clean fitted shirt dress, minimal luxury urban lifestyle fashion",
    "short-sleeve blouse dress, soft mature dating fashion, natural social-media outfit",
    "floral tailored top with high-waist skirt, soft romantic rich-girl styling",
    "lace tailored blouse with delicate panel detail, clean refined feminine fashion",
    "off-shoulder floral tailored top with elegant shoulder line, light luxury dating style",
    "off-shoulder cable-knit sweater, soft knit, gentle girlfriend styling",
    "ribbed off-shoulder knit sweater, clean rich-girl casual fashion",
    "off-shoulder mini dress, refined slim silhouette, weekend city date fashion",
    "pleated mini skirt with fitted blouse, soft intellectual date styling",
    "layered tulle skirt with lightweight blouse, romantic urban lifestyle outfit",
    "high-waist straight-leg jeans with fitted blouse, elegant city walk styling",
    "shoulder-draped striped sweater over fitted blouse, clean rich-girl lifestyle fashion",
]

ZHAO_JINMAI_ORIGINAL_COLOR_THEMES = [
    "white floral lace blouse with opaque lining and bell sleeves, paired with light-blue distressed high-waist denim shorts, polished summer street style",
    "white-based blue small-floral wrap dress with a modest V neckline, fitted waist, and soft A-line skirt, fresh garden style",
    "pink ribbed cropped cardigan over a white fitted straight-neck inner top, paired with a black high-waist skirt or trousers, sweet modern styling",
    "blue, cyan, lime, and white striped crochet-knit sleeveless top with medium-wash high-waist straight-leg jeans, colorful creative casual style",
    "black velvet mermaid evening gown with a modest sweetheart neckline and white chiffon shoulder wrap; keep the gown as dense soft-pile low-sheen velvet and the wrap as lightweight airy opaque chiffon, elegant banquet styling",
    "white fitted ribbed tank top with a gray high-waist pleated skirt and small blue ribbon accent, clean youthful preppy style",
    "cream open-knit oversized sweater with restrained red, orange, navy, and light-blue stripes, paired with light-wash denim shorts, creative casual style",
    "white crossover draped sleeveless top with a modest neckline and coordinated white skirt or trousers, minimalist resort styling",
    "light-blue oversized button-up shirt with rolled sleeves and a dark-navy high-waist A-line mini skirt, clean intellectual casual style",
    "white flowing maxi resort dress with a gathered bow-front bodice and relaxed full-length skirt, airy vacation styling",
    "sky-blue seamless athletic top with wide straps and matching high-waist full-length leggings, clean pilates styling",
    "green-and-white small-check oversized button-up shirt with a gray high-waist pleated skirt and restrained colorful scarf accent, playful preppy style",
    "white mock-neck short-sleeve inner top with a tailored gray sleeveless vest and matching straight skirt, modern preppy set",
    "burgundy cropped lightweight windbreaker over a white inner top with a dark-gray high-waist pleated skirt and black sturdy boots, sporty preppy styling",
    "burgundy knit pullover layered over a blue button-up shirt with a dark-green high-waist corduroy straight skirt, cozy retro preppy style",
    "boxy olive-green and gray plaid wool jacket with a matching skirt and simple black fitted inner top, coordinated autumn set",
    "plain black oversized T-shirt with gray wide-leg sweatpants and a light-beige low-profile cap, relaxed travel casual style",
    "white relaxed crew-neck T-shirt with a black asymmetric athletic wrap skirt, clean sporty daily style",
    "navy-and-white striped short-sleeve knit top with a white clean A-line skirt, brown loafers, and restrained preppy styling",
    "white-based red small-floral camisole midi dress with a square neckline, gathered waist, and softly flowing skirt, gentle garden vacation style",
]

ZHAO_JINMAI_COLOR_FREE_THEMES = [
    "floral lace blouse with opaque lining, bell sleeves, and tailored high-waist denim shorts, polished summer street style",
    "small-floral wrap dress with a modest V neckline, fitted waist, and soft A-line skirt, fresh garden style",
    "ribbed cropped cardigan over a fitted straight-neck inner top, paired with a high-waist skirt or trousers, sweet modern styling",
    "striped crochet-knit sleeveless top with high-waist straight-leg jeans, colorful creative casual style",
    "velvet mermaid evening gown with a modest sweetheart neckline and lightweight chiffon shoulder wrap; keep the gown as dense soft-pile low-sheen velvet and the wrap as lightweight airy opaque chiffon, elegant banquet styling",
    "fitted ribbed tank top with a high-waist pleated skirt and small ribbon accent, clean youthful preppy style",
    "oversized multicolor open-knit sweater with relaxed denim shorts, creative casual street style",
    "crossover draped sleeveless top with a modest neckline and coordinated skirt or trousers, minimalist resort styling",
    "oversized button-up shirt with rolled sleeves and a high-waist A-line mini skirt, clean intellectual casual style",
    "flowing maxi resort dress with a gathered bow-front bodice and relaxed full-length skirt, airy vacation styling",
    "seamless athletic top with wide straps and matching high-waist full-length leggings, clean pilates styling",
    "small-check oversized button-up shirt with a high-waist pleated skirt and restrained scarf accent, playful preppy style",
    "mock-neck short-sleeve inner top with a tailored sleeveless vest and matching straight skirt, modern preppy set",
    "cropped lightweight windbreaker over a simple inner top with a high-waist pleated skirt and sturdy boots, sporty preppy styling",
    "knit pullover layered over a button-up shirt with a high-waist corduroy straight skirt, cozy retro preppy style",
    "boxy plaid wool jacket with a matching skirt and simple fitted inner top, coordinated autumn set",
    "plain oversized T-shirt with wide-leg sweatpants and a low-profile cap, relaxed travel casual style",
    "relaxed crew-neck T-shirt with an asymmetric athletic wrap skirt, clean sporty daily style",
    "striped short-sleeve knit top with a clean A-line skirt, loafers, and restrained preppy styling",
    "small-floral camisole midi dress with a square neckline, gathered waist, and softly flowing skirt, gentle garden vacation style",
]

CLOTHING_CATEGORY_OPTIONS = [
    {
        "key": "zhao_jinmai_original",
        "label": "风格: 赵今麦原版服装",
        "themes": ZHAO_JINMAI_ORIGINAL_COLOR_THEMES,
    },
    {
        "key": "zhao_jinmai_color_free",
        "label": "风格: 赵今麦无配色服装",
        "themes": ZHAO_JINMAI_COLOR_FREE_THEMES,
    },
    {
        "key": "yang_mi_original",
        "label": "风格: 杨幂原版服装",
        "themes": YANG_MI_ORIGINAL_COLOR_THEMES,
    },
    {
        "key": "yang_mi_color_free",
        "label": "风格: 杨幂无配色服装",
        "themes": YANG_MI_COLOR_FREE_THEMES,
    },
    {
        "key": "zhang_wonyoung_original",
        "label": "风格: 张元英原版服装",
        "themes": ZHANG_WONYOUNG_ORIGINAL_COLOR_THEMES,
    },
    {
        "key": "zhang_wonyoung_color_free",
        "label": "风格: 张元英无配色服装",
        "themes": ZHANG_WONYOUNG_COLOR_FREE_THEMES,
    },
    {
        "key": "zhang_ruonan_original",
        "label": "风格: 章若楠原版服装",
        "themes": ZHANG_RUONAN_ORIGINAL_COLOR_THEMES,
    },
    {
        "key": "zhang_ruonan_color_free",
        "label": "风格: 章若楠无配色服装",
        "themes": ZHANG_RUONAN_COLOR_FREE_THEMES,
    },
    {
        "key": "daily_city",
        "label": "风格: 日常 / 城市 / 休闲",
        "keywords": [
            "casual", "streetwear", "city", "light-novel", "youthful", "picnic",
            "bakery", "cafe casual", "graphic T-shirt", "denim", "wide-leg pants",
            "zip hoodie", "hoodie", "windbreaker",
        ],
    },
    {
        "key": "school_preppy_date",
        "label": "风格: 学院 / 清爽约会",
        "keywords": [
            "academy", "sailor", "pinafore", "pleated", "preppy", "tennis",
            "date outfit", "sundress", "A-line skirt", "loafers",
        ],
    },
    {
        "key": "sport_event",
        "label": "风格: 运动 / 活动 / 赛车",
        "keywords": [
            "athletic", "sport", "fitness", "racing", "motorsport", "cheer",
            "rehearsal", "performance event", "running shorts", "yoga", "pilates",
        ],
    },
    {
        "key": "knit_home_soft",
        "label": "风格: 针织 / 居家 / 软外套",
        "keywords": [
            "knit", "ribbed", "cardigan", "sweater", "lounge", "homewear",
            "outerwear", "pullover", "zip hoodie",
        ],
    },
    {
        "key": "sweet_skirt_dress",
        "label": "风格: 甜美 / 碎花 / 轻裙装",
        "keywords": [
            "floral", "ruffled", "chiffon", "fairy", "lace dress",
            "lolita", "cottagecore", "romantic", "gingham",
        ],
    },
    {
        "key": "qingke_light_luxury",
        "label": "风格: 青稞全麦 / 轻奢约会",
        "keywords": [
            "light luxury", "rich-girl", "quiet luxury", "weekend date",
            "city-date", "urban lifestyle", "soft mature", "gentle girlfriend",
            "social-media outfit", "intellectual date", "city walk",
            "refined feminine", "weekend city date",
        ],
    },
    {
        "key": "short_skirt_focus",
        "label": "单品: 短裙 / 短裙摆",
        "keywords": [
            "mini skirt", "mini dress", "short pleated sport skirt",
            "pleated mini skirt", "pencil mini skirt", "denim mini skirt",
            "sport skirt", "tiered fairy dress", "short skirt",
            "short one-piece dress", "pleated skirt",
        ],
    },
    {
        "key": "stage_formal_fantasy",
        "label": "风格: 礼服 / 舞台 / 幻想",
        "keywords": [
            "gown", "bridal", "evening", "stage", "idol", "fantasy",
            "asymmetric", "trailing", "princess", "performance", "tailored top",
        ],
    },
    {
        "key": "resort_beach_vacation",
        "label": "风格: 度假 / 沙滩 / 泳装",
        "keywords": [
            "beach", "resort", "vacation", "swim", "swimsuit", "cover shirt",
            "satin lounge slip", "summer sport mood",
        ],
    },
    {
        "key": "special_low_frequency",
        "label": "风格: 特殊 / 黑丝 / 品牌低概率",
        "keywords": [
            "black hosiery", "Adidas-inspired", "Yonex-inspired", "maid remix",
            "bridal dress", "race queen", "motorsport sponsor",
        ],
    },
]

SAFE_DAILY_CLOTHING_POOL = [
    LIGHT_NOVEL_OUTFIT,
    YOUNG_CASUAL_OUTFIT,
    SOFT_DATE_OUTFIT,
    YOUTHFUL_CASUAL_OUTFIT,
    PICNIC_OUTFIT,
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
        "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit",
        "waist-shaped mini dress, lace panels, bell sleeves, boots, idol stagewear",
        "long-sleeve cropped active top, high-waist flare yoga pants, soft pilates outfit",
        "simple camisole, high-waist flare pants, balletcore pilates fashion",
        "retro athletic cheer set, sleeveless high-neck cropped athletic top with large number graphic, matching standard-waist athletic shorts, side stripes, piping and drawstring, semi-opaque polka-dot tights",
        "ruffled chiffon mini dress, tiered fairy dress, idol rehearsal outfit",
        "racing crop jacket, motorsport sponsor top, performance event costume",
        CAFE_MAID_OUTFIT,
        *LOW_PROBABILITY_BRAND_THEMES,
    ],
    "capsule_toy_corner": [
        LIGHT_NOVEL_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        CAFE_MAID_OUTFIT,
    ],
    "graphic_poster_studio": [
        LIGHT_NOVEL_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit",
        "waist-shaped mini dress, lace panels, bell sleeves, boots, idol stagewear",
        "racing crop jacket, motorsport sponsor top, performance event costume",
        "retro athletic cheer set, sleeveless high-neck cropped athletic top with large number graphic, matching standard-waist athletic shorts, side stripes, piping and drawstring, semi-opaque polka-dot tights",
    ],
    "balcony_breeze_half_out_frame": [
        LIGHT_NOVEL_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "greenhouse_terrace_reflection": [
        FLOWER_FANTASY_OUTFIT,
        SOFT_DATE_OUTFIT,
        BRIDAL_OUTFIT,
        FAIRY_FLOATING_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
        "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
        "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt",
        "straight-neck tailored mini dress, clean neckline, asymmetric hem, long flowing side panels forming a dramatic trailing train, opaque satin opera gloves, pointed high heels",
        "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
    ],
    "flower_sea_afternoon": [
        FLOWER_FANTASY_OUTFIT,
        SOFT_DATE_OUTFIT,
        BRIDAL_OUTFIT,
        FAIRY_FLOATING_OUTFIT,
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
        "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
        "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt",
        "straight-neck tailored mini dress, clean neckline, asymmetric hem, long flowing side panels forming a dramatic trailing train, opaque satin opera gloves, pointed high heels",
        "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
    ],
    "flower_bridal_garden": [
        BRIDAL_OUTFIT,
        FLOWER_FANTASY_OUTFIT,
        FAIRY_FLOATING_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
        "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
        "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt",
        "straight-neck tailored mini dress, clean neckline, asymmetric hem, long flowing side panels forming a dramatic trailing train, opaque satin opera gloves, pointed high heels",
        "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
    ],
    "white_room_floor_window": [
        *REGULAR_CLOTHING_THEMES,
    ],
    "pure_white_character_focus": [
        *REGULAR_CLOTHING_THEMES,
    ],
    "zero_gravity_fairy_room": [
        FAIRY_FLOATING_OUTFIT,
        FLOWER_FANTASY_OUTFIT,
        BRIDAL_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
        "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
        "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt",
        "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
    ],
    "zero_gravity_fairy_garden": [
        FAIRY_FLOATING_OUTFIT,
        FLOWER_FANTASY_OUTFIT,
        BRIDAL_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
        "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
        "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt",
        "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
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
        FIVE_SLEEVE_WHITE_SPORT_T_OUTFIT,
    ],
    "far_shot_readable_room": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "telephoto_layered_interior": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "record_shop_listening_corner": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BLUE_GINGHAM_DENIM_OUTFIT,
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "planetarium_star_dome": [
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "beach_wind_open_sand": [
        "striped swim top under loose cover shirt, clean beach resort style",
        "straight-neck maxi dress, simple straight bodice, loose flowing resort silhouette",
        "minimal one-piece swimsuit, modest scoop neckline, standard leg openings, clean fitted silhouette, thin straps wrapping around the upper thighs",
        WHITE_SUNDRESS_STRAW_HAT_OUTFIT,
        SOFT_DATE_OUTFIT,
    ],
    "transparent_acrylic_display_wall": [
        PURE_WHITE_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        SOFT_DATE_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "frosted_glass_partition_scene": [
        SOFT_DATE_OUTFIT,
        PURE_WHITE_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "mirror_fragment_corner": [
        SUNNY_STUDIO_OUTFIT,
        PURE_WHITE_OUTFIT,
        YOUNG_CASUAL_OUTFIT,
        SOFT_DATE_OUTFIT,
        BRIGHT_RED_SHORT_DRESS_OUTFIT,
        "spaghetti-strap lightly fitted mini dress, clean silhouette, minimalist cocktail eveningwear",
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
    "monochrome_color_block_studio": [
        PURE_WHITE_OUTFIT,
        SUNNY_STUDIO_OUTFIT,
        LIGHT_NOVEL_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        "academy pinafore dress, shirt, ribbon tie, round glasses, preppy school style",
        *QINGKE_LIGHT_LUXURY_THEMES,
        "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit",
        "waist-shaped mini dress, lace panels, bell sleeves, boots, idol stagewear",
        "racing crop jacket, motorsport sponsor top, performance event costume",
        "retro athletic cheer set, sleeveless high-neck cropped athletic top with large number graphic, matching standard-waist athletic shorts, side stripes, piping and drawstring, semi-opaque polka-dot tights",
        "straight-neck tailored mini dress, clean neckline, asymmetric hem, long flowing side panels forming a dramatic trailing train, opaque satin opera gloves, pointed high heels",
        "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
    ],
    "hanging_fabric_light_tunnel": [
        SOFT_DATE_OUTFIT,
        YOUTHFUL_CASUAL_OUTFIT,
        ASYMMETRIC_WHITE_T_OUTFIT,
        LACE_OFF_SHOULDER_DRESS_OUTFIT,
        "satin lounge slip dress, lace panel, halter neck, side tie ribbon, relaxed resort-home mood",
        "straight-neck opaque top with oversized cardigan worn off shoulders, relaxed knit loungewear style",
        "knit halter dress, textured fabric, clean upper-body fit, soft draped summer silhouette",
        *QINGKE_LIGHT_LUXURY_THEMES,
    ],
}
LOW_PROBABILITY_SCENE_ONLY_CLOTHING_BY_PLAN = {
    "trend_mirror_studio": LOW_PROBABILITY_BRAND_THEMES,
}
REGULAR_CLOTHING_THEMES = [
    theme for theme in CLOTHING_THEMES
    if theme not in STRONG_SCENE_ONLY_CLOTHING_THEMES
]
SAFE_DAILY_CLOTHING_POOL = REGULAR_CLOTHING_THEMES[:]
SCENE_CATEGORY_OPTIONS = [
    {
        "key": "studio_closeup",
        "label": "棚拍 / 近景 / 白色落地窗",
        "plan_names": [
            "trend_mirror_studio",
            "capsule_toy_corner",
            "graphic_poster_studio",
            "white_room_floor_window",
        ],
    },
    {
        "key": "daily_outdoor_date",
        "label": "日常 / 户外 / 约会",
        "plan_names": [
            "balcony_breeze_half_out_frame",
            "rooftop_laundry_sunset",
            "beach_wind_open_sand",
            "record_shop_listening_corner",
            "planetarium_star_dome",
        ],
    },
    {
        "key": "mechanism_installation",
        "label": "机制型场景 / 装置构图",
        "plan_names": [
            "transparent_acrylic_display_wall",
            "frosted_glass_partition_scene",
            "mirror_fragment_corner",
            "monochrome_color_block_studio",
            "hanging_fabric_light_tunnel",
        ],
    },
    {
        "key": "dream_garden_dress",
        "label": "花园 / 梦幻 / 礼服",
        "plan_names": [
            "greenhouse_terrace_reflection",
            "flower_sea_afternoon",
            "flower_bridal_garden",
            "zero_gravity_fairy_room",
            "zero_gravity_fairy_garden",
        ],
    },
    {
        "key": "pure_white",
        "label": "纯白",
        "plan_names": ["pure_white_character_focus"],
    },
    {
        "key": "perspective_camera_composition",
        "label": "透视 / 镜头构图 / 室内空间",
        "plan_names": [
            "overhead_deep_perspective_space",
            "low_angle_foreground_depth",
            "far_shot_readable_room",
            "telephoto_layered_interior",
        ],
    },
]
LAST_RUNTIME_GIT_PULL_AT = 0.0
LAST_RUNTIME_CONFIG_REVISION = art_options.RUNTIME_CONFIG_REVISION
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


def recompute_clothing_theme_pools() -> None:
    LOW_PROBABILITY_BRAND_THEMES[:] = [
        theme for theme in CLOTHING_THEMES
        if "Adidas-inspired" in theme or "Yonex-inspired" in theme
    ]
    STRONG_SCENE_ONLY_CLOTHING_THEMES[:] = [
        theme for theme in CLOTHING_THEMES
        if theme in LOW_PROBABILITY_BRAND_THEMES
        or theme in CONDITIONAL_SCENE_ONLY_CLOTHING_THEMES
        or "black hosiery" in theme
        or "maid remix" in theme
        or "bridal dress" in theme
    ]
    REGULAR_CLOTHING_THEMES[:] = [
        theme for theme in CLOTHING_THEMES
        if theme not in STRONG_SCENE_ONLY_CLOTHING_THEMES
    ]
    SAFE_DAILY_CLOTHING_POOL[:] = REGULAR_CLOTHING_THEMES[:]


def validate_runtime_batch_config(config_data: dict) -> None:
    plan_names = {plan["name"] for plan in ART_DIRECTION_PLANS}
    clothing_themes = set(CLOTHING_THEMES)
    compatibility = config_data.get("plan_compatible_clothing_themes", PLAN_COMPATIBLE_CLOTHING_THEMES)
    categories = config_data.get("scene_category_options", SCENE_CATEGORY_OPTIONS)
    if not isinstance(compatibility, dict):
        raise ValueError("plan_compatible_clothing_themes must be an object")
    unknown_plans = sorted(set(compatibility) - plan_names)
    if unknown_plans:
        raise ValueError(f"plan_compatible_clothing_themes references unknown plans: {unknown_plans}")
    for plan_name, themes in compatibility.items():
        if not isinstance(themes, list):
            raise ValueError(f"compatible clothing for {plan_name} must be a list")
        unknown_themes = sorted(theme for theme in themes if theme not in clothing_themes)
        if unknown_themes:
            raise ValueError(f"compatible clothing for {plan_name} references unknown themes: {unknown_themes}")
    if not isinstance(categories, list):
        raise ValueError("scene_category_options must be a list")
    seen_keys: set[str] = set()
    for option in categories:
        if not isinstance(option, dict):
            raise ValueError("scene_category_options contains a non-object item")
        key = option.get("key")
        label = option.get("label")
        plan_list = option.get("plan_names")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("scene category missing key")
        if key in seen_keys:
            raise ValueError(f"duplicate scene category key: {key}")
        seen_keys.add(key)
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"scene category {key} missing label")
        if not isinstance(plan_list, list) or not plan_list:
            raise ValueError(f"scene category {key} must contain plan_names")
        unknown_category_plans = sorted(name for name in plan_list if name not in plan_names)
        if unknown_category_plans:
            raise ValueError(f"scene category {key} references unknown plans: {unknown_category_plans}")


def apply_runtime_batch_config(config_data: dict) -> str:
    previous_config = {
        "revision": art_options.RUNTIME_CONFIG_REVISION,
        "outfit_directions": list(CLOTHING_THEMES),
        "art_direction_plans": [dict(plan) for plan in ART_DIRECTION_PLANS],
        "plan_weight_overrides": dict(art_options.NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES),
    }
    previous_compatibility = {
        plan_name: list(themes)
        for plan_name, themes in PLAN_COMPATIBLE_CLOTHING_THEMES.items()
    }
    previous_categories = [dict(option) for option in SCENE_CATEGORY_OPTIONS]
    try:
        revision = art_options.apply_runtime_art_direction_config(config_data)
        validate_runtime_batch_config(config_data)
        compatibility = config_data.get("plan_compatible_clothing_themes", PLAN_COMPATIBLE_CLOTHING_THEMES)
        categories = config_data.get("scene_category_options", SCENE_CATEGORY_OPTIONS)
        PLAN_COMPATIBLE_CLOTHING_THEMES.clear()
        PLAN_COMPATIBLE_CLOTHING_THEMES.update({
            str(plan_name): list(themes)
            for plan_name, themes in compatibility.items()
        })
        SCENE_CATEGORY_OPTIONS[:] = [dict(option) for option in categories]
        recompute_clothing_theme_pools()
        return revision
    except Exception:
        art_options.apply_runtime_art_direction_config(previous_config)
        PLAN_COMPATIBLE_CLOTHING_THEMES.clear()
        PLAN_COMPATIBLE_CLOTHING_THEMES.update(previous_compatibility)
        SCENE_CATEGORY_OPTIONS[:] = previous_categories
        recompute_clothing_theme_pools()
        raise


def load_runtime_batch_config(path: Path = RUNTIME_CONFIG_PATH) -> str:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return apply_runtime_batch_config(data)


def git_current_revision() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def git_pull_runtime_config() -> bool:
    result = subprocess.run(
        ["git", "pull", "--ff-only"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=False,
        timeout=RUNTIME_GIT_PULL_TIMEOUT_SECONDS,
    )
    if result.returncode == 0:
        detail = (result.stdout or "").strip().splitlines()
        print(f"Runtime git pull ok: {detail[-1] if detail else 'up to date'}", flush=True)
        return True
    stderr = (result.stderr or result.stdout or "").strip()
    print(f"Runtime git pull skipped/failed; keeping current config: {stderr}", flush=True)
    return False


def maybe_refresh_runtime_config(
    *,
    force: bool = False,
    enable_git_pull: bool = True,
) -> str:
    global LAST_RUNTIME_GIT_PULL_AT, LAST_RUNTIME_CONFIG_REVISION
    now = time.monotonic()
    due = force or (now - LAST_RUNTIME_GIT_PULL_AT >= RUNTIME_GIT_PULL_INTERVAL_SECONDS)
    if not due:
        return LAST_RUNTIME_CONFIG_REVISION
    LAST_RUNTIME_GIT_PULL_AT = now
    if enable_git_pull:
        git_pull_runtime_config()
    if not RUNTIME_CONFIG_PATH.exists():
        print(f"Runtime config not found; using Python defaults: {RUNTIME_CONFIG_PATH}", flush=True)
        LAST_RUNTIME_CONFIG_REVISION = art_options.RUNTIME_CONFIG_REVISION
        return LAST_RUNTIME_CONFIG_REVISION
    try:
        revision = load_runtime_batch_config(RUNTIME_CONFIG_PATH)
    except Exception as exc:
        print(f"Runtime config reload failed; keeping previous valid config: {exc}", flush=True)
        return LAST_RUNTIME_CONFIG_REVISION
    LAST_RUNTIME_CONFIG_REVISION = revision
    print(
        f"Runtime config active: revision={revision}, git={git_current_revision()}, "
        f"plans={len(ART_DIRECTION_PLANS)}, clothing={len(CLOTHING_THEMES)}",
        flush=True,
    )
    return LAST_RUNTIME_CONFIG_REVISION


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


def focus_chatgpt_input() -> None:
    plus_x, plus_y = COORDS["plus_button"]
    input_x = int(plus_x + 100)
    input_y = int(plus_y)
    click_slow(input_x, input_y, after=0.35)


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
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.15)
    print(f"Upload: selecting reference files: {file_list}", flush=True)
    paste_text(file_list)
    pyautogui.press("enter")

    # Wait for ChatGPT to attach/process thumbnails before typing text.
    wait_with_echo(upload_settle_seconds(len(upload_files)), "Upload settle")
    return upload_files


def send_prompt(prompt: str) -> None:
    print("Prompt: focusing ChatGPT input", flush=True)
    focus_chatgpt_input()
    print("Prompt: pasting text", flush=True)
    paste_text(prompt)

    # Upload completion can leave the send button inactive briefly.
    wait_with_echo(TEXT_BEFORE_SEND_SECONDS, "Before send")
    print("Prompt: clicking send button", flush=True)
    click_send_button()


def with_image_prompt_prefix(prompt: str) -> str:
    prompt = str(prompt).strip()
    if prompt.startswith(IMAGE_PROMPT_PREFIX):
        return prompt
    return f"{IMAGE_PROMPT_PREFIX}\n{prompt}"


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
    shot_scale: dict | None = None,
    outfit_prompt: str | None = None,
    black_hosiery_applied: bool = False,
    config_revision: str = "",
    composition_plan: dict | None = None,
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
            "outfit_prompt": outfit_prompt or theme,
            "black_hosiery_applied": black_hosiery_applied,
            "scene": scene,
            "pose": pose,
            "lighting": lighting,
            "mood": mood,
            "prompt_template": prompt_name,
            "config_revision": config_revision,
            "propagation_profile": propagation_profile,
            "required_identity_tokens": required_identity_tokens or [],
            "viewer_distance": viewer_distance,
            "shot_scale": shot_scale,
            "composition_plan": composition_plan or {},
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

    if (
        scene_only_compatible
        and random.random() < SCENE_ONLY_COMPATIBLE_OUTFIT_CHANCE
    ):
        return random.choice(scene_only_compatible)

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
    print("Input examples: Enter/r/random = all scenes; 1 = category 1; 137 = categories 1,3,7.", flush=True)
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


def _parse_clothing_selection(raw_choice: str) -> list[str] | None:
    choice = raw_choice.strip()
    if not choice or choice.lower() in {"r", "random", "all-random", "全随机", "随机"}:
        return None

    normalized = choice.replace("，", ",").replace("、", ",").replace(" ", ",")
    tokens = [token.strip() for token in normalized.split(",") if token.strip()]

    selected: list[str] = []
    theme_lookup = {theme.lower(): theme for theme in CLOTHING_THEMES}
    for token in tokens:
        themes: list[str] = []
        if token.startswith("#") and token[1:].isdigit():
            index = int(token[1:])
            if 1 <= index <= len(CLOTHING_THEMES):
                themes = [CLOTHING_THEMES[index - 1]]
        elif "-" in token:
            start_text, end_text = token.split("-", 1)
            if not start_text.isdigit() or not end_text.isdigit():
                raise ValueError(f"Unknown clothing selection: {token!r}")
            start_index = int(start_text)
            end_index = int(end_text)
            if start_index > end_index:
                raise ValueError(f"Clothing range must be ascending: {token!r}")
            if start_index < 1 or end_index > len(CLOTHING_CATEGORY_OPTIONS):
                raise ValueError(f"Clothing category range out of bounds: {token!r}")
            for option in CLOTHING_CATEGORY_OPTIONS[start_index - 1:end_index]:
                themes.extend(_themes_for_clothing_category(option))
        elif token.isdigit():
            index = int(token)
            if 1 <= index <= len(CLOTHING_CATEGORY_OPTIONS):
                themes = _themes_for_clothing_category(CLOTHING_CATEGORY_OPTIONS[index - 1])
        else:
            option = _clothing_category_by_key_or_label(token)
            if option:
                themes = _themes_for_clothing_category(option)
            theme = theme_lookup.get(token.lower())
            if theme and not themes:
                themes = [theme]

        if not themes:
            raise ValueError(f"Unknown clothing selection: {token!r}")
        for theme in themes:
            if theme not in selected:
                selected.append(theme)

    if not selected:
        raise ValueError("No valid clothing themes selected")
    return selected


def _themes_for_clothing_category(option: dict) -> list[str]:
    explicit_themes = option.get("themes")
    if explicit_themes is not None:
        return [
            theme for theme in explicit_themes
            if theme in CLOTHING_THEMES
        ]
    keywords = [str(keyword).lower() for keyword in option.get("keywords", [])]
    themes = [
        theme for theme in CLOTHING_THEMES
        if any(keyword in theme.lower() for keyword in keywords)
    ]
    return themes


def _clothing_category_by_key_or_label(value: str) -> dict | None:
    target = value.strip().lower()
    for option in CLOTHING_CATEGORY_OPTIONS:
        if target in {option["key"].lower(), option["label"].lower()}:
            return option
    return None


def _print_full_clothing_list() -> None:
    print("-" * 72, flush=True)
    print("完整服装列表:", flush=True)
    for index, theme in enumerate(CLOTHING_THEMES, start=1):
        label = CLOTHING_DISPLAY_LABELS.get(theme, theme)
        print(f"  #{index}. {label} - {theme}", flush=True)


def prompt_clothing_selection() -> list[str] | None:
    print("=" * 72, flush=True)
    print("选择本次服装大类:", flush=True)
    for index, option in enumerate(CLOTHING_CATEGORY_OPTIONS, start=1):
        themes = _themes_for_clothing_category(option)
        print(f"  {index}. {option['label']} ({len(themes)}套) - {option['key']}", flush=True)
    print("输入示例: 回车/r/random = 按场景自动随机; 1 = 第1类随机; 1,3 = 多个大类随机; 2-4 = 第2到4类; list = 展开完整服装; #12 = 完整列表第12套。", flush=True)

    while True:
        raw_choice = input("服装选择: ")
        if raw_choice.strip().lower() in {"list", "ls", "列表", "完整", "all", "全部"}:
            _print_full_clothing_list()
            continue
        try:
            selected_themes = _parse_clothing_selection(raw_choice)
        except ValueError as exc:
            print(f"{exc}. 请重新输入。", flush=True)
            continue

        if selected_themes is None:
            print("服装模式: 按场景自动兼容随机。", flush=True)
        else:
            selected_labels = [
                CLOTHING_DISPLAY_LABELS.get(theme, theme)
                for theme in selected_themes
            ]
            print(f"服装模式: 固定选择池 -> {'、'.join(selected_labels)}", flush=True)
        return selected_themes


def _cli_option_value(option_name: str) -> str | None:
    if option_name not in sys.argv:
        return None
    option_index = sys.argv.index(option_name)
    if option_index + 1 >= len(sys.argv):
        raise ValueError(f"{option_name} requires a value")
    return sys.argv[option_index + 1]


def _env_option_value(name: str) -> str | None:
    value = os.environ.get(name)
    if value is None or not value.strip():
        return None
    return value


def noninteractive_selection_enabled() -> bool:
    return (
        "--auto-start" in sys.argv
        or "--skip-selection" in sys.argv
        or _env_option_value("AUTO_CREATE_AUTO_START") is not None
        or _env_option_value("AUTO_CREATE_SKIP_SELECTION") is not None
    )


def startup_character_selection() -> list[str] | None:
    raw_choice = _cli_option_value("--characters") or _env_option_value("AUTO_CREATE_CHARACTERS")
    if raw_choice is None:
        if noninteractive_selection_enabled():
            print("Character mode: full random cycle (--auto-start).", flush=True)
            return None
        return prompt_character_selection()
    selected = _parse_character_selection(raw_choice)
    if selected is None:
        print("Character mode: full random cycle (startup option).", flush=True)
    else:
        print(f"Character mode: fixed selection from startup option -> {'、'.join(selected)}", flush=True)
    return selected


def startup_scene_selection() -> list[str] | None:
    raw_choice = _cli_option_value("--scenes") or _env_option_value("AUTO_CREATE_SCENES")
    if raw_choice is None:
        if noninteractive_selection_enabled():
            print("Scene mode: full random art-plan cycle (--auto-start).", flush=True)
            return None
        return prompt_scene_category_selection()
    selected_plan_names = _parse_scene_category_selection(raw_choice)
    if selected_plan_names is None:
        print("Scene mode: full random art-plan cycle (startup option).", flush=True)
    else:
        selected_labels = [
            option["label"]
            for option in SCENE_CATEGORY_OPTIONS
            if any(plan_name in selected_plan_names for plan_name in option["plan_names"])
        ]
        print(f"Scene mode: fixed category from startup option -> {'、'.join(selected_labels)}", flush=True)
    return selected_plan_names


def startup_clothing_selection() -> list[str] | None:
    raw_choice = _cli_option_value("--clothing") or _env_option_value("AUTO_CREATE_CLOTHING")
    if raw_choice is None:
        if noninteractive_selection_enabled():
            print("服装模式: 按场景自动兼容随机 (--auto-start).", flush=True)
            return None
        return prompt_clothing_selection()
    selected_themes = _parse_clothing_selection(raw_choice)
    if selected_themes is None:
        print("服装模式: 按场景自动兼容随机 (startup option).", flush=True)
    else:
        selected_labels = [
            CLOTHING_DISPLAY_LABELS.get(theme, theme)
            for theme in selected_themes
        ]
        print(f"服装模式: 启动参数固定选择池 -> {'、'.join(selected_labels)}", flush=True)
    return selected_themes


def next_start_datetime(hour: int, minute: int, now: dt.datetime | None = None) -> dt.datetime:
    if not 0 <= hour <= 23:
        raise ValueError("Hour must be between 0 and 23")
    if not 0 <= minute <= 59:
        raise ValueError("Minute must be between 0 and 59")
    now = now or dt.datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += dt.timedelta(days=1)
    return target


def _prompt_bounded_integer(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
        except ValueError:
            print(f"Please enter an integer from {minimum} to {maximum}.", flush=True)
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Please enter an integer from {minimum} to {maximum}.", flush=True)


def startup_start_time_selection() -> dt.datetime | None:
    if noninteractive_selection_enabled():
        print("Start mode: immediate (--auto-start).", flush=True)
        return None

    print("=" * 72, flush=True)
    print("Choose when to start generating:", flush=True)
    print("  1. Start immediately", flush=True)
    print("  2. Start at a scheduled time", flush=True)
    while True:
        choice = input("Start mode [1/2]: ").strip()
        if choice in {"", "1"}:
            print("Start mode: immediate.", flush=True)
            return None
        if choice == "2":
            hour = _prompt_bounded_integer("Start hour [0-23]: ", 0, 23)
            minute = _prompt_bounded_integer("Start minute [0-59]: ", 0, 59)
            target = next_start_datetime(hour, minute)
            print(f"Start mode: scheduled for {target:%Y-%m-%d %H:%M}.", flush=True)
            return target
        print("Please enter 1 or 2.", flush=True)


def wait_until_start_time(target: dt.datetime | None) -> None:
    if target is None:
        return
    while True:
        remaining = (target - dt.datetime.now()).total_seconds()
        if remaining <= 0:
            print(f"Scheduled start time reached: {target:%Y-%m-%d %H:%M}.", flush=True)
            return
        print(
            f"Waiting for scheduled start: {target:%Y-%m-%d %H:%M} "
            f"({dt.timedelta(seconds=int(remaining))} remaining). Press Ctrl+C to abort.",
            flush=True,
        )
        time.sleep(min(remaining, 60))


def choose_fixed_clothing_theme(
    fixed_clothing_themes: list[str],
    art_plan: dict | None = None,
    cycle_used_themes: set[str] | None = None,
) -> str:
    cycle_used_themes = cycle_used_themes if cycle_used_themes is not None else set()
    if fixed_clothing_themes and all(theme in cycle_used_themes for theme in fixed_clothing_themes):
        cycle_used_themes.clear()
        print(
            "Fixed clothing selection cycle complete; clearing fixed-pool history and starting a new randomized cycle.",
            flush=True,
        )

    if art_plan is not None:
        compatible = [
            theme for theme in fixed_clothing_themes
            if theme in PLAN_COMPATIBLE_CLOTHING_THEMES.get(art_plan["name"], [])
        ]
        if compatible:
            available_compatible = [
                theme for theme in compatible
                if theme not in cycle_used_themes
            ]
            if available_compatible:
                return random.choice(available_compatible)

    available = [
        theme for theme in fixed_clothing_themes
        if theme not in cycle_used_themes
    ]
    return random.choice(available or fixed_clothing_themes)


def black_hosiery_chance_for_character(character_name: str) -> float:
    return CHARACTER_BLACK_HOSIERY_CHANCES.get(character_name, DEFAULT_BLACK_HOSIERY_CHANCE)


def can_add_black_hosiery(theme: str, art_plan: dict) -> bool:
    if art_plan.get("name") in BLACK_HOSIERY_INCOMPATIBLE_PLAN_NAMES:
        return False
    text = f"{theme} {' '.join(art_plan.get('tags', []))}".lower()
    return not any(keyword in text for keyword in BLACK_HOSIERY_INCOMPATIBLE_KEYWORDS)


def outfit_with_optional_black_hosiery(
    character_name: str,
    theme: str,
    art_plan: dict,
) -> tuple[str, bool]:
    if not can_add_black_hosiery(theme, art_plan):
        return theme, False
    if random.random() >= black_hosiery_chance_for_character(character_name):
        return theme, False
    return f"{theme}; {BLACK_HOSIERY_ACCENT}", True


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
    global RUNTIME_GIT_PULL_INTERVAL_SECONDS
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.15

    calibration_only = "--calibrate" in sys.argv
    if calibration_only or not CALIBRATION_FILE.exists():
        calibrate_coords()
        if calibration_only:
            print("Calibration completed. Exiting without starting character or scene selection.")
            return
    else:
        load_calibrated_coords()

    print("Keep ChatGPT desktop open, unlocked, and focused.")
    print("Press Ctrl+C in this terminal to abort. Moving the mouse to a virtual-screen corner pauses the next click.")
    safety_shutdown_enabled = "--shutdown" in sys.argv
    if not safety_shutdown_enabled:
        print("Safety shutdown is disabled for this feedback run. Use --shutdown to enable it.")
    enable_runtime_git_pull = "--no-runtime-git-pull" not in sys.argv
    if "--runtime-pull-interval" in sys.argv:
        interval_index = sys.argv.index("--runtime-pull-interval")
        if interval_index + 1 >= len(sys.argv):
            raise ValueError("--runtime-pull-interval requires seconds")
        RUNTIME_GIT_PULL_INTERVAL_SECONDS = max(30, int(sys.argv[interval_index + 1]))
    maybe_refresh_runtime_config(force=True, enable_git_pull=enable_runtime_git_pull)
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
    fixed_character_selection = startup_character_selection()
    fixed_scene_plan_names = startup_scene_selection()
    fixed_clothing_themes = startup_clothing_selection()
    fixed_clothing_cycle_used: set[str] = set()
    scheduled_start = startup_start_time_selection()
    wait_until_start_time(scheduled_start)
    if safety_shutdown_enabled:
        schedule_safety_shutdown()
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
        print(
            "Clothing mode: "
            + ("automatic compatible random" if fixed_clothing_themes is None else f"{len(fixed_clothing_themes)} fixed clothing themes"),
            flush=True,
        )

        for character_name in selected_characters:
            if run_number > total_runs:
                break

            config_revision = maybe_refresh_runtime_config(enable_git_pull=enable_runtime_git_pull)
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
            shot_scale = choose_shot_scale(recent_visual_tags, art_plan)
            if fixed_clothing_themes is None:
                theme = choose_compatible_clothing_theme(
                    character_name,
                    art_plan,
                    used_by_character,
                    batch_used_themes,
                )
            else:
                theme = choose_fixed_clothing_theme(
                    fixed_clothing_themes,
                    art_plan,
                    fixed_clothing_cycle_used,
                )
            plan_name = art_plan["name"]
            batch_used_themes.add(theme)
            if fixed_clothing_themes is not None:
                fixed_clothing_cycle_used.add(theme)
            batch_used_plans.add(plan_name)
            outfit_prompt, black_hosiery_applied = outfit_with_optional_black_hosiery(
                character_name,
                theme,
                art_plan,
            )
            composition_plan = choose_composition_plan(
                recent_visual_tags,
                art_plan,
                action_style,
                outfit_prompt,
            )
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
                outfit_direction=outfit_prompt,
                shot_scale=shot_scale,
                composition_plan=composition_plan,
            )
            prompt = with_image_prompt_prefix(prompt)

            print("=" * 72, flush=True)
            print(f"[{run_number:02d}/{total_runs}] Starting run", flush=True)
            print(f"[{run_number:02d}] batch character: {character_name}", flush=True)
            print(f"[{run_number:02d}] character: {character_name}", flush=True)
            print(f"[{run_number:02d}] references: {reference_files}", flush=True)
            print(f"[{run_number:02d}] clothing theme: {theme}", flush=True)
            print(f"[{run_number:02d}] black hosiery accent: {'yes' if black_hosiery_applied else 'no'}", flush=True)
            print(f"[{run_number:02d}] scene: {scene}", flush=True)
            print(f"[{run_number:02d}] pose: {pose}", flush=True)
            print(f"[{run_number:02d}] lighting: {lighting}", flush=True)
            print(f"[{run_number:02d}] mood: {mood}", flush=True)
            print(f"[{run_number:02d}] art plan: {plan_name}", flush=True)
            print(f"[{run_number:02d}] config revision: {config_revision}", flush=True)
            print(f"[{run_number:02d}] action style: {action_style['name']}", flush=True)
            print(f"[{run_number:02d}] propagation: {propagation_profile['propagation_translation']}", flush=True)
            print(f"[{run_number:02d}] viewer distance: {viewer_distance}", flush=True)
            print(f"[{run_number:02d}] shot scale: {shot_scale['name']} -> {shot_scale['description']}", flush=True)
            print(f"[{run_number:02d}] composition plan: {composition_plan['name']}", flush=True)
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
                shot_scale,
                outfit_prompt,
                black_hosiery_applied,
                config_revision,
                composition_plan,
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






