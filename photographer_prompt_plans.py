import random


_ACTIVE_SCENE_PLAN_NAMES = None


PHOTOGRAPHER_SCENE_PLANS = [
    {
        "name": "pure_white_studio",
        "label": "纯白背景 / 人物服装优先",
        "graphic_concept": "pure white studio background with the character and outfit as the complete visual focus",
        "spatial_structure": "clean white seamless wall and floor with only a subtle contact shadow; no furniture, props, panels, or decorative scenery",
        "visual_device": "white negative space supports a clear face and outfit silhouette without pushing the character to the edge",
        "body_silhouette": "front or front three-quarter standing, relaxed weight shift, or upright seated pose; simple readable hands and balanced posture",
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
        "body_silhouette": "front or front three-quarter standing, natural pause, or upright seated posture; no back-facing head-turn",
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
        "body_silhouette": "front three-quarter standing or quiet pause, shoulders relaxed, gaze toward camera or slightly aside",
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
        "body_silhouette": "front three-quarter standing, natural pause, or slight side angle with torso and face remaining clearly readable",
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
        "body_silhouette": "front three-quarter standing, relaxed weight shift, or small daily pause; face and outfit are the first visual focus",
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
        "body_silhouette": "front three-quarter standing, natural pause, or relaxed side angle into the breeze; no body-facing-away turn-back pose",
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
        "body_silhouette": "front three-quarter standing, upright seated pause, or relaxed lean near the window",
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
        "body_silhouette": "front three-quarter standing, quiet pause, or upright seated posture with simple object-empty hands",
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
        "body_silhouette": "front three-quarter standing, upright seated pause, or relaxed weight shift with balanced posture",
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
        "body_silhouette": "front three-quarter standing, relaxed weight shift, or side-angle pause",
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
        "body_silhouette": "front three-quarter standing, natural pause, or shallow diagonal body angle",
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
        "body_silhouette": "front or front three-quarter standing pose, relaxed weight shift, upright seated pause, or a light lean",
        "outfit_direction": "commercial fashion outfit with knit, blouse, short jacket, dress, skirt, or trousers",
        "material_language": "matte colored paper, opaque fabric, subtle floor shadow, clean hair shine",
        "color_strategy": "use one restrained background color family selected to contrast with the outfit; avoid rainbow or neon mixing",
        "lighting_behavior": "large soft studio light keeps face, outfit construction, and fabric texture clearly readable",
        "tags": ["photographer_scene", "studio", "commercial", "colored_backdrop", "character_focus"],
        "weight": 1.1,
    },
    {
        "name": "studio_living_room_set",
        "label": "客厅搭景棚拍 / 沙发落地灯",
        "graphic_concept": "controlled living-room studio set photographed as a clean fashion and character portrait",
        "spatial_structure": "one simple sofa, one floor lamp, and a restrained rug define the set behind or beside the character",
        "visual_device": "three large clean shapes create a comfortable interior impression while leaving face and outfit dominant",
        "body_silhouette": "front three-quarter standing, upright seated pause, or relaxed weight shift beside the set",
        "outfit_direction": "wearable indoor fashion with knit, blouse, cardigan, jacket, dress, skirt, or trousers",
        "material_language": "matte upholstery, simple lamp shade, restrained rug, opaque fabric, soft floor shadow",
        "color_strategy": "set colors stay calm and coordinated; outfit keeps the strongest readable main value",
        "lighting_behavior": "large soft studio key light with a gentle warm practical-lamp accent behind the character",
        "tags": ["photographer_scene", "studio_set", "living_room", "editorial", "character_focus"],
        "weight": 0.8,
    },
    {
        "name": "retro_wood_studio_set",
        "label": "复古木质棚拍 / 暖灯矮柜",
        "graphic_concept": "restrained retro wood studio set with warm editorial atmosphere and clear character focus",
        "spatial_structure": "one wood wall section, one low cabinet, and one small warm lamp establish the set without clutter",
        "visual_device": "wood grain and a single warm light pool support the fashion silhouette",
        "body_silhouette": "front three-quarter standing, natural pause, or upright seated posture near the set",
        "outfit_direction": "polished retro-inspired daily fashion with knit, blouse, jacket, dress, skirt, or trousers",
        "material_language": "warm wood, matte cabinet, simple lamp, opaque fabric, controlled brass accent",
        "color_strategy": "warm brown and amber stay secondary; outfit must separate clearly from the wood background",
        "lighting_behavior": "soft studio key light balanced with one warm practical lamp, face and outfit remain crisp",
        "tags": ["photographer_scene", "studio_set", "retro_wood", "warm_light", "character_focus"],
        "weight": 0.7,
    },
    {
        "name": "industrial_concrete_studio_set",
        "label": "工业水泥棚拍 / 金属椅",
        "graphic_concept": "minimal industrial studio set using concrete texture and one metal chair for a strong fashion read",
        "spatial_structure": "one concrete wall plane, clean floor, and one simple metal chair create a restrained set",
        "visual_device": "hard-edged wall shadow adds structure while the character and outfit remain the first focus",
        "body_silhouette": "front or front three-quarter standing, upright seated pause, or small weight shift beside the chair",
        "outfit_direction": "modern structured fashion with knit, blouse, short jacket, dress, skirt, or trousers",
        "material_language": "matte concrete, restrained metal chair, opaque fabric, controlled shadow edge",
        "color_strategy": "gray set remains neutral and secondary; outfit receives clear color or value separation",
        "lighting_behavior": "controlled side-front studio light with one clean shadow edge and readable facial planes",
        "tags": ["photographer_scene", "studio_set", "industrial", "fashion", "character_focus"],
        "weight": 0.7,
    },
    {
        "name": "restrained_floral_studio_set",
        "label": "花艺棚拍 / 少量花台",
        "graphic_concept": "restrained floral studio portrait using a few arranged flower stems as a supporting color accent",
        "spatial_structure": "one low flower stand and two or three sparse flower stems stay behind or beside the character",
        "visual_device": "small floral color accents support the face and outfit without forming a flower wall or covering the body",
        "body_silhouette": "front three-quarter standing, upright seated pause, or gentle side-angle posture",
        "outfit_direction": "wearable romantic fashion with knit, blouse, cardigan, jacket, dress, skirt, or trousers",
        "material_language": "matte flower stand, sparse stems, opaque fabric, simple studio floor",
        "color_strategy": "flowers use limited muted accents; outfit remains the strongest cohesive color mass",
        "lighting_behavior": "soft clean studio light with readable eyes, face, hands, and outfit details",
        "tags": ["photographer_scene", "studio_set", "floral", "editorial", "character_focus"],
        "weight": 0.65,
    },
    {
        "name": "spring_window_studio_set",
        "label": "春日假窗棚拍 / 柔光墙面",
        "graphic_concept": "spring-inspired studio set with a simple artificial window and soft daylight feeling",
        "spatial_structure": "one clean window-frame set piece and one pale wall create a bright interior suggestion without extra furniture",
        "visual_device": "soft rectangular window light supports the face and outfit while the set remains simple",
        "body_silhouette": "front three-quarter standing, natural pause, upright seated posture, or relaxed weight shift",
        "outfit_direction": "light but opaque spring daily fashion with knit, blouse, cardigan, jacket, dress, skirt, or trousers",
        "material_language": "matte wall, simple window-frame set, opaque fabric, soft floor contact shadow",
        "color_strategy": "set stays bright and restrained; outfit must retain a clearly non-white main value",
        "lighting_behavior": "large soft side-front studio light imitating daylight, with clean facial detail",
        "tags": ["photographer_scene", "studio_set", "window_light", "spring", "character_focus"],
        "weight": 0.8,
    },
    {
        "name": "night_light_studio_set",
        "label": "夜景灯光棚拍 / 深色背景",
        "graphic_concept": "controlled night-light studio portrait with a dark backdrop and a few restrained distant light points",
        "spatial_structure": "dark matte wall and two or three small distant circular lights create atmosphere without becoming a busy night scene",
        "visual_device": "small warm or cool light points remain behind the character and support a clean silhouette",
        "body_silhouette": "front or front three-quarter standing pose, natural pause, or upright seated posture",
        "outfit_direction": "evening-ready wearable fashion with knit, blouse, jacket, dress, skirt, or trousers",
        "material_language": "dark matte backdrop, restrained distant lights, opaque fabric, subtle accessory shine",
        "color_strategy": "dark background remains controlled; outfit and face receive clear tonal and color separation",
        "lighting_behavior": "soft front key light with a gentle rim, keeping face and outfit fully readable",
        "tags": ["photographer_scene", "studio_set", "night_light", "dark_background", "character_focus"],
        "weight": 0.75,
    },
    {
        "name": "geometric_steps_studio_set",
        "label": "几何台阶棚拍 / 时装轮廓",
        "graphic_concept": "minimal geometric-step studio set designed to clarify fashion silhouette and balanced posture",
        "spatial_structure": "one or two broad low steps and a plain wall form a clean set with no additional props",
        "visual_device": "simple horizontal and diagonal step lines support the body and outfit silhouette",
        "body_silhouette": "front three-quarter standing, one foot resting on a low step, upright seated pause, or balanced weight shift",
        "outfit_direction": "fashion-forward wearable outfit with knit, blouse, short jacket, dress, skirt, or trousers",
        "material_language": "matte geometric blocks, plain wall, opaque fabric, controlled floor shadow",
        "color_strategy": "steps and wall use one restrained neutral or muted color family; outfit remains clearly separated",
        "lighting_behavior": "large soft studio key light with clean step shadows and readable face",
        "tags": ["photographer_scene", "studio_set", "geometric_steps", "fashion", "character_focus"],
        "weight": 0.8,
    },
]


