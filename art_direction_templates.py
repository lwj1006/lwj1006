from textwrap import dedent

from art_direction_options import (
    ANTI_SAFE_COMPOSITION,
    choose_action_style,
    choose_art_plan,
    outfit_variation_for,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
    hard_negative_tokens_for,
    strict_identity_block_for,
    outfit_lock_for,
)


CHARACTER_LOCKS = {
    "千夏": (
        "千夏：严格贴合参考图身份。薄荷绿/浅灰绿色中短层次发，后发自然散开，轻微短发狼尾感；"
        "后顶部偏右只有一小束装饰性小揪发，绑大号薄荷绿蝴蝶结，绝不是双马尾、长马尾或普通短发。"
        "厚重不对称刘海，一侧遮挡额头与部分眼部，另一侧露耳，脸侧发束贴脸并带轻微外翘；黑色心形耳饰；粉金渐变瞳。"
        "气质是紧张但认真、清透、努力装镇定的青春陪伴感。不要用学习记录类道具来定义她。"
    ),
    "南宫": (
        "南宫羽：黑色中短发，厚重整齐齐刘海，短直包脸侧发；"
        "高位短束状双马尾，不是长双马尾，发尾黑色渐变到高饱和粉色/玫红色。"
        "保留小呆毛、白色猫咪发夹、粉色三角发卡；科技感光环或背后小型机械光片只是可选符号，不要求每张都出现背后结构。"
        "气质是慵懒聪明、狡黠从容、轻微坏笑、掌控现场。"
    ),
    "爱芮": (
        "爱芮：高饱和粉色双马尾，蓬松外翘卷曲，额前明显黑色挑染刘海；"
        "两侧大体积包脸侧发，蓝粉渐变高光眼。"
        "保留黑色耳机式发饰、蝴蝶结和爱心元素；粉色机械光片或舞台背光只是可选符号，不要求每张都出现背后结构。"
        "气质是开朗自信的完美 Vocal，甜酷小恶魔偶像但不低幼。"
    ),
    "丹": (
        "丹：浅粉色短发，空气感厚刘海，不对称刘海，两侧包脸短发，发尾外翻；"
        "柔软羽毛感短层次发型，浅粉色头发渐变，粉紫色眼睛。"
        "银白细头环、蓝银色星形发卡、耳侧轻机械模块或透明蓝银小光片至少出现一个，作为轻未来识别件。"
        "气质是安静温柔、略淡漠、未来感与透明感，不把服装固定成同一套圣女制服。"
    ),
    "星见雅": (
        "星见雅：黑色长直发，厚重整齐的齐刘海（姬发式），头顶有醒目的黑色兽耳；"
        "长发自然披散且发量丰厚，一侧常伴有明显的单股编发细节。"
        "锐利的红色眼瞳，武士风格的绳结、挂饰、红色刀线、刀鞘剪影或收刀后的气场可以作为剑客锚点；实体太刀不是每张必须出现。"
        "气质是冷静沉稳、严肃认真、凛然的剑客、优雅且极具压迫感。"
        "不要短发、不要卷发、不要蓬松偶像发型；黑色兽耳识别要清楚，剑客锚点不能被普通饰品替代。"
    ),
    "仪玄": (
        "仪玄：银白色长发，发量丰厚且自然蓬松，带有轻微凌乱感，头顶有一根明显的呆毛；"
        "侧分刘海上佩戴着一个醒目的黑色波浪状/闪电状发饰。"
        "锐利且略带慵懒的金黄色/琥珀色眼瞳，成熟修长的体态；黑色羽影、灵鸟剪影或金色术光可以作为可选神秘符号。"
        "气质是成熟从容、慵懒自信、带着些许戏谑与游刃有余的神秘感。"
        "不要短发、不要少女化、不要过度甜美；黑色闪电状发饰识别要清楚，但不要求每张都出现实体灵鸟。"
    ),
    "叶瞬光": (
        "叶瞬光：温柔师姐型守护少女，气质清亮、沉稳、可靠，带承担型保护者气场。"
        "必须保留暖棕长发、棕褐兽耳、大棕尾、红绳或红色发饰、白金系清爽服装；剑、剑光、剑穗可以出现，但不是每张必须出现，红绳、发带、衣摆方向线、柔和守护姿态也能承担识别锚点。"
        "她不是纯冷酷杀手；表情可以温柔、垂眸、回身守望，动作可以收剑、护住身后或只是安静引路。"
    ),
    "席德": (
        "席德：天真危险的机械改造少女，核心是机械、改造、老席德、电弧、花朵反差和不按常识理解世界的童真逻辑。"
        "必须保留蓝紫电光、电路纹、机械零件、驾驶舱/机库气息或大型机械伙伴痕迹。"
        "表情可以纯真，但动作和画面装置带危险机械感；不要变成普通军服少女或纯冷酷机器人。"
    ),
    "橘福福": (
        "橘福福：虎系元气师姐，火属性暖光、虎虎生风、明亮能打的亲近感是核心。"
        "必须保留虎系元素、火属性暖光、虎威或虎形装置；场景应更自由，可以是节日街景、摄影棚、清爽户外或幻想色块。"
        "她不是普通猫娘；要明亮、热情、可爱但能打，像会招呼 viewer 去吃饭又立刻冲出去行动。"
    ),
}



