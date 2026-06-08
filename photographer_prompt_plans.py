import random


PHOTOGRAPHER_SCENE_PLANS = [
    {
        "name": "doorframe_observer_room",
        "graphic_concept": "private interior seen from a half-open doorway; the room geometry and doorframe decide the image before the character pose",
        "spatial_structure": "camera stays outside or just inside the doorway, with wall edge, doorframe, floor line, and window light forming deep layered space",
        "visual_device": "door edge cuts one side of the frame, a strip of foreground shadow, scattered room details, and a bright window plane guide the eye inward",
        "body_silhouette": "character is caught turning, pausing, or looking back from inside the room; not centered, body partly screened by the doorframe when useful",
        "outfit_direction": "soft daily outfit with cardigan, blouse or knit top, skirt or relaxed trousers, wearable indoor styling",
        "material_language": "painted doorframe, matte wall, soft fabric, floor reflection, window curtain, small domestic details",
        "color_strategy": "room can be pale or warm, but clothing should use a clear non-white main value with calm tonal separation",
        "lighting_behavior": "window side light creates a readable face plane, rim on hair, and softer foreground shadow",
        "tags": ["photographer_scene", "interior", "doorframe", "foreground_occlusion", "deep_space"],
    },
    {
        "name": "low_table_foreground_depth",
        "graphic_concept": "low table-height slice of a room, cafe corner, studio floor, or shop counter; foreground mass makes the image feel photographed from a real position",
        "spatial_structure": "camera is close to table, counter, stair, chair, or floor edge, looking past a blurred foreground plane toward a midground character",
        "visual_device": "large soft foreground edge, diagonal table or floor line, midground figure, and bright background plane form a strong depth stack",
        "body_silhouette": "character pauses, leans lightly, walks through the midground, or turns across the light; hands stay simple and object-empty",
        "outfit_direction": "clean casual fashion with textured top, skirt or pants, small accessory detail, everyday editorial styling",
        "material_language": "wood, metal, tile, cloth texture, blurred foreground edge, window highlight, clean fabric grain",
        "color_strategy": "foreground may be dark or warm; outfit should sit clearly between foreground shadow and background light",
        "lighting_behavior": "directional side or back light separates foreground, subject, and background without hiding eyes",
        "tags": ["photographer_scene", "low_camera", "foreground_depth", "daily", "interior"],
    },
    {
        "name": "overhead_room_geometry",
        "graphic_concept": "high-angle anime CG where floor plan, furniture edges, window shadows, and body placement make the composition",
        "spatial_structure": "camera looks down from stair height, balcony height, mezzanine, or upper corner; floor geometry and object spacing create a readable map",
        "visual_device": "diagonal shadows, furniture rectangles, rug or tile rhythm, and one offset character create a designed overhead frame",
        "body_silhouette": "character looks up, pauses mid-step, sits near a light patch, or turns within the floor pattern; face and hair identity remain readable",
        "outfit_direction": "wearable fashion with a clear silhouette from above, such as knit top with skirt, shirt dress, or layered casual outfit",
        "material_language": "floor tiles, rug edge, tabletop, fabric folds, window shadow, soft hair highlights",
        "color_strategy": "large floor shapes can be neutral; outfit needs a distinct mid-tone, dark, earthy, or muted-chromatic main value",
        "lighting_behavior": "top-side window light casts clean geometric shadows while keeping face and hair readable",
        "tags": ["photographer_scene", "high_camera", "deep_perspective", "interior", "negative_space"],
    },
    {
        "name": "telephoto_through_shelves",
        "graphic_concept": "telephoto view through shelves, plants, curtains, display panels, or corridor edges; the character feels found inside a layered space",
        "spatial_structure": "compressed foreground, midground character, and background rows overlap tightly, like a long-lens shot through the environment",
        "visual_device": "soft vertical foreground strips, repeated shelf or window lines, small reflected highlights, and an offset readable face",
        "body_silhouette": "character browses, pauses, turns slightly, or looks past the camera; body may be partially cut by foreground layers",
        "outfit_direction": "stylish indoor daily outfit, blouse or light jacket with skirt or trousers, bookstore or gallery compatible",
        "material_language": "shelf rows, glass glints, paper, plants, fabric texture, compressed background lights",
        "color_strategy": "background can be busy; outfit should have a cohesive main value that separates from shelf and wall tones",
        "lighting_behavior": "soft compressed light bands and eye catchlights separate the face from layered foreground",
        "tags": ["photographer_scene", "telephoto", "layered_space", "foreground_occlusion", "indoor"],
    },
    {
        "name": "window_backlight_half_screen",
        "graphic_concept": "window-backlit half-screen composition; curtain, window frame, and light sheet act as the primary graphic structure",
        "spatial_structure": "character stands, sits, or turns near a window, with curtain or frame slicing one third of the image and the room falling into soft shade",
        "visual_device": "bright window rectangle, translucent curtain edge, hair rim light, floor reflection, and quiet negative space",
        "body_silhouette": "character is partly hidden by curtain or window edge, caught before or after moving through the light; face remains readable",
        "outfit_direction": "soft knit, blouse, or relaxed dress with opaque fabric and clean daily silhouette",
        "material_language": "curtain fabric, glass, wood floor, soft knit or woven clothing, rim-lit hair",
        "color_strategy": "bright window may be white, but outfit must not become white by default; use a colored or grounded main value",
        "lighting_behavior": "backlight creates hair rim and atmosphere while a gentle fill keeps eyes and facial planes visible",
        "tags": ["photographer_scene", "window_frame", "backlight", "foreground_occlusion", "interior"],
    },
    {
        "name": "street_corner_motion_frame",
        "graphic_concept": "bright daily street or shop-corner frame; architecture, signs without readable text, awning edge, and pedestrian-space perspective carry the shot",
        "spatial_structure": "camera is across a street corner, shop entrance, mall walkway, or riverside path, using diagonal pavement or storefront lines to place the character off-center",
        "visual_device": "awning shadow, window reflection, pavement line, soft passerby-like abstract shapes without extra people, and a clear character silhouette",
        "body_silhouette": "character walks, turns, adjusts hair, or pauses mid-step as if photographed between actions; avoid posed front-facing stillness",
        "outfit_direction": "modern daily outfit with jacket, knit, blouse, skirt, shorts, or trousers, suited for a shop or street walk",
        "material_language": "glass window, pavement, cloth awning, bag strap, soft outdoor fabric, clean daylight reflections",
        "color_strategy": "street colors can vary; outfit should be cohesive and visible against shop glass and pavement",
        "lighting_behavior": "bright outdoor fill with side shadow from awning or building edge, crisp but not harsh",
        "tags": ["photographer_scene", "bright_daily", "street", "shop", "walking", "diagonal_space"],
    },
    {
        "name": "studio_negative_space_crop",
        "graphic_concept": "studio editorial frame where negative space, crop, and body placement do more work than props",
        "spatial_structure": "minimal studio wall, floor contact shadow, one panel or paper sweep, and generous empty area around an off-center character",
        "visual_device": "deliberate crop, large quiet margin, one strong color or shadow block, and a readable outfit silhouette",
        "body_silhouette": "character stands, leans, takes a small step, sits on a low block, or turns through the frame; never a flat ID-photo pose",
        "outfit_direction": "fashion-editorial daily outfit with strong silhouette, such as knitwear, structured blouse, short jacket, skirt, or trousers",
        "material_language": "matte backdrop, paper sweep, fabric texture, subtle floor shadow, clean hair shine",
        "color_strategy": "background can be high-key or graphic, but outfit should use a distinct main color or value separation",
        "lighting_behavior": "large softbox feel with controlled shadow edge and clean face readability",
        "tags": ["photographer_scene", "studio", "editorial", "negative_space", "fashion"],
    },
    {
        "name": "corridor_vanishing_point",
        "graphic_concept": "corridor, museum, library aisle, hotel lobby, or mall passage with strong vanishing-point perspective",
        "spatial_structure": "long floor lines, ceiling lights, wall panels, shelves, or railing guide the eye toward an off-center character",
        "visual_device": "repeating architectural lines, light pools, distant depth, and one foreground edge create a composed perspective shot",
        "body_silhouette": "character walks across the perspective, pauses near a wall, turns at an aisle end, or looks back briefly",
        "outfit_direction": "polished indoor outfit with blouse, jacket, knit, dress, skirt, or trousers, suitable for gallery or lobby space",
        "material_language": "stone floor, wood shelf, wall panel, glass reflection, soft fabric, overhead light rhythm",
        "color_strategy": "architecture may be neutral; outfit needs a readable colored, dark, earthy, or muted-chromatic main value",
        "lighting_behavior": "overhead or window light repeats into depth while face remains readable near the camera side",
        "tags": ["photographer_scene", "corridor", "vanishing_point", "indoor", "deep_space"],
    },
    {
        "name": "mirror_fragment_single_subject_photo",
        "graphic_concept": "mirror or glass-fragment editorial shot; reflections are graphic fragments around one real character, never a second subject",
        "spatial_structure": "angled mirror, shop glass, acrylic panel, or glossy wall creates partial reflections and cropped shapes across foreground and background",
        "visual_device": "fragmented hair color echoes, eye glints, panel edges, and one real readable face create the design",
        "body_silhouette": "character turns near the reflective surface, seated or standing; real body remains the only complete body",
        "outfit_direction": "clean modern outfit with crisp silhouette, blouse or knit plus skirt or trousers, editorial but wearable",
        "material_language": "mirror glass, acrylic edge, polished floor, crisp cloth, reflected highlights",
        "color_strategy": "reflections may echo identity accents; outfit main value remains model-chosen and not locked to white",
        "lighting_behavior": "controlled side light creates thin glass highlights without overexposed face or duplicate silhouettes",
        "tags": ["photographer_scene", "mirror", "reflection", "glass", "editorial", "single_character_only"],
    },
    {
        "name": "rooftop_wide_environment_cut",
        "graphic_concept": "wide rooftop, balcony, riverside, or open terrace shot where environment lines and sky space frame a readable character",
        "spatial_structure": "railing, roof floor, laundry line, river edge, distant buildings, or terrace wall place the character near a third with a lot of air",
        "visual_device": "large sky or wall negative space, diagonal railing, wind-blown fabric or hair, and one foreground edge",
        "body_silhouette": "character walks, leans on railing, turns into wind, or pauses at the edge; body remains readable but not centered",
        "outfit_direction": "outdoor daily outfit with knit, hoodie, blouse, light jacket, skirt, shorts, or trousers, wind-compatible silhouette",
        "material_language": "concrete, railing metal, cloth, wind-touched hair, distant building shapes, sky gradient",
        "color_strategy": "sky and architecture can be bright; clothing should carry a distinct non-white main value for separation",
        "lighting_behavior": "late afternoon or bright overcast side light with rim on hair and enough fill for face",
        "tags": ["photographer_scene", "wide_shot", "outdoor", "large_space", "wind"],
    },
]