PHOTOGRAPHER_ACTION_STYLES = [
    {
        "name": "square_front_power_stance",
        "body_silhouette": "decisive squared stance facing the selected camera, shoulders and hips nearly frontal, feet clearly separated, weight evenly planted, arms relaxed away from the torso",
        "tags": ["standing", "pose_front_square", "strong_silhouette"],
        "weight": 1.0,
    },
    {
        "name": "contrapposto_hip_shift",
        "body_silhouette": "clear contrapposto pose with weight fully on one leg, the free knee bent, hips visibly shifted, shoulders counterbalanced, and both hands simple and separate from the body",
        "tags": ["standing", "pose_contrapposto", "strong_silhouette"],
        "weight": 1.0,
    },
    {
        "name": "true_profile_walk",
        "body_silhouette": "true side-profile walk moving horizontally across the image plane, face and torso sharing the same side direction, legs separated mid-step, with no turn-back glance",
        "tags": ["walking", "pose_true_profile", "dynamic_pose"],
        "weight": 0.25,
    },
    {
        "name": "cross_step_fashion_pose",
        "body_silhouette": "fashion cross-step pose with one foot crossing clearly in front of the other, hips offset, upper body tall, one arm lowered and the other bent loosely away from the face",
        "tags": ["standing", "pose_cross_step", "fashion_pose"],
        "weight": 1.0,
    },
    {
        "name": "asymmetric_seated_pose",
        "body_silhouette": "clearly seated asymmetric pose on the available seat or low set edge, one knee raised slightly above the other, torso leaning forward a little, forearms separated and hands relaxed",
        "tags": ["seated", "pose_asymmetric_seated", "strong_silhouette"],
        "weight": 1.0,
    },
    {
        "name": "full_body_side_stretch",
        "body_silhouette": "standing side stretch forming a clear curved silhouette, one arm raised overhead, the opposite arm lowered, hips and ribcage shifting in opposite directions while balance stays natural",
        "tags": ["standing", "stretch", "pose_side_stretch"],
        "weight": 1.0,
    },
]


