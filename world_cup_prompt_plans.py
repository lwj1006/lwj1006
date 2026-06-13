import random

from art_direction_options import CHARACTER_PROFILES


# Each team is selected for palette, silhouette, and character temperament rather
# than ranking alone. Keep this list aligned with TEAM_SPECS below.
CHARACTER_NAMES = [
    "南宫", "爱芮", "千夏", "丹", "星见雅", "仪玄", "叶瞬光", "席德", "橘福福",
    "柚叶", "爱丽丝", "普罗米娅", "薇薇安", "安比", "可琳", "艾莲", "琉音",
    "耀嘉音", "柏妮思", "妮可", "简", "月城柳", "青衣", "伊芙琳", "朱鸢", "卢西娅",
]


TEAM_SPECS = [
    ("Italy", "italy_home", "royal azzurri-blue jersey with restrained white-and-gold trim, white shorts", "classic, elegant, tactically composed"),
    ("Italy", "italy_away", "clean ivory-white jersey with azzurri-blue and antique-gold trim, blue shorts", "refined, luminous, quietly confident"),
    ("Argentina", "argentina_home", "sky-blue and white vertical-striped jersey with dark trim, black shorts", "quiet, effortless, technically gifted"),
    ("Argentina", "argentina_away", "deep midnight-blue jersey with sky-blue and silver accents, dark shorts", "cool, focused, technically gifted"),
    ("Germany", "germany_home", "white jersey with black trim and restrained warm-color accents, black shorts", "sharp, disciplined, powerful"),
    ("Germany", "germany_away", "deep burgundy-black jersey with restrained red-and-gold geometry, black shorts", "strong, graphic, controlled"),
    ("Portugal", "portugal_home", "deep crimson jersey with dark-green trim and restrained gold accents, green shorts", "calm, luminous, confident"),
    ("Portugal", "portugal_away", "pearl-white jersey with crimson-green graphic panels and gold details, white shorts", "gentle, composed, polished"),
    ("Spain", "spain_home", "rich red jersey with gold and navy trim, navy shorts", "technical, graceful, composed"),
    ("Spain", "spain_away", "pale golden-cream jersey with red-and-navy details, red shorts", "warm, elegant, expressive"),
    ("France", "france_home", "deep navy jersey with restrained tricolor trim, white shorts", "modern, powerful, controlled"),
    ("France", "france_away", "clean white jersey with fine blue-red pinstripes, navy shorts", "polished, poised, modern"),
    ("Netherlands", "netherlands_home", "vivid orange jersey with restrained black trim, orange shorts", "bold, kinetic, unmistakable"),
    ("Netherlands", "netherlands_away", "deep navy jersey with luminous orange geometric accents, navy shorts", "cool, graphic, energetic"),
    ("Croatia", "croatia_home", "red-and-white checked jersey with deep-blue trim, white shorts", "distinctive, tactical, mysterious"),
    ("Croatia", "croatia_away", "deep-blue jersey with restrained red-white check fragments, blue shorts", "composed, distinctive, clever"),
    ("England", "england_home", "clean white jersey with navy trim and restrained red details, navy shorts", "classic, elegant, polished"),
    ("England", "england_away", "deep red jersey with navy-and-white trim, dark shorts", "confident, graphic, traditional"),
    ("Uruguay", "uruguay_home", "celeste sky-blue jersey with black trim, black shorts", "compact, reserved, resilient"),
    ("Uruguay", "uruguay_away", "clean white jersey with celeste and black graphic accents, white shorts", "calm, crisp, resilient"),
    ("Brazil", "brazil_home", "canary-yellow jersey with green trim, blue shorts", "rhythmic, playful, creative"),
    ("Brazil", "brazil_away", "deep cobalt-blue jersey with green-yellow accents, white shorts", "confident, fluid, creative"),
    ("Belgium", "belgium_home", "deep red jersey with black shoulders and restrained gold trim, black shorts", "professional, strong, graphic"),
    ("Belgium", "belgium_away", "warm ivory jersey with burgundy-black and gold details, burgundy shorts", "refined, modern, composed"),
    ("Sweden", "sweden_home", "bright yellow jersey with blue trim, blue shorts", "sunny, light, elegant"),
    ("Sweden", "sweden_away", "deep royal-blue jersey with bright yellow graphic accents, blue shorts", "cool, clean, focused"),
]