PHOTOGRAPHER_ACTION_STYLES = [
    {
        "name": "caught_turning_before_pose",
        "body_silhouette": "caught just before a pose forms: torso turning, weight shifting, one shoulder leading, gaze halfway toward or away from the camera",
        "tags": ["candid", "turning", "story_pose"],
    },
    {
        "name": "walking_across_frame",
        "body_silhouette": "walking across the frame rather than toward the viewer; one foot or knee leads naturally, arms swing simply, face remains readable",
        "tags": ["walking", "side_motion", "candid"],
    },
    {
        "name": "half_screened_observation",
        "body_silhouette": "partly screened by doorframe, curtain, plant, shelf, glass edge, or foreground shadow, with face and identity tokens still visible",
        "tags": ["foreground_occlusion", "observed", "story_pose"],
    },
    {
        "name": "looking_back_at_edge",
        "body_silhouette": "near one edge of the image, body angled away while head turns back enough to keep the face readable; use as a rare cinematic beat",
        "tags": ["edge_framing", "looking_back", "candid"],
    },
    {
        "name": "paused_inside_light",
        "body_silhouette": "paused inside a window beam, doorway light, shop light, or corridor light pool; posture relaxed, hands object-empty and readable",
        "tags": ["light_cut", "stable_hands", "story_pose"],
    },
    {
        "name": "seated_diagonal_weight",
        "body_silhouette": "seated or leaning with diagonal body line, one hand supporting on seat, floor, railing, or table edge; avoid chest-forward posing",
        "tags": ["seated", "diagonal_body", "stable_hands"],
    },
    {
        "name": "hair_or_sleeve_micro_action",
        "body_silhouette": "small natural action such as adjusting hair, sleeve, collar edge, bag strap, or outer layer; fingers stay simple and away from clothing openings",
        "tags": ["micro_action", "hair_touch", "simple_hand"],
    },
    {
        "name": "environment_attention",
        "body_silhouette": "attention belongs to the scene: looking at window light, shelf, corridor depth, floor pattern, or sky rather than posing directly",
        "tags": ["eyes_away", "observed", "story_pose"],
    },
]


