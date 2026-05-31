import random


OUTFIT_DIRECTIONS = [
    "reference-faithful outfit with only small fabric and accessory variation",
    "clean light-novel casual outfit, keeping the character palette recognizable",
    "soft bakery or cafe casual outfit, warm and simple",
    "fresh meadow picnic outfit, clear color blocks, low ornament density",
    "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
    "minimal sunny studio outfit, face and hair identity as the main focus",
    "romantic flower bridal dress, elegant veil or bouquet, clean and non-adult",
    "classic cafe maid outfit, neat apron, ribbons, cute and polished",
    "elegant black stockings outfit, refined fashion styling, no explicit posing",
    "white blouse and black stockings, clean light-novel heroine styling",
]


ANTI_SAFE_COMPOSITION = []


CHARACTER_PROFILES = {
    "南宫": {
        "official_core": "黑发短双马尾，发尾粉色渐变，齐刘海，粉色眼睛，猫咪发夹，俏皮又危险的少女气质。",
        "identity_tokens": ["short black twin tails with pink gradient tips", "straight blunt bangs", "pink eyes", "cat hairpin"],
        "viewer_relationship": "像在悄悄观察观众，表情聪明、轻微挑衅，但不夸张。",
        "thumbnail_strategy": "黑粉发色和猫咪小饰品必须在小图里仍然清楚。",
        "interaction_rule": "允许对视、侧身回头、轻笑；避免手指指向镜头。",
        "safe_sensuality": "保持可爱与精致，表达干净。",
        "color_anchor": "black, pink, clean white",
    },
    "爱芮": {
        "official_core": "高饱和粉色双马尾，黑色挑染刘海，明亮粉蓝眼睛，偶像感、元气感强。",
        "identity_tokens": ["vivid pink twin tails", "black streak in bangs", "pink-blue bright eyes", "idol-like hair accessories"],
        "viewer_relationship": "像正在和观众营业互动，亲近、明亮、有舞台感。",
        "thumbnail_strategy": "粉色双马尾和明亮眼睛是第一识别点。",
        "interaction_rule": "允许挥手、微笑、转身看向观众；避免自拍道具和伸手贴镜头。",
        "safe_sensuality": "偶像营业感优先，保持干净亲近。",
        "color_anchor": "hot pink, cyan, clean black",
    },
    "千夏": {
        "official_core": "薄荷灰绿短发，柔软分层发型，侧边小发束与大蝴蝶结，粉金色眼睛，清爽安静的夏日少女。",
        "identity_tokens": ["mint gray-green short layered hair", "large mint bow", "soft asymmetrical bangs", "pink-gold eyes"],
        "viewer_relationship": "像安静陪伴观众，温柔、干净、带一点害羞。",
        "thumbnail_strategy": "薄荷发色、蝴蝶结、清透眼睛必须稳定，不要改成普通长发角色。",
        "interaction_rule": "允许坐姿、窗边回头、自然整理头发；避免纸笔和创作者设定。",
        "safe_sensuality": "青春清爽，表达干净。",
        "color_anchor": "mint, pale gold, soft white",
    },
    "丹": {
        "official_core": "浅粉短发，空气感碎刘海，粉紫眼睛，安静、透明、梦境感的少女。",
        "identity_tokens": ["pale pink short layered hair", "airy uneven bangs", "pink-purple eyes", "small silver-blue hair accessory"],
        "viewer_relationship": "像从安静梦境里看向观众，神秘但亲近。",
        "thumbnail_strategy": "浅粉短发和透明感眼睛必须稳定，服装可以变化。",
        "interaction_rule": "允许站立、坐姿、侧脸、轻微回头；避免固定同一套服装。",
        "safe_sensuality": "以清冷和梦境感为主，保持干净克制。",
        "color_anchor": "pale pink, violet, silver blue",
    },
    "星见雅": {
        "official_core": "黑色长直发，姬发式齐刘海，尖锐黑色兽耳，红色眼睛，冷静、锋利、克制的剑士气质。",
        "identity_tokens": ["long straight black hair", "hime-cut blunt bangs", "sharp black animal ears", "red eyes"],
        "viewer_relationship": "像冷静地看穿观众，距离感强但角色存在感清楚。",
        "thumbnail_strategy": "黑长直、黑兽耳、红眼是核心；剑可以作为气质符号但不是必须手持。",
        "interaction_rule": "允许刀鞘、红色线条、远处剑影；避免复杂手部持物。",
        "safe_sensuality": "冷感优雅，不强调暴露。",
        "color_anchor": "black, red, white",
    },
    "仪玄": {
        "official_core": "银白长发，柔软呆毛，黑色雷纹或波纹发饰，金色眼睛，成熟安静的神秘术士气质。",
        "identity_tokens": ["long silver-white hair", "small ahoge", "black wave hair ornament", "golden eyes"],
        "viewer_relationship": "像平静地邀请观众进入仪式，沉稳、有神秘感。",
        "thumbnail_strategy": "银白长发和金眼必须清晰，背景不要压过人物。",
        "interaction_rule": "允许手在胸前、袖摆自然下垂、侧身凝视；避免复杂法阵手势。",
        "safe_sensuality": "成熟优雅即可，表达干净。",
        "color_anchor": "silver white, black, gold",
    },
    "叶瞬光": {
        "official_core": "暖棕长发，棕色兽耳，蓬松棕色尾巴，红色眼睛，红色发带或花饰，温柔可靠的守护者气质。",
        "identity_tokens": ["warm brown long hair", "brown animal ears", "fluffy brown tail", "red eyes", "red ribbon or flower accessory"],
        "viewer_relationship": "像温柔地回头照看观众，亲和但有守护感。",
        "thumbnail_strategy": "暖棕发色、棕色兽耳和尾巴要稳定，不要变成黑发红眼冷剑士。",
        "interaction_rule": "剑是可选符号，不强制手持；避免固定宗门或山门元素。",
        "safe_sensuality": "温柔端正，保持清爽可靠。",
        "color_anchor": "warm brown, red, ivory",
    },
    "席德": {
        "official_core": "银灰短发或中短发，蓝紫色眼睛，带少量蓝紫光纹与异质感，天真但危险的少女。",
        "identity_tokens": ["silver-gray short hair", "blue-violet eyes", "subtle blue-violet light marks", "innocent dangerous expression"],
        "viewer_relationship": "像天真地展示一个不可思议的小秘密，表情无辜但气氛有轻微危险感。",
        "thumbnail_strategy": "银灰发、蓝紫眼睛和细小光纹必须清楚，避免普通校园少女化。",
        "interaction_rule": "允许花朵、玻璃糖纸、蓝紫小光点；避免复杂硬质装置和多手结构。",
        "safe_sensuality": "以异质感和可爱危险感为主，保持干净表达。",
        "color_anchor": "silver gray, blue violet, soft white",
    },
    "橘福福": {
        "official_core": "橘色短发，明亮金橙眼睛，虎纹或虎主题小饰品，活泼、可靠、热烈的少女气质。",
        "identity_tokens": ["short orange hair", "golden-orange eyes", "tiger-themed accessory", "warm lively expression"],
        "viewer_relationship": "像元气地把观众拉进热闹场面，亲近、明亮、行动感强。",
        "thumbnail_strategy": "橘发、金橙眼、虎主题识别要稳定，避免被背景同化。",
        "interaction_rule": "允许奔跑、回头笑、舞台动作；避免固定宗门或山门元素。",
        "safe_sensuality": "明快可爱，表达干净。",
        "color_anchor": "orange, gold, white",
    },
}