# Explicit modern national-team-inspired garment instructions. These prioritize
# image-generation readability over exact official-kit reproduction.
KIT_DESIGNS_2026 = {
    "italy_home": "luminous royal azzurri-blue jersey with subtle tonal Renaissance geometry, crisp white structure, restrained antique-gold edges",
    "italy_away": "ivory-white jersey with elegant azzurri-blue side panels, subtle tonal marble geometry, restrained antique-gold edges",
    "argentina_home": "sky-blue and white vertical stripes using several shifting blue gradients, dark trim, modern clean collar",
    "argentina_away": "midnight-blue jersey with luminous sky-blue diagonal movement, restrained silver details, modern clean cuffs",
    "germany_home": "white jersey with a bold black-red-gold central chevron, white diamond separators, black-and-red trim",
    "germany_away": "burgundy-black jersey with angular red-gold tonal geometry, black shoulder structure, restrained warm highlights",
    "portugal_home": "deep crimson jersey with asymmetric dark-green graphic movement, refined gold micro-accents",
    "portugal_away": "pearl-white jersey with sweeping crimson-green panels, refined gold micro-accents, structured clean collar",
    "spain_home": "rich red jersey with fine yellow-gold vertical pinstripes, dark navy structure at collar and side panels",
    "spain_away": "pale golden-cream jersey with warm red graphic arcs, navy structural details, restrained yellow-gold texture",
    "france_home": "deep navy jersey with layered tricolor edge details, subtle tonal movement, structured shoulder construction",
    "france_away": "clean white jersey with fine blue-red pinstripes, subtle tonal movement, modern navy shoulder structure",
    "netherlands_home": "vivid orange jersey with energetic tonal geometric texture and restrained black structure",
    "netherlands_away": "deep navy jersey with luminous orange angular geometry, clean dark structure, energetic side panels",
    "croatia_home": "red-and-white check identity reworked as clean shifting check geometry with deep-blue trim",
    "croatia_away": "deep-blue jersey with fragmented red-white check geometry, modern clean collar and side panels",
    "england_home": "clean white jersey with subtle tonal lion-and-star jacquard and patriotic navy-red details",
    "england_away": "deep red jersey with subtle tonal heritage geometry, navy-white collar and cuff details",
    "uruguay_home": "celeste jersey with subtle tonal sun-ray geometry, black collar and cuff structure",
    "uruguay_away": "clean white jersey with sweeping celeste panels, restrained black geometry, modern clean cuffs",
    "brazil_home": "canary-yellow jersey with refined tonal cultural pattern, deep-green V-neck and layered sleeve cuffs",
    "brazil_away": "deep cobalt-blue jersey with rhythmic green-yellow tonal movement, modern clean shoulder panels",
    "belgium_home": "deep-red jersey with stained-glass-inspired tonal pattern, black structural panels, refined gold edges",
    "belgium_away": "warm ivory jersey with restrained burgundy-black stained-glass geometry and refined gold edges",
    "sweden_home": "bright yellow jersey with retro-inspired blue collar and sleeve structure, subtle tonal body pattern",
    "sweden_away": "deep royal-blue jersey with bright yellow Nordic geometric movement, clean modern collar and cuffs",
}


TEAM_PROFILE_POOL = [
    {
        "team": team,
        "slug": slug,
        "kit": kit,
        "fit_reason": fit_reason,
    }
    for team, slug, kit, fit_reason in TEAM_SPECS
]

WORLD_CUP_SELECTION_MODE = "random"