PHOTOGRAPHER_COMPOSITION_PLANS = [
    {
        "name": "eye_level_front_camera",
        "composition": "clean front-facing camera direction with balanced character placement and restrained background",
        "camera": "natural eye-level frontal viewpoint with normal perspective; distance follows the selected shot scale",
        "pose": "selected action remains natural and readable from the front",
        "foreground": "minimal foreground; keep all scene elements behind or beside the character",
        "lighting": "clean side-front or soft frontal light keeps face and clothing readable",
        "guardrail": "background remains subordinate; selected shot scale controls framing distance",
        "tags": ["photographer_composition", "eye_level", "front_view"],
        "weight": 1.0,
    },
    {
        "name": "eye_level_three_quarter_camera",
        "composition": "clean three-quarter camera direction showing facial depth, hairstyle, and outfit silhouette",
        "camera": "natural eye-level three-quarter viewpoint with normal perspective; distance follows the selected shot scale",
        "pose": "selected action remains clearly expressed and coherent from the three-quarter direction",
        "foreground": "none; scene lines stay behind or beside the character",
        "lighting": "soft directional light separates character from a restrained background",
        "guardrail": "selected shot scale controls framing distance; preserve natural proportions",
        "tags": ["photographer_composition", "eye_level", "three_quarter"],
        "weight": 1.0,
    },
    {
        "name": "gentle_diagonal_camera",
        "composition": "gentle diagonal camera direction adds energy while keeping the character and background geometry stable",
        "camera": "eye-level camera shifted slightly to one side, normal perspective, no dramatic roll; distance follows the selected shot scale",
        "pose": "selected action aligns naturally with the shallow diagonal direction",
        "foreground": "none; simple background lines provide the diagonal rhythm",
        "lighting": "environment light leads gently toward the face and outfit",
        "guardrail": "keep horizon and body proportions stable; selected shot scale controls distance",
        "tags": ["photographer_composition", "eye_level", "diagonal_camera"],
        "weight": 1.0,
    },
    {
        "name": "side_three_quarter_camera",
        "composition": "side three-quarter camera direction balancing facial profile, hairstyle, and outfit depth",
        "camera": "eye-level viewpoint between three-quarter and profile, normal perspective; distance follows the selected shot scale",
        "pose": "selected action remains coherent with the side three-quarter direction",
        "foreground": "none; keep the character silhouette clean",
        "lighting": "even readable light with clear separation from the ground and background",
        "guardrail": "keep face readable and proportions natural; selected shot scale controls distance",
        "tags": ["photographer_composition", "eye_level", "side_three_quarter"],
        "weight": 1.0,
    },
    {
        "name": "clean_profile_editorial",
        "composition": "clean side-profile editorial frame emphasizing face outline, hair silhouette, and outfit line",
        "camera": "eye-level side view with normal perspective; distance follows the selected shot scale",
        "pose": "body and face share the same clear side direction without twisting backward",
        "foreground": "none or one tiny scene-native edge that does not overlap the character",
        "lighting": "soft side-front or rim-balanced light separates profile from background",
        "guardrail": "keep both profile and outfit readable; avoid silhouette-only darkness",
        "tags": ["photographer_composition", "profile", "side_view"],
        "weight": 1.0,
    },
    {
        "name": "restrained_low_angle_editorial",
        "composition": "restrained low-angle editorial frame with the character presented large and directly front-facing",
        "camera": "camera slightly below waist or seat height, centered directly in front of the character, gentle upward view with normal lens feeling",
        "pose": "preserve the selected pose while keeping the face, shoulders, ribcage, and hips squarely oriented toward the camera",
        "subject_orientation": "mandatory large frontal character orientation: face, shoulders, chest line, ribcage, and hips all face directly toward the camera; no three-quarter, side, profile, turned-away, or diagonal body orientation",
        "foreground": "none; floor line or low step may remain behind the character",
        "lighting": "clean face light and subtle rim preserve readable facial planes",
        "guardrail": "keep face prominent and proportions natural; preserve the selected pose but never rotate the person away from a direct frontal orientation; do not emphasize legs, chest, or underside anatomy",
        "tags": ["photographer_composition", "low_camera", "editorial"],
        "weight": 1.0,
    },
    {
        "name": "controlled_high_angle_portrait",
        "composition": "controlled high-angle portrait using floor or set geometry while keeping character large and immediately readable",
        "camera": "camera moderately above eye level, looking downward at a clear face and outfit silhouette",
        "pose": "standing, seated, or gentle upward gaze stays simple and anatomically clear",
        "foreground": "none; floor or set shapes remain behind the character",
        "lighting": "soft top-side light with clean eyes and readable clothing detail",
        "guardrail": "character remains large; avoid tiny subject or excessive floor area",
        "tags": ["photographer_composition", "high_camera", "character_focus"],
        "weight": 1.0,
    },
    {
        "name": "floor_level_leg_length_low_angle",
        "composition": "dramatic floor-level upward fashion frame with the character presented large and directly front-facing",
        "camera": "camera centered directly in front of the character, close to floor level and below knee height, looking upward with a moderate wide-angle fashion lens",
        "pose": "preserve the selected pose while keeping the face, shoulders, ribcage, and hips squarely oriented toward the camera",
        "subject_orientation": "mandatory large frontal character orientation: face, shoulders, chest line, ribcage, and hips all face directly toward the camera; no three-quarter, side, profile, turned-away, or diagonal body orientation",
        "foreground": "a clean floor edge may anchor the bottom of frame; no foreground obstruction",
        "lighting": "clean face light and a controlled rim keep the upward silhouette readable",
        "guardrail": "show an intentional from-below perspective while preserving the selected pose and a strict direct frontal person orientation; avoid fetish framing, underwear visibility, distorted feet, or losing the face",
        "tags": ["photographer_composition", "low_camera", "floor_level", "leg_length_perspective"],
        "weight": 1.0,
    },
    {
        "name": "extreme_chest_up_close_portrait",
        "composition": "large tight portrait cropped strictly from the upper chest upward, with face, eyes, hairstyle, shoulders, and neckline filling nearly the entire frame",
        "camera": "close portrait distance at eye level or a gentle three-quarter angle, normal portrait lens, shallow depth of field",
        "pose": "simple head-and-shoulder posture with a natural gaze; hands remain outside the crop unless one simple fingertip edge appears",
        "foreground": "none; background becomes a restrained soft field",
        "lighting": "precise facial light and eye highlights with clean separation around hair and shoulders",
        "guardrail": "crop only from upper chest upward; do not widen to waist-up or half-body, do not emphasize cleavage, and do not let scenery compete with the face",
        "tags": ["photographer_composition", "extreme_closeup", "chest_up_crop", "character_focus"],
        "weight": 1.0,
    },
]