PHOTOGRAPHER_COMPOSITION_PLANS = [
    {
        "name": "doorframe_cut_observer",
        "composition": "camera frames through a doorway or wall edge; character is offset and partly cut by architecture, creating a found-moment image",
        "camera": "medium to medium-wide, photographer stands outside the main space, slight diagonal angle into the room",
        "pose": "selected action must feel interrupted by the camera, not arranged for a portrait",
        "foreground": "doorframe, wall edge, curtain, shelf, or shadow occupies 15-35 percent of one side without hiding the face",
        "lighting": "foreground is darker or softer, face receives clean side light",
        "guardrail": "do not center the character or remove the foreground cut; keep only one character",
        "tags": ["photographer_composition", "doorframe", "foreground_occlusion"],
    },
    {
        "name": "low_foreground_pressure",
        "composition": "low camera with a large foreground plane creates depth pressure; the character sits or moves in the readable midground",
        "camera": "table-height, counter-height, stair-height, or floor-edge height; slight upward or level view without body distortion",
        "pose": "selected action remains natural and readable from the low viewpoint",
        "foreground": "large blurred table, railing, floor, plant, chair, or counter edge anchors the bottom or side of the image",
        "lighting": "rim or side light separates foreground, character, and background",
        "guardrail": "avoid legs-first distortion, extreme nostril angle, or hands becoming the main subject",
        "tags": ["photographer_composition", "low_camera", "foreground_depth"],
    },
    {
        "name": "high_angle_floor_map",
        "composition": "high camera uses floor shapes and object spacing as the graphic design; character is one readable point inside the layout",
        "camera": "moderate overhead from stairs, balcony, mezzanine, or upper corner, not a flat top-down diagram",
        "pose": "selected action should align with floor lines, light patches, or furniture edges",
        "foreground": "upper railing, shelf edge, bed edge, curtain edge, or ceiling shadow may frame the top or side",
        "lighting": "window or ceiling light draws geometric paths to the face",
        "guardrail": "identity tokens must remain readable; avoid making character tiny or faceless",
        "tags": ["photographer_composition", "high_camera", "deep_perspective"],
    },
    {
        "name": "telephoto_layered_observation",
        "composition": "long-lens compressed layers place foreground strips, character, and background rows close together",
        "camera": "medium-long to long lens feeling, shot through shelves, plants, glass, doorway, or corridor edges",
        "pose": "selected action feels observed from across the space; gaze may stay away from the camera",
        "foreground": "soft vertical or diagonal strips cross the image edges without covering both eyes",
        "lighting": "small highlights and compressed light bands separate the layers",
        "guardrail": "do not add extra people or readable text; keep foreground scene-native",
        "tags": ["photographer_composition", "telephoto", "layered_space"],
    },
    {
        "name": "negative_space_edge_subject",
        "composition": "large negative space dominates one half or two thirds of the image while the character holds an edge or lower-third position",
        "camera": "medium-wide to wide editorial framing, stable horizon or wall/floor geometry",
        "pose": "selected action remains readable as a silhouette inside the open space",
        "foreground": "minimal foreground, one quiet edge or shadow shape if needed",
        "lighting": "clean tonal separation prevents the subject from dissolving into the empty area",
        "guardrail": "avoid centered ID-photo composition and avoid making the character too small",
        "tags": ["photographer_composition", "negative_space", "editorial"],
    },
    {
        "name": "reflection_fragment_crop",
        "composition": "mirror, glass, or acrylic fragments crop the character into graphic pieces while one real face remains the anchor",
        "camera": "medium-close to medium shot angled across reflective panels or shop glass",
        "pose": "selected action must belong to the real body; reflections only echo fragments",
        "foreground": "glass edge, acrylic panel, mirror slice, or glossy reflection crosses one side of the image",
        "lighting": "thin highlights on reflective edges, face not overexposed",
        "guardrail": "reflections must never become a second character or duplicate full body",
        "tags": ["photographer_composition", "reflection", "foreground_occlusion"],
    },
    {
        "name": "vanishing_point_walkthrough",
        "composition": "strong corridor or street perspective leads the eye through the image before reaching the character",
        "camera": "medium-wide, slightly off-axis to the vanishing lines, character placed near a third rather than center",
        "pose": "walking, turning, pausing, or looking back must align with the perspective direction",
        "foreground": "floor line, railing, shelf edge, window frame, or awning cuts into the nearest edge",
        "lighting": "repeating light pools or side light create readable depth",
        "guardrail": "avoid flat front-facing pose and avoid empty corridor with tiny subject",
        "tags": ["photographer_composition", "vanishing_point", "deep_space"],
    },
]


