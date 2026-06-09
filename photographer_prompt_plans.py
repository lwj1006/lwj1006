import random


_ACTIVE_SCENE_PLAN_NAME = None


PHOTOGRAPHER_SCENE_PLANS = [
    {
        "name": "pure_white_studio",
        "label": "纯白背景 / 人物服装优先",
        "graphic_concept": "pure white studio background with the character and outfit as the complete visual focus",
        "spatial_structure": "clean white seamless wall and floor with only a subtle contact shadow; no furniture, props, panels, or decorative scenery",
        "visual_device": "white negative space supports a clear face and outfit silhouette without pushing the character to the edge",
        "body_silhouette": "front or front three-quarter standing, gentle walking, or upright seated pose; simple readable hands and balanced posture",
        "outfit_direction": "wearable fashion with a strong clear silhouette, such as knitwear, blouse, jacket, dress, skirt, or trousers",
        "material_language": "opaque clothing fabric, clean white seamless backdrop, subtle floor contact shadow",
        "color_strategy": "background is pure white, but outfit must use a clearly non-white colored, mid-tone, dark, earthy, or muted-chromatic main value",
        "lighting_behavior": "soft high-key studio light with clear facial planes and controlled clothing detail, never washing out the outfit",
        "tags": ["photographer_scene", "studio", "pure_white", "simple_background", "character_focus"],
        "weight": 1.0,
    },
    {
        "name": "clean_studio_character_focus",
        "label": "干净棚拍 / 人物优先",
        "graphic_concept": "clean studio editorial portrait where the character, face, and outfit are the first visual focus",
        "spatial_structure": "simple studio wall and floor with one restrained panel or shadow shape; character occupies a clear central or near-third position",
        "visual_device": "one calm background color field and a soft floor contact shadow support the silhouette without competing for attention",
        "body_silhouette": "front or front three-quarter standing pose, relaxed weight shift, or one small step; face and outfit remain fully readable",
        "outfit_direction": "fashion-editorial daily outfit with a strong wearable silhouette, such as knitwear, blouse, short jacket, skirt, or trousers",
        "material_language": "matte backdrop, opaque fabric texture, subtle floor shadow, clean hair shine",
        "color_strategy": "background stays restrained; outfit uses a cohesive colored, mid-tone, dark, earthy, or muted-chromatic main value",
        "lighting_behavior": "large soft studio light with clean facial planes, gentle shadow, and no chest-emphasizing highlight",
        "tags": ["photographer_scene", "studio", "editorial", "character_focus"],
        "weight": 1.4,
    },
    {
        "name": "soft_editorial_wall",
        "label": "杂志墙面 / 柔和棚拍",
        "graphic_concept": "simple magazine-style wall portrait with controlled color, clean lines, and a clear fashion read",
        "spatial_structure": "plain wall, shallow floor area, and one subtle architectural line create a calm frame around the character",
        "visual_device": "soft wall shadow or a single muted color block adds structure while leaving face and outfit dominant",
        "body_silhouette": "front three-quarter pose, gentle side angle, upright seated pose, or a natural standing pause",
        "outfit_direction": "polished wearable fashion with knit, blouse, jacket, dress, skirt, or trousers",
        "material_language": "matte wall, soft woven or knit fabric, restrained accessory shine",
        "color_strategy": "use calm tonal contrast; avoid all-white clothing and avoid loud background colors",
        "lighting_behavior": "soft side-front light keeps eyes, face, shoulders, and outfit silhouette clear without dramatic distortion",
        "tags": ["photographer_scene", "studio", "editorial", "simple_background", "character_focus"],
        "weight": 1.2,
    },
    {
        "name": "bright_room_character_focus",
        "label": "明亮房间 / 小说CG",
        "graphic_concept": "bright lived-in room or novel-CG interior where the character remains the unmistakable first read",
        "spatial_structure": "window, wall, floor, and one or two simple furniture shapes establish the room without surrounding or hiding the character",
        "visual_device": "window light and a few orderly room lines guide attention toward the face and outfit",
        "body_silhouette": "front or front three-quarter standing, walking, or upright seated posture; no back-facing head-turn",
        "outfit_direction": "soft daily outfit with cardigan, blouse, knit top, skirt, dress, or relaxed trousers",
        "material_language": "wood floor, matte wall, opaque fabric, soft curtain kept in the background, restrained domestic detail",
        "color_strategy": "room may be bright, but clothing should retain a distinct non-white main value",
        "lighting_behavior": "soft window side-front light keeps face and upper body evenly readable",
        "tags": ["photographer_scene", "interior", "bright_room", "character_focus"],
        "weight": 1.5,
    },
    {
        "name": "balanced_gallery_lobby",
        "label": "展馆大厅 / 室内空间",
        "graphic_concept": "museum, gallery, library lobby, or quiet public interior photographed as a clean character-focused scene",
        "spatial_structure": "simple wall panels, floor lines, and distant room depth create context while the character remains large and clear",
        "visual_device": "one or two architectural lines lead gently toward the character; no foreground obstruction or reflective fragments",
        "body_silhouette": "front three-quarter standing or walking pause, shoulders relaxed, gaze toward camera or slightly aside",
        "outfit_direction": "polished indoor outfit with blouse, jacket, knit, dress, skirt, or trousers",
        "material_language": "stone or wood floor, matte wall panel, opaque fabric, soft overhead light",
        "color_strategy": "neutral architecture supports a clearly separated outfit main value",
        "lighting_behavior": "balanced room light with clean eye highlights and mild depth separation",
        "tags": ["photographer_scene", "indoor", "gallery", "lobby", "character_focus"],
        "weight": 1.1,
    },
    {
        "name": "clean_corridor_medium_depth",
        "label": "干净走廊 / 中等景深",
        "graphic_concept": "clean corridor or aisle scene with moderate perspective and a clearly readable character",
        "spatial_structure": "floor and wall lines create gentle depth, but the character occupies the foreground-midground and never becomes tiny",
        "visual_device": "repeating lights or wall lines quietly support the pose without dominating the image",
        "body_silhouette": "front three-quarter walk, natural pause, or slight side angle with torso and face remaining clearly readable",
        "outfit_direction": "wearable indoor fashion with blouse, jacket, knit, dress, skirt, or trousers",
        "material_language": "matte wall, floor line, soft overhead light, opaque clothing fabric",
        "color_strategy": "architecture stays controlled; outfit remains the strongest color and value cue",
        "lighting_behavior": "soft repeated room light keeps face and outfit brighter than the distant background",
        "tags": ["photographer_scene", "corridor", "indoor", "moderate_depth", "character_focus"],
        "weight": 0.9,
    },
    {
        "name": "bright_shopfront_daily",
        "label": "明亮店铺 / 街区日常",
        "graphic_concept": "bright cafe, bookstore, bakery, mall, or shopfront daily scene with the character as the clear subject",
        "spatial_structure": "shop entrance, window, awning, or pavement line creates simple context around a medium-size character",
        "visual_device": "one storefront line and soft daylight establish place; signs remain abstract and background detail stays restrained",
        "body_silhouette": "front three-quarter standing, walking, or small daily pause; face and outfit are the first visual focus",
        "outfit_direction": "modern daily outfit with jacket, knit, blouse, skirt, shorts, dress, or trousers",
        "material_language": "shop window kept behind the character, pavement, cloth awning, opaque fabric, clean daylight",
        "color_strategy": "shop colors stay secondary; outfit remains cohesive and clearly separated",
        "lighting_behavior": "bright outdoor side-front light with gentle shadow and readable eyes",
        "tags": ["photographer_scene", "bright_daily", "shop", "street", "character_focus"],
        "weight": 1.4,
    },
    {
        "name": "riverside_rooftop_daily",
        "label": "河畔天台 / 明亮户外",
        "graphic_concept": "bright riverside, rooftop, balcony, park, or open terrace daily scene with balanced environment and character focus",
        "spatial_structure": "railing, path, terrace wall, or distant buildings provide simple depth while the character stays medium-large",
        "visual_device": "sky, path, or railing line supports a clear front three-quarter silhouette without excessive empty space",
        "body_silhouette": "front three-quarter standing, gentle walking, or relaxed side angle into the breeze; no body-facing-away turn-back pose",
        "outfit_direction": "outdoor daily outfit with knit, hoodie, blouse, light jacket, skirt, shorts, dress, or trousers",
        "material_language": "railing, path, sky, opaque fabric, lightly wind-touched hair",
        "color_strategy": "sky and architecture remain secondary; clothing carries a distinct non-white main value",
        "lighting_behavior": "bright overcast or late-afternoon side-front light with clean face readability",
        "tags": ["photographer_scene", "bright_daily", "outdoor", "balanced_environment", "character_focus"],
        "weight": 1.0,
    },
    {
        "name": "warm_cafe_window_daily",
        "label": "咖啡店窗边 / 暖光日常",
        "graphic_concept": "warm cafe window-side portrait with quiet daily atmosphere and the character as the clear first read",
        "spatial_structure": "window, simple wall, seat, and one clean tabletop line establish the cafe while staying behind or beside the character",
        "visual_device": "soft window light and restrained warm interior tones support the face and outfit without handheld food or drink props",
        "body_silhouette": "front three-quarter standing, upright seated pause, or gentle walking step near the window",
        "outfit_direction": "wearable cafe-date outfit with knit, blouse, cardigan, jacket, dress, skirt, or trousers",
        "material_language": "wood, matte wall, opaque fabric, soft window light, restrained interior detail",
        "color_strategy": "warm interior colors remain secondary; outfit keeps a distinct cohesive main value",
        "lighting_behavior": "warm side-front window light with clean eyes, readable face, and gentle fabric texture",
        "tags": ["photographer_scene", "cafe", "window", "warm_light", "character_focus"],
        "weight": 1.1,
    },
    {
        "name": "library_reading_area",
        "label": "图书馆阅览区 / 安静室内",
        "graphic_concept": "quiet library reading area photographed as a polished character-focused indoor scene",
        "spatial_structure": "orderly bookcases remain in the background, with a simple reading table or wall line giving moderate depth",
        "visual_device": "soft shelf rhythm and one pool of reading light guide attention toward the face and outfit",
        "body_silhouette": "front three-quarter standing, walking pause, or upright seated posture with simple object-empty hands",
        "outfit_direction": "polished indoor daily outfit with knit, blouse, cardigan, jacket, skirt, dress, or trousers",
        "material_language": "wood shelf, paper texture kept distant, matte table, opaque fabric, soft reading light",
        "color_strategy": "shelf and wood tones stay subdued; outfit remains the strongest color cue",
        "lighting_behavior": "balanced window and reading light keeps the character brighter than the background shelves",
        "tags": ["photographer_scene", "library", "indoor", "quiet_daily", "character_focus"],
        "weight": 1.0,
    },
    {
        "name": "modern_lounge_character_focus",
        "label": "现代休息区 / 简洁室内",
        "graphic_concept": "modern lounge, hotel sitting area, or office rest space with clean commercial photography balance",
        "spatial_structure": "one sofa or bench, a simple wall, and restrained floor lines establish the location without surrounding the character",
        "visual_device": "clean upholstery shape and soft architectural lighting support a clear fashion silhouette",
        "body_silhouette": "front three-quarter standing, upright seated pause, or gentle diagonal walk with relaxed posture",
        "outfit_direction": "clean modern fashion with blouse, knit, short jacket, dress, skirt, or trousers",
        "material_language": "matte upholstery, wall panel, opaque fabric, restrained metal accent, soft floor shadow",
        "color_strategy": "interior palette stays calm and secondary; outfit receives the clearest value separation",
        "lighting_behavior": "soft commercial interior light with clean facial planes and mild background falloff",
        "tags": ["photographer_scene", "lounge", "modern_interior", "editorial", "character_focus"],
        "weight": 0.9,
    },
    {
        "name": "tree_lined_park_path",
        "label": "林荫公园 / 自然日常",
        "graphic_concept": "tree-lined park path portrait with clean natural light and a simple daily-photography feeling",
        "spatial_structure": "path, grass edge, and softly separated trees create moderate depth while the character remains medium-large",
        "visual_device": "soft leaf color and a clear path line support the silhouette without dense flowers or foreground branches",
        "body_silhouette": "front three-quarter standing, gentle diagonal walk, or relaxed side-angle pause",
        "outfit_direction": "outdoor daily outfit with knit, blouse, light jacket, dress, skirt, shorts, or trousers",
        "material_language": "path surface, soft greenery, opaque fabric, lightly wind-touched hair",
        "color_strategy": "greenery stays muted and secondary; outfit remains clearly separated and cohesive",
        "lighting_behavior": "bright open shade or soft afternoon side-front light with clear face readability",
        "tags": ["photographer_scene", "park", "nature", "bright_daily", "character_focus"],
        "weight": 1.0,
    },
    {
        "name": "sunset_city_wall_street",
        "label": "城市墙面 / 黄昏街拍",
        "graphic_concept": "simple city wall or quiet street-edge portrait during warm late-afternoon light",
        "spatial_structure": "one textured wall, pavement line, and distant soft city hint create a restrained street-photography setting",
        "visual_device": "warm wall light and a clean diagonal shadow add atmosphere while face and outfit remain dominant",
        "body_silhouette": "front three-quarter standing, natural pause, or shallow diagonal walking step",
        "outfit_direction": "modern street-date outfit with knit, blouse, jacket, dress, skirt, shorts, or trousers",
        "material_language": "matte wall, pavement, opaque fabric, subtle city texture, warm light",
        "color_strategy": "warm wall and sunset tones remain controlled; outfit keeps clear tonal separation",
        "lighting_behavior": "late-afternoon side-front light with a soft long shadow and readable facial detail",
        "tags": ["photographer_scene", "city_wall", "street", "sunset", "character_focus"],
        "weight": 1.0,
    },
    {
        "name": "colored_paper_commercial_studio",
        "label": "彩纸棚拍 / 商业摄影",
        "graphic_concept": "commercial studio portrait using one or two restrained colored paper backdrops around a clear character and outfit",
        "spatial_structure": "simple paper sweep and floor with one broad color transition; no decorative objects or complex installation",
        "visual_device": "controlled color contrast and a soft shadow create a polished advertising-photo rhythm",
        "body_silhouette": "front or front three-quarter standing pose, relaxed weight shift, upright seated pause, or one small walking step",
        "outfit_direction": "commercial fashion outfit with knit, blouse, short jacket, dress, skirt, or trousers",
        "material_language": "matte colored paper, opaque fabric, subtle floor shadow, clean hair shine",
        "color_strategy": "use one restrained background color family selected to contrast with the outfit; avoid rainbow or neon mixing",
        "lighting_behavior": "large soft studio light keeps face, outfit construction, and fabric texture clearly readable",
        "tags": ["photographer_scene", "studio", "commercial", "colored_backdrop", "character_focus"],
        "weight": 1.1,
    },
]