ACTION_COMPOSITION_COMPATIBILITY = {
    "square_front_power_stance": {
        "eye_level_front_camera",
        "eye_level_three_quarter_camera",
        "gentle_diagonal_camera",
        "restrained_low_angle_editorial",
        "controlled_high_angle_portrait",
    },
    "contrapposto_hip_shift": {
        "eye_level_front_camera",
        "eye_level_three_quarter_camera",
        "gentle_diagonal_camera",
        "side_three_quarter_camera",
        "restrained_low_angle_editorial",
        "controlled_high_angle_portrait",
    },
    "true_profile_walk": {
        "side_three_quarter_camera",
        "clean_profile_editorial",
    },
    "cross_step_fashion_pose": {
        "eye_level_front_camera",
        "eye_level_three_quarter_camera",
        "gentle_diagonal_camera",
        "side_three_quarter_camera",
        "restrained_low_angle_editorial",
    },
}

FRONTAL_LOW_ANGLE_COMPOSITION_NAMES = {
    "restrained_low_angle_editorial",
    "floor_level_leg_length_low_angle",
}


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
    {
        "name": "face_closeup",
        "description": "intentional face close-up with eyes, expression, hairstyle, and a small shoulder-level outfit detail clearly readable",
        "weight": 1.0,
    },
    {
        "name": "bust_closeup",
        "description": "bust-up portrait centered on face, hairstyle, shoulders, and upper outfit construction with comfortable framing",
        "weight": 1.0,
    },
]

