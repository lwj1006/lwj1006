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


# Explicit modern national-team-inspired garment instructions. These prioritize
# image-generation readability over exact official-kit reproduction.
KIT_DESIGNS_2026 = {
    "samurai_blue": "2026-style oceanic ash-blue jersey, deep blue tonal wave-like field, sharp pale-blue shoulder and sleeve geometry, modern structured V-neck",
    "navy_red_white": "2026 dark home-style jersey with bespoke tonal star jacquard, crisp red-and-white edge details, modern clean collar and structured sleeve panels",
    "white_green": "2026-era white jersey with fresh green shoulder structure, restrained yellow-red cultural accents, subtle tonal performance texture",
    "sky_blue_stripes": "2026 home-style sky-blue and white vertical stripes using several shifting blue gradients inspired by championship eras, dark trim, modern clean collar",
    "white_black": "2026 white jersey with a bold black-red-gold central chevron, white diamond separators, black-and-red collar and sleeve trim",
    "crimson_green": "2026-era deep crimson jersey with asymmetric dark-green graphic movement, refined gold micro-accents, modern structured collar and cuffs",
    "red_gold": "2026 red jersey with fine yellow-gold vertical pinstripes, dark navy structure at collar and side panels, clean modern cuffs",
    "deep_navy": "2026-era deep navy jersey with layered tricolor edge details, subtle tonal movement across the body, modern structured shoulder and sleeve construction",
    "oranje": "2026-era vivid orange jersey with energetic tonal geometric texture, restrained black collar and sleeve structure, modern clean side panels",
    "orange_green": "2026-era rich orange jersey with modern green-and-white angular side graphics, subtle tonal cultural texture, clean structured cuffs",
    "yellow_blue": "2026 home-style bright yellow jersey with retro-inspired blue collar and sleeve structure, subtle tonal body pattern, clean modern fit",
    "red_white_checks": "2026-era red-and-white check identity reworked as clean shifting check geometry, deep-blue trim, modern structured collar and side panels",
    "clean_white_navy": "2026-style clean white jersey with subtle tonal lion-and-star jacquard, patriotic navy-and-red collar and cuff details, modern structured shoulder panels",
    "celeste": "2026-era celeste jersey with subtle tonal sun-ray geometry, black collar and cuff structure, modern clean side panels",
    "green_white_red": "2026 green jersey with bold tonal Aztec Sun Stone-inspired pattern, refined red-white-blue host accents, structured collar and sleeve trim",
    "hot_red": "2026-era vivid red jersey with flowing black tonal brush or tiger-inspired motion pattern, clean black collar and sleeve structure",
    "canary_yellow": "2026-era canary-yellow jersey with a refined tonal cultural pattern, deep-green V-neck and layered sleeve cuffs, modern green side-panel details",
    "minimal_red": "2026-era deep red jersey with subtle tonal Scandinavian geometric texture, crisp white collar and cuff details, minimal modern structure",
    "gold_green": "2026-era rich gold jersey with deep-green V-neck, layered green-gold cuffs, and a refined tonal star or constellation-inspired body pattern",
    "yellow_blue_red": "2026 yellow jersey with delicate tonal butterfly motifs, refined blue-red edge details, modern clean collar and sleeve panels",
    "red_navy": "2026-era strong red jersey with deep-navy shoulder and side structure, subtle Nordic tonal geometry, crisp white micro-accents",
    "crimson_white": "2026-era crimson jersey with clean white geometric movement, subtle tonal alpine-inspired structure, modern collar and cuffs",
    "red_green": "2026-era rich red jersey with deep-green geometric cultural patterning, clean green collar and cuffs, restrained white detailing",
    "red_black_gold": "2026 deep-red jersey with stained-glass-inspired tonal pattern, black structural panels, refined gold edge details",
    "maple_red": "2026-era maple-red jersey with subtle tonal leaf-inspired geometry, crisp white structure, modern clean collar and sleeve panels",
    "crimson_green_alt": "2026-era deep crimson supporter jersey with flowing dark-green graphic panels, restrained gold accents, modern structured collar and cuffs",
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


FOOTBALL_ACTIONS = [
    {
        "name": "scarf_raised_overhead",
        "body_silhouette": "front-facing football-supporter poster pose, both arms raised clearly overhead while stretching a plain team-color scarf horizontally, chest lifted, wide proud smile with bright excited eyes, strong triangular silhouette",
        "tags": ["supporter_poster", "football_culture", "scarf_overhead"],
    },
    {
        "name": "scarf_across_chest",
        "body_silhouette": "front-facing football-supporter poster pose, both hands holding the ends of a plain team-color scarf stretched cleanly across the upper chest, shoulders open, warm confident smile and lively eyes",
        "tags": ["supporter_poster", "football_culture", "scarf_chest"],
    },
    {
        "name": "flag_spread_behind_shoulders",
        "body_silhouette": "front-facing football-supporter hero pose, both arms opened wide while holding the two upper corners of a large national flag fully spread behind the shoulders as a bold background silhouette, flag not worn or wrapped around the body, confident celebratory smile",
        "tags": ["supporter_poster", "football_culture", "flag_spread"],
    },
    {
        "name": "large_flag_front_diagonal",
        "body_silhouette": "front-facing football-supporter hero pose holding a large national flag diagonally across the lower foreground with both hands, flag sweeping from one lower corner toward the opposite side while face, upper torso, and jersey design remain fully visible, proud energized smile",
        "tags": ["supporter_poster", "football_culture", "flag_front"],
    },
    {
        "name": "large_flag_side_wave",
        "body_silhouette": "front-facing football-supporter celebration pose using both hands to control a clean flagpole at one side while a large national flag billows outward beside the body in a strong side arc, torso engaged, joyful open smile and excited eyes",
        "tags": ["supporter_poster", "football_culture", "flag_side"],
    },
    {
        "name": "large_flag_front_open",
        "body_silhouette": "front-facing football-supporter poster pose holding the two upper corners of a large national flag opened across the lower front of the body at waist height, keeping the jersey upper body, hands, face, and hair identity clearly visible, confident bright smile",
        "tags": ["supporter_poster", "football_culture", "flag_front"],
    },
    {
        "name": "small_flag_wave",
        "body_silhouette": "front-facing football-supporter celebration pose, one hand holding a small national flag on a short clean pole and waving it diagonally above shoulder height, other arm bent in an energetic cheer, open joyful smile",
        "tags": ["supporter_poster", "football_culture", "flag_wave"],
    },
    {
        "name": "double_low_fist_goal_celebration",
        "body_silhouette": "front-facing football-supporter goal celebration, both fists held low beside the waist with elbows bent and torso leaning slightly forward, delighted open smile and sparkling excited eyes",
        "tags": ["supporter_poster", "football_culture", "goal_celebration"],
    },
    {
        "name": "tense_clasped_supporter",
        "body_silhouette": "front-facing football-supporter tense-match pose, both hands clasped firmly together near the upper chest, shoulders slightly raised, eyes wide and intensely hopeful, lips slightly parted",
        "tags": ["supporter_poster", "football_culture", "tense_match"],
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
    return dict(random.choice(TEAM_PROFILE_POOL))


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
    return dict(random.choice(FOOTBALL_ACTIONS))


def choose_world_cup_shot_scale(recent_tags=None, art_plan=None):
    return dict(random.choice(WORLD_CUP_SHOT_SCALES))


def choose_world_cup_composition_plan(recent_tags=None, art_plan=None, action_style=None, outfit_direction=None):
    return dict(random.choice(FOOTBALL_COMPOSITIONS))
