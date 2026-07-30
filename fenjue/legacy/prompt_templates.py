import random
from textwrap import dedent

from fenjue.legacy.prompt_options import GROUP_SHOT_CONCEPTS, HORIZONTAL_POSES, POSES, SINGLE_SHOT_CONCEPTS


CHARACTER_PROFILES = {
    "千夏": {
        "identity": (
            "千夏，《绝区零》妄想天使成员，内向创作与作曲担当。"
            "视觉必须锁定为薄荷绿/浅灰绿色中短发少女：厚重空气感中短层次发，后发自然散开，轻微短发狼尾感；"
            "仅后顶部偏右有一小束装饰性小揪发，绑大号薄荷绿蝴蝶结，不是马尾。"
            "厚重不对称刘海，一侧遮挡额头和部分眼部，另一侧露耳，黑色心形耳饰；"
            "空气感包脸侧发、碎发层次、自然外翘发尾；粉金渐变瞳。"
        ),
        "palette": (
            "气质：紧张但认真、努力装镇定。"
            "可出现谱子、红色背包或大喇叭作为辅助。"
            "禁止 bob 头、贴脸直发、高马尾、双马尾、长马尾、纯元气营业偶像。"
        ),
    },
    "南宫": {
        "identity": (
            "南宫羽，《绝区零》妄想天使成员，天才队长、编舞与控场担当。"
            "视觉必须锁定为黑色中短发少女：厚重整齐齐刘海，刘海下缘平直贴近眉上；"
            "两侧短直包脸侧发，形成清晰脸部轮廓。"
            "双马尾位置偏高，位于头部左右后侧，但不是传统长双马尾；"
            "马尾为短束状、花瓣感、外翻分叉结构，每侧由多个圆润发束组成，发尾黑色渐变到高饱和粉色/玫红色。"
            "头顶有小呆毛，必须保留白色猫咪发夹、粉色三角发卡、科技感光环、背后机械小翅膀。"
        ),
        "palette": (
            "气质：慵懒聪明、狡黠从容、轻微坏笑、掌控现场。"
            "可以表现看穿一切、调度队友、故意逗千夏但实际照顾团队。"
            "禁止成熟御姐化、普通长双马尾、长卷发、波浪大卷、蓬松韩系长发、爱芮式高营业甜酷感。"
        ),
    },
    "爱芮": {
        "identity": (
            "爱芮，《绝区零》妄想天使成员，完美 Vocal 与舞台中心，粉色系小恶魔偶像少女。"
            "视觉必须锁定为高饱和粉色双马尾少女：双马尾蓬松、外翘卷曲、存在明显动感轮廓；"
            "额前有明显黑色挑染刘海，两侧有大体积包脸侧发，形成甜系偶像轮廓。"
            "瞳孔带蓝粉渐变高光感。"
            "必须保留黑色耳机式发饰、蝴蝶结装饰、粉色机械小翅膀、爱心元素、甜酷小恶魔气质。"
        ),
        "palette": (
            "气质：舞台上开朗明亮、自信主动、会带动气氛；私下有纯真、认真、反应慢半拍的机娘歌者感。"
            "适合面向镜头、唱歌、舞台动作、元气但不低幼。"
            "禁止成熟御姐化、普通 JK 路人化、只剩小恶魔属性、简约无舞台感、丢失黑色挑染或粉色机械翅膀。"
        ),
    },
    "丹": {
        "identity": (
            "丹不属于妄想天使阵容。视觉锁定为玫粉色分层包脸发型、圆润及肩轮廓与长斜刘海，"
            "拥有紫红色多层虹膜、两枚银色星形发夹和后侧大型蓝紫折叠饰带。"
            "背部固定为一对羽翼，可呈白紫羽毛形态或深靛色羽毛机械形态；只能保留一个一致形态和左右两翼。"
            "气质从容、自信、柔和且略带洞察感，不能退化成普通粉发少女。"
        ),
        "palette": (
            "气质：从容、自信、柔和、略带洞察感；保持成熟但不夸张的女性角色观感。"
            "身份配色锚点为玫粉、紫红、银色、蓝紫；羽翼依形态使用白紫或深靛色。"
            "禁止普通粉发甜妹化、丢失星形发夹与后侧饰带、遗漏成对羽翼、同时混合浅色与深色羽翼形态或生成额外翅膀。"
        ),
    },
    "铃": {
        "identity": (
            "铃，明快机灵的学院音乐少女。"
            "视觉必须锁定为短款深蓝紫色 bob 发：发尾轻微外翘，层次蓬松，"
            "大面积侧扫刘海遮挡部分额头与单侧眼部轮廓，但青蓝色/蓝绿色眼睛必须清晰。"
            "必须保留橙色 N 字母小发夹、小型青绿色耳坠、干净活泼的动漫脸。"
        ),
        "palette": (
            "气质：友好、聪明、轻快、带一点调皮，可以眨眼、微笑、听音乐或拿唱片。"
            "可出现唱片、磁带盒、便携式 CD 机、学院制服帽、黑白橙金配色作为辅助元素。"
            "禁止长发化、成熟御姐化、普通蓝发路人化、丢失 N 发夹、丢失短发轮廓，也不要把活动国风服装误当成永久身份。"
        ),
    },
}


