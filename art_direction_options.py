import random


OUTFIT_DIRECTIONS = [
    "reference-faithful outfit with only small fabric and accessory variation",
    "clean light-novel casual outfit, keeping the character palette recognizable",
    "soft stage outfit, simple silhouette, no complex props",
    "seasonal everyday outfit, clear color blocks, low ornament density",
    "elegant fantasy outfit, simplified layers, no weapon requirement",
    "minimal studio outfit, face and hair identity as the main focus",
]


ANTI_SAFE_COMPOSITION = []


CHARACTER_PROFILES = {
    "南宫": {
        "official_core": "黑发短双马尾，发尾粉色渐变，齐刘海，粉色眼睛，猫咪发夹，俏皮又危险的赛博少女气质。",
        "identity_tokens": ["short black twin tails with pink gradient tips", "straight blunt bangs", "pink eyes", "cat hairpin"],
        "viewer_relationship": "像在悄悄观察观众，表情聪明、轻微挑衅，但不夸张。",
        "thumbnail_strategy": "黑粉发色和猫咪小饰品必须在小图里仍然清楚。",
        "interaction_rule": "允许对视、侧身回头、轻笑；避免手指指向镜头。",
        "safe_sensuality": "保持可爱与精致，不使用成人化表达。",
        "color_anchor": "black, pink, clean white",
    },
    "爱芮": {
        "official_core": "高饱和粉色双马尾，黑色挑染刘海，明亮粉蓝眼睛，偶像感、电子感、元气感强。",
        "identity_tokens": ["vivid pink twin tails", "black streak in bangs", "pink-blue bright eyes", "idol-like cyber accessories"],
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
        "safe_sensuality": "青春清爽，不使用成人化姿态。",
        "color_anchor": "mint, pale gold, soft white",
    },
    "丹": {
        "official_core": "浅粉短发，空气感碎刘海，粉紫眼睛，安静、透明。",
        "identity_tokens": ["pale pink short layered hair", "airy uneven bangs", "pink-purple eyes", "small silver-blue hair accessory"],
        "viewer_relationship": "像从安静梦境里看向观众，神秘但亲近。",
        "thumbnail_strategy": "浅粉短发和透明感眼睛必须稳定，服装可以变化。",
        "interaction_rule": "允许站立、坐姿、侧脸、轻微回头；避免固定同一套服装。",
        "safe_sensuality": "以清冷和梦境感为主，保持干净克制。",
        "color_anchor": "pale pink, violet, silver blue",
    },
    "星见雅": {
        "official_core": "黑色长直发，姬发式齐刘海，尖锐黑色兽耳，红色眼睛，冷静、锋利、克制。",
        "identity_tokens": ["long straight black hair", "hime-cut blunt bangs", "sharp black animal ears", "red eyes"],
        "viewer_relationship": "像冷静地看穿观众，距离感强但角色存在感清楚。",
        "thumbnail_strategy": "黑长直、黑兽耳、红眼是核心",
        "interaction_rule": "允许刀鞘、红色线条、远处剑影；避免复杂手部持物。",
        "safe_sensuality": "冷感优雅，不强调暴露。",
        "color_anchor": "black, red, white",
    },
    "仪玄": {
        "official_core": "银白长发，柔软呆毛，黑色雷纹或波纹发饰，金色眼睛，成熟安静。",
        "identity_tokens": ["long silver-white hair", "small ahoge", "black wave hair ornament", "golden eyes"],
        "viewer_relationship": "像平静地邀请观众进入仪式，沉稳、有神秘感。",
        "thumbnail_strategy": "银白长发和金眼必须清晰。",
        "interaction_rule": "允许手在胸前、袖摆自然下垂、侧身凝视；避免复杂法阵手势。",
        "safe_sensuality": "成熟优雅即可，不走成人化描述。",
        "color_anchor": "silver white, black, gold",
    },
    "叶瞬光": {
        "official_core": "暖棕长发，棕色兽耳，蓬松棕色尾巴，红色眼睛，红色发带或花饰，温柔可靠。",
        "identity_tokens": ["warm brown long hair", "brown animal ears", "fluffy brown tail", "red eyes", "red ribbon or flower accessory"],
        "viewer_relationship": "像温柔地回头照看观众，亲和但有守护感。",
        "thumbnail_strategy": "暖棕发色、棕色兽耳和尾巴要稳定，不要变成黑发红眼冷剑士。",
        "interaction_rule": "避免固定宗门或山门元素。",
        "safe_sensuality": "温柔端正，保持清爽可靠。",
        "color_anchor": "warm brown, red, ivory",
    },
    "席德": {
        "official_core": "银灰短发或中短发，蓝紫色眼睛，机械少女与危险纯真并存，带轻微电弧、线路或旧式机械伙伴暗示。",
        "identity_tokens": ["silver-gray short hair", "blue-violet eyes", "mechanical girl details", "tiny electric arcs"],
        "viewer_relationship": "像天真地向观众展示危险实验，表情无辜但气氛有压迫感。",
        "thumbnail_strategy": "银灰发、蓝紫电光。",
        "interaction_rule": "避免复杂机械手和多手结构。",
        "safe_sensuality": "以异质感和可爱危险感为主，保持干净表达。",
        "color_anchor": "silver gray, blue violet, black",
    },
    "橘福福": {
        "official_core": "橘色短发，明亮金橙眼睛，活泼、可靠、热烈的少女气质。",
        "identity_tokens": ["short orange hair", "golden-orange eyes", "tiger-themed accessory", "warm lively expression"],
        "viewer_relationship": "像元气地把观众拉进热闹场面，亲近、明亮、行动感强。",
        "thumbnail_strategy": "橘发、金橙眼，避免被背景同化。",
        "interaction_rule": "允许奔跑、回头笑、舞台动作；避免固定宗门或山门元素。",
        "safe_sensuality": "明快可爱，不走低俗表达。",
        "color_anchor": "orange, gold, white",
    },
}