ART_DIRECTION_PLANS = [
    {
        "name": "sunny_cafe_window",
        "graphic_concept": "阳光咖啡店窗边，温暖日常感和角色表情优先。",
        "spatial_structure": "木桌、窗光、咖啡杯或甜点只保留一两个，背景干净柔和。",
        "visual_device": "窗框和桌面光斑把视线引向角色脸部。",
        "body_silhouette": "三分之二身或膝上构图，坐姿或轻靠桌边，双手自然可见。",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "棉布、针织、木纹、陶瓷杯、柔软发丝。",
        "color_strategy": "奶油白、浅木色、角色主色构成清楚温暖的画面。",
        "lighting_behavior": "午后窗光，脸部明亮，阴影柔和。",
        "tags": ["cafe", "window", "warm_light"],
    },
    {
        "name": "small_bakery_morning",
        "graphic_concept": "清晨面包房，柔软香气和生活感支撑角色。",
        "spatial_structure": "面包架、纸袋、玻璃柜和暖色灯光，元素少而可读。",
        "visual_device": "圆形面包和暖灯形成柔和重复节奏。",
        "body_silhouette": "站在柜台旁或轻轻回头，手部动作简单，不做复杂持物。",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "围裙、棉麻、纸袋、木架、柔软烘焙暖光。",
        "color_strategy": "浅棕、奶油黄和角色识别色平衡，避免整张图发黄。",
        "lighting_behavior": "暖色室内光加柔和窗光，眼睛保持清楚。",
        "tags": ["bakery", "morning", "warm_light"],
    },
    {
        "name": "open_grassland_breeze",
        "graphic_concept": "开阔草原微风，清爽自然色和角色轮廓优先。",
        "spatial_structure": "低矮草地、远处柔和地平线、少量小花，不堆复杂景物。",
        "visual_device": "风吹发丝和衣摆形成轻方向线。",
        "body_silhouette": "站姿或轻步行走，三分之二身到全身之间，动作稳定。",
        "outfit_direction": "fresh meadow picnic outfit, clear color blocks, low ornament density",
        "material_language": "轻薄布料、草叶、小花、柔软发丝。",
        "color_strategy": "草地绿色低饱和，角色主色保持明确，不被背景吞掉。",
        "lighting_behavior": "晴天漫射光，整体明亮但不过曝。",
        "tags": ["grassland", "breeze", "natural_light"],
    },
    {
        "name": "flower_sea_afternoon",
        "graphic_concept": "午后花海，梦幻但不杂乱，人物仍是主视觉。",
        "spatial_structure": "大片花田作为柔和色块，前景只放少量虚化花朵。",
        "visual_device": "花海色块围绕角色发色和眼睛形成记忆点。",
        "body_silhouette": "站姿、坐姿或回头，手可以轻碰花枝但不遮脸。",
        "outfit_direction": "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "花瓣、轻纱、棉布、发饰，细节密度适中。",
        "color_strategy": "花色服务角色主色，避免满屏同一种高饱和颜色。",
        "lighting_behavior": "柔和午后光，脸部清晰，背景轻虚化。",
        "tags": ["flower_field", "afternoon", "dream"],
    },
    {
        "name": "picnic_under_tree",
        "graphic_concept": "树荫野餐，温柔陪伴感和角色亲近度优先。",
        "spatial_structure": "野餐布、篮子、树荫、远处草地，画面简洁。",
        "visual_device": "格纹野餐布形成图形底，树影轻轻压住背景。",
        "body_silhouette": "自然坐姿或跪坐，双手放在膝边、篮子旁或衣摆上。",
        "outfit_direction": "fresh meadow picnic outfit, clear color blocks, low ornament density",
        "material_language": "棉布、藤篮、草地、轻柔树影。",
        "color_strategy": "浅绿、奶油白和角色主色组合，整体清爽。",
        "lighting_behavior": "树荫斑驳光，但脸部不能被遮暗。",
        "tags": ["picnic", "tree_shadow", "soft_daylight"],
    },
    {
        "name": "greenhouse_flower_room",
        "graphic_concept": "阳光玻璃花房，花和绿植只是气氛，不抢人物身份。",
        "spatial_structure": "玻璃墙、藤蔓、几盆植物和浅色地面，空间轻而干净。",
        "visual_device": "花枝形成自然外框，角色脸部无遮挡。",
        "body_silhouette": "站姿或坐姿，半身以上到膝上之间，手部简单。",
        "outfit_direction": "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "透明玻璃、柔软布料、少量花饰。",
        "color_strategy": "浅绿浅白背景，角色主色作为记忆点。",
        "lighting_behavior": "扩散自然光，低噪点，清晰线稿。",
        "tags": ["greenhouse", "flower", "natural_light"],
    },
    {
        "name": "bookstore_cafe_corner",
        "graphic_concept": "书店咖啡角，安静生活感和柔和知识气氛。",
        "spatial_structure": "书架、圆桌、暖灯、窗边座位，书脊不出现可读文字。",
        "visual_device": "书架竖线和圆桌形成稳定构图。",
        "body_silhouette": "坐姿或站在书架旁，手部放松，不拿复杂道具。",
        "outfit_direction": "clean light-novel casual outfit, keeping the character palette recognizable",
        "material_language": "纸张、木架、针织、柔软发丝。",
        "color_strategy": "暖木色和浅奶油色托住角色主色。",
        "lighting_behavior": "柔和室内灯加窗边自然光。",
        "tags": ["bookstore", "cafe", "quiet"],
    },
    {
        "name": "pastel_room_sweets",
        "graphic_concept": "柔和甜点房间，简约可爱但不幼稚。",
        "spatial_structure": "浅色墙面、小圆桌、蛋糕或水果盘，背景极简。",
        "visual_device": "圆桌和甜点成为小型视觉锚点，人物脸部最清楚。",
        "body_silhouette": "站姿或坐姿，膝上构图，手靠近杯盘或自然下垂。",
        "outfit_direction": "minimal sunny studio outfit, face and hair identity as the main focus",
        "material_language": "奶油色布料、陶瓷、甜点、轻柔发饰。",
        "color_strategy": "淡彩背景，角色发色和眼睛必须更明确。",
        "lighting_behavior": "柔和室内高调光，避免发白。",
        "tags": ["sweets", "pastel_room", "soft_light"],
    },
    {
        "name": "garden_tea_table",
        "graphic_concept": "花园茶桌，精致但轻量的童话日常。",
        "spatial_structure": "小茶桌、花篱、白色椅子和浅色桌布，布景清楚不拥挤。",
        "visual_device": "茶桌圆形和花篱弧线围住角色。",
        "body_silhouette": "坐姿、侧身回头或轻扶椅背，手指清楚自然。",
        "outfit_direction": "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "桌布、花朵、茶杯、柔软裙摆。",
        "color_strategy": "白、浅绿、花色点缀，角色主色仍是最高识别。",
        "lighting_behavior": "晴天花园柔光，空气清透。",
        "tags": ["garden", "tea_table", "fairy_tale"],
    },
    {
        "name": "flower_bridal_garden",
        "graphic_concept": "花嫁感花园插画，浪漫、干净、明亮，重点是角色脸和发型。",
        "spatial_structure": "浅色花门、白色纱帘、花束和草地，布景轻量不拥挤。",
        "visual_device": "头纱、花束和花门形成柔和外框。",
        "body_silhouette": "站姿或坐姿，三分之二身，双手自然捧花或放在裙摆旁。",
        "outfit_direction": "romantic flower bridal dress, elegant veil or bouquet, clean and non-adult",
        "material_language": "薄纱、花束、柔软白裙、少量丝带。",
        "color_strategy": "白色和浅花色托住角色主色，不把角色发色冲淡。",
        "lighting_behavior": "晴天花园柔光，脸部清晰，整体干净。",
        "tags": ["bridal", "garden", "flower", "soft_light"],
    },
    {
        "name": "cafe_maid_afternoon",
        "graphic_concept": "咖啡店女仆风插画，可爱、整洁、带轻营业感。",
        "spatial_structure": "咖啡桌、甜点盘、浅色墙面和窗光，背景简单。",
        "visual_device": "围裙轮廓和甜点盘形成清楚记忆点。",
        "body_silhouette": "站姿或坐在桌边，手部自然放在托盘、裙摆或桌边。",
        "outfit_direction": "classic cafe maid outfit, neat apron, ribbons, cute and polished",
        "material_language": "围裙、蝴蝶结、棉布、陶瓷杯、甜点。",
        "color_strategy": "黑白女仆服作为稳定色块，角色发色和眼睛必须更突出。",
        "lighting_behavior": "午后咖啡店柔光，眼睛和脸最清楚。",
        "tags": ["maid", "cafe", "sweets", "warm_light"],
    },
    {
        "name": "black_stockings_tea_room",
        "graphic_concept": "精致茶室时装插画，黑丝作为优雅服装元素，不做成人化姿态。",
        "spatial_structure": "小茶桌、椅子、浅色窗帘和花瓶，空间简洁柔和。",
        "visual_device": "黑白服装对比和角色发色形成强识别。",
        "body_silhouette": "坐姿或侧身站姿，腿部姿态自然，手部简单清楚。",
        "outfit_direction": "elegant black stockings outfit, refined fashion styling, no explicit posing",
        "material_language": "黑色长袜、轻裙摆、白衬衫、丝带、柔软布料。",
        "color_strategy": "黑白服装压住画面，背景用奶油白和浅木色，角色主色清楚。",
        "lighting_behavior": "柔和室内自然光，避免强烈阴影。",
        "tags": ["black_stockings", "tea_room", "fashion", "soft_light"],
    },
]