PHOTOGRAPHER_ACTION_STYLES = [
    {
        "name": "front_three_quarter_natural_pause",
        "body_silhouette": "front three-quarter natural pause, torso and face generally toward the camera, relaxed shoulders, balanced posture, simple readable hands",
        "tags": ["front_three_quarter", "stable_pose", "character_focus"],
        "weight": 3.6,
    },
    {
        "name": "simple_front_standing",
        "body_silhouette": "simple upright standing posture viewed from the front or a slight three-quarter angle, with a small natural weight shift",
        "tags": ["front_view", "stable_pose", "character_focus"],
        "weight": 2.8,
    },
    {
        "name": "gentle_diagonal_walk",
        "body_silhouette": "gentle walking step across a shallow diagonal while torso stays mostly front three-quarter; face and outfit remain clearly readable",
        "tags": ["walking", "front_three_quarter", "character_focus"],
        "weight": 2.0,
    },
    {
        "name": "soft_side_angle_pause",
        "body_silhouette": "clean side or three-quarter side pause with both shoulders and facial profile readable; body does not face away from the camera",
        "tags": ["side_angle", "stable_pose", "character_focus"],
        "weight": 1.2,
    },
    {
        "name": "hair_or_sleeve_micro_action",
        "body_silhouette": "small natural action such as adjusting hair, sleeve, collar edge, bag strap, or outer layer; fingers stay simple and away from clothing openings",
        "tags": ["micro_action", "simple_hand", "front_three_quarter"],
        "weight": 1.1,
    },
    {
        "name": "upright_seated_pause",
        "body_silhouette": "upright seated posture with torso facing front three-quarter, shoulders relaxed, hands resting simply near lap or seat",
        "tags": ["seated", "stable_hands", "character_focus"],
        "weight": 0.7,
    },
]


