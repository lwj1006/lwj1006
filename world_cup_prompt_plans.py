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
    ("Japan", "samurai_blue", "deep blue jersey, white shorts, blue socks, restrained red trim", "precise, clever, technical"),
    ("United States", "navy_red_white", "navy jersey with clean red-and-white trim, white shorts, navy socks", "bright, pop-minded, commercial"),
    ("Senegal", "white_green", "white jersey with green and restrained yellow-red trim, green shorts", "warm, friendly, fresh"),
    ("Argentina", "sky_blue_stripes", "sky-blue and white vertical-striped jersey, black shorts, white socks", "quiet, effortless, technically gifted"),
    ("Germany", "white_black", "white jersey with black trim and restrained warm-color shoulder accents, black shorts", "sharp, disciplined, powerful"),
    ("Portugal", "crimson_green", "deep crimson jersey with dark-green trim, green shorts, crimson socks", "calm, luminous, confident"),
    ("Spain", "red_gold", "rich red jersey with gold and navy trim, navy shorts, red socks", "technical, graceful, composed"),
    ("France", "deep_navy", "deep navy jersey with restrained tricolor trim, white shorts, red socks", "modern, powerful, controlled"),
    ("Netherlands", "oranje", "vivid orange jersey with restrained black trim, orange shorts, orange socks", "bold, kinetic, unmistakable"),
    ("Cote d'Ivoire", "orange_green", "rich orange jersey with green-and-white trim, orange shorts", "vivid, warm, celebratory"),
    ("Sweden", "yellow_blue", "bright yellow jersey with blue trim, blue shorts, yellow socks", "sunny, light, elegant"),
    ("Croatia", "red_white_checks", "red-and-white checked jersey, white shorts, blue socks", "distinctive, tactical, mysterious"),
    ("England", "clean_white_navy", "clean white jersey with navy trim, navy shorts, white socks", "classic, elegant, polished"),
    ("Uruguay", "celeste", "celeste sky-blue jersey with black trim, black shorts, black socks", "compact, reserved, resilient"),
    ("Mexico", "green_white_red", "deep green jersey with white and restrained red trim, white shorts", "graphic, festive, determined"),
    ("South Korea", "hot_red", "hot-red jersey with restrained black trim, black shorts, red socks", "fast, compact, energetic"),
    ("Brazil", "canary_yellow", "canary-yellow jersey with green trim, blue shorts, white socks", "rhythmic, playful, creative"),
    ("Denmark", "minimal_red", "minimal deep-red jersey with white trim, red shorts, white socks", "clean, clever, understated"),
    ("Australia", "gold_green", "gold jersey with dark-green trim, green shorts, gold socks", "active, resilient, outdoorsy"),
    ("Colombia", "yellow_blue_red", "golden-yellow jersey with blue and restrained red trim, navy shorts", "fashionable, charismatic, joyful"),
    ("Norway", "red_navy", "red jersey with navy shoulders and restrained white trim, navy shorts", "cool, sharp, focused"),
    ("Switzerland", "crimson_white", "crimson jersey with a simple white geometric accent, white shorts", "precise, modern, composed"),
    ("Morocco", "red_green", "strong red jersey with green trim, red shorts, red socks", "graceful, patient, proud"),
    ("Belgium", "red_black_gold", "deep red jersey with black shoulders and restrained gold trim, black shorts", "professional, strong, graphic"),
    ("Canada", "maple_red", "clean maple-red jersey with white trim, black shorts, red socks", "disciplined, direct, host-nation energy"),
    ("Portugal", "crimson_green_alt", "deep crimson jersey with dark-green trim, green shorts, crimson socks", "gentle, mysterious, composed"),
]


CHARACTER_TEAM_SPECS = {
    character_name: {
        "team": team,
        "slug": slug,
        "kit": kit,
        "fit_reason": fit_reason,
    }
    for character_name, (team, slug, kit, fit_reason) in zip(CHARACTER_NAMES, TEAM_SPECS)
}

if set(CHARACTER_TEAM_SPECS) != set(CHARACTER_PROFILES):
    raise ValueError("World Cup character assignments must exactly match CHARACTER_PROFILES")