ACTION_STYLES = [
    {
        "name": "steady_eye_contact",
        "body_silhouette": "自然站立或轻微侧身，直接看向观众，手放在身侧或衣摆附近。",
        "tags": ["eye_contact", "stable_pose"],
    },
    {
        "name": "gentle_side_glance",
        "body_silhouette": "三分之二侧身回头，头发自然流动，手部保持放松。",
        "tags": ["side_glance", "stable_pose"],
    },
    {
        "name": "seated_quiet_pose",
        "body_silhouette": "安静坐姿，膝上到全身之间，双手自然放在膝边或座位上。",
        "tags": ["seated", "stable_hands"],
    },
    {
        "name": "walking_forward",
        "body_silhouette": "轻微向前走，身体重心清楚，双手自然摆动。",
        "tags": ["walking", "stable_hands"],
    },
    {
        "name": "adjusting_hair",
        "body_silhouette": "一只手轻轻整理头发，另一只手自然下垂，手指完整清楚。",
        "tags": ["hair_touch", "simple_hand"],
    },
    {
        "name": "hands_near_chest",
        "body_silhouette": "双手靠近胸前或领口附近，动作轻，手指数量清楚。",
        "tags": ["hands_visible", "simple_hand"],
    },
]


CHARACTER_PLAN_HINTS = {
    "南宫": ["sunny_cafe_window", "pastel_room_sweets", "bookstore_cafe_corner"],
    "爱芮": ["small_bakery_morning", "cafe_maid_afternoon", "pastel_room_sweets"],
    "千夏": ["sunny_cafe_window", "open_grassland_breeze", "picnic_under_tree"],
    "丹": ["flower_bridal_garden", "flower_sea_afternoon", "greenhouse_flower_room"],
    "星见雅": ["black_stockings_tea_room", "garden_tea_table", "bookstore_cafe_corner"],
    "仪玄": ["flower_bridal_garden", "greenhouse_flower_room", "garden_tea_table"],
    "叶瞬光": ["open_grassland_breeze", "flower_bridal_garden", "flower_sea_afternoon"],
    "席德": ["pastel_room_sweets", "cafe_maid_afternoon", "greenhouse_flower_room"],
    "橘福福": ["small_bakery_morning", "cafe_maid_afternoon", "picnic_under_tree"],
}


