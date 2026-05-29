from textwrap import dedent

from art_direction_options import (
    ANTI_SAFE_COMPOSITION,
    choose_action_style,
    choose_art_plan,
    propagation_profile_for,
)


CHARACTER_LOCKS = {
    "千夏": (
        "千夏：薄荷绿/浅灰绿色中短层次发，后发自然散开，轻微短发狼尾感；"
        "后顶部偏右只有一小束装饰性小揪发，绑大号薄荷绿蝴蝶结，不是马尾。"
        "厚重不对称刘海，一侧遮挡额头与部分眼部，另一侧露耳，黑色心形耳饰；粉金渐变瞳。"
        "气质是紧张但认真、敏感创作者、努力装镇定。"
    ),
    "南宫": (
        "南宫羽：黑色中短发，厚重整齐齐刘海，短直包脸侧发；"
        "高位短束状双马尾，不是长双马尾，发尾黑色渐变到高饱和粉色/玫红色。"
        "保留小呆毛、白色猫咪发夹、粉色三角发卡、科技感光环、背后机械小翅膀。"
        "气质是慵懒聪明、狡黠从容、轻微坏笑、掌控现场。"
    ),
    "爱芮": (
        "爱芮：高饱和粉色双马尾，蓬松外翘卷曲，额前明显黑色挑染刘海；"
        "两侧大体积包脸侧发，蓝粉渐变高光眼。"
        "保留黑色耳机式发饰、蝴蝶结、粉色机械小翅膀、爱心元素。"
        "气质是开朗自信的完美 Vocal，甜酷小恶魔偶像但不低幼。"
    ),
    "丹": (
        "丹：浅粉色短发，空气感厚刘海，不对称刘海，两侧包脸短发，发尾外翻；"
        "柔软羽毛感短层次发型，浅粉色头发渐变，粉紫色眼睛。"
        "可保留银白细头环、蓝银色星形发卡、耳侧轻机械模块。"
        "气质是安静温柔、略淡漠、未来圣女感，但不成熟化。"
    ),
    "星见雅": (
        "星见雅：黑色长直发，厚重整齐的齐刘海（姬发式），头顶有醒目的黑色兽耳；"
        "长发自然披散且发量丰厚，一侧常伴有明显的单股编发细节。"
        "锐利的红色眼瞳，常随身携带武士刀（太刀），保留武士风格的绳结与挂饰元素。"
        "气质是冷静沉稳、严肃认真、凛然的剑客、优雅且极具压迫感。"
        "不要短发、不要卷发、不要蓬松偶像发型，不要丢失黑色兽耳与太刀识别。"
    ),
    "仪玄": (
        "仪玄：银白色长发，发量丰厚且自然蓬松，带有轻微凌乱感，头顶有一根明显的呆毛；"
        "侧分刘海上佩戴着一个醒目的黑色波浪状/闪电状发饰。"
        "锐利且略带慵懒的金黄色/琥珀色眼瞳，成熟修长的体态，身边常伴有一只发光的黑色鸟类（灵纹乌鸦）。"
        "气质是成熟从容、慵懒自信、带着些许戏谑与游刃有余的神秘感。"
        "不要短发、不要少女化、不要过度甜美，不要丢失黑色闪电状发饰与黑色灵鸟识别。"
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
    return "fenjue_v3_social_anime_character"


def _identity_lock(character_name: str) -> str:
    names = _character_names(character_name)
    locks = " ".join(CHARACTER_LOCKS.get(name, CHARACTER_LOCKS["丹"]) for name in names)
    if _is_group(names):
        subject_rule = (
            "本次虽然保留多人能力，但当前 art direction pipeline 优先单人；如果出现多人，必须逐个锁定对应参考图身份，不允许发型、发色、发饰互换。"
        )
    else:
        subject_rule = (
            "本次是 single character only，只允许一个人物实体。不要生成其他队友、第二个人物、分身、远处小人、半透明大脸剪影或画中画重复人物。"
        )
    return dedent(f"""
    【Identity Lock / 角色锁定】
    上传图片只作为 {character_name} 的人物身份参考，不复制原图构图。
    {subject_rule}
    {locks}
    角色识别只锁头发轮廓、发色、发饰、眼睛和脸部气质；服装主色由本次视觉企划决定，不被角色默认配色支配。
    """).strip()


def _visual_direction(plan: dict) -> str:
    return dedent(f"""
    【Fenjue 3.0 / 二次元角色传播企划】
    你不是电影摄影师，也不是 AAA 概念图画师；请以社交平台头部二次元插画师的判断来设计画面。
    第一目标是停滑、点击、收藏和传播；角色人格、幻想感、情绪价值和缩略图识别优先于真实空间逻辑。
    世界从角色人格中生长出来，不是角色进入一个写实场景。

    核心情绪钩子：{plan["graphic_concept"]}。
    人格化世界：{plan["spatial_structure"]}。
    幻想传播符号：{plan["visual_device"]}。
    符号预算：本张图最多一个 primary hook symbol，再加一个 secondary support symbol；不要同时堆光环、爱心、UI、翅膀、星星、手机、耳机、漂浮物。
    构图分配：角色脸、眼睛、发型大形和上半身是第一视觉锚点；角色存在感约 55% 到 75%，背景和幻想元素只负责放大角色魅力。
    缩略图检查：手机小图里必须先读到角色是谁、她的情绪、主色记忆点和一个大幻想符号。
    """).strip()


def _official_personality_translation(character_name: str) -> str:
    profile = propagation_profile_for(character_name)
    primary_symbols = " / ".join(profile["primary_hook_symbols"])
    secondary_symbols = " / ".join(profile["secondary_support_symbols"])
    thumbnail_modes = " / ".join(profile["thumbnail_modes"])
    suppressed = "；".join(profile["suppressed_misreads"])
    return dedent(f"""
    【Official Personality Translation / 官方人格传播转译】
    本次角色不是 generic anime girl。请先遵守角色官方/项目人格核心，再把人格转译成社交平台传播画面。
    官方/项目核心：{profile["official_core"]}
    传播人格：{profile["propagation_translation"]}
    Viewer 关系：{profile["viewer_relationship"]}
    互动方式硬规则：{profile["interaction_rule"]}
    缩略图策略：{profile["thumbnail_strategy"]}
    可用缩略图类型：{thumbnail_modes}。
    Primary hook symbol 只能选一个：{primary_symbols}。
    Secondary support symbol 最多选一个：{secondary_symbols}。
    其他幻想元素必须降级为很小的背景点缀，不能同时抢画面。
    安全吸引力策略：{profile["safe_sensuality"]}
    高优先级误读惩罚：{suppressed}。
    """).strip()


def _performance(plan: dict, action: dict) -> str:
    return dedent(f"""
    【Character Appeal / 角色人格与互动】
    本次互动语言：{action["name"]}。
    角色画面表现：{action["body_silhouette"]}。
    人格驱动：{action["personality_logic"]}。
    缩略图支撑：{action["support_rule"]}。
    禁忌：{action["avoid_rule"]}。
    视觉企划原始姿态参考：{plan["body_silhouette"]}；如果它和互动语言冲突，以互动语言为准。
    角色不只是被观看，而是在和 viewer 形成关系；允许对视、靠近、通话感、偶像营业感、恋爱感和安全亲密感。
    表情必须有可传播的情绪钩子：心动、陪伴、秘密感、清爽感、梦境感、崇拜感或被角色选中的感觉。
    不要让所有角色都变成同一种大脸自拍；根据角色传播人格选择大脸型、半身型、姿态型、色块型、符号型或极简头像型。
    """).strip()


def _fashion(plan: dict) -> str:
    return dedent(f"""
    【Fashion & Character Icon / 服装与角色图标】
    服装主题：{plan["outfit_direction"]}。
    材料语言：{plan["material_language"]}。
    色彩策略：{plan["color_strategy"]}。
    服装必须服务角色人格和社交传播：轮廓要一眼记住，配色要有角色专属记忆点。
    允许更强二次元幻想设计、偶像感、恋爱感、小配件和发光装饰，但不要堆满碎件。
    头发、眼睛、发饰、领口、袖口、腰线和手部附近的装饰是高细节区；其他区域可以简化成漂亮大色块。
    """).strip()


def _rendering(plan: dict) -> str:
    return dedent(f"""
    【Rendering Layer / Pixiv-Social 完成度】
    光影行为：{plan["lighting_behavior"]}。
    top-tier social anime illustration atmosphere，Pixiv-like premium character artwork quality，clean appealing lineart，beautiful color design。
    high thumbnail impact，strong character aura，memorable color palette，dreamlike fantasy symbols，emotion-first composition。
    detail hierarchy：最高细节集中在眼睛、脸、发型大形、发饰、手部附近和主幻想符号；背景减少真实建筑细节。
    画面要像会被收藏转发的二次元角色图、头像级封面、偶像视觉图或梦境角色海报，不是电影截图、游戏 loading 图、UE5 宣传图或西式概念设定稿。
    """).strip()


def _negative() -> str:
    anti_safe = "，".join(ANTI_SAFE_COMPOSITION)
    return dedent(f"""
    【Avoid / 反安全模板】
    {anti_safe}。
    avoid cinematic realism，avoid AAA game key visual，avoid western concept art，avoid UE5 promotional render，avoid industrial hard-surface scene。
    avoid tiny character swallowed by space，avoid complicated architecture，avoid realistic photography logic，avoid gray abandoned building mood。
    avoid overrendering，avoid AI detail noise，avoid excessive texture，avoid oversharpening，avoid plastic anime look。
    avoid random decorative clutter，avoid cheap fantasy effects，avoid generic AI anime style，avoid low-quality fanservice。
    avoid extra fingers，malformed hands，extra arms，duplicated face，misaligned eyes。
    不要画面文字、英文标牌、角色名拼写、logo 或海报排版文字。
    """).strip()


def prompt_for_art_direction(character_name: str, plan: dict | None = None, action: dict | None = None) -> str:
    selected_plan = plan or choose_art_direction_plan(character_name)
    selected_action = action or choose_action_style(character_name)
    return dedent(f"""
    {_visual_direction(selected_plan)}

    {_official_personality_translation(character_name)}

    {_performance(selected_plan, selected_action)}

    {_fashion(selected_plan)}

    {_identity_lock(character_name)}

    {_rendering(selected_plan)}

    {_negative()}
    """).strip()


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
    return prompt_for_art_direction(character_name, plan, action)