FOOTBALL_ACTIONS = [
    {
        "name": "scarf_raised_overhead",
        "body_silhouette": "front-facing football-supporter poster pose, both arms raised clearly overhead while stretching a plain team-color scarf horizontally, chest lifted, natural pleased expression that stays faithful to the character's usual personality, strong triangular silhouette",
        "tags": ["supporter_poster", "football_culture", "scarf_overhead"],
    },
    {
        "name": "scarf_across_chest",
        "body_silhouette": "front-facing football-supporter poster pose, both hands holding the ends of a plain team-color scarf stretched cleanly across the upper chest, shoulders open, subtle confident expression faithful to the character",
        "tags": ["supporter_poster", "football_culture", "scarf_chest"],
    },
    {
        "name": "flag_spread_behind_shoulders",
        "body_silhouette": "front-facing football-supporter hero pose, both arms opened wide while holding the two upper corners of a large national flag fully spread behind the shoulders as a bold background silhouette, flag not worn or wrapped around the body, restrained proud expression faithful to the character",
        "tags": ["supporter_poster", "football_culture", "flag_spread"],
    },
    {
        "name": "large_flag_front_diagonal",
        "body_silhouette": "front-facing football-supporter hero pose holding a large national flag diagonally across the lower foreground with both hands, flag sweeping from one lower corner toward the opposite side while face, upper torso, and jersey design remain fully visible, natural confident expression",
        "tags": ["supporter_poster", "football_culture", "flag_front"],
    },
    {
        "name": "large_flag_side_wave",
        "body_silhouette": "front-facing football-supporter celebration pose using both hands to control a clean flagpole at one side while a large national flag billows outward beside the body in a strong side arc, torso engaged, naturally cheerful expression without exaggeration",
        "tags": ["supporter_poster", "football_culture", "flag_side"],
    },
    {
        "name": "large_flag_front_open",
        "body_silhouette": "front-facing football-supporter poster pose holding the two upper corners of a large national flag opened across the lower front of the body at waist height, keeping the jersey upper body, hands, face, and hair identity clearly visible, subtle proud expression",
        "tags": ["supporter_poster", "football_culture", "flag_front"],
    },
    {
        "name": "small_flag_wave",
        "body_silhouette": "front-facing football-supporter celebration pose, one hand holding a small national flag on a short clean pole and waving it diagonally above shoulder height, other arm bent in an energetic cheer, natural friendly smile faithful to the character",
        "tags": ["supporter_poster", "football_culture", "flag_wave"],
    },
    {
        "name": "double_low_fist_goal_celebration",
        "body_silhouette": "front-facing football-supporter goal celebration, both fists held low beside the waist with elbows bent and torso leaning slightly forward, controlled happy reaction faithful to the character's normal expression range",
        "tags": ["supporter_poster", "football_culture", "goal_celebration"],
    },
    {
        "name": "tense_clasped_supporter",
        "body_silhouette": "front-facing football-supporter tense-match pose, both hands clasped gently together near the upper chest, shoulders only slightly raised, focused attentive expression with restrained natural tension",
        "tags": ["supporter_poster", "football_culture", "tense_match"],
    },
]

RECOMMENDED_CHARACTER_MATCHES = {
    "南宫": ("argentina_home", "scarf_across_chest"),
    "爱芮": ("netherlands_home", "small_flag_wave"),
    "千夏": ("sweden_home", "scarf_raised_overhead"),
    "丹": ("france_away", "large_flag_front_open"),
    "星见雅": ("germany_away", "large_flag_front_diagonal"),
    "仪玄": ("italy_away", "flag_spread_behind_shoulders"),
    "叶瞬光": ("spain_home", "large_flag_front_open"),
    "席德": ("uruguay_home", "large_flag_side_wave"),
    "橘福福": ("netherlands_home", "double_low_fist_goal_celebration"),
    "柚叶": ("belgium_home", "large_flag_front_diagonal"),
    "爱丽丝": ("portugal_away", "scarf_across_chest"),
    "普罗米娅": ("france_home", "flag_spread_behind_shoulders"),
    "薇薇安": ("croatia_away", "large_flag_front_open"),
    "安比": ("germany_home", "scarf_across_chest"),
    "可琳": ("sweden_away", "small_flag_wave"),
    "艾莲": ("england_away", "large_flag_front_diagonal"),
    "琉音": ("brazil_away", "scarf_raised_overhead"),
    "耀嘉音": ("italy_home", "flag_spread_behind_shoulders"),
    "柏妮思": ("brazil_home", "double_low_fist_goal_celebration"),
    "妮可": ("spain_away", "large_flag_side_wave"),
    "简": ("belgium_away", "large_flag_front_open"),
    "月城柳": ("croatia_home", "flag_spread_behind_shoulders"),
    "青衣": ("uruguay_away", "scarf_across_chest"),
    "伊芙琳": ("portugal_home", "large_flag_front_diagonal"),
    "朱鸢": ("england_home", "scarf_raised_overhead"),
    "卢西娅": ("argentina_away", "small_flag_wave"),
}


