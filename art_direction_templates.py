from textwrap import dedent

from art_direction_options import (
    ANTI_SAFE_COMPOSITION,
    choose_action_style,
    choose_art_plan,
    outfit_variation_for,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
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
        "叶瞬光：云岿山温柔师姐型执剑少女，气质清亮、沉稳、可靠，带承担型保护者气场。"
        "必须保留云岿山修行者气质；剑、剑光、剑穗可以出现，但不是每张必须出现，符纹、山风、云气、石阶、红绳或护人姿态也能承担识别锚点。"
        "她不是纯冷酷杀手；表情可以温柔、垂眸、回身守望，动作可以收剑、护住身后或只是安静引路。"
    ),
    "席德": (
        "席德：天真危险的机械改造少女，核心是机械、改造、老席德、电弧、花朵反差和不按常识理解世界的童真逻辑。"
        "必须保留蓝紫电光、电路纹、机械零件、驾驶舱/机库气息或大型机械伙伴痕迹。"
        "表情可以纯真，但动作和画面装置带危险机械感；不要变成普通军服少女或纯冷酷机器人。"
    ),
    "橘福福": (
        "橘福福：云岿山虎系元气师姐，火属性击破、虎虎生风、猛虎伏魔感是核心。"
        "必须保留虎系元素、火属性暖光、云岿山武修气质、虎威或虎形装置/伏魔符纸。"
        "她不是普通猫娘；要明亮、热情、可爱但能打，像会招呼 viewer 去吃饭又立刻冲出去伏魔。"
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


def _compact_prompt(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def _identity_lock(character_name: str) -> str:
    names = _character_names(character_name)
    locks = " ".join(CHARACTER_LOCKS.get(name, CHARACTER_LOCKS["丹"]) for name in names)
    required_tokens = [
        token
        for name in names
        for token in required_identity_tokens_for(name)
    ]
    required_line = ""
    if required_tokens:
        required_line = (
            "\n【Non-negotiable Identity Tokens / 不可协商身份锚点】\n"
            f"本角色必须同时满足这些识别 token：{'；'.join(required_tokens)}。\n"
            "这些 token 的优先级高于服装主题、场景主题、背景符号、构图企划和本轮随机变化。"
        )
    if _is_group(names):
        subject_rule = (
            "本次虽然保留多人能力，但当前 art direction pipeline 优先单人；如果出现多人，必须逐个锁定对应参考图身份，不允许发型、发色、发饰互换。"
        )
    else:
        subject_rule = (
            "本次是 single character only，只允许一个人物实体。不要生成其他队友、第二个人物、分身、远处小人、半透明大脸剪影或画中画重复人物。"
        )
    return _compact_prompt(dedent(f"""
    【Identity Lock / 角色锁定】
    上传图片只作为 {character_name} 的人物身份参考，不复制原图构图。
    {subject_rule}
    {locks}
    {required_line}
    角色身份优先级高于服装主题、场景主题和视觉企划。服装可以变化，但不能改变头发轮廓、发色、发饰、眼睛、核心符号和人格气质。
    """))


def _visual_direction(plan: dict) -> str:
    return _compact_prompt(dedent(f"""
    闭嘴画图不要评论
    【Fenjue 3.0 / 二次元角色传播企划】
    你不是电影摄影师，也不是 AAA 概念图画师；请以社交平台头部二次元插画师的判断来设计画面。
    第一目标是停滑、点击、收藏和传播；角色人格、幻想感、情绪价值和缩略图识别优先于真实空间逻辑。
    世界从角色人格中生长出来，不是角色进入一个写实场景。

    核心情绪钩子：{plan["graphic_concept"]}。
    人格化世界：{plan["spatial_structure"]}。
    幻想传播符号：{plan["visual_device"]}。
    符号预算：本张图最多一个 primary hook symbol，再加一个 secondary support symbol；不要同时堆光环、爱心、UI、背后结构、星星、手持设备、耳机、漂浮物。
    构图分配：角色脸、眼睛、发型大形、肩线、腰线和膝上姿态是第一视觉锚点；角色存在感约 55% 到 75%，背景和幻想元素只负责放大角色魅力。避免连续生成纯大脸或过近裁切。
    缩略图检查：小图里优先读到角色是谁、她的情绪、主色记忆点和一个大幻想符号。
    """))


def _official_personality_translation(character_name: str) -> str:
    profile = propagation_profile_for(character_name)
    viewer_distance = viewer_distance_for(character_name)
    primary_symbols = " / ".join(profile["primary_hook_symbols"])
    secondary_symbols = " / ".join(profile["secondary_support_symbols"])
    thumbnail_modes = " / ".join(profile["thumbnail_modes"])
    suppressed = "；".join(profile["suppressed_misreads"])
    return _compact_prompt(dedent(f"""
    【Official Personality Translation / 官方人格传播转译】
    本次角色不是 generic anime girl。请先遵守角色官方/项目人格核心，再把人格转译成社交平台传播画面。
    官方/项目核心：{profile["official_core"]}
    传播人格：{profile["propagation_translation"]}
    Viewer 关系：{profile["viewer_relationship"]}
    Viewer distance：{viewer_distance}
    互动方式硬规则：{profile["interaction_rule"]}
    缩略图策略：{profile["thumbnail_strategy"]}
    可用缩略图类型：{thumbnail_modes}。
    Primary hook symbol 只能选一个：{primary_symbols}。
    Secondary support symbol 最多选一个：{secondary_symbols}。
    其他幻想元素降级为很小的背景点缀，不能同时抢画面。
    安全吸引力策略：{profile["safe_sensuality"]}
    高优先级误读惩罚：{suppressed}。
    """))


def _performance(character_name: str, plan: dict, action: dict) -> str:
    viewer_distance = viewer_distance_for(character_name)
    return _compact_prompt(dedent(f"""
    【Character Appeal / 角色人格与互动】
    本次互动语言：{action["name"]}。
    角色画面表现：{action["body_silhouette"]}。
    人格驱动：{action["personality_logic"]}。
    缩略图支撑：{action["support_rule"]}。
    禁忌：{action["avoid_rule"]}。
    Viewer distance 执行：{viewer_distance}
    视觉企划原始姿态参考：{plan["body_silhouette"]}；如果它和互动语言冲突，以互动语言为准。
    角色不只是被观看，而是在和 viewer 形成关系；互动距离必须服从本角色的 Viewer distance，不要把所有角色都拉成贴脸亲密营业。
    表情需要有可传播的情绪钩子：心动、陪伴、秘密感、清爽感、梦境感、崇拜感或被角色选中的感觉。
    不要让所有角色都变成同一种大脸自拍；根据角色传播人格选择膝上型、三分之二身型、姿态型、色块型、符号型或极简头像型。
    """))


def _anatomy_control() -> str:
    return _compact_prompt(dedent("""
    【Hand & Foot Control / 手脚稳定】
    手和脚不是本张图的卖点，除非动作明确需要，否则让手保持简单、自然、低风险。
    可见手部优先采用：手指自然并拢、轻握小道具、手扶耳机、手放胸前、手藏进袖口、手在身体侧边或被衣袖/道具部分遮挡。
    避免手指指向屏幕、手指指向 viewer、手掌贴近镜头、广角大手、复杂手势、双手交叉成团、手指张开过大、手指被发丝或饰品切碎。
    如果需要互动感，用眼神、表情、耳机、麦克风、小道具和身体朝向完成，不使用手机，也不要用食指戳向画面。
    如果角色有剑客或执剑设定，优先把剑意转译为腰侧小配件、红色线状光轨、剑穗、符纹、衣摆方向线、背景剪影或收刀后的气场；不要强制让手握剑、拔剑、持剑指向画面。
    每只可见手保持清楚的五指结构；不要额外手、缺失手、六指七指、融合手指、断指、反向拇指、畸形指节。
    如果画到脚或鞋，双脚要有明确落点和方向；避免多余脚、缺失脚、悬空脚、鞋子融合、脚踝扭曲。
    优先保证脸、眼睛、发型和角色轮廓；手脚不清楚时宁可简化或遮挡，不要强行展示复杂细节。
    """))


def _fashion(character_name: str, plan: dict) -> str:
    outfit_variation = outfit_variation_for(character_name, plan["name"])
    outfit_variation_line = (
        f"本次服装变体：{outfit_variation}。"
        if outfit_variation
        else "本次服装变体：跟随服装主题，但不要重复上一张的具体衣形。"
    )
    return _compact_prompt(dedent(f"""
    【Fashion & Character Icon / 服装与角色图标】
    服装主题：{plan["outfit_direction"]}。
    {outfit_variation_line}
    材料语言：{plan["material_language"]}。
    色彩策略：{plan["color_strategy"]}。
    服装服务角色人格和社交传播：轮廓要一眼记住，配色要有角色专属记忆点。
    允许更强二次元幻想设计、偶像感、恋爱感、小配件和发光装饰，但不要堆满碎件。
    头发、眼睛、发饰、领口、袖口和腰线是高细节区；手部附近只保留少量清楚装饰，避免让手部结构变复杂。
    """))


def _rendering(plan: dict) -> str:
    return _compact_prompt(dedent(f"""
    【Rendering Layer / Pixiv-Social 完成度】
    光影行为：{plan["lighting_behavior"]}。
    top-tier social anime illustration atmosphere，Pixiv-like premium character artwork quality，clean appealing lineart，beautiful color design。
    high thumbnail impact，strong character aura，memorable color palette，dreamlike fantasy symbols，emotion-first composition。
    画风融合：轻量手绘感二次元插画、轻小说插画美术、柔和淡彩但不发白、干净动漫线稿、纤细草稿感轮廓线、柔和扁平化配色。
    线稿优先：以清爽线条、空气感轮廓和明确颜色分区表达角色，不追求厚重材质、3D质感、油画笔触或半写实皮肤。
    色彩纪律：保持淡彩氛围，但角色主色、服装主色和视觉重点颜色必须清楚；避免整体低饱和雾化、画面发白、主色被冲淡、高饱和霓虹糖果色和过强对比。
    背景色纪律：背景不能直接铺满角色头发、发饰、服装边线或瞳色的同色相高饱和色；尤其避免整张背景变成高饱和粉色、洋红、紫红、荧光蓝或角色主色。背景应使用米白、浅灰、雾蓝、奶油色、低饱和互补色或有明度差的柔和渐变来托出人物。
    移动端肖像语法：允许亲近的竖图壁纸感、柔和自然光、金色时段边缘光、脸部强焦点、干净留白和轻微背景虚化；但不要强制极端大头裁切，不要手伸向镜头，不要只剩头肩。
    detail hierarchy：最高细节集中在眼睛、脸、发型大形、发饰、领口、腰线和主幻想符号；手脚保持清楚但简化，背景减少真实建筑细节。
    画面要像会被收藏转发的二次元角色图、头像级封面、偶像视觉图、轻小说封面或梦境角色海报，不是电影截图、游戏 loading 图、UE5 宣传图或西式概念设定稿。
    """))


def _negative() -> str:
    anti_safe = "，".join(ANTI_SAFE_COMPOSITION)
    return _compact_prompt(dedent(f"""
    【Avoid / 反安全模板】
    {anti_safe}。
    avoid cinematic realism，avoid AAA game key visual，avoid western concept art，avoid UE5 promotional render，avoid industrial hard-surface scene。
    avoid tiny character swallowed by space，avoid complicated architecture，avoid realistic photography logic，avoid gray abandoned building mood。
    avoid overrendering，avoid AI detail noise，avoid excessive texture，avoid oversharpening，avoid plastic anime look。
    avoid random decorative clutter，avoid cheap fantasy effects，avoid generic AI anime style，avoid low-quality fanservice。
    avoid semi-realistic anime，heavy impasto rendering，oil painting feeling，glossy oily skin，cinematic dramatic shadows，realistic 3D render，heavy material texture，washed-out pastel fog，whitewashed image，diluted clothing main color，neon candy over-saturation，full-frame hot pink background，full-frame magenta background，background same hue as character accent color。
    avoid extra fingers，missing fingers，six fingers，seven fingers，fused fingers，broken fingers，malformed hands，missing hands，extra hands，extra arms，extra feet，missing feet，twisted ankles，duplicated face，misaligned eyes。
    不要画面文字、英文标牌、角色名拼写、logo 或海报排版文字。
    """))


def prompt_for_art_direction(character_name: str, plan: dict | None = None, action: dict | None = None) -> str:
    selected_plan = plan or choose_art_direction_plan(character_name)
    selected_action = action or choose_action_style(character_name)
    return _compact_prompt(dedent(f"""
    {_visual_direction(selected_plan)}
    {_official_personality_translation(character_name)}
    {_identity_lock(character_name)}
    {_performance(character_name, selected_plan, selected_action)}
    {_anatomy_control()}
    {_fashion(character_name, selected_plan)}
    {_rendering(selected_plan)}
    {_negative()}
    """))


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