PHOTOGRAPHER_SHOT_SCALES = [
    {"name": "environment_first_medium_wide", "description": "medium-wide frame where environment lines read first, character remains clearly identifiable", "weight": 2.1},
    {"name": "edge_cropped_knee_up", "description": "knee-up or thigh-up frame with deliberate edge crop, face, hair, hands, and outfit silhouette readable", "weight": 1.9},
    {"name": "layered_half_body", "description": "half-body or waist-up frame seen through foreground layers, identity readable through the composition", "weight": 1.5},
    {"name": "full_body_in_space", "description": "full-body or near full-body figure placed inside strong room, corridor, street, or rooftop geometry", "weight": 1.1},
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


def choose_photographer_scene_plan(character_name=None, recent_tags=None):
    return _weighted_choice(PHOTOGRAPHER_SCENE_PLANS)


def choose_photographer_action_style(character_name=None, recent_tags=None, plan=None):
    return _weighted_choice(PHOTOGRAPHER_ACTION_STYLES)


def choose_photographer_composition_plan(recent_tags=None, plan=None, action=None, outfit_direction=None):
    plan_tags = set((plan or {}).get("tags", []))
    compatible = []
    for composition in PHOTOGRAPHER_COMPOSITION_PLANS:
        tags = set(composition.get("tags", []))
        if plan_tags & tags or not (plan_tags & {"doorframe", "low_camera", "high_camera", "telephoto", "reflection", "vanishing_point"}):
            compatible.append(composition)
    return _weighted_choice(compatible or PHOTOGRAPHER_COMPOSITION_PLANS)


def choose_photographer_shot_scale(recent_tags=None, plan=None):
    return _weighted_choice(PHOTOGRAPHER_SHOT_SCALES)