PHOTOGRAPHER_COMPOSITION_PLANS = [
    {
        "name": "stable_medium_character_focus",
        "composition": "stable medium character-focused frame; face and outfit are the first visual focus and the character occupies about 45-65 percent of the image",
        "camera": "natural eye-level, medium shot to knee-up, front or front three-quarter viewpoint, normal perspective",
        "pose": "selected action stays simple, balanced, and readable without turning the body away",
        "foreground": "minimal foreground; keep all scene elements behind or beside the character",
        "lighting": "clean side-front or soft frontal light keeps face and clothing readable",
        "guardrail": "background remains subordinate; use comfortable eye-level distance, balanced body orientation, and controlled empty space",
        "tags": ["photographer_composition", "medium_shot", "character_focus"],
        "weight": 3.8,
    },
    {
        "name": "clean_knee_up_editorial",
        "composition": "clean knee-up editorial frame with a front three-quarter character and enough simple environment to establish place",
        "camera": "eye-level knee-up framing with normal lens feeling and no body-part exaggeration",
        "pose": "selected action remains calm and naturally balanced",
        "foreground": "none or one very small soft edge that never overlaps the body",
        "lighting": "soft directional light separates character from a restrained background",
        "guardrail": "character and outfit must dominate; avoid mirror, glass fragments, doorway cuts, or large props",
        "tags": ["photographer_composition", "knee_up", "editorial", "character_focus"],
        "weight": 2.8,
    },
    {
        "name": "balanced_environment_medium",
        "composition": "balanced medium-wide frame where the environment explains the location but the character remains the first read",
        "camera": "eye-level or gentle slight-high viewpoint, medium to medium-wide, normal perspective",
        "pose": "front three-quarter standing or walking action remains clearly readable",
        "foreground": "minimal and unobtrusive; no object should cover the face, torso, or outfit silhouette",
        "lighting": "environment light leads gently toward the face and outfit",
        "guardrail": "character occupies at least 45 percent of image height; avoid tiny subject, clutter, or scenery dominance",
        "tags": ["photographer_composition", "medium_wide", "balanced_environment", "character_focus"],
        "weight": 1.7,
    },
    {
        "name": "clean_full_body_walk",
        "composition": "clean full-body or near full-body fashion frame with a simple walking or standing silhouette",
        "camera": "natural eye-level full-body framing with normal perspective and stable horizon",
        "pose": "selected action keeps feet, hands, face, and outfit silhouette readable",
        "foreground": "none; use simple background lines only",
        "lighting": "even readable light with clear separation from the ground and background",
        "guardrail": "use eye-level fashion framing with balanced proportions, readable feet, and a restrained background",
        "tags": ["photographer_composition", "full_body", "character_focus"],
        "weight": 0.8,
    },
]