FOOTBALL_COMPOSITIONS = [
    {
        "name": "official_supporter_campaign_poster",
        "composition": "front-facing vertical national-team supporter campaign poster, character centered or heroically near-center, with clear title-space negative area above or beside the character",
        "camera": "stable eye-level knee-up or thigh-up poster view, direct eye contact, full hair silhouette visible, clean margin around head, shoulders, and hair",
        "foreground": "restrained team-color border shapes, scarf-like framing accents, and a clean white pitch-line curve used as graphic layers",
        "lighting": "bright premium daylight campaign light with clear facial detail and fresh stadium atmosphere",
        "guardrail": "must read as a designed front-facing supporter poster; no candid viewing behavior, no cramped crop, no dark environment",
    },
    {
        "name": "bright_stadium_graphic_poster",
        "composition": "vertical graphic supporter campaign poster with an iconic front-facing pose, bright football stadium, and structured national-color design blocks",
        "camera": "stable eye-level knee-up or thigh-up poster framing with direct eye contact, full hair silhouette, readable outfit, and deliberate clean margins",
        "foreground": "large diagonal national-color banner shapes, abstract scarf borders, and one clean green-pitch layer",
        "lighting": "bright sunny commercial light with soft controlled shadows and clean blue-sky fill",
        "guardrail": "football stadium stays bright, open, simplified, and subordinate; no night lighting, screen viewing, street, cafe, or realistic match action",
    },
    {
        "name": "national_color_hero_poster",
        "composition": "series-ready vertical national-team supporter hero poster with the front-facing character as the central icon and a clear empty title zone",
        "camera": "stable front-facing thigh-up or knee-up view with direct eye contact, full hairstyle and outfit silhouette readable with generous breathing room",
        "foreground": "clean national-color arcs, cross-inspired or stripe-inspired abstract blocks, bright pitch-line geometry, and restrained supporter framing",
        "lighting": "polished bright daylight campaign lighting with controlled graphic separation",
        "guardrail": "national colors must become large designed poster elements; stadium remains bright and clean; no readable text, scores, logos, or crests",
    },
]


WORLD_CUP_SHOT_SCALES = [
    {
        "name": "supporter_poster_knee_up",
        "description": "vertical knee-up or thigh-up supporter-poster framing with full hair silhouette visible, clean margin around head and shoulders, readable face, hands, jersey, and bottom silhouette",
    },
    {
        "name": "supporter_poster_three_quarter",
        "description": "vertical three-quarter supporter-poster framing with the complete main silhouette, generous breathing room, and a clear negative-space title area",
    },
]


SUPPORTER_OUTFIT_VARIANTS = [
    (
        "a regular-length short-sleeve supporter T-shirt worn naturally with the hem down",
        "clean athletic shorts",
        "fresh, active, and easy to read",
    ),
    (
        "a slightly oversized short-sleeve supporter T-shirt worn naturally with the hem down",
        "a clean pleated short skirt",
        "youthful national-team supporter poster styling",
    ),
    (
        "a longline supporter T-shirt with the front hem tied into one small neat knot while the back hem stays loose",
        "clean athletic shorts",
        "playful, energetic, and clearly suited to a front-facing supporter poster",
    ),
    (
        "a longline supporter T-shirt with the front hem tied into one small neat knot",
        "a simple A-line short skirt",
        "fashionable national-team supporter poster styling",
    ),
]


FACE_SUPPORTER_MARKS = [
    "no face paint or cheek marking",
    "no face paint or cheek marking",
    "one tiny simple team-color stripe painted on one cheek, with no text, crest, flag emblem, or detailed symbol",
    "one tiny simple team-color geometric cheek mark, abstract and unofficial, with no readable symbol or official crest",
    "one tiny simplified unofficial team-inspired cheek emblem, painted cleanly on one cheek with no text and no exact official crest reproduction",
]


def world_cup_spec_for(character_name=None):
    if WORLD_CUP_SELECTION_MODE == "recommended":
        slug, _ = RECOMMENDED_CHARACTER_MATCHES.get(character_name, (None, None))
        if slug:
            return dict(next(spec for spec in TEAM_PROFILE_POOL if spec["slug"] == slug))
    return dict(random.choice(TEAM_PROFILE_POOL))