def _character_names(character_name: str) -> list[str]:
    names = [name.strip() for name in character_name.replace("，", "、").split("、") if name.strip()]
    return names or ["丹"]


def _is_group(names: list[str]) -> bool:
    return len(names) >= 2


def _character_identity(character_name: str) -> str:
    names = _character_names(character_name)
    profile_blocks = []
    for name in names:
        profile = CHARACTER_PROFILES.get(name, CHARACTER_PROFILES["丹"])
        profile_blocks.append(f"{name}：{profile['identity']} {profile['palette']}")

    if _is_group(names):
        slots = ["左侧或前景", "中央或中景", "右侧或后景"]
        slot_lines = "；".join(
            f"{slots[index]}人物必须是{name}"
            for index, name in enumerate(names[:3])
        )
        subject_rule = (
            "本次是多人组合插画。人物之间需要有队友互动、视线呼应、前后层次或三角构图，不要排成死板一排，也不要全部挤在画面同一侧。"
            f"站位身份：{slot_lines}。"
            "多人身份必须按参考图逐个锁定：每个人只继承自己对应角色的发型、发色、发饰、眼睛和气质。"
            "禁止互相借用特征：千夏不能变成长发或双马尾；南宫不能变成薄荷绿头发或普通长双马尾；爱芮不能丢失粉色双马尾、黑色挑染和机械小翅膀；丹不能变成长发，也不能被画成妄想天使成员。"
        )
    else:
        subject_rule = (
            "本次只画一个角色，画面里只能有一个人物实体。"
            "不要生成其他队友、不要三人合照、不要组合海报、不要画中画重复人物。"
        )

    return dedent(f"""
    【角色身份固定】
    使用上传图片仅作为 {character_name} 的人物形象参考，不复制原图构图。
    是否多人只由本次指定的角色名数量决定；不要因为设定内容自动增加其他成员。
    {subject_rule}
    {" ".join(profile_blocks)}
    可以改变服装、姿态、镜头和场景，但头发轮廓、发色识别点、眼睛气质、发饰和角色性格气质必须稳定。
    """).strip()


def _artist_direction(concept: str, scene: str, pose: str) -> str:
    return dedent(f"""
    【画师企划】
    本次画面企划：{concept}
    本次场景：{scene}
    本次姿态：{pose}
    请像画师在设计一张能吸引人停留的角色插画，而不是机械堆关键词。
    第一眼吸引点由角色眼神、发型大形、上半身服装、腰线、姿态剪影、前景遮挡、背景节奏和场景留白共同组成。
    场景必须服务人物，不要让背景变成主角。
    """).strip()