ART_DIRECTION_PLANS = [
    {
        "name": "clean_studio_portrait",
        "graphic_concept": "干净摄影棚感，人物是唯一视觉中心，背景只保留柔和色块。",
        "spatial_structure": "浅色无缝背景或简单布景，少量投影，不堆道具。",
        "visual_device": "一块柔和主色背景和一条轻微轮廓光。",
        "body_silhouette": "三分之二身或膝上构图，身体完整自然，双手可见且动作简单。",
        "outfit_direction": "minimal studio outfit, face and hair identity as the main focus",
        "material_language": "柔软布料、干净线条、少量金属或发饰点缀。",
        "color_strategy": "背景用低饱和中性色，角色主色清楚但不刺眼。",
        "lighting_behavior": "柔和大面积灯光，脸部和眼睛清晰。",
        "tags": ["studio", "simple_background", "soft_light"],
    },
    {
        "name": "summer_window_room",
        "graphic_concept": "夏日窗边二次元插画，空气感和角色表情优先。",
        "spatial_structure": "窗、窗帘、桌边或地面光斑，空间元素控制在三种以内。",
        "visual_device": "窗光形成清晰方向线，背景不过度写实。",
        "body_silhouette": "坐姿或站姿都可，三分之二身，手自然放在膝边或身侧。",
        "outfit_direction": "clean light-novel casual outfit, keeping the character palette recognizable",
        "material_language": "棉布、薄纱、发带、小饰品。",
        "color_strategy": "清透蓝白或薄荷色背景，角色主色保持明确。",
        "lighting_behavior": "明亮窗光，软阴影，避免强烈戏剧光。",
        "tags": ["window", "summer", "daily"],
    },
    {
        "name": "rainy_city_walk",
        "graphic_concept": "雨后城市散步，干净反光和情绪氛围服务角色。",
        "spatial_structure": "简化街角、湿地反光、远处灯牌虚化。",
        "visual_device": "地面反光把视线引向角色脸部。",
        "body_silhouette": "行走或回头站立，双手不做复杂持物动作。",
        "outfit_direction": "seasonal everyday outfit, clear color blocks, low ornament density",
        "material_language": "湿润地面、轻薄外套、清晰发丝。",
        "color_strategy": "冷色背景配一个角色专属暖色焦点。",
        "lighting_behavior": "雨后柔光和远处霓虹，只做轻微点缀。",
        "tags": ["rain", "city", "reflection"],
    },
    {
        "name": "sunset_train_window",
        "graphic_concept": "黄昏列车窗边，安静、亲近、适合角色对视。",
        "spatial_structure": "列车座位、窗框、远处夕阳，不塞满乘客或广告。",
        "visual_device": "窗框把角色脸部框住。",
        "body_silhouette": "坐姿三分之二身，手自然放在座位或衣摆上。",
        "outfit_direction": "clean light-novel casual outfit, keeping the character palette recognizable",
        "material_language": "布料、玻璃、柔和逆光发丝。",
        "color_strategy": "金橙夕阳配角色本色，避免整张图变成单一橙色。",
        "lighting_behavior": "夕阳边缘光，脸部仍然明亮清楚。",
        "tags": ["train", "sunset", "quiet"],
    },
    {
        "name": "flower_glasshouse",
        "graphic_concept": "玻璃花房，花只做气氛，不抢人物身份。",
        "spatial_structure": "玻璃墙、少量植物、远景光斑。",
        "visual_device": "花枝形成外框，角色脸部保持无遮挡。",
        "body_silhouette": "站姿或坐姿，半身以上到膝上之间，手部简单。",
        "outfit_direction": "elegant fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "透明玻璃、柔软布料、少量花饰。",
        "color_strategy": "背景浅绿浅白，角色主色作为记忆点。",
        "lighting_behavior": "扩散自然光，低噪点，清晰线稿。",
        "tags": ["glasshouse", "flower", "natural_light"],
    },
    {
        "name": "night_vending_light",
        "graphic_concept": "夜晚自动贩卖机附近的轻剧情感，简单但有颜色记忆。",
        "spatial_structure": "一台发光机器、简化墙面、少量地面反光。",
        "visual_device": "机器光照亮角色侧脸。",
        "body_silhouette": "站姿三分之二身，手放口袋、身侧或轻扶衣摆。",
        "outfit_direction": "seasonal everyday outfit, clear color blocks, low ornament density",
        "material_language": "塑料光、布料、清晰发丝。",
        "color_strategy": "夜色背景加角色专属色光，避免高饱和乱闪。",
        "lighting_behavior": "低对比夜光，脸部不能黑。",
        "tags": ["night", "vending", "street"],
    },
    {
        "name": "soft_fantasy_stage",
        "graphic_concept": "轻幻想舞台，不是游戏宣传图，角色像插画主角。",
        "spatial_structure": "简单圆形舞台、帘幕或光环形构图。",
        "visual_device": "一个大几何光环强化缩略图识别。",
        "body_silhouette": "站姿或轻微转身，双手自然，不做复杂武器动作。",
        "outfit_direction": "soft stage outfit, simple silhouette, no complex props",
        "material_language": "布料、丝带、少量发光饰品。",
        "color_strategy": "单一背景主色加角色对比色，避免纯大红大粉铺满画面。",
        "lighting_behavior": "柔和舞台灯，眼睛和脸是最高对比区域。",
        "tags": ["stage", "fantasy", "graphic"],
    },
    {
        "name": "quiet_mechanical_room",
        "graphic_concept": "安静机械房间，机械元素是背景秩序，不抢人物。",
        "spatial_structure": "简化控制台、圆形灯、少量线缆和墙面模块。",
        "visual_device": "圆形冷光从背后勾出角色轮廓。",
        "body_silhouette": "站姿或坐姿，双手自然可见，不出现复杂机械义肢。",
        "outfit_direction": "reference-faithful outfit with only small fabric and accessory variation",
        "material_language": "磨砂金属、软布、干净电光。",
        "color_strategy": "冷灰蓝背景配角色专属暖色或电光色。",
        "lighting_behavior": "冷色背光加柔和正面补光。",
        "tags": ["mechanical", "cool_light", "simple_room"],
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
    "席德": ["quiet_mechanical_room", "night_vending_light", "clean_studio_portrait"],
    "橘福福": ["soft_fantasy_stage", "sunset_train_window", "clean_studio_portrait"],
    "叶瞬光": ["summer_window_room", "sunset_train_window", "flower_glasshouse"],
    "千夏": ["summer_window_room", "aquarium_blue_light", "clean_studio_portrait"],
    "丹": ["aquarium_blue_light", "quiet_mechanical_room", "clean_studio_portrait"],
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
        overlap = len(_tags_of(item) & recent)
        score -= overlap * 0.6
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
        "propagation_translation": "稳定角色身份、清晰构图、干净二次元插画质量优先。",
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
        return f"{base}; vary Dan's outfit between soft future casual, light dress, simple jacket, and airy uniform while keeping pale pink short hair unchanged"
    if character_name in {"星见雅", "叶瞬光"}:
        return f"{base}; sword-related items may appear as sheath, distant silhouette, or small accessory, but do not force hand-held sword"
    if character_name in {"千夏"}:
        return f"{base}; no creator desk, no pen-and-paper theme; keep mint short hair and bow faithful to reference"
    if character_name in {"席德"}:
        return f"{base}; add only small mechanical accessories or light modules, not extra limbs"
    if character_name in {"橘福福"}:
        return f"{base}; tiger motif should be small and readable, without fixed sect scenery"
    return f"{base}; keep {profile['color_anchor']} as the recognizable palette"