def _tags_of(item):
    tags = item.get("tags", [])
    return set(tags if isinstance(tags, list) else list(tags))


def _recent_set(recent_tags=None):
    if not recent_tags:
        return set()
    return set(recent_tags)


def _weighted_choice(items, preferred_names=None, recent_tags=None):
    recent = _recent_set(recent_tags)
    preferred = set(preferred_names or [])
    scored = []
    for item in items:
        score = 1.0
        if item["name"] in preferred:
            score += 1.5
        score -= len(_tags_of(item) & recent) * 0.6
        scored.append((max(score, 0.2), item))
    total = sum(score for score, _ in scored)
    pick = random.random() * total
    cursor = 0.0
    for score, item in scored:
        cursor += score
        if pick <= cursor:
            return item
    return scored[-1][1]


def choose_art_plan(character_name=None, recent_tags=None):
    preferred = CHARACTER_PLAN_HINTS.get(character_name or "", [])
    return dict(_weighted_choice(ART_DIRECTION_PLANS, preferred, recent_tags))


def choose_action_style(character_name=None, recent_tags=None):
    return dict(_weighted_choice(ACTION_STYLES, recent_tags=recent_tags))


def choose_plan_and_action(character_name, recent_tags=None):
    plan = choose_art_plan(character_name, recent_tags)
    action = choose_action_style(character_name, recent_tags)
    return plan, action