def is_horizontal_concept(concept: str) -> bool:
    return "横" in concept or "16:9" in concept or "wide" in concept


def _composition_system(concept: str, is_group: bool) -> str:
    is_horizontal = is_horizontal_concept(concept)
    horizontal_rule = ""
    if is_horizontal and is_group:
        horizontal_rule = """
    本次是多人横向画幅：16:9 landscape composition / wide horizontal poster。
    人物之间需要有前后层次、视线呼应、三角构图或动作互动；不要排成一排，不要全部挤在同一侧。
    横幅两侧都必须有视觉任务：人物、前景、光线、远景剪影、装饰流或透视线至少占两项；不要出现半张图只有空背景。
    """
    elif is_horizontal:
        horizontal_rule = """
    本次是单人横向画幅：16:9 landscape composition / wide horizontal poster。
    只能通过前景遮挡、窗框、栏杆、雨线、光带、植物、远景色块、透视线和道具剪影来平衡左右空间。
    不得增加第二个人物、分身、半透明人物、大脸剪影或画中画人物。
    横幅两侧都必须有视觉任务；留白可以存在，但必须像封面设计的一部分。
    """

    return dedent(f"""
    【构图系统】
    {horizontal_rule}
    默认使用 medium shot，中景角色插画。
    优先 waist-up to knee-up framing，显示头部、肩部、上半身、腰线，并尽量露出部分腿部或膝上轮廓。
    脸部是第一焦点，但不是画面最大面积；服装上半身设计、袖口、腰线和整体人物姿态必须被看见。
    画面需要有 visual flow：眼睛 -> 发型大形 -> 肩线 -> 服装上半身 -> 腰线 -> 前景/背景节奏 -> 画面另一侧的视觉锚点。
    头顶、身体两侧、腰部和下半身方向都要有呼吸空间，但呼吸空间里必须有构图价值。
    避免死板正面站姿、T pose、证件照和背景人物平均用力。
    """).strip()


def _scene_control(lighting: str, mood: str) -> str:
    return dedent(f"""
    【场景、光影、情绪】
    光线：{lighting}
    情绪：{mood}
    背景简化成光、色块、空间线条和柔和氛围，但不能完全消失。
    可以有少量真实场景元素，但必须低细节、低存在感、虚化或块面化。
    soft natural lighting，gentle brightness around the face，light atmospheric glow。
    """).strip()


def _clothing(theme: str, character_name: str) -> str:
    names = _character_names(character_name)
    group_note = ""
    if _is_group(names):
        group_note = (
            "多人服装同主题但不同款：千夏偏清爽创作担当，南宫偏黑粉机能队长感，爱芮偏粉白甜酷 Vocal 感，丹若出现则保持轻科幻圣女感。"
            "不要让多人完全同款，也不要因为服装主题互换角色固定配色和发型。"
        )
    else:
        group_note = "单人服装围绕本角色气质设计，不要为了版式增加其他人物或重复人物。"

    return dedent(f"""
    【服装设计】
    本次服装主题：{theme}
    {group_note}
    服装设计要具体但克制：领口、外套、袖口、腰线、肩部、小饰件可以有设计点。
    构图必须能看见服装上半身和腰线。
    不要过度复杂花纹、全身堆满配件、武器或无关手持道具；千夏的谱子、红色背包或大喇叭只能作为身份辅助元素自然出现。
    """).strip()


def _color_detail_control() -> str:
    return dedent("""
    【颜色与细节层级】
    limited color palette，one dominant color atmosphere across the entire image。
    颜色像手绘二次元插画：柔和但清楚，不全图过淡，也不做 AI 式强饱和。
    高细节只集中在眼睛、脸部、发型大形、肩线、服装上半身、袖口、腰线和少量发丝。
    outer areas intentionally simplified，controlled detail hierarchy。
    头发先看大形：large clean hair shapes first，only a few detailed strands around focal areas。
    controlled natural hair messiness，不能发丝爆炸。
    """).strip()