FOOTBALL_ACTIONS = [
    {
        "name": "front_facing_hopeful_supporter",
        "body_silhouette": "front-facing iconic supporter-poster pose, shoulders open and upper body stable, hands lightly clasped near the chest, direct eye contact with the viewer, hopeful elegant smile",
        "tags": ["supporter_poster", "front_facing", "hopeful"],
    },
    {
        "name": "front_facing_cheer_fist",
        "body_silhouette": "front-facing clean supporter-poster pose, shoulders open, one small encouraging fist raised beside the shoulder, direct eye contact and a bright confident smile",
        "tags": ["supporter_poster", "front_facing", "cheer"],
    },
    {
        "name": "front_facing_team_pride",
        "body_silhouette": "front-facing supporter-poster pose with shoulders open, one hand resting lightly over the upper chest and the other relaxed, direct proud gaze, clean stable silhouette",
        "tags": ["supporter_poster", "front_facing", "team_pride"],
    },
    {
        "name": "front_facing_scarf_supporter",
        "body_silhouette": "front-facing supporter campaign pose with shoulders open and a restrained team-color scarf held neatly across the upper body, direct welcoming gaze and readable face",
        "tags": ["supporter_poster", "front_facing", "scarf"],
    },
    {
        "name": "front_facing_open_cheer",
        "body_silhouette": "front-facing supporter-poster pose with shoulders open, both hands forming a small clean encouraging gesture near shoulder height, direct friendly gaze and cheerful expression",
        "tags": ["supporter_poster", "front_facing", "cheer"],
    },
]


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
        "youthful roadside supporter styling",
    ),
    (
        "a longline supporter T-shirt with the front hem tied into one small neat knot while the back hem stays loose",
        "clean athletic shorts",
        "playful, energetic, and clearly spectator-like",
    ),
    (
        "a longline supporter T-shirt with the front hem tied into one small neat knot",
        "a simple A-line short skirt",
        "fashionable but casual fan-zone styling",
    ),
    (
        "a longline supporter T-shirt worn loose with the full hem naturally down",
        "a flowing ankle-length casual skirt with a clean simple silhouette",
        "soft, relaxed, and suitable for a quieter spectator",
    ),
    (
        "a regular-length short-sleeve supporter T-shirt worn naturally with the hem down",
        "a flowing calf-length or ankle-length casual skirt",
        "comfortable street-viewing fashion with gentle movement",
    ),
]


FACE_SUPPORTER_MARKS = [
    "no face paint or cheek marking",
    "no face paint or cheek marking",
    "one tiny simple team-color stripe painted on one cheek, with no text, crest, flag emblem, or detailed symbol",
    "one tiny simple team-color geometric cheek mark, abstract and unofficial, with no readable symbol or official crest",
    "one tiny simplified unofficial team-inspired cheek emblem, painted cleanly on one cheek with no text and no exact official crest reproduction",
]


def world_cup_spec_for(character_name):
    return CHARACTER_TEAM_SPECS.get(character_name, {
        "team": "Japan",
        "slug": "samurai_blue",
        "kit": "deep blue jersey, white shorts, blue socks, restrained red trim",
        "fit_reason": "clean, technical, character-first",
    })


def world_cup_outfit_for(character_name):
    spec = world_cup_spec_for(character_name)
    top, bottom, styling_mood = random.choice(SUPPORTER_OUTFIT_VARIANTS)
    face_mark = random.choice(FACE_SUPPORTER_MARKS)
    return (
        f"{spec['team']}-inspired national-team supporter poster outfit; team-color reference only: {spec['kit']}; "
        f"adapt the classic team colors and jersey color blocking into {top}, paired with {bottom}; "
        f"styling mood: {styling_mood}; face supporter detail: {face_mark}; "
        "the selected top and bottom must remain a coherent casual outfit; a tied front hem uses only one small neat knot and must not expose or distort the body; "
        "no football socks or player boots; "
        "tailored to preserve all character hair, ears, tail, mechanical parts, and identity accessories; "
        "no official crest, no sponsor, no readable text, no readable player name, no readable number"
    )


def world_cup_plan_for(character_name):
    spec = world_cup_spec_for(character_name)
    return {
        "name": f"world_cup_{spec['slug']}",
        "label": f"{spec['team']} football special",
        "team": spec["team"],
        "fit_reason": spec["fit_reason"],
        "graphic_concept": f"official campaign-style 2026 World Cup-inspired front-facing supporter poster for a {spec['team']}-inspired character fan",
        "spatial_structure": "bright open football stadium in daylight with clean green pitch, pale seating tiers, blue sky, soft white clouds, and simplified shallow stadium geometry",
        "visual_device": "large team-color graphic panels, diagonal banner shapes, scarf-like borders, clean pitch-line curves, bright stadium shapes, and a clear title-space negative area",
        "body_silhouette": "clean iconic supporter-poster pose with a clearly readable face, character identity, jersey, and outfit silhouette",
        "outfit_direction": world_cup_outfit_for(character_name),
        "material_language": "opaque supporter jersey fabric, fresh green grass, pale stadium seating, matte graphic panels, abstract fabric banners, and bright campaign daylight",
        "color_strategy": f"national-team colors form large bold poster framing and structured design blocks; character identity colors remain stable; suitability mood is {spec['fit_reason']}",
        "lighting_behavior": "bright premium daylight campaign lighting with clear face, eyes, full hair silhouette, jersey color blocks, blue-sky freshness, and controlled graphic separation",
        "extra_prompt_guardrail": "one clearly featured front-facing character only; make a series-ready national-team supporter campaign poster, never a candid viewing scene; no night, darkness, street, cafe, public screen, pitch action, football-playing pose, teammates, opponents, referees, trophy, readable signage, or official branding",
        "tags": ["world_cup_special", "supporter_campaign_poster", "national_team_jersey", "bright_stadium", "front_facing", spec["slug"]],
        "weight": 1.0,
    }


def choose_world_cup_action_style(character_name=None, recent_tags=None, art_plan=None):
    return dict(random.choice(FOOTBALL_ACTIONS))


def choose_world_cup_shot_scale(recent_tags=None, art_plan=None):
    return dict(random.choice(WORLD_CUP_SHOT_SCALES))


def choose_world_cup_composition_plan(recent_tags=None, art_plan=None, action_style=None, outfit_direction=None):
    return dict(random.choice(FOOTBALL_COMPOSITIONS))