def collect_cooldown_tags(plan, action):
    return sorted(_tags_of(plan) | _tags_of(action))


def propagation_profile_for(character_name):
    profile = CHARACTER_PROFILES.get(character_name, CHARACTER_PROFILES["丹"])
    return {
        "official_core": profile["official_core"],
        "viewer_relationship": profile["viewer_relationship"],
        "interaction_rule": profile["interaction_rule"],
        "thumbnail_strategy": profile["thumbnail_strategy"],
        "safe_sensuality": profile["safe_sensuality"],
        "color_anchor": profile["color_anchor"],
        "propagation_translation": "稳定角色身份、温暖柔和场景、干净二次元插画质量优先。",
    }


def required_identity_tokens_for(character_name):
    return list(CHARACTER_PROFILES.get(character_name, CHARACTER_PROFILES["丹"])["identity_tokens"])


def viewer_distance_for(character_name):
    if character_name in {"爱芮", "南宫", "橘福福"}:
        return "medium-close to three-quarter body framing, friendly eye contact"
    if character_name in {"星见雅", "仪玄", "叶瞬光"}:
        return "three-quarter body framing, calm distance, face clearly visible"
    return "medium shot to three-quarter body framing, quiet direct presence"


def outfit_variation_for(character_name, plan_name=None):
    profile = CHARACTER_PROFILES.get(character_name, CHARACTER_PROFILES["丹"])
    base = random.choice(OUTFIT_DIRECTIONS)
    if character_name == "丹":
        return f"{base}; vary Dan's outfit between soft casual dress, light cardigan, simple blouse, and airy uniform while keeping pale pink short hair unchanged"
    if character_name in {"星见雅", "叶瞬光"}:
        return f"{base}; sword-related items may appear as sheath, distant silhouette, or small accessory, but do not force hand-held sword"
    if character_name == "千夏":
        return f"{base}; no creator desk, no pen-and-paper theme; keep mint short hair and bow faithful to reference"
    if character_name == "席德":
        return f"{base}; add only tiny blue-violet light marks, glass candy, ribbons, or soft floral accessories"
    if character_name == "橘福福":
        return f"{base}; tiger motif should be small and readable, without fixed sect scenery"
    return f"{base}; keep {profile['color_anchor']} as the recognizable palette"