SPECIAL_COMPOSITION_SHOT_SCALES = {
    "floor_level_leg_length_low_angle": {
        "name": "floor_level_full_figure",
        "description": "complete character framing that preserves the selected standing, moving, stretching, or seated pose; the upward perspective stays clear while face and full pose remain readable",
    },
    "extreme_chest_up_close_portrait": {
        "name": "strict_upper_chest_closeup",
        "description": "very large upper-chest-up close portrait; only upper chest, shoulders, neck, face, and hair are visible, filling about 75-90 percent of the image",
    },
}

ACTION_SHOT_SCALES = {
    "square_front_power_stance": {
        "name": "pose_visible_near_full_body",
        "description": "near full-body framing that clearly shows the squared shoulders, planted feet, separated arms, and complete body silhouette",
    },
    "contrapposto_hip_shift": {
        "name": "pose_visible_near_full_body",
        "description": "near full-body framing that clearly shows the supporting leg, bent free knee, hip shift, and counterbalanced shoulders",
    },
    "true_profile_walk": {
        "name": "pose_visible_full_body",
        "description": "full-body side-profile framing with both separated legs visible and enough horizontal room for the walking direction",
    },
    "cross_step_fashion_pose": {
        "name": "pose_visible_near_full_body",
        "description": "near full-body fashion framing with crossed feet, shifted hips, arms, and complete silhouette clearly visible",
    },
    "asymmetric_seated_pose": {
        "name": "pose_visible_seated",
        "description": "knee-up to near full-body framing that clearly shows the asymmetric seated leg levels, forward lean, arms, and seat edge",
    },
    "full_body_side_stretch": {
        "name": "pose_visible_full_body",
        "description": "full-body framing with raised hand, lowered hand, feet, and the complete curved side-stretch silhouette visible",
    },
}

SPECIAL_COMPOSITION_ACTION_STYLES = {
    "extreme_chest_up_close_portrait": {
        "name": "quiet_head_and_shoulders",
        "body_silhouette": "quiet head-and-shoulder portrait moment with a natural gaze and relaxed neckline; hands stay outside the tight upper-chest-up crop",
        "tags": ["extreme_closeup", "stable_pose", "camera_specific"],
    },
}


