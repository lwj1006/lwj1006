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
        "name": "watching_screen_with_focus",
        "body_silhouette": "standing naturally at the roadside fan area, looking slightly upward toward an off-frame public screen with focused anticipation, hands relaxed and simple",
        "tags": ["football_spectator", "watching", "focused"],
    },
    {
        "name": "restrained_goal_reaction",
        "body_silhouette": "caught just after a goal with a bright natural smile and one small raised fist, joyful but not performing for the camera",
        "tags": ["football_spectator", "goal_reaction", "emotion"],
    },
    {
        "name": "tense_match_moment",
        "body_silhouette": "watching a tense match moment with shoulders slightly forward and hands lightly gathered near the chest, face and identity clearly readable",
        "tags": ["football_spectator", "tense", "candid"],
    },
    {
        "name": "casual_fan_zone_pause",
        "body_silhouette": "relaxed roadside pause near the fan zone, attention staying on the off-frame match screen, with a small team-color scarf or wrist accent",
        "tags": ["football_spectator", "street", "casual"],
    },
    {
        "name": "quiet_halftime_wait",
        "body_silhouette": "quiet halftime moment beside a roadside railing or storefront, calmly waiting while distant match light reflects across the face",
        "tags": ["football_spectator", "halftime", "quiet"],
    },
]


FOOTBALL_COMPOSITIONS = [
    {
        "name": "roadside_public_viewing",
        "composition": "vertical commercial key visual at a roadside public-viewing area, character medium-large and slightly off-center",
        "camera": "natural eye-level street-photography view with the character's attention directed toward an off-frame screen",
        "foreground": "one soft railing, curb, or blurred team-color decoration at the edge, never blocking the character",
        "lighting": "evening street light mixed with soft public-screen glow across the face and jersey",
        "guardrail": "the character is a spectator, not a football player; keep the public screen off-frame or distant and unreadable",
    },
    {
        "name": "shopfront_match_screen",
        "composition": "character-focused street scene outside a cafe, convenience store, or shop showing the match on a distant screen",
        "camera": "front three-quarter medium to knee-up candid view, with the character looking toward the screen rather than posing",
        "foreground": "soft storefront edge and one restrained team-color ribbon or scarf shape",
        "lighting": "shop-window light and cool match-screen glow keep face and jersey clear",
        "guardrail": "screen content stays abstract and unreadable; no detailed players, score, logos, or duplicate people",
    },
    {
        "name": "night_fan_zone_portrait",
        "composition": "clean nighttime fan-zone portrait with the character and national-team jersey as the dominant visual read",
        "camera": "stable front three-quarter waist-up to knee-up candid view",
        "foreground": "abstract team-color bunting, scarf edge, and soft street-light bokeh only",
        "lighting": "premium commercial night-street light with gentle screen glow",
        "guardrail": "all signs and screen marks stay abstract; no readable text, scores, logos, crests, or sponsor marks",
    },
]


WORLD_CUP_SHOT_SCALES = [
    {
        "name": "spectator_three_quarter",
        "description": "three-quarter or knee-up roadside spectator framing with face, hair identity, jersey construction, hands, and surrounding fan-zone atmosphere clearly readable",
    },
    {
        "name": "spectator_half_body",
        "description": "waist-up or half-body candid spectator portrait with expression, gaze direction, hair identity, and national-team jersey clearly readable",
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
        f"{spec['team']}-inspired roadside supporter outfit; team-color reference: {spec['kit']}; "
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
        "graphic_concept": f"2026 World Cup-inspired roadside viewing anime key visual for a {spec['team']}-inspired character supporter",
        "spatial_structure": "roadside public-viewing area, cafe or shopfront exterior, or nighttime fan zone with the match screen kept distant or off-frame",
        "visual_device": "team-color street decorations, soft public-screen glow, restrained fan-zone bokeh, and subtle football-event atmosphere",
        "body_silhouette": "natural football-spectator reaction with a clearly readable face, character identity, and supporter jersey",
        "outfit_direction": world_cup_outfit_for(character_name),
        "material_language": "opaque supporter jersey fabric, pavement, storefront glass, railing, team-color scarf accents, and restrained evening lighting",
        "color_strategy": f"the kit's national-team color blocking is dominant and recognizable; character identity colors remain stable; suitability mood is {spec['fit_reason']}",
        "lighting_behavior": "premium evening street lighting and soft screen glow with clear face, eyes, hair silhouette, and jersey color blocks",
        "extra_prompt_guardrail": "one clearly featured character only; the character is a roadside spectator, never a player; no pitch action, football-playing pose, teammates, opponents, referees, trophy, readable signage, or official branding",
        "tags": ["world_cup_special", "football_spectator", "national_team_jersey", "roadside_viewing", spec["slug"]],
        "weight": 1.0,
    }


def choose_world_cup_action_style(character_name=None, recent_tags=None, art_plan=None):
    return dict(random.choice(FOOTBALL_ACTIONS))


def choose_world_cup_shot_scale(recent_tags=None, art_plan=None):
    return dict(random.choice(WORLD_CUP_SHOT_SCALES))


def choose_world_cup_composition_plan(recent_tags=None, art_plan=None, action_style=None, outfit_direction=None):
    return dict(random.choice(FOOTBALL_COMPOSITIONS))