def _character_names(character_name: str) -> list[str]:
    names = [name.strip() for name in character_name.replace("，", "、").split("、") if name.strip()]
    return names or ["丹"]


def _is_group(names: list[str]) -> bool:
    return len(names) >= 2


def choose_art_direction_plan(character_name: str | None = None) -> dict:
    return choose_art_plan(character_name)


def prompt_template_name(template_index: int = 0) -> str:
    return "fenjue_v4_natural_language_compact"


def _compact_prompt(text: str) -> str:
    lines = [line.strip() for line in str(text).splitlines()]
    return "\n".join(line for line in lines if line)


def _sentence_join(parts: list[str]) -> str:
    cleaned = []
    for part in parts:
        part = " ".join(str(part).split())
        if part:
            cleaned.append(part)
    return " ".join(cleaned)


def _safe_get(data: dict, key: str, default: str = "") -> str:
    value = data.get(key, default) if isinstance(data, dict) else default
    return str(value).strip()


def _identity_text(character_name: str) -> str:
    names = _character_names(character_name)
    locks = " ".join(CHARACTER_LOCKS.get(name, CHARACTER_LOCKS["丹"]) for name in names)

    required_tokens = [
        token
        for name in names
        for token in required_identity_tokens_for(name)
    ]
    strict_tokens = [
        token
        for name in names
        for token in strict_identity_block_for(name)
    ]

    subject_rule = (
        "Single character only; do not create extra teammates, clones, distant small people, repeated faces, or picture-in-picture copies."
        if not _is_group(names)
        else "If multiple characters appear, keep each uploaded reference identity separate and never swap hairstyle, hair color, accessories, or symbols."
    )

    token_line = ""
    if required_tokens:
        token_line += " Required identity tokens: " + "; ".join(required_tokens) + "."
    if strict_tokens:
        token_line += " Strict correction tokens: " + "; ".join(strict_tokens) + "."

    return _sentence_join([
        f"Use the uploaded images only as identity reference for {character_name}, not as composition reference.",
        subject_rule,
        locks,
        token_line,
        "Character identity has higher priority than outfit, scene, camera angle, and random visual theme.",
    ])