def _rendering() -> str:
    return dedent("""
    【画风】
    masterpiece，modern high-aesthetic anime artwork，premium anime illustration atmosphere。
    干净二次元线稿，thin precise outlines，stable line quality。
    soft matte anime skin，minimal skin texture，clean elegant anime eyes，restrained eyelash detail。
    lightweight premium anime rendering，不要厚涂、半写实或 3D 感。
    整体像高级画师完成的角色插画、轻小说封面、官方视觉图或画册写真页。
    """).strip()


def _negative(is_group: bool) -> str:
    subject_negative = (
        "多人图不要身份混淆、发色互换或发型互换；千夏不能变成长发或双马尾，南宫不能变成薄荷绿头发或普通长双马尾，爱芮不能丢失粉色双马尾和黑色挑染，丹不能变成长发或妄想天使成员发型。"
        if is_group
        else "单人图不要其他队友、第二个人物、分身、远处小人、半透明大脸剪影或画中画重复人物。"
    )
    return dedent(f"""
    【避免项】
    avoid overrendering，avoid AI detail noise，avoid excessive texture，avoid oversharpening。
    avoid plastic anime look，avoid random decorative clutter，avoid overly glossy eyes，avoid RGB lighting，avoid cheap fantasy effects，avoid generic AI anime style。
    avoid dirty shadows，avoid uncontrolled glow，avoid extra fingers，avoid malformed hands，avoid extra arms，avoid duplicated face，avoid misaligned eyes。
    {subject_negative}
    不要画面文字、英文标牌、角色名拼写、logo 或海报排版文字。
    爱芮不要总是闭一只眼，优先双眼自然睁开或轻微眯眼。
    """).strip()


def _prompt_for_character_scene(
    theme: str,
    scene: str,
    pose: str,
    lighting: str,
    mood: str,
    concept: str,
    character_name: str,
) -> str:
    names = _character_names(character_name)
    is_group = _is_group(names)
    return dedent(f"""
    {_character_identity(character_name)}

    {_artist_direction(concept, scene, pose)}

    {_composition_system(concept, is_group)}

    {_scene_control(lighting, mood)}

    {_clothing(theme, character_name)}

    {_color_detail_control()}

    {_rendering()}

    {_negative(is_group)}
    """).strip()


PROMPT_TEMPLATE_FUNCTIONS = [
    _prompt_for_character_scene,
]

PROMPT_TEMPLATE_NAMES = [
    "artist_scene_modular",
]


def prompt_template_name(template_index: int) -> str:
    return PROMPT_TEMPLATE_NAMES[template_index % len(PROMPT_TEMPLATE_NAMES)]


def choose_concept(character_name: str) -> str:
    names = _character_names(character_name)
    pool = GROUP_SHOT_CONCEPTS if _is_group(names) else SINGLE_SHOT_CONCEPTS
    return random.choice(pool)


def choose_pose(concept: str) -> str:
    pool = HORIZONTAL_POSES if is_horizontal_concept(concept) else POSES
    return random.choice(pool)


def prompt_for_theme(
    theme: str,
    scene: str,
    pose: str | None = None,
    lighting: str = "",
    mood: str = "",
    template_index: int = 0,
    character_name: str = "丹",
    concept: str | None = None,
) -> str:
    """Return one artist-directed scene prompt for the selected character."""
    template = PROMPT_TEMPLATE_FUNCTIONS[template_index % len(PROMPT_TEMPLATE_FUNCTIONS)]
    selected_concept = concept or choose_concept(character_name)
    selected_pose = pose or choose_pose(selected_concept)
    return template(theme, scene, selected_pose, lighting, mood, selected_concept, character_name)
