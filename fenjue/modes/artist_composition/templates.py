from textwrap import dedent

from fenjue.modes.original.plans import propagation_profile_for, required_identity_tokens_for

from .plans import (
    ANTI_SAFE_COMPOSITION,
    choose_action_style,
    choose_art_plan as choose_art_direction_plan,
    choose_develop_combo,
    choose_information_balance,
)


CHARACTER_LOCKS = {
    "千夏": (
        "千夏：薄荷绿/浅灰绿色层次 bob 短发，后部扎成高位侧马尾；"
        "侧马尾根部固定大号深薄荷绿几何蝴蝶结，不是长发或双马尾。"
        "厚重不对称刘海，一侧遮挡额头与部分眼部；瞳色是琥珀金与青色交织的多色渐变。"
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
    "铃": (
        "铃：短款深蓝紫色 bob 发，发尾轻微外翘，头顶和侧发有蓬松层次；"
        "大面积侧扫刘海遮住一部分额头和单侧眼部轮廓，但必须露出清晰的青蓝色/蓝绿色眼睛。"
        "保留橙色 N 字母小发夹、小型青绿色耳坠、活泼学院感与音乐爱好者气质。"
        "可以出现唱片、磁带盒、便携式 CD 机、学院制服帽或黑白橙金配色作为辅助元素，但这些不是每张图都必须复制的固定服装。"
        "气质是明快、机灵、友好、带一点调皮；可以眨眼、微笑或做轻快手势。"
        "不要长发化、成熟御姐化、普通蓝发路人化、丢失 N 发夹、丢失短发轮廓，也不要把活动国风服装误当成永久身份。"
    ),
}


def _character_lock(name: str) -> str:
    if name in CHARACTER_LOCKS:
        return CHARACTER_LOCKS[name]
    profile = propagation_profile_for(name)
    required = "；".join(required_identity_tokens_for(name))
    return (
        f"{name}：{profile['official_core']} "
        f"必须清楚保留：{required}。"
        f"人物表现规则：{profile['interaction_rule']}"
    )


def _character_names(character_name: str) -> list[str]:
    names = [name.strip() for name in character_name.replace("，", "、").split("、") if name.strip()]
    return names or ["丹"]


def _is_group(names: list[str]) -> bool:
    return len(names) >= 2


def choose_art_direction_plan(character_name: str | None = None) -> dict:
    return choose_art_plan(character_name)


def prompt_template_name(template_index: int = 0) -> str:
    return "art_direction_single_cover"


def _identity_lock(character_name: str) -> str:
    names = _character_names(character_name)
    locks = " ".join(_character_lock(name) for name in names)
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


def _visual_direction(plan: dict, information_balance: dict) -> str:
    return dedent(f"""
    【Visual Direction / 本张视觉企划】
    这张图先成立画面逻辑，再让角色进入画面；角色是演员，不是整张图的唯一目的。
    核心 graphic idea：{plan["graphic_concept"]}。
    空间结构：{plan["spatial_structure"]}。
    视觉装置：{plan["visual_device"]}。
    信息分配策略：{information_balance["label"]}。
    {information_balance["prompt_concept"]}
    导演备注：{information_balance["director_note"]}
    画面缩小、去色或模糊后，仍然要能读出大形、动势和明暗结构。
    """).strip()


def _director_class(director_class: dict | None) -> str:
    if not director_class:
        return ""
    return dedent(f"""
    【Master Director / 主导演规则】
    本次导演类型：{director_class["name"]}。
    视觉宪法：{director_class["constitution"]}
    其他模块只做 variation，不得改变主导演语言；如果动作、天气、镜头或光影互相冲突，以本条主导演规则为准。
    """).strip()


def _energy_profile(energy_profile: dict | None, energy_state: dict | None) -> str:
    if not energy_profile:
        return ""
    score_text = ""
    if energy_state:
        score_text = (
            f"低气压分数：{energy_state.get('low_pressure_score', 0)}/"
            f"{energy_state.get('max_low_pressure_score', 0)}。"
        )
    return dedent(f"""
    【Energy Profile / 审美能量】
    本次能量类型：{energy_profile["name"]} / {energy_profile["label"]}。
    平台审美规则：{energy_profile["constitution"]}
    {score_text}
    画面可以有压迫、留白、暗部或神秘感，但默认要保持高级、干净、有生命力；不要主动走向废弃大楼、霉味灰墙、潮湿脏暗、战后残骸或世界已经死掉的感觉。
    """).strip()


def _performance(plan: dict, action: dict) -> str:
    return dedent(f"""
    【Character Performance / 剪影动作】
    本次动作类型：{action["name"]}。
    身体剪影：{action["body_silhouette"]}。
    人格动作逻辑：{action["personality_logic"]}。
    重量与支撑：{action["support_rule"]}。
    动作禁忌：{action["avoid_rule"]}。
    视觉企划原始动作参考：{plan["body_silhouette"]}；如果它和本次动作类型冲突，以本次动作类型为准。
    动作先看 silhouette readability：黑白剪影要成立，轮廓要有独特形状，不要只靠漂亮脸和柔光。
    动作必须服务角色人格，而不是单纯服务镜头冲击；避免普通半身写真、手靠脸、轻微回头这种安全动作重复。
    """).strip()


def _camera_language(lens: dict | None) -> str:
    if not lens:
        return ""
    return dedent(f"""
    【Camera Language / 镜头语言】
    本次镜头：{lens["name"]}。
    镜头控制：{lens["prompt_concept"]}。
    镜头必须服务动作和空间，不要为了冲击力而破坏角色身份、身体结构或画面可读性。
    """).strip()


def _atmosphere(weather: dict | None) -> str:
    if not weather:
        return ""
    return dedent(f"""
    【Atmosphere / 空气介质】
    本次空气环境：{weather["name"]}。
    空气控制：{weather["prompt_concept"]}。
    天气和空气介质只负责增强空间情绪，不要抢走角色、动作和主图形结构。
    """).strip()


def _lighting_strategy(lighting: dict | None, plan: dict) -> str:
    if not lighting:
        return ""
    return dedent(f"""
    【Lighting Strategy / 光影调度】
    本次光影策略：{lighting["name"]}。
    光影控制：{lighting["prompt_concept"]}。
    视觉企划原始光影：{plan["lighting_behavior"]}。
    如果二者冲突，以本次光影策略为主，但必须保留脸部可读性和大形明暗结构。
    """).strip()


def _complexity_budget(complexity_budget: dict | None) -> str:
    if not complexity_budget:
        return ""
    budget = complexity_budget.get("budget", {})
    counts = complexity_budget.get("counts", {})
    over_budget = complexity_budget.get("over_budget", [])
    over_budget_note = "当前组合已经压低超预算模块。" if over_budget else "当前组合在复杂度预算内。"
    return dedent(f"""
    【Visual Complexity Budget / 视觉密度预算】
    粒子层 {counts.get("particle_layers", 0)}/{budget.get("max_particle_layers", 0)}，
    前景装置 {counts.get("foreground_devices", 0)}/{budget.get("max_foreground_devices", 0)}，
    反射系统 {counts.get("reflection_systems", 0)}/{budget.get("max_reflection_systems", 0)}，
    二级运动 {counts.get("secondary_motion", 0)}/{budget.get("max_secondary_motion", 0)}。
    {over_budget_note}
    不要额外添加雨、雾、纸屑、鸟群、线缆、玻璃反射、UI 或杂物；所有视觉负载只服务主导演语言和角色焦点。
    """).strip()


def _fashion(plan: dict) -> str:
    return dedent(f"""
    【Fashion Direction / 服装企划】
    服装主题：{plan["outfit_direction"]}。
    材料语言：{plan["material_language"]}。
    色彩策略：{plan["color_strategy"]}。
    服装整体必须偏女性向设计：强调收腰、领口、肩线、袖口、裙摆、短外套、披肩、精致鞋靴、柔软或半透明材质。
    即使使用工业、战斗、未来或机能元素，也要转译成女性服装剪裁和高级时装语言，不要画成男性工装、厚重战术服、重甲、维修服或粗笨户外装备。
    允许高腰短裙、不规则半裙、裙裤、贴身内搭、短款夹克、轻礼服外套、细腰带、精致扣件和小面积金属饰件。
    角色识别色只允许占服装约 15% 到 25%；头发、眼睛、发饰负责身份识别，服装主色必须服务本张 visual direction。
    服装要有明确廓形、腰线、领口、袖口或鞋靴设计，但不要满身碎配件。
    """).strip()


def _rendering(plan: dict) -> str:
    return dedent(f"""
    【Rendering Layer / 画面完成】
    光影行为：{plan["lighting_behavior"]}。
    modern high-aesthetic anime artwork，premium illustration atmosphere，clean lineart，thin precise outlines。
    detail hierarchy：高细节只集中在眼睛、脸部、头发大形、服装关键边缘和视觉装置交汇点；outer areas intentionally simplified。
    large clean hair shapes first，only a few detailed strands around focal areas。
    画面要像作者性单人封面、Key Visual、CD cover 或游戏视觉海报，不是 AI 自拍、头像、普通美少女壁纸。
    """).strip()


def _negative() -> str:
    anti_safe = "，".join(ANTI_SAFE_COMPOSITION)
    return dedent(f"""
    【Avoid / 反安全模板】
    {anti_safe}。
    avoid overusing toward-camera hands，avoid repeated wide-angle hand intrusion，avoid always-floating composition，avoid cloth tornado repetition。
    如果本次动作不是 stage_intrusion，不要朝镜头伸手，不要广角大手前景；如果本次动作不是 high_view_floating，不要让角色失去重量支撑。
    avoid overrendering，avoid AI detail noise，avoid excessive texture，avoid oversharpening，avoid plastic anime look。
    avoid random decorative clutter，avoid overly glossy eyes，avoid RGB lighting，avoid cheap fantasy effects，avoid generic AI anime style。
    avoid extra fingers，malformed hands，extra arms，duplicated face，misaligned eyes。
    不要画面文字、英文标牌、角色名拼写、logo 或海报排版文字。
    """).strip()


def prompt_for_art_direction(
    character_name: str,
    plan: dict | None = None,
    director_class: dict | None = None,
    energy_profile: dict | None = None,
    energy_state: dict | None = None,
    action: dict | None = None,
    weather: dict | None = None,
    lens: dict | None = None,
    lighting_strategy: dict | None = None,
    information_balance: dict | None = None,
    complexity_budget: dict | None = None,
) -> str:
    selected_plan = plan or choose_art_direction_plan(character_name)
    selected_action = action or choose_action_style(character_name)
    selected_information_balance = information_balance or choose_information_balance(character_name, selected_plan, selected_action)
    optional_sections = "\n\n".join(
        section
        for section in [
            _camera_language(lens),
            _atmosphere(weather),
            _lighting_strategy(lighting_strategy, selected_plan),
        ]
        if section
    )
    return dedent(f"""
    {_visual_direction(selected_plan, selected_information_balance)}

    {_director_class(director_class)}

    {_energy_profile(energy_profile, energy_state)}

    {_performance(selected_plan, selected_action)}

    {optional_sections}

    {_complexity_budget(complexity_budget)}

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
    combo = choose_develop_combo(character_name)
    return prompt_for_art_direction(
        character_name,
        combo["art_plan"],
        combo["director_class"],
        combo["energy_profile"],
        combo["energy_state"],
        combo["action_style"],
        combo["weather_atmosphere"],
        combo["camera_lens"],
        combo["lighting_strategy"],
        combo["information_balance"],
        combo["complexity_budget"],
    )