def _personality_text(character_name: str) -> str:
    profile = propagation_profile_for(character_name)
    primary_symbols = " / ".join(profile.get("primary_hook_symbols", []))
    secondary_symbols = " / ".join(profile.get("secondary_support_symbols", []))
    suppressed = " / ".join(profile.get("suppressed_misreads", []))

    return _sentence_join([
        f"Official personality core: {profile.get('official_core', '')}",
        f"Social illustration translation: {profile.get('propagation_translation', '')}",
        f"Viewer relationship: {profile.get('viewer_relationship', '')}",
        f"Interaction rule: {profile.get('interaction_rule', '')}",
        f"Viewer distance: {viewer_distance_for(character_name)}",
        f"Use only one primary hook symbol from: {primary_symbols}." if primary_symbols else "",
        f"Use at most one secondary support symbol from: {secondary_symbols}." if secondary_symbols else "",
        f"Avoid these misreads: {suppressed}." if suppressed else "",
    ])


def _outfit_text(character_name: str, plan: dict) -> str:
    outfit_variation = outfit_variation_for(character_name, _safe_get(plan, "name"))
    outfit_lock = outfit_lock_for(character_name)

    return _sentence_join([
        f"Outfit direction: {_safe_get(plan, 'outfit_direction', 'clean character-focused outfit')}.",
        f"This outfit variation: {outfit_variation}." if outfit_variation else "Do not repeat the exact same clothing shape from the previous image.",
        f"Mandatory outfit lock: {outfit_lock}." if outfit_lock else "",
        f"Material language: {_safe_get(plan, 'material_language', 'clean fabric, simple accessories, clear silhouette')}.",
        f"Color strategy: {_safe_get(plan, 'color_strategy', 'clear character colors with a clean supporting background')}.",
        "Keep hair, eyes, face, hair accessories, neckline, shoulders, waistline, and the main character symbol as the most detailed areas.",
    ])


def _action_text(character_name: str, plan: dict, action: dict) -> str:
    return _sentence_join([
        f"Action language: {_safe_get(action, 'name', 'natural character pose')}.",
        f"Body performance: {_safe_get(action, 'body_silhouette', _safe_get(plan, 'body_silhouette', 'clear knee-up or three-quarter character pose'))}.",
        f"Personality logic: {_safe_get(action, 'personality_logic', '')}.",
        f"Support rule: {_safe_get(action, 'support_rule', '')}.",
        f"Action avoid rule: {_safe_get(action, 'avoid_rule', '')}.",
        "Hands should be simple, readable, and low-risk: near the body, lightly holding one prop, touching hair/accessory, hidden by sleeve, or naturally relaxed.",
    ])


def _scene_text(plan: dict, camera_angle: str = "eye-level medium shot") -> str:
    return _sentence_join([
        f"Camera angle: {camera_angle}.",
        f"Scene concept: {_safe_get(plan, 'graphic_concept', 'clean social anime character illustration')}.",
        f"Scene structure: {_safe_get(plan, 'spatial_structure', 'simple background that supports the character')}.",
        f"Visual device: {_safe_get(plan, 'visual_device', 'one clear visual hook only')}.",
        "The world should grow from the character personality, not from realistic location logic.",
        "The character should occupy strong visual presence, roughly knee-up to three-quarter framing unless the selected plan clearly needs otherwise.",
    ])


def _rendering_text(plan: dict) -> str:
    return _sentence_join([
        "High-quality anime style illustration, crisp cel shading, vibrant and clean colors, precise lineart, polished character design, clean commercial illustration finish.",
        "Top-tier social anime illustration, Pixiv-like premium character artwork, high thumbnail impact, strong character aura, memorable color palette.",
        f"Lighting: {_safe_get(plan, 'lighting_behavior', 'soft clear light on the face and eyes')}.",
        "Detail hierarchy: eyes, face, hairstyle silhouette, hair accessories, neckline, waistline, and the single main fantasy symbol first; hands, feet, and background stay simplified.",
        "Avoid heavy oil painting, 3D render, cinematic realism, AAA concept art, industrial hard-surface scene, over-detailed architecture, washed-out fog, and noisy AI texture.",
    ])