def set_world_cup_selection_mode(mode):
    global WORLD_CUP_SELECTION_MODE
    normalized = str(mode or "random").strip().lower()
    if normalized not in {"random", "recommended"}:
        raise ValueError(f"Unknown World Cup selection mode: {mode}")
    WORLD_CUP_SELECTION_MODE = normalized


def world_cup_selection_mode():
    return WORLD_CUP_SELECTION_MODE


def world_cup_outfit_for(character_name):
    spec = world_cup_spec_for(character_name)
    return world_cup_outfit_for_spec(spec)


def world_cup_outfit_for_spec(spec):
    top, bottom, styling_mood = random.choice(SUPPORTER_OUTFIT_VARIANTS)
    face_mark = random.choice(FACE_SUPPORTER_MARKS)
    jersey_design = KIT_DESIGNS_2026.get(spec["slug"], spec["kit"])
    return (
        f"{spec['team']}-inspired modern national-team supporter poster outfit; jersey design: {jersey_design}; "
        f"apply this explicit jersey pattern, collar, sleeve-cuff, and panel language to {top}, paired with {bottom}; "
        f"styling mood: {styling_mood}; face supporter detail: {face_mark}; "
        "the selected top and bottom must remain a coherent casual outfit; a tied front hem uses only one small neat knot and must not expose or distort the body; "
        "no football socks or player boots; "
        "tailored to preserve all character hair, ears, tail, mechanical parts, and identity accessories; "
        "preserve the specified tonal pattern and garment construction; do not simplify it into a plain-color jersey; "
        "no official crest, no sponsor, no manufacturer logo, no readable text, no readable player name, no readable number"
    )


def world_cup_plan_for(character_name, spec=None):
    spec = dict(spec or world_cup_spec_for(character_name))
    return {
        "name": f"world_cup_{spec['slug']}",
        "label": f"{spec['team']} football special",
        "team": spec["team"],
        "fit_reason": spec["fit_reason"],
        "graphic_concept": f"official campaign-style 2026 World Cup-inspired front-facing supporter poster for a {spec['team']}-inspired character fan",
        "spatial_structure": "bright open football stadium in daylight with clean green pitch, pale seating tiers, blue sky, soft white clouds, and simplified shallow stadium geometry",
        "visual_device": "large team-color graphic panels, diagonal banner shapes, scarf-like borders, clean pitch-line curves, bright stadium shapes, and a clear title-space negative area",
        "body_silhouette": "clean iconic supporter-poster pose with a clearly readable face, character identity, jersey, and outfit silhouette",
        "outfit_direction": world_cup_outfit_for_spec(spec),
        "material_language": "opaque supporter jersey fabric, fresh green grass, pale stadium seating, matte graphic panels, abstract fabric banners, and bright campaign daylight",
        "color_strategy": f"national-team colors form large bold poster framing and structured design blocks; character identity colors remain stable; suitability mood is {spec['fit_reason']}",
        "lighting_behavior": "bright premium daylight campaign lighting with clear face, eyes, full hair silhouette, jersey color blocks, blue-sky freshness, and controlled graphic separation",
        "extra_prompt_guardrail": "one clearly featured front-facing character only; make a series-ready national-team supporter campaign poster, never a candid viewing scene; no night, darkness, street, cafe, public screen, pitch action, football-playing pose, teammates, opponents, referees, trophy, readable signage, or official branding",
        "tags": ["world_cup_special", "supporter_campaign_poster", "national_team_jersey", "bright_stadium", "front_facing", spec["slug"]],
        "weight": 1.0,
    }


def choose_world_cup_action_style(character_name=None, recent_tags=None, art_plan=None):
    if WORLD_CUP_SELECTION_MODE == "recommended":
        _, action_name = RECOMMENDED_CHARACTER_MATCHES.get(character_name, (None, None))
        if action_name:
            return dict(next(action for action in FOOTBALL_ACTIONS if action["name"] == action_name))
    return dict(random.choice(FOOTBALL_ACTIONS))


def choose_world_cup_shot_scale(recent_tags=None, art_plan=None):
    return dict(random.choice(WORLD_CUP_SHOT_SCALES))


def choose_world_cup_composition_plan(recent_tags=None, art_plan=None, action_style=None, outfit_direction=None):
    return dict(random.choice(FOOTBALL_COMPOSITIONS))