def resolve_photographer_shot_scale(composition_plan, shot_scale, action_style=None):
    special = SPECIAL_COMPOSITION_SHOT_SCALES.get(composition_plan.get("name"))
    if special:
        return dict(special)
    action_scale = ACTION_SHOT_SCALES.get((action_style or {}).get("name"))
    return dict(action_scale) if action_scale else dict(shot_scale)


def resolve_photographer_action_style(composition_plan, action_style):
    special = SPECIAL_COMPOSITION_ACTION_STYLES.get(composition_plan.get("name"))
    return dict(special) if special else dict(action_style)


def _weighted_choice(items):
    total = sum(max(float(item.get("weight", 1.0)), 0.01) for item in items)
    pick = random.random() * total
    cursor = 0.0
    for item in items:
        cursor += max(float(item.get("weight", 1.0)), 0.01)
        if pick <= cursor:
            return dict(item)
    return dict(items[-1])


def set_active_photographer_scene_plans(plan_names=None):
    global _ACTIVE_SCENE_PLAN_NAMES
    if isinstance(plan_names, str):
        plan_names = [plan_names]
    if plan_names and any(name in {"", "all", "random", "full_random"} for name in plan_names):
        plan_names = None
    valid_names = {plan["name"] for plan in PHOTOGRAPHER_SCENE_PLANS}
    if plan_names is not None:
        unknown = [name for name in plan_names if name not in valid_names]
        if unknown:
            raise ValueError(f"unknown photographer scene plans: {unknown}")
        plan_names = list(dict.fromkeys(plan_names))
    _ACTIVE_SCENE_PLAN_NAMES = plan_names


def active_photographer_scene_plans():
    return None if _ACTIVE_SCENE_PLAN_NAMES is None else list(_ACTIVE_SCENE_PLAN_NAMES)


def photographer_scene_plan_label(plan_names=None):
    plan_names = _ACTIVE_SCENE_PLAN_NAMES if plan_names is None else plan_names
    if isinstance(plan_names, str):
        plan_names = [plan_names]
    if not plan_names:
        return "全随机摄影师背景"
    labels = []
    for plan in PHOTOGRAPHER_SCENE_PLANS:
        if plan["name"] in plan_names:
            labels.append(plan.get("label", plan["name"]))
    return "、".join(labels)


def photographer_scene_plans_for_selection(plan_names=None):
    plan_names = _ACTIVE_SCENE_PLAN_NAMES if plan_names is None else plan_names
    if isinstance(plan_names, str):
        plan_names = [plan_names]
    if not plan_names:
        return [dict(plan) for plan in PHOTOGRAPHER_SCENE_PLANS]
    selected_names = set(plan_names)
    plans = [
        dict(plan)
        for plan in PHOTOGRAPHER_SCENE_PLANS
        if plan["name"] in selected_names
    ]
    return plans or [dict(plan) for plan in PHOTOGRAPHER_SCENE_PLANS]


def choose_photographer_scene_plan(character_name=None, recent_tags=None):
    return dict(random.choice(photographer_scene_plans_for_selection()))


def choose_photographer_action_style(character_name=None, recent_tags=None, plan=None):
    recent = set(recent_tags or [])
    fresh_actions = [
        action for action in PHOTOGRAPHER_ACTION_STYLES
        if not recent.intersection(
            tag for tag in action.get("tags", [])
            if tag.startswith("pose_")
        )
    ]
    return _weighted_choice(fresh_actions or PHOTOGRAPHER_ACTION_STYLES)


def choose_photographer_composition_plan(recent_tags=None, plan=None, action=None, outfit_direction=None):
    compatible_names = ACTION_COMPOSITION_COMPATIBILITY.get((action or {}).get("name"))
    if not compatible_names:
        compatible = list(PHOTOGRAPHER_COMPOSITION_PLANS)
    else:
        special_names = set(SPECIAL_COMPOSITION_SHOT_SCALES)
        compatible = [
            composition for composition in PHOTOGRAPHER_COMPOSITION_PLANS
            if composition["name"] in compatible_names or composition["name"] in special_names
        ]
    if (action or {}).get("name") == "true_profile_walk":
        compatible = [
            composition for composition in compatible
            if composition["name"] not in FRONTAL_LOW_ANGLE_COMPOSITION_NAMES
        ]
    return dict(random.choice(compatible))


def choose_photographer_shot_scale(recent_tags=None, plan=None):
    return dict(random.choice(PHOTOGRAPHER_SHOT_SCALES))