def _negative_text(character_name: str = "") -> str:
    anti_safe = ", ".join(ANTI_SAFE_COMPOSITION)
    hard_negative = ", ".join(hard_negative_tokens_for(character_name)) if character_name else ""

    return _sentence_join([
        f"Avoid: {anti_safe}." if anti_safe else "",
        f"Character-specific avoid: {hard_negative}." if hard_negative else "",
        "Avoid extra fingers, missing fingers, fused fingers, broken hands, extra arms, extra feet, twisted ankles, duplicated face, misaligned eyes, incorrect character features, cluttered background, text, logos, signs, posters, and character-name typography.",
    ])


def build_master_prompt(
    character_details: str,
    scene_context: str,
    camera_angle: str = "eye-level medium shot",
    outfit_context: str | None = None,
    action_context: str | None = None,
    mood_context: str | None = None,
    negative_context: str | None = None,
) -> str:
    """
    Natural-language master prompt builder.

    This function avoids long tag piles and director-manual style rules.
    It keeps the prompt readable while preserving the minimum identity, outfit,
    action, scene, rendering, and negative-control layers.
    """
    style_base = (
        "High-quality anime style illustration, crisp cel shading, vibrant and clean colors, "
        "precise lineart, polished character design, clean commercial illustration finish."
    )
    character_block = f"The central subject is {character_details}. Keep the character identity clear and consistent."
    outfit_block = f"The outfit is {outfit_context}." if outfit_context else ""
    action_block = f"The character is {action_context}." if action_context else ""
    mood_block = f"The mood is {mood_context}." if mood_context else ""
    direction_block = f"Camera angle: {camera_angle}. {scene_context}"
    negative_block = (
        f"Avoid: {negative_context}."
        if negative_context
        else "Avoid messy composition, extra limbs, distorted hands, incorrect character features, overly realistic 3D rendering, heavy oil painting texture, cluttered background, text, logos, and posters."
    )
    return _sentence_join([style_base, character_block, outfit_block, action_block, mood_block, direction_block, negative_block])


def prompt_for_art_direction(character_name: str, plan: dict | None = None, action: dict | None = None) -> str:
    selected_plan = plan or choose_art_direction_plan(character_name)
    selected_action = action or choose_action_style(character_name)

    character_details = _sentence_join([
        _identity_text(character_name),
        _personality_text(character_name),
    ])
    outfit_context = _outfit_text(character_name, selected_plan)
    action_context = _action_text(character_name, selected_plan, selected_action)
    scene_context = _scene_text(selected_plan, camera_angle="eye-level medium shot")
    mood_context = _sentence_join([
        _rendering_text(selected_plan),
        "Composition should be character-first, clean, collectible, mobile-friendly, and easy to read as a thumbnail.",
    ])
    negative_context = _negative_text(character_name)

    return build_master_prompt(
        character_details=character_details,
        scene_context=scene_context,
        camera_angle="eye-level medium shot",
        outfit_context=outfit_context,
        action_context=action_context,
        mood_context=mood_context,
        negative_context=negative_context,
    )


def prompt_for_theme(
    theme: str = "",
    scene: str = "",
    pose: str | None = None,
    lighting: str = "",
    mood: str = "",
    template_index: int = 0,
    character_name: str = "丹",
    concept: str | None = None,
) -> str:
    plan = choose_art_direction_plan(character_name)
    action = choose_action_style(character_name)
    if scene:
        plan = dict(plan)
        plan["spatial_structure"] = scene
    if theme:
        plan = dict(plan)
        plan["outfit_direction"] = theme
    if concept:
        plan = dict(plan)
        plan["graphic_concept"] = concept
    if pose:
        action = dict(action)
        action["body_silhouette"] = pose
    if lighting:
        plan = dict(plan)
        plan["lighting_behavior"] = lighting
    if mood:
        plan = dict(plan)
        plan["color_strategy"] = mood
    return prompt_for_art_direction(character_name, plan, action)