PHOTOGRAPHER_SHOT_SCALES = [
    {
        "name": "knee_up_character_focus",
        "description": "knee-up or thigh-up framing; character occupies about 50-65 percent of the image and face plus outfit are the first read",
        "weight": 3.4,
    },
    {
        "name": "medium_character_focus",
        "description": "medium shot with character occupying about 45-60 percent of the image; face, hands, and outfit silhouette remain clear",
        "weight": 2.8,
    },
    {
        "name": "waist_up_clear_portrait",
        "description": "waist-up framing with comfortable headroom and clear outfit context; avoid chest-dominant crop or close pressure",
        "weight": 0.9,
    },
    {
        "name": "full_body_clean_context",
        "description": "full-body or near full-body framing with simple context; character remains large enough to be the first visual focus",
        "weight": 0.7,
    },
]


def _weighted_choice(items):
    total = sum(max(float(item.get("weight", 1.0)), 0.01) for item in items)
    pick = random.random() * total
    cursor = 0.0
    for item in items:
        cursor += max(float(item.get("weight", 1.0)), 0.01)
        if pick <= cursor:
            return dict(item)
    return dict(items[-1])


def set_active_photographer_scene_plan(plan_name=None):
    global _ACTIVE_SCENE_PLAN_NAME
    if plan_name in {"", "all", "random", "full_random"}:
        plan_name = None
    valid_names = {plan["name"] for plan in PHOTOGRAPHER_SCENE_PLANS}
    if plan_name is not None and plan_name not in valid_names:
        raise ValueError(f"unknown photographer scene plan: {plan_name}")
    _ACTIVE_SCENE_PLAN_NAME = plan_name


def active_photographer_scene_plan():
    return _ACTIVE_SCENE_PLAN_NAME


def photographer_scene_plan_label(plan_name=None):
    plan_name = _ACTIVE_SCENE_PLAN_NAME if plan_name is None else plan_name
    for plan in PHOTOGRAPHER_SCENE_PLANS:
        if plan["name"] == plan_name:
            return plan.get("label", plan_name)
    return "全随机摄影师背景"


def photographer_scene_plans_for_selection(plan_name=None):
    plan_name = _ACTIVE_SCENE_PLAN_NAME if plan_name is None else plan_name
    if plan_name is None:
        return [dict(plan) for plan in PHOTOGRAPHER_SCENE_PLANS]
    plans = [
        dict(plan)
        for plan in PHOTOGRAPHER_SCENE_PLANS
        if plan["name"] == plan_name
    ]
    return plans or [dict(plan) for plan in PHOTOGRAPHER_SCENE_PLANS]


def choose_photographer_scene_plan(character_name=None, recent_tags=None):
    return _weighted_choice(photographer_scene_plans_for_selection())


def choose_photographer_action_style(character_name=None, recent_tags=None, plan=None):
    return _weighted_choice(PHOTOGRAPHER_ACTION_STYLES)


def choose_photographer_composition_plan(recent_tags=None, plan=None, action=None, outfit_direction=None):
    return _weighted_choice(PHOTOGRAPHER_COMPOSITION_PLANS)


def choose_photographer_shot_scale(recent_tags=None, plan=None):
    return _weighted_choice(PHOTOGRAPHER_SHOT_SCALES)
