import random

ART_DIRECTION_PLANS = [
    {
        "name": "black_frame_pressure",
        "graphic_concept": "巨大黑色机械框景压缩空间，角色不在画面中心，黑白剪影先成立",
        "spatial_structure": "狭窄纵向机械框架与倾斜玻璃切割画面，前景黑色结构占画面约三分之一",
        "visual_device": "半透明显示器、黑色框架、斜向光带共同形成画面骨架",
        "body_silhouette": "角色蹲坐或半跪在画面下方，身体形成紧凑三角轮廓，一只手靠近前景形成近大远小",
        "outfit_direction": "未来感救援时装：短款结构外套、高腰修身下装、轻量束带、细反光边与局部结构件，强调清楚腰线、肩颈线与修长腿部轮廓",
        "material_language": "哑光防水布、细金属扣、透明塑料片、少量反光织带",
        "color_strategy": "深灰蓝主色，低饱和黑作为大块压色，只用橙色安全扣或小标记做强调；角色识别色只占服装 15% 到 25%",
        "lighting_behavior": "低位冷白侧光与局部暖色安全灯，脸部保持清楚，背景不过度霓虹",
    },
    {
        "name": "tilted_glass_cut",
        "graphic_concept": "巨大倾斜玻璃切割画面，人物被透明结构分割成不稳定但优雅的版式",
        "spatial_structure": "倾斜玻璃幕墙、反射层和远景色块形成斜向空间，画面有明显切割线",
        "visual_device": "玻璃反射、水汽痕迹、斜向窗框和局部投影遮住部分身体边缘",
        "body_silhouette": "角色侧身回头，身体形成长斜线，衣摆和头发沿玻璃切线方向流动",
        "outfit_direction": "未来通勤装：短款结构外套、高腰短裙或修身短裤、简洁领口、轻机能腰带，整体偏都市设计感与高端二次元时装轮廓",
        "material_language": "半哑光尼龙、细银边、透明扣件、柔软内搭",
        "color_strategy": "冷白与雾蓝为环境主调，服装主色可用米灰、烟蓝或低饱和黑，角色固有色只作为头发与小饰件识别",
        "lighting_behavior": "高处漫射天光穿过玻璃，反射柔和，不使用强烈电影光",
    },
    {
        "name": "cloth_s_curve",
        "graphic_concept": "巨大布料或外套形成 S 曲线，把人物包围成封面式图形",
        "spatial_structure": "背景极简，空间由布料弧线、衣摆和阴影决定，不依赖具体地点",
        "visual_device": "大面积外套、披肩或布料前景绕过角色，形成可读的 S 形视觉流",
        "body_silhouette": "角色身体后仰或轻微旋转，手臂和衣摆构成开放弧线，轮廓优雅但不自拍",
        "outfit_direction": "设计师外套造型：大廓形短外套、柔软内搭、高腰短裙或短裤，外套与裙摆形成优雅 S 曲线，轮廓轻盈流畅",
        "material_language": "柔软厚棉、轻薄防风布、少量半透明边缘、干净缝线",
        "color_strategy": "米白、灰黑或雾粉作服装主色，使用一处高纯角色色作为视觉钩子，避免全身角色默认配色",
        "lighting_behavior": "摄影棚柔光与大面积柔和投影，保留图形明暗关系",
    },
    {
        "name": "high_view_floating",
        "graphic_concept": "俯视漂浮构图，角色像被空间托起，四周道具形成旋转节奏",
        "spatial_structure": "高角度俯视的平面化空间，地面、玻璃或水面成为抽象背景板",
        "visual_device": "漂浮纸张、耳机线、透明 UI、小型装饰物或水面反光围绕角色旋转",
        "body_silhouette": "角色仰面或侧躺，四肢形成清楚的放射状剪影，脸不是唯一中心",
        "outfit_direction": "轻量学院时装：短外套、衬衫或修身内搭、高腰短裙或短裤、厚底鞋或运动鞋，整体带轻运动与青春设计感",
        "material_language": "棉质衬衫、轻尼龙、软皮革、透明小配件",
        "color_strategy": "淡灰、海军蓝或烟紫作为大面积主色，角色识别色压缩到发饰、腰带扣或袖口",
        "lighting_behavior": "上方大面积柔光，边缘有轻微反射，不要强 bloom",
    },
    {
        "name": "stair_perspective",
        "graphic_concept": "狭窄楼梯透视把人物推向画面一角，空间线条比背景地点更重要",
        "spatial_structure": "楼梯、扶手和墙面形成强透视，前景台阶切割画面",
        "visual_device": "扶手、台阶阴影、墙面光带和画面边缘裁切制造压迫与方向",
        "body_silhouette": "角色单腿踩高或坐在台阶转角，身体有明显折线和斜向动势",
        "outfit_direction": "街头轻机能：短夹克、层次内搭、高腰不规则半裙或修身短裤、具有设计感的鞋袜组合，强调腰线与腿部轮廓",
        "material_language": "硬挺斜纹布、软皮带、金属环、少量织带",
        "color_strategy": "低饱和卡其、冷灰或深绿作服装主色，角色色只作为发色与一两处细节呼应",
        "lighting_behavior": "楼梯顶部自然光切入，阴影清楚但不脏",
    },
    {
        "name": "plant_shadow_mask",
        "graphic_concept": "植物阴影覆盖半张画面，角色被光影切成安静而有张力的图形",
        "spatial_structure": "浅色墙面或窗边空间，大片植物影子成为主要图形结构",
        "visual_device": "叶影、窗格、半透明帘子和前景模糊植物形成多层遮挡",
        "body_silhouette": "角色靠墙或半蹲，头部略避开镜头，手臂与肩线形成安静剪影",
        "outfit_direction": "柔软日常设计款：短上衣、轻薄外套、高腰简洁下装，具有清楚领口、袖口与轻柔布料层次",
        "material_language": "棉麻、轻薄针织、柔软透明纱、哑光小扣",
        "color_strategy": "暖白、鼠尾草绿、浅灰褐或淡金属色作主色，避免直接使用角色默认全身配色",
        "lighting_behavior": "午后自然窗光，叶影边缘柔和，脸部局部明亮",
    },
    {
        "name": "foreground_hand_intrusion",
        "graphic_concept": "前景手臂或物件侵入镜头，制造强近大远小和非自拍式压迫感",
        "spatial_structure": "浅景深空间被前景大形切开，背景只保留几何光块",
        "visual_device": "靠近镜头的手、透明卡片、栏杆或布料遮挡 25% 到 40% 画面",
        "body_silhouette": "角色伸手接近镜头，身体后退形成纵深，另一只手保持自然平衡",
        "outfit_direction": "运动实验装：短款上衣、轻运动外套、高腰机能短裙或修身短裤、具有速度感的鞋袜设计，整体强调轻盈剪影",
        "material_language": "弹力运动布、半透明外层、轻量塑料扣、细反光边",
        "color_strategy": "主色从服装主题决定，可用灰白、冷蓝、深海绿或低饱和黑；角色识别色只做小面积强调",
        "lighting_behavior": "近景高光柔和，背景光点克制，不做廉价 RGB",
    },
    {
        "name": "small_figure_large_space",
        "graphic_concept": "让角色失去中心性，人物较小，巨大空间和留白成为主视觉",
        "spatial_structure": "高空平台、巨大白墙、空旷地面或大型圆形结构压缩人物体量",
        "visual_device": "大面积留白、远景几何块、地面投影和一条强方向线引导视线",
        "body_silhouette": "角色站在画面下三分之一或角落，姿态清楚，衣摆/头发提供小型动势",
        "outfit_direction": "封面概念装：主廓形短外套或裙摆成为人物剪影核心，整体强调腰线、肩颈线与修长腿部比例",
        "material_language": "硬挺外套、干净内搭、少量金属件、低细节大色块",
        "color_strategy": "环境主色决定全图，服装主色与环境形成对比；角色固有色不主导全图",
        "lighting_behavior": "干净远光或阴天大面积柔光，重视明暗块面，不追求脸部特写光",
    },
    {
        "name": "telephoto_compression",
        "graphic_concept": "长焦镜头压缩空间，巨大背景结构贴近人物，画面拒绝开阔感",
        "spatial_structure": "巨型月亮、工业塔、桥墩或全息广告牌占据大部分背景，人物被远景结构压住",
        "visual_device": "极度虚化的铁丝网、雨滴、栏杆或前景碎片切过画面，背景逆光形成清楚轮廓光",
        "body_silhouette": "角色半身、膝上或收敛站姿，动作幅度很小，主要靠眼神、肩线和局部手部动作建立压迫感",
        "outfit_direction": "冷感高端机能时装：防风高领、修身结构外套、短披肩与轻量结构件，整体具有都市感与成熟时装轮廓",
        "material_language": "哑光战术面料、粗糙金属磨损、玻璃反光、湿润边缘高光",
        "color_strategy": "高对比单色调，冷蓝、猩红或暗金环境光吞没服装主色，只保留少量角色识别高光",
        "lighting_behavior": "强背景逆光与边缘轮廓光，面部保持柔和阴影，不使用正面平光",
    },
    {
        "name": "neon_puddle_reflection",
        "graphic_concept": "贴地低视角，真实人物与积水或玻璃倒影共同分割画面",
        "spatial_structure": "地平线位于画面中线或偏上，潮湿地面和积水占据极大比例，空间被倒影拉长",
        "visual_device": "霓虹倒影、水波纹扭曲、低对比暗部、雨点和地面反光形成第二构图",
        "body_silhouette": "角色低头注视水面、缓慢跨步、蹲姿或停在水边，倒影与本体形成对称或微妙错位",
        "outfit_direction": "雨夜机能时装：防水短外套、高腰修身下装或短裙叠穿、设计感厚底鞋靴、少量搭扣与反光边，整体具有冷感都市气质",
        "material_language": "湿润皮革、反光 PVC、金属扣件局部高光、雨水附着的哑光布料",
        "color_strategy": "冷雨夜深蓝底色，倒影中只用少量橙、粉或青色霓虹点缀，不让全图 RGB 爆炸",
        "lighting_behavior": "顶光微弱，主要依赖地面冷暖反射光照亮人物，暗部保留空气感",
    },
    {
        "name": "kinetic_motion_blur",
        "graphic_concept": "人物主体保持清晰，前景或背景出现受控运动模糊，制造瞬间抓拍感",
        "spatial_structure": "隧道、街道、列车站台或强线性空间形成速度方向，背景色块被拉成条状",
        "visual_device": "列车残影、掠过镜头的飞鸟、碎片轨迹或光斑拖尾，围绕角色形成速度层",
        "body_silhouette": "角色转身、急停或低幅度启动的瞬间，衣摆和头发受风阻拉扯，但身体结构必须清楚",
        "outfit_direction": "速度感机能服：短款轻量夹克、修身运动内搭、高腰短裙或短裤、长带与清楚鞋靴设计，整体强调流线腰线与腿部动势",
        "material_language": "轻薄防风尼龙、高反光条、运动内搭、少量硬质扣件",
        "color_strategy": "背景色块被速度拉扯成低细节条纹，人物主色保持清楚纯净，避免全画面噪点化",
        "lighting_behavior": "强对比光斑和少量高光拖尾，人物脸部与轮廓必须保持稳定清楚",
    },
]



OUTFIT_DIRECTIONS = [plan["outfit_direction"] for plan in ART_DIRECTION_PLANS]

ANTI_SAFE_COMPOSITION = [
    "avoid centered portrait composition",
    "avoid simple window-side photography framing",
    "avoid symmetrical standing pose",
    "avoid soft idol-photo composition",
    "avoid generic anime wallpaper layout",
    "avoid repeating hand-on-face pose",
    "avoid always sitting by the window",
]


PLAN_TAGS = {
    "black_frame_pressure": {"hard_geometry", "foreground_pressure", "grounded", "compressed", "tense"},
    "tilted_glass_cut": {"hard_geometry", "glass", "diagonal", "medium_energy"},
    "cloth_s_curve": {"soft_curve", "cloth_flow", "medium_energy"},
    "high_view_floating": {"floating", "overhead", "explosive", "visual_noise_risk"},
    "stair_perspective": {"grounded", "support", "hard_geometry", "compressed", "quiet"},
    "plant_shadow_mask": {"quiet", "static", "shadow", "low_energy"},
    "foreground_hand_intrusion": {"reach", "wide_angle", "foreground_pressure", "explosive"},
    "small_figure_large_space": {"large_space", "static", "quiet", "low_energy"},
    "telephoto_compression": {"compressed", "background_pressure", "static", "telephoto"},
    "neon_puddle_reflection": {"grounded", "reflection", "dark_mood", "rain"},
    "kinetic_motion_blur": {"explosive", "speed", "dynamic", "motion_blur"},
}


CHARACTER_PLAN_WEIGHTS = {
    "千夏": {
        "stair_perspective": 5,
        "black_frame_pressure": 4,
        "plant_shadow_mask": 3,
        "tilted_glass_cut": 3,
        "small_figure_large_space": 2,
        "cloth_s_curve": 1,
        "high_view_floating": 1,
        "foreground_hand_intrusion": 0,
        "telephoto_compression": 2,
        "neon_puddle_reflection": 2,
        "kinetic_motion_blur": 1,
    },
    "南宫": {
        "black_frame_pressure": 5,
        "stair_perspective": 4,
        "tilted_glass_cut": 4,
        "foreground_hand_intrusion": 2,
        "plant_shadow_mask": 2,
        "cloth_s_curve": 1,
        "small_figure_large_space": 1,
        "high_view_floating": 1,
        "telephoto_compression": 4,
        "neon_puddle_reflection": 3,
        "kinetic_motion_blur": 1,
    },
    "爱芮": {
        "small_figure_large_space": 4,
        "high_view_floating": 3,
        "foreground_hand_intrusion": 2,
        "cloth_s_curve": 2,
        "tilted_glass_cut": 2,
        "black_frame_pressure": 1,
        "plant_shadow_mask": 1,
        "stair_perspective": 1,
        "telephoto_compression": 1,
        "neon_puddle_reflection": 1,
        "kinetic_motion_blur": 1,
    },
    "丹": {
        "small_figure_large_space": 6,
        "plant_shadow_mask": 5,
        "tilted_glass_cut": 4,
        "stair_perspective": 2,
        "cloth_s_curve": 1,
        "black_frame_pressure": 1,
        "high_view_floating": 0,
        "foreground_hand_intrusion": 0,
        "telephoto_compression": 2,
        "neon_puddle_reflection": 1,
        "kinetic_motion_blur": 0,
    },
    "星见雅": {
        "black_frame_pressure": 6,
        "tilted_glass_cut": 5,
        "stair_perspective": 4,
        "small_figure_large_space": 3,
        "plant_shadow_mask": 2,
        "cloth_s_curve": 1,
        "high_view_floating": 0,
        "foreground_hand_intrusion": 0,
        "telephoto_compression": 5,
        "neon_puddle_reflection": 3,
        "kinetic_motion_blur": 2,
    },
    "仪玄": {
        "black_frame_pressure": 5,
        "tilted_glass_cut": 5,
        "stair_perspective": 3,
        "small_figure_large_space": 3,
        "cloth_s_curve": 2,
        "plant_shadow_mask": 1,
        "high_view_floating": 1,
        "foreground_hand_intrusion": 0,
        "telephoto_compression": 4,
        "neon_puddle_reflection": 3,
        "kinetic_motion_blur": 1,
    },
}


ACTION_STYLES = [
    {
        "name": "quiet_observation",
        "tags": {"quiet", "static", "low_energy", "no_reach"},
        "body_silhouette": "角色低幅度转头或侧身停顿，身体重心安静，手臂贴近身体，只有衣摆、发尾或肩线产生轻微动势",
        "personality_logic": "动作服务观察感与疏离感，不主动冲向镜头；画面力量来自沉默、留白和空间压迫",
        "support_rule": "身体必须有明确支撑点：墙面、栏杆、地面、台阶或玻璃边缘",
        "avoid_rule": "不要朝镜头伸手，不要广角大手前景，不要跳跃或失重漂浮",
    },
    {
        "name": "defensive_fold",
        "tags": {"compressed", "grounded", "support", "no_reach"},
        "body_silhouette": "角色身体轻微折叠，肩线内收，单腿支撑、坐台阶或靠栏杆，形成被空间压住的防御型剪影",
        "personality_logic": "动作服务内向、防御、认真装镇定的角色状态，像角色真的在空间中思考或等待",
        "support_rule": "必须表现重量：脚踩台阶、膝盖受力、手肘靠墙或身体倚靠扶手",
        "avoid_rule": "不要舞台式张开身体，不要主动伸手触碰镜头，不要轻飘飘悬空",
    },
    {
        "name": "controlled_command",
        "tags": {"controlled", "grounded", "medium_energy", "no_reach"},
        "body_silhouette": "角色以斜靠、低位蹲坐、单腿踩高或从框架阴影中观察的姿态出现，身体线条从容但有掌控感",
        "personality_logic": "动作服务队长与调度者气质，像她在判断画面和现场，而不是单纯摆拍",
        "support_rule": "身体必须和硬结构发生关系：框架、扶手、楼梯、墙面或机械边缘支撑姿态",
        "avoid_rule": "不要普通偶像营业动作，不要过度甜酷，不要把动作做成爱芮式主动冲镜头",
    },
    {
        "name": "stage_intrusion",
        "tags": {"reach", "wide_angle", "explosive", "foreground_pressure"},
        "body_silhouette": "角色主动形成舞台动势，手臂、衣摆或背后光片形成外扩轮廓，但只有一个前景爆点，不让全画面同时爆炸",
        "personality_logic": "动作服务舞台中心、主动表演和镜头占有欲；这种动作优先给爱芮使用，其他角色慎用",
        "support_rule": "即使有广角冲击，也要保留清楚的身体轴线和腰线，不能只剩前景大手",
        "avoid_rule": "不要连续使用伸手构图，不要让手掌遮住脸部焦点，不要把所有漂浮物、丝带、UI 同时打开",
    },
    {
        "name": "large_space_stillness",
        "tags": {"large_space", "static", "quiet", "low_energy", "no_reach"},
        "body_silhouette": "角色体量较小，站在巨大空间下方或画面边缘，姿态几乎不动，只用衣摆、发丝或投影提供小型动势",
        "personality_logic": "动作服务孤独感、空洞感和空间情绪，让角色暂时失去中心性",
        "support_rule": "人物必须稳定站立、倚靠或停在明确平面上，巨大建筑或留白才是主导视觉",
        "avoid_rule": "不要靠近镜头，不要强表演，不要把角色画成普通漂亮壁纸中心人物",
    },
    {
        "name": "weighted_recline",
        "tags": {"grounded", "support", "medium_energy", "no_reach"},
        "body_silhouette": "角色坐下、半躺或侧靠，身体重量明确压在地面、台阶、墙面或玻璃结构上，腿部和肩线形成稳定斜向构图",
        "personality_logic": "动作服务身体重量和空间叙事，抵消漂浮泛滥，让画面有真实支撑感",
        "support_rule": "必须画出身体接触面和受力关系，衣物褶皱跟随重力而不是无规则飘动",
        "avoid_rule": "不要失重漂浮，不要 MV 式冲镜头，不要让动作只为镜头冲击服务",
    },
    {
        "name": "blade_stillness",
        "tags": {"controlled", "grounded", "hard_geometry", "no_reach", "quiet"},
        "body_silhouette": "角色以极低幅度拔刀前、收刀后或侧身停步的姿态出现，长发、狐耳、刀鞘和衣摆形成锐利纵向剪影",
        "personality_logic": "动作服务寡言冷静和顶级执行者气场，危险感来自克制、停顿和空间压迫，而不是大幅度表演",
        "support_rule": "身体必须稳定落地或靠近硬结构，刀和长发只做方向线，不要变成战斗乱舞",
        "avoid_rule": "不要朝镜头伸手，不要大跳跃，不要满屏刀光，不要把画面做成复杂战斗场面",
    },
    {
        "name": "occult_command",
        "tags": {"controlled", "grounded", "medium_energy", "hard_geometry", "no_reach"},
        "body_silhouette": "角色从容站立、斜靠或单腿支撑，手势靠近身体或略向侧方展开，符咒、灵鸟或流苏作为方向线围绕身体",
        "personality_logic": "动作服务从容强势、轻蔑玩味和掌控欲；像术法已经启动，而她本人不需要夸张动作",
        "support_rule": "身体必须有清楚重心，术法元素围绕空间结构运动，不要让角色失去重量",
        "avoid_rule": "不要舞台偶像式伸手，不要漂浮过多，不要满屏符咒和鸟群造成信息爆炸",
    },
    {
        "name": "post_combat_exhaustion",
        "tags": {"grounded", "support", "low_energy", "quiet", "heavy_weight", "no_reach"},
        "body_silhouette": "角色重心极低，靠在残骸、墙壁、台阶或栏杆上，武器随意拄在地上或垂落，肩线彻底放松",
        "personality_logic": "动作服务战后真实感和地心引力，展现顶级战力卸下防备的一瞬间，而不是漂亮摆拍",
        "support_rule": "必须有极强支撑受力点：背靠、手撑、武器支撑或膝盖受力，身体呈现疲惫下坠感",
        "avoid_rule": "不要看镜头营业，不要完美站姿，不要轻飘飘头发，不要满屏特效",
    },
    {
        "name": "half_drawn_tension",
        "tags": {"controlled", "medium_energy", "no_reach", "tension", "grounded"},
        "body_silhouette": "动作幅度极小，手掌刚覆盖在武器刀柄或法器上，身体微微前倾，重心下压，下颌微收",
        "personality_logic": "动作服务爆发前一秒的极限拉扯，不直接展现战斗，而是展现纯粹杀气和压迫感",
        "support_rule": "双脚必须稳稳抓地，肩颈和腰线带有紧绷感，空间线条压向角色",
        "avoid_rule": "不要完全拔出武器，不要夸张挥砍，不要大幅度肢体伸展，不要前景大手",
    },
    {
        "name": "over_shoulder_departure",
        "tags": {"no_reach", "depth", "quiet", "reject", "grounded"},
        "body_silhouette": "角色背对或侧背对镜头，正向画面深处走去，头部向后瞥向镜头，或者根本不看镜头",
        "personality_logic": "动作服务拒绝感、纵深感和神秘离场，引导视线进入背景空间，而不是迎合镜头",
        "support_rule": "背部线条与腰部扭转必须符合人体工学，衣摆和长发顺着行进方向摆动",
        "avoid_rule": "不要正面朝向镜头，不要迎合感微笑，不要伸手互动，不要过度可爱化",
    },
]


CHARACTER_ACTION_WEIGHTS = {
    "千夏": {
        "defensive_fold": 6,
        "quiet_observation": 4,
        "weighted_recline": 4,
        "controlled_command": 1,
        "large_space_stillness": 2,
        "stage_intrusion": 0,
        "post_combat_exhaustion": 2,
        "half_drawn_tension": 0,
        "over_shoulder_departure": 2,
    },
    "南宫": {
        "controlled_command": 6,
        "weighted_recline": 3,
        "quiet_observation": 3,
        "defensive_fold": 2,
        "large_space_stillness": 1,
        "stage_intrusion": 1,
        "post_combat_exhaustion": 2,
        "half_drawn_tension": 1,
        "over_shoulder_departure": 3,
    },
    "爱芮": {
        "stage_intrusion": 3,
        "large_space_stillness": 3,
        "weighted_recline": 3,
        "controlled_command": 2,
        "quiet_observation": 1,
        "defensive_fold": 0,
        "post_combat_exhaustion": 1,
        "half_drawn_tension": 0,
        "over_shoulder_departure": 1,
    },
    "丹": {
        "large_space_stillness": 6,
        "quiet_observation": 6,
        "weighted_recline": 3,
        "defensive_fold": 1,
        "controlled_command": 0,
        "stage_intrusion": 0,
        "blade_stillness": 0,
        "occult_command": 0,
        "post_combat_exhaustion": 1,
        "half_drawn_tension": 0,
        "over_shoulder_departure": 3,
    },
    "星见雅": {
        "blade_stillness": 7,
        "controlled_command": 4,
        "large_space_stillness": 3,
        "quiet_observation": 3,
        "weighted_recline": 1,
        "defensive_fold": 0,
        "stage_intrusion": 0,
        "occult_command": 0,
        "post_combat_exhaustion": 4,
        "half_drawn_tension": 8,
        "over_shoulder_departure": 5,
    },
    "仪玄": {
        "occult_command": 7,
        "controlled_command": 4,
        "quiet_observation": 3,
        "large_space_stillness": 2,
        "weighted_recline": 1,
        "defensive_fold": 0,
        "stage_intrusion": 0,
        "blade_stillness": 0,
        "post_combat_exhaustion": 2,
        "half_drawn_tension": 3,
        "over_shoulder_departure": 6,
    },
}


COOLDOWN_TAG_BLOCKS = {
    "reach": {"reach", "wide_angle", "foreground_pressure"},
    "wide_angle": {"reach", "wide_angle", "foreground_pressure"},
    "foreground_pressure": {"reach", "wide_angle", "foreground_pressure"},
    "floating": {"floating", "overhead"},
    "explosive": {"explosive", "wide_angle", "foreground_pressure"},
    "soft_curve": {"soft_curve", "cloth_flow"},
    "cloth_flow": {"soft_curve", "cloth_flow"},
    "motion_blur": {"motion_blur", "speed", "explosive"},
    "speed": {"motion_blur", "speed", "explosive"},
    "dynamic": {"motion_blur", "speed"},
}


def _weighted_choice(items: list[dict], weights: list[int]) -> dict:
    positive_items = [(item, weight) for item, weight in zip(items, weights) if weight > 0]
    if not positive_items:
        return random.choice(items)
    choices, positive_weights = zip(*positive_items)
    return random.choices(list(choices), weights=list(positive_weights), k=1)[0]


def _character_names(character_name: str) -> list[str]:
    names = [name.strip() for name in character_name.replace("，", "、").split("、") if name.strip()]
    return names or ["丹"]


def _primary_character(character_name: str) -> str:
    return _character_names(character_name)[0]


def _blocked_tags(recent_tags: list[str] | None) -> set[str]:
    blocked: set[str] = set()
    for tag in recent_tags or []:
        blocked.update(COOLDOWN_TAG_BLOCKS.get(tag, set()))
    return blocked


def choose_art_plan(character_name: str | None = None, recent_tags: list[str] | None = None) -> dict:
    character = _primary_character(character_name or "丹")
    weights_by_name = CHARACTER_PLAN_WEIGHTS.get(character, CHARACTER_PLAN_WEIGHTS["丹"])
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for plan in ART_DIRECTION_PLANS:
        tags = PLAN_TAGS.get(plan["name"], set())
        if tags & blocked:
            continue
        weight = weights_by_name.get(plan["name"], 1)
        if weight <= 0:
            continue
        candidates.append(plan)
        weights.append(weight)
    if not candidates:
        candidates = [plan for plan in ART_DIRECTION_PLANS if weights_by_name.get(plan["name"], 1) > 0]
        weights = [weights_by_name.get(plan["name"], 1) for plan in candidates]
    return _weighted_choice(candidates, weights)


# ---------------------------------------------------------------------------
# ZZZ new characters + stricter plan gates
# ---------------------------------------------------------------------------

if "CHARACTER_PROPAGATION_PROFILES" not in globals():
    CHARACTER_PROPAGATION_PROFILES = {}
if "CHARACTER_OUTFIT_VARIATIONS" not in globals():
    CHARACTER_OUTFIT_VARIATIONS = {}
if "CHARACTER_PLAN_WEIGHTS" not in globals():
    CHARACTER_PLAN_WEIGHTS = {}
if "CHARACTER_REQUIRED_IDENTITY_TOKENS" not in globals():
    CHARACTER_REQUIRED_IDENTITY_TOKENS = {}
if "CHARACTER_FORBIDDEN_PLANS" not in globals():
    CHARACTER_FORBIDDEN_PLANS = {}
if "CHARACTER_VIEWER_DISTANCE" not in globals():
    CHARACTER_VIEWER_DISTANCE = {}

NEW_CHARACTER_PROPAGATION_PROFILES = {
    "叶瞬光": {
        "official_core": "《绝区零》云岿山代理人，温柔可靠的师姐型执剑少女；核心是云岿山修行者气质、清亮剑光、承担感和保护他人的稳定强者气场。",
        "propagation_translation": "gentle blade senior sister：她不是冷酷杀手，而是温柔、可靠、会回身护人的执剑强者。",
        "viewer_relationship": "像师姐在晨雾山门前回头确认 viewer 是否安全；亲近但克制，可靠而有距离。",
        "interaction_rule": "她保护 viewer。画面关系是守护、承担、温柔引导和安静剑意，不是甜美营业或压迫挑衅。",
        "thumbnail_strategy": "脸 + 清亮眼神 + 云岿山气质 + 剑/剑光 + 山风云气 + 温柔师姐感；小图里必须读到云岿山、剑、可靠保护者。",
        "thumbnail_modes": ["温柔师姐半身型", "山门剑光型", "回身保护型", "云雾头像型"],
        "primary_hook_symbols": ["剑光", "云岿山山风", "符纹", "晨雾山门"],
        "secondary_support_symbols": ["剑穗", "竹影", "云气", "石阶"],
        "fantasy_symbols": ["剑光", "剑穗", "符纹", "山风", "云气", "竹影", "山门石阶", "月色剑痕"],
        "safe_sensuality": "吸引力来自温柔可靠、清亮剑意和保护感；不要做冷酷杀手、媚态营业或现代普通校园少女。",
        "preferred_hooks": {"modern_guofeng_character_poster", "rainy_clear_umbrella_date", "storybook_castle_balcony", "train_window_weekend", "dream_mist_portrait", "ritual_star_idol"},
        "preferred_actions": {"dreamy_side_glance", "symbolic_center_pose", "direct_eye_contact"},
        "suppressed_misreads": ["纯冷酷杀手", "现代普通校园少女", "无剑无门派气质", "甜妹营业", "西式骑士少女"],
    },
    "席德": {
        "official_core": "《绝区零》S级电属性强攻代理人，天真危险的机械改造少女；核心是机械、改造、老席德、电弧、花朵反差和不按常识理解世界的童真逻辑。",
        "propagation_translation": "electric mechanic innocent danger：她用纯真的表情展示危险改造，机械与花朵形成强反差。",
        "viewer_relationship": "像认真把危险机械装置当新玩具展示给 viewer；可爱、离谱、带一点危险。",
        "interaction_rule": "她向 viewer 展示改造。画面关系是童真说明、机械共犯感和电光危险，不是军武冷酷或普通机器人展示。",
        "thumbnail_strategy": "脸 + 电弧蓝紫光 + 机械零件/机库 + 老席德或大型机械伙伴痕迹 + 花朵反差；小图里必须读到机械改造、电光、席德式童真。",
        "thumbnail_modes": ["电光机械半身型", "驾驶舱头像型", "机械伙伴肩上型", "花与零件反差型"],
        "primary_hook_symbols": ["蓝紫电弧", "机械改造零件", "老席德机械痕迹", "花朵反差"],
        "secondary_support_symbols": ["四叶草", "油菜花", "电路纹", "机械手臂"],
        "fantasy_symbols": ["蓝紫电弧", "电路纹", "机械手臂", "驾驶舱光", "老席德残影", "四叶草", "油菜花", "机械手心开花"],
        "safe_sensuality": "吸引力来自天真危险和机械花朵反差；不要普通军服少女、无机械元素、纯冷酷机器人或过度武器炫耀。",
        "preferred_hooks": {"game_ui_battle_select", "pixel_cloud_savepoint", "neon_call_night", "gacha_capsule_corner", "arcade_prize_date"},
        "preferred_actions": {"direct_eye_contact", "symbolic_center_pose", "dreamy_side_glance"},
        "suppressed_misreads": ["普通军服少女", "无机械元素", "纯冷酷机器人", "普通机甲驾驶员", "只有花没有电光机械"],
    },
    "橘福福": {
        "official_core": "《绝区零》云岿山S级火属性击破代理人，虎系元气师姐；核心是虎系元素、火属性暖光、云岿山武修、虎威或虎形装置和猛虎伏魔感。",
        "propagation_translation": "tiger fire senior sister：她明亮、热情、能打，像会拉着你去吃饭又马上冲出去伏魔的虎系师姐。",
        "viewer_relationship": "像热闹招呼 viewer 加入队伍；亲近、元气、可靠，下一秒就能跃起伏魔。",
        "interaction_rule": "她带动 viewer。画面关系是元气召唤、热情陪伴和虎虎生风的行动感，不是普通猫娘卖萌。",
        "thumbnail_strategy": "脸 + 虎系特征 + 火光虎纹 + 云岿山武修气质 + 虎威/虎形装置；小图里必须读到虎、火、云岿山。",
        "thumbnail_modes": ["火光虎纹半身型", "跃起伏魔型", "灯笼庙会型", "练武场元气型"],
        "primary_hook_symbols": ["虎纹火焰", "虎威装置", "虎耳/虎系轮廓", "伏魔符纸"],
        "secondary_support_symbols": ["灯笼火光", "山门练武场", "红色符纸", "点心小袋"],
        "fantasy_symbols": ["虎纹火焰", "虎形剪影", "虎威装置", "伏魔符纸", "灯笼火光", "云岿山石阶", "练武场风线"],
        "safe_sensuality": "吸引力来自元气、火光、能打和师姐感；不要普通猫娘、过度阴暗、无虎无火无云岿山。",
        "preferred_hooks": {"rpg_town_square_festival", "fantasy_cooking_class", "theme_park_twilight", "game_ui_battle_select", "idol_practice_mirror_clean", "modern_guofeng_character_poster"},
        "preferred_actions": {"symbolic_center_pose", "direct_eye_contact", "idol_business_smile"},
        "suppressed_misreads": ["普通猫娘", "过度阴暗", "无虎无火无云岿山", "柔弱软妹", "纯偶像舞台少女"],
    },
}

CHARACTER_PROPAGATION_PROFILES.update(NEW_CHARACTER_PROPAGATION_PROFILES)

NEW_CHARACTER_OUTFIT_VARIATIONS = {
    "叶瞬光": [
        "云岿山修行短披肩 + 清亮浅色内搭 + 剑穗小饰件，温柔师姐感优先",
        "雨后石阶轻外套 + 中式盘扣腰线 + 剑鞘或剑穗，清爽可靠",
        "竹影练剑服：简洁修行外袍 + 轻裙裤 + 符纹边，不做厚重古装",
        "晨雾山门服：浅色披帛 + 干净领口 + 细剑光配饰，清亮不冷酷",
    ],
    "席德": [
        "机库改造短外套 + 电路纹内搭 + 四叶草小配饰，机械与花朵反差清楚",
        "驾驶舱轻机能服 + 蓝紫电光边 + 小花贴纸，天真危险感优先",
        "维修台私服：短夹克 + 工具带简化 + 机械手臂小光片，不做军武厚重",
        "大型机械伙伴旁的轻量装甲裙裤 + 油菜花色点缀 + 电弧发光扣",
    ],
    "橘福福": [
        "云岿山练武短外套 + 虎纹腰饰 + 暖色裙裤，元气师姐感优先",
        "灯笼庙会服：红橙短披肩 + 伏魔符纸小饰件 + 虎纹边，不变普通猫娘",
        "石阶跃起战斗服：轻便武修上衣 + 火光束带 + 虎威小装置",
        "早市点心日常服：明亮短外套 + 点心袋配饰 + 虎纹发饰，热闹但能打",
    ],
}
for character_name, outfit_list in NEW_CHARACTER_OUTFIT_VARIATIONS.items():
    CHARACTER_OUTFIT_VARIATIONS.setdefault(character_name, []).extend(outfit_list)

NEW_CHARACTER_PLAN_WEIGHTS = {
    "叶瞬光": {
        "modern_guofeng_character_poster": 10,
        "rainy_clear_umbrella_date": 6,
        "storybook_castle_balcony": 5,
        "dream_mist_portrait": 7,
        "ritual_star_idol": 6,
        "train_window_weekend": 4,
        "planetarium_soft_date": 3,
        "fairy_tale_bookshop": 2,
    },
    "席德": {
        "game_ui_battle_select": 9,
        "neon_call_night": 6,
        "gacha_capsule_corner": 6,
        "pixel_cloud_savepoint": 6,
        "arcade_prize_date": 4,
        "pajama_game_party": 3,
        "ultra_minimal_character_poster": 3,
    },
    "橘福福": {
        "modern_guofeng_character_poster": 8,
        "rpg_town_square_festival": 8,
        "fantasy_cooking_class": 6,
        "theme_park_twilight": 5,
        "game_ui_battle_select": 5,
        "idol_practice_mirror_clean": 4,
        "bakery_morning_window": 4,
    },
}
for character_name, plan_weights in NEW_CHARACTER_PLAN_WEIGHTS.items():
    CHARACTER_PLAN_WEIGHTS.setdefault(character_name, {}).update(plan_weights)

WHITE_INFINITY_ROOM_PLAN = {
    "name": "white_infinity_room",
    "graphic_concept": "纯白无限空间中只有角色和少量符号存在，像轻小说封面或高传播白色极简角色海报",
    "spatial_structure": "无边界白色或浅灰空间，大量留白托出角色轮廓，背景只保留极少量透明几何块、白色花瓣或柔影",
    "visual_device": "primary hook 只选一个：透明几何块 / 白色花瓣 / 极简椅子 / 角色专属小符号；secondary support 只允许一块柔影或一条低饱和细线",
    "body_silhouette": "角色单独站立、缓慢行走或安静坐姿，膝上到三分之二身为主，脸、发型轮廓、肩线和腰线清楚",
    "outfit_direction": "极简高端时装或未来感白色系穿搭：干净领口、明确腰线、少量角色识别色点缀",
    "material_language": "哑光白布、透明塑料、细金属、柔和无影棚光",
    "color_strategy": "白、浅灰、奶油色和极低饱和冷色主导；角色识别色只允许小面积出现，禁止背景同色吞没角色",
    "lighting_behavior": "极柔和无影棚拍光，脸和眼睛清楚，背景保持白但不发灰、不过曝、不吞轮廓",
}

if not any(plan["name"] == WHITE_INFINITY_ROOM_PLAN["name"] for plan in ART_DIRECTION_PLANS):
    ART_DIRECTION_PLANS.append(WHITE_INFINITY_ROOM_PLAN)
    OUTFIT_DIRECTIONS = [plan["outfit_direction"] for plan in ART_DIRECTION_PLANS]

PLAN_TAGS["white_infinity_room"] = {"minimal", "white_space", "character_icon", "clean_color"}

WHITE_INFINITY_ROOM_WEIGHTS = {
    "南宫": 5,
    "丹": 9,
    "仪玄": 5,
    "席德": 2,
    "星见雅": 3,
}
for character_name, weight in WHITE_INFINITY_ROOM_WEIGHTS.items():
    CHARACTER_PLAN_WEIGHTS.setdefault(character_name, {})["white_infinity_room"] = weight

for character_name in ["南宫", "丹", "仪玄", "席德", "星见雅"]:
    if character_name in CHARACTER_PROPAGATION_PROFILES:
        CHARACTER_PROPAGATION_PROFILES[character_name]["preferred_hooks"].add("white_infinity_room")

STRICT_PLAN_CHARACTERS = {"丹", "星见雅", "仪玄", "叶瞬光", "席德", "橘福福"}

CHARACTER_FORBIDDEN_TAGS = {
    "丹": {"idol", "practice", "theme_park", "gacha", "collectible"},
    "星见雅": {"cute", "theme_park", "home", "daily", "flower"},
    "仪玄": {"cute", "home", "domestic_daily", "theme_park"},
    "叶瞬光": {"cute", "theme_park", "gacha", "home"},
    "席德": {"soft_emotion", "flower", "warm_light"},
    "橘福福": {"quiet", "blue_light", "aquarium"},
}


def _default_plan_weight_for(character: str) -> int:
    return 0 if character in STRICT_PLAN_CHARACTERS else CHARACTER_PLAN_WEIGHT_FLOOR


def _allowed_plan_for_character(character: str, plan_name: str) -> bool:
    if plan_name in CHARACTER_FORBIDDEN_PLANS.get(character, set()):
        return False
    plan_tags = PLAN_TAGS.get(plan_name, set())
    forbidden_tags = CHARACTER_FORBIDDEN_TAGS.get(character, set())
    return not (plan_tags & forbidden_tags)


def choose_art_plan(character_name: str | None = None, recent_tags: list[str] | None = None) -> dict:
    character = _primary_character(character_name or "丹")
    profile = propagation_profile_for(character)
    weights_by_name = CHARACTER_PLAN_WEIGHTS.get(character, CHARACTER_PLAN_WEIGHTS["丹"])
    default_weight = _default_plan_weight_for(character)
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for plan in ART_DIRECTION_PLANS:
        plan_name = plan["name"]
        if not _allowed_plan_for_character(character, plan_name):
            continue
        tags = PLAN_TAGS.get(plan_name, set())
        if tags & blocked:
            continue
        weight = weights_by_name.get(plan_name, default_weight)
        if weight <= 0:
            continue
        candidates.append(plan)
        weights.append(_profile_adjusted_weight(plan_name, weight, profile["preferred_hooks"]))
    if not candidates:
        candidates = [
            plan for plan in ART_DIRECTION_PLANS
            if _allowed_plan_for_character(character, plan["name"])
            and weights_by_name.get(plan["name"], default_weight) > 0
        ]
        weights = [
            _profile_adjusted_weight(
                plan["name"],
                weights_by_name.get(plan["name"], default_weight),
                profile["preferred_hooks"],
            )
            for plan in candidates
        ]
    if not candidates:
        candidates = [
            plan for plan in ART_DIRECTION_PLANS
            if _allowed_plan_for_character(character, plan["name"])
        ] or ART_DIRECTION_PLANS[:]
        weights = [1 for _ in candidates]
    return _weighted_choice(candidates, weights)


# ---------------------------------------------------------------------------
# Additional plan late apply: white minimal propagation room
# ---------------------------------------------------------------------------

WHITE_INFINITY_ROOM_PLAN = {
    "name": "white_infinity_room",
    "graphic_concept": "纯白无限空间中只有角色和少量符号存在，像轻小说封面或高传播白色极简角色海报",
    "spatial_structure": "无边界白色或浅灰空间，大量留白托出角色轮廓，背景只保留极少量透明几何块、白色花瓣或柔影",
    "visual_device": "primary hook 只选一个：透明几何块 / 白色花瓣 / 极简椅子 / 角色专属小符号；secondary support 只允许一块柔影或一条低饱和细线",
    "body_silhouette": "角色单独站立、缓慢行走或安静坐姿，膝上到三分之二身为主，脸、发型轮廓、肩线和腰线清楚",
    "outfit_direction": "极简高端时装或未来感白色系穿搭：干净领口、明确腰线、少量角色识别色点缀",
    "material_language": "哑光白布、透明塑料、细金属、柔和无影棚光",
    "color_strategy": "白、浅灰、奶油色和极低饱和冷色主导；角色识别色只允许小面积出现，禁止背景同色吞没角色",
    "lighting_behavior": "极柔和无影棚拍光，脸和眼睛清楚，背景保持白但不发灰、不过曝、不吞轮廓",
}

if not any(plan["name"] == WHITE_INFINITY_ROOM_PLAN["name"] for plan in ART_DIRECTION_PLANS):
    ART_DIRECTION_PLANS.append(WHITE_INFINITY_ROOM_PLAN)
    OUTFIT_DIRECTIONS = [plan["outfit_direction"] for plan in ART_DIRECTION_PLANS]

PLAN_TAGS["white_infinity_room"] = {"minimal", "white_space", "character_icon", "clean_color"}

WHITE_INFINITY_ROOM_WEIGHTS = {
    "南宫": 5,
    "丹": 9,
    "仪玄": 5,
    "席德": 2,
    "星见雅": 3,
}
for character_name, weight in WHITE_INFINITY_ROOM_WEIGHTS.items():
    CHARACTER_PLAN_WEIGHTS.setdefault(character_name, {})["white_infinity_room"] = weight

for character_name in ["南宫", "丹", "仪玄", "席德", "星见雅"]:
    if character_name in CHARACTER_PROPAGATION_PROFILES:
        CHARACTER_PROPAGATION_PROFILES[character_name]["preferred_hooks"].add("white_infinity_room")


# ---------------------------------------------------------------------------
# New character action weights + stricter theme safety gates
# ---------------------------------------------------------------------------

CHARACTER_ACTION_WEIGHTS.update({
    "叶瞬光": {
        "dreamy_side_glance": 7,
        "direct_eye_contact": 5,
        "symbolic_center_pose": 6,
        "floating_daydream_pose": 2,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
        "idol_business_smile": 0,
    },
    "席德": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 7,
        "earpiece_call_gaze": 3,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "idol_business_smile": 0,
    },
    "橘福福": {
        "direct_eye_contact": 6,
        "symbolic_center_pose": 6,
        "idol_business_smile": 4,
        "dreamy_side_glance": 2,
        "floating_daydream_pose": 1,
        "near_camera_whisper": 0,
        "earpiece_call_gaze": 0,
    },
})

NEW_CHARACTER_PLAN_WEIGHTS.update({
    "叶瞬光": {
        "modern_guofeng_character_poster": 12,
        "dream_mist_portrait": 9,
        "ritual_star_idol": 7,
        "rainy_clear_umbrella_date": 4,
        "train_window_weekend": 2,
        "storybook_castle_balcony": 1,
        "planetarium_soft_date": 1,
        "fairy_tale_bookshop": 1,
    },
    "席德": {
        "game_ui_battle_select": 10,
        "neon_call_night": 7,
        "gacha_capsule_corner": 6,
        "arcade_prize_date": 5,
        "ultra_minimal_character_poster": 4,
    },
    "橘福福": {
        "modern_guofeng_character_poster": 10,
        "rpg_town_square_festival": 9,
        "game_ui_battle_select": 6,
        "fantasy_cooking_class": 4,
        "theme_park_twilight": 2,
        "idol_practice_mirror_clean": 1,
        "bakery_morning_window": 0,
    },
})
for character_name, plan_weights in NEW_CHARACTER_PLAN_WEIGHTS.items():
    CHARACTER_PLAN_WEIGHTS.setdefault(character_name, {}).update(plan_weights)

CHARACTER_FORBIDDEN_PLANS.update({
    "橘福福": {
        "planetarium_soft_date",
        "fairy_tale_bookshop",
        "laundry_sun_room",
        "aquarium_blue_date",
        "bakery_morning_window",
    },
})

CHARACTER_FORBIDDEN_TAGS.update({
    "席德": {"warm_light"},
})

CHARACTER_PROPAGATION_PROFILES["叶瞬光"]["interaction_rule"] += (
    " 叶瞬光的剑意必须是护人而不是杀人；如果使用约会类主题，必须转译为师姐护送 viewer 经过山门、雨巷或石阶。"
)
CHARACTER_PROPAGATION_PROFILES["席德"]["interaction_rule"] += (
    " 席德的可爱必须来自天真地展示危险改造；花朵只能作为机械反差点缀，不能变成普通花园少女。"
)
CHARACTER_PROPAGATION_PROFILES["橘福福"]["interaction_rule"] += (
    " 橘福福的元气必须带能打和伏魔气质；日常或料理主题必须转译为虎系师姐招呼 viewer 后马上出发伏魔。"
)


def choose_action_style(character_name: str, recent_tags: list[str] | None = None) -> dict:
    character = _primary_character(character_name)
    weights_by_name = CHARACTER_ACTION_WEIGHTS.get(character, CHARACTER_ACTION_WEIGHTS["丹"])
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for action in ACTION_STYLES:
        if action["tags"] & blocked:
            continue
        weight = weights_by_name.get(action["name"], 0)
        if weight <= 0:
            continue
        candidates.append(action)
        weights.append(weight)
    if not candidates:
        candidates = [action for action in ACTION_STYLES if weights_by_name.get(action["name"], 0) > 0]
        weights = [weights_by_name.get(action["name"], 0) for action in candidates]
    return _weighted_choice(candidates, weights)


def collect_cooldown_tags(plan: dict, action: dict) -> list[str]:
    tags = set(PLAN_TAGS.get(plan["name"], set()))
    tags.update(action.get("tags", set()))
    return sorted(tags)


def choose_plan_and_action(character_name: str, recent_tags: list[str] | None = None) -> tuple[dict, dict]:
    plan = choose_art_plan(character_name, recent_tags)
    plan_tags = sorted(PLAN_TAGS.get(plan["name"], set()))
    action = choose_action_style(character_name, [*(recent_tags or []), *plan_tags])
    return plan, action


# ---------------------------------------------------------------------------
# Fenjue 3.0 override: social anime character propagation system
#
# V3 intentionally turns away from cinematic realism and hard concept-art space.
# The active plan pool below is built for platform spread: strong thumbnail read,
# character-first fantasy, emotional intimacy, and high-color memory.
# ---------------------------------------------------------------------------

ART_DIRECTION_PLANS = [
    {
        "name": "heart_signal_closeup",
        "graphic_concept": "角色靠近观众，爱心、发光耳机线或小型 UI 像情绪信号一样围绕脸和手",
        "spatial_structure": "空间从角色表情向外扩散，背景是简化的粉色、蓝紫或霓虹梦境色块",
        "visual_device": "primary hook 只选一个：近景对视 / 爱心轨道 / 发光耳机线；secondary support 只选一个：小聊天气泡 / 柔亮色块",
        "body_silhouette": "角色膝上到三分之二身构图，眼神直视 viewer，手部动作保持在胸前、耳机旁或身体侧边，不向镜头伸出",
        "outfit_direction": "社交平台头像级偶像服装：短外套、蝴蝶结、耳机、细腰线和高识别小配件",
        "material_language": "柔软布料、透明亚克力、发光小饰件、轻薄丝带",
        "color_strategy": "高记忆角色色占主导，背景用互补色托脸，缩略图先读到眼睛和发色",
        "lighting_behavior": "脸部明亮，眼睛高光清楚，边缘有梦境柔光，不做真实摄影暗部",
    },
    {
        "name": "summer_mint_afterglow",
        "graphic_concept": "薄荷夏日空气从角色周围生长，风、透明饮料、窗帘和水光形成清凉幻想",
        "spatial_structure": "浅色房间、天台或海边被压成大色块，空间不复杂，只服务清透情绪",
        "visual_device": "primary hook 只选一个：大号薄荷蝴蝶结 / 薄荷色风 / 透明饮料；secondary support 只选一个：窗帘 / 水光 / 发光云",
        "body_silhouette": "角色轻轻回头或扶着窗边，动作小但眼神有陪伴感",
        "outfit_direction": "清爽夏日二次元私服：短衬衫、轻薄外套、高腰裙裤、透明小饰件",
        "material_language": "棉麻、薄纱、透明塑料、湿润高光和清透玻璃",
        "color_strategy": "薄荷绿、奶白、天空蓝和少量粉金作为记忆色，避免灰暗低气压",
        "lighting_behavior": "明亮自然光和轻微逆光，脸、发丝和眼睛必须清楚发亮",
    },
    {
        "name": "idol_stage_dream",
        "graphic_concept": "不是写实舞台，而是角色人格化的偶像梦境，灯光、星星和观众应援色变成图形背景",
        "spatial_structure": "舞台被简化成圆形光环、斜向色块和漂浮星屑，角色占据第一视觉中心",
        "visual_device": "primary hook 只选一个：麦克风 / idol spotlight / 爱心环；secondary support 只选一个：应援光 / 飘带 / 星形小粒子",
        "body_silhouette": "角色面向 viewer 做营业感动作，身体打开但不夸张挑逗",
        "outfit_direction": "甜酷偶像服：短夹克、裙摆、舞台鞋靴、蝴蝶结和少量金属高光",
        "material_language": "亮面布料、软纱、闪粉边缘、透明装饰片",
        "color_strategy": "高饱和粉、蓝、紫或角色主色形成一眼记住的缩略图",
        "lighting_behavior": "高亮舞台柔光，眼睛和脸比背景更亮，避免脏暗演唱会截图感",
    },
    {
        "name": "moon_confession_fantasy",
        "graphic_concept": "巨型月亮、花瓣、窗台和夜色像告白场景一样围绕角色，重点是幻想恋爱感",
        "spatial_structure": "夜空和月亮被图形化处理，空间不追求真实比例，角色和月亮形成强记忆剪影",
        "visual_device": "primary hook 只选一个：巨型月亮 / 发光窗格 / 近景悄悄话手势；secondary support 只选一个：花瓣 / 薄云 / 星光",
        "body_silhouette": "角色坐在窗边、回头对视或侧身靠近画面中心，像在对 viewer 说悄悄话，但不压向镜头",
        "outfit_direction": "夜色约会感服装：轻礼服外套、短裙或裙裤、精致领口和柔软披肩",
        "material_language": "软缎、薄纱、月光边缘、透明宝石小饰件",
        "color_strategy": "深蓝紫夜色加角色发色高光，局部暖粉或金色制造恋爱记忆点",
        "lighting_behavior": "月光和柔暖补光并存，暗部保持干净，不进入恐怖或废墟气质",
    },
    {
        "name": "floating_room_daydream",
        "graphic_concept": "房间、书本、枕头、小物件和云朵轻微漂浮，表现角色的白日梦人格空间",
        "spatial_structure": "真实房间被改造成梦境平面，透视可以不合理，但画面必须可爱、清楚、可收藏",
        "visual_device": "primary hook 只选一个：抱枕梦境 / 透明饮料 / 窗外超现实天空；secondary support 只选一个：云朵 / 色块贴纸 / 柔光线",
        "body_silhouette": "角色坐、趴或半躺在画面中央偏近位置，表情要有亲近感",
        "outfit_direction": "居家幻想私服：宽松短外套、可爱内搭、短裙或软裤、袜子和小发饰",
        "material_language": "柔软棉布、毛绒、透明贴片、色块贴纸、透明光点",
        "color_strategy": "奶油白、粉蓝、薰衣草紫或角色主色形成舒服但显眼的封面感",
        "lighting_behavior": "柔亮室内光，像梦醒前一秒，脸部绝对不能暗",
    },
    {
        "name": "candy_sky_poster",
        "graphic_concept": "糖果色天空、巨大云层和漂浮图形符号把角色包装成社交平台视觉海报",
        "spatial_structure": "天空是平面化大色块，地面和建筑尽量简化，角色是海报中心",
        "visual_device": "primary hook 只选一个：糖果云 / 巨大圆形太阳或月亮 / 高纯度角色色块；secondary support 只选一个：彩色光带 / 星星贴纸 / 小图标",
        "body_silhouette": "角色站姿或轻跳动作清楚，轮廓 logo 化，缩略图也能读出人物",
        "outfit_direction": "明亮海报服装：短夹克、裙摆、厚底鞋、强识别配色和大形发饰",
        "material_language": "亮色布料、轻软皮革、透明装饰、贴纸质感",
        "color_strategy": "高纯度但干净的角色色和天空色对撞，画面必须有停滑色彩记忆点",
        "lighting_behavior": "整体明亮，角色脸、发型和膝上姿态是第一焦点，不追求真实阴影",
    },
    {
        "name": "ritual_star_idol",
        "graphic_concept": "仪式感不再阴暗，而是星光、符号、灵鸟或刀线变成华丽二次元视觉符号",
        "spatial_structure": "背景是抽象星图、圆环、光阵和纯色夜空，角色像幻想偶像或神性主角",
        "visual_device": "primary hook 只选一个：星图圆环 / 黑鸟剪影 / 刀线高光；secondary support 只选一个：符纸光点 / 漂浮发饰 / 大面积角色色",
        "body_silhouette": "角色正面或三分之二角度面对 viewer，姿态从容，有被崇拜的主角感",
        "outfit_direction": "华丽幻想服装：收腰外套、短披肩、精致袖饰、裙摆或裙裤、角色专属符号",
        "material_language": "半透明纱、金属细饰、发光符号、丝带和亮面小面积材质",
        "color_strategy": "黑、金、红、银或角色主色形成高辨识幻想组合，避免西式废墟概念图",
        "lighting_behavior": "星光和角色前方柔光同时存在，脸部和眼睛必须比背景清楚",
    },
    {
        "name": "ultra_minimal_character_poster",
        "graphic_concept": "超级简约角色海报：只保留角色脸、发型大形、一个专属符号和一块克制的中性/低饱和背景",
        "spatial_structure": "没有真实空间，背景是米白、浅灰、雾蓝、淡奶油或低饱和互补色的干净纯色/轻微渐变；角色以膝上或三分之二身构图为主，避免连续纯胸像",
        "visual_device": "primary hook 只选一个：角色专属发饰 / 一个小道具 / 一个简洁图形符号；secondary support 只允许一条细线、一个小光点或一块低饱和背景色",
        "body_silhouette": "角色正面或三分之二身，脸、眼睛、头发轮廓、肩线和手部小动作极清楚，姿态克制但有情绪",
        "outfit_direction": "极简但有角色识别的膝上服装：干净领口、明确肩线、腰线提示、一个小配饰或一处角色色",
        "material_language": "平滑色块、干净线稿、少量柔光、无复杂材质",
        "color_strategy": "最多两到三种主色，角色专属高饱和色只能用于头发、发饰、领口、细线和小符号；背景必须低饱和且与角色主色拉开色相/明度，禁止整张背景使用高饱和粉、洋红、紫红或角色同色",
        "lighting_behavior": "柔亮均匀光，眼睛和脸部最清楚，不追求真实阴影和复杂光效",
    },
    {
        "name": "dream_mist_portrait",
        "graphic_concept": "梦幻感角色近景：像半醒梦里的角色图，只保留柔雾、眼神、发丝和一个人格化幻想符号",
        "spatial_structure": "空间几乎融化成浅色雾面背景，角色半身到膝上占画面主体，边缘可有少量漂浮光尘但不形成复杂场景",
        "visual_device": "primary hook 只选一个：月亮 / 羽毛 / 发光云 / 透明耳机线；secondary support 只选一个：薄雾色块 / 小星点 / 柔光圆",
        "body_silhouette": "角色微侧脸或轻回头，肩颈线干净，表情安静但有被收藏的情绪余韵",
        "outfit_direction": "柔软轻薄的角色服装，领口、腰线和发饰清楚，避免复杂层叠和大型机械装饰",
        "material_language": "透明薄纱、柔软棉感、轻微珠光、雾面渐变",
        "color_strategy": "低噪声高记忆浅色系，角色色作为第一阅读点，背景只负责托出脸和眼睛",
        "lighting_behavior": "大面积柔光包裹，眼睛高光清楚，阴影极浅，不做电影暗调",
    },
    {
        "name": "fairytale_pop_storybook",
        "graphic_concept": "童话感社交插画：角色像从一本发光绘本里跳出来，画面可爱但不低幼",
        "spatial_structure": "背景是扁平化绘本舞台、窗框、糖果云或小花园的一小角，绝不展开复杂建筑透视",
        "visual_device": "primary hook 只选一个：绘本窗框 / 小皇冠 / 糖果云 / 花环；secondary support 只选一个：小星点 / 丝带 / 软色块",
        "body_silhouette": "角色膝上或三分之二身构图，动作轻快，有明确表情和手势，缩略图先读到脸、发型和整体姿态",
        "outfit_direction": "童话偶像感服装：小披肩、蝴蝶结、短裙边或领结只保留一个重点，不做全身堆装饰",
        "material_language": "柔软布料、绘本质感色块、少量亮片、圆润干净线条",
        "color_strategy": "高明度但控制色数，最多三种主色，避免全画面彩虹噪音",
        "lighting_behavior": "明亮童话棚光，脸部和发色最清楚，背景像舞台布景一样轻",
    },
    {
        "name": "clean_idol_studio_shot",
        "graphic_concept": "摄影棚式二次元角色图：不是写实摄影，而是干净棚拍感的角色商业头像",
        "spatial_structure": "纯色无缝背景、简洁地台或一块软阴影，角色以膝上到三分之二身为主，画面结构极清楚",
        "visual_device": "primary hook 只选一个：角色专属道具 / 发饰 / 手势 / 眼神；secondary support 只选一个：背景色块 / 柔影 / 小型补光边",
        "body_silhouette": "角色姿态稳定，肩线、腰线和脸部表情清楚，像可以直接用于社交平台封面或头像",
        "outfit_direction": "干净精修的角色服装，脸周、领口、腰线和角色色同时可读，少量配饰集中但不只截到上半身",
        "material_language": "平滑布料、干净皮肤光、克制高光、少量透明或金属小件",
        "color_strategy": "单一背景主色配角色识别色，强缩略图读取，避免复杂环境抢戏",
        "lighting_behavior": "柔和棚拍主光加轻边光，眼睛、脸和发型是绝对焦点",
    },
    {
        "name": "modern_guofeng_character_poster",
        "graphic_concept": "现代国风角色海报：用留白、墨色线条和一个东方意象强化角色人格，不做古装旅游照",
        "spatial_structure": "背景是大面积宣纸感留白、圆窗、折扇弧线或水墨色块，角色膝上到三分之二身占主视觉",
        "visual_device": "primary hook 只选一个：圆月窗 / 折扇弧线 / 墨色花枝 / 玉饰；secondary support 只选一个：淡墨云气 / 细金线 / 水纹",
        "body_silhouette": "角色正面或三分之二身，姿态克制，手部动作像轻握扇、整理发饰或安静回眸，不向镜头前伸",
        "outfit_direction": "现代改良国风服装：盘扣、短披帛、云肩或玉饰只保留一个重点，并保持角色原本发型和人格",
        "material_language": "丝缎、宣纸纹理、淡墨、细金线、玉石小饰件",
        "color_strategy": "一块角色识别色 + 墨色/米白/淡金支撑，不能变成传统厚重古风杂色",
        "lighting_behavior": "清透柔光，脸部现代二次元插画感明确，水墨元素只做气氛不压角色",
    },
    {
        "name": "fairy_garden_picnic",
        "graphic_concept": "角色在童话花园野餐，周围漂浮花瓣和甜点元素",
        "spatial_structure": "开阔花园色块，简化树木与天空，空间轻松明亮",
        "visual_device": "漂浮糕点、发光花瓣、小彩灯",
        "body_silhouette": "角色坐在草地上或半躺，轻松手势与微笑",
        "outfit_direction": "轻盈可爱日常裙装，短外套或小披肩",
        "material_language": "棉麻、薄纱、柔软丝带",
        "color_strategy": "明亮粉、薄荷绿、奶白、淡黄",
        "lighting_behavior": "明亮自然光，柔和阴影，角色脸部清楚",
    },
    {
        "name": "magical_library_day",
        "graphic_concept": "角色在魔法图书馆，漂浮书本围绕",
        "spatial_structure": "书架和光束大色块简化，梦幻但干净",
        "visual_device": "发光书页、漂浮文字、透明符号",
        "body_silhouette": "角色站或轻抬手触碰书本",
        "outfit_direction": "学院风制服或轻礼服",
        "material_language": "棉布、柔纱、发光纸张",
        "color_strategy": "浅蓝、奶白、紫色点缀",
        "lighting_behavior": "光线从天窗倾泻，柔光包裹角色",
    },
    {
        "name": "cafe_date_summer",
        "graphic_concept": "角色在街边咖啡店，桌上饮品和小物增添甜美感",
        "spatial_structure": "街道和店铺色块简化，突出角色",
        "visual_device": "饮品光泽、飘落叶子、小道具",
        "body_silhouette": "角色坐或轻靠桌面，手握饮品",
        "outfit_direction": "夏日轻裙或衬衫短裙组合",
        "material_language": "棉麻、透明玻璃、柔软织物",
        "color_strategy": "淡橙、奶白、粉色，角色色点缀",
        "lighting_behavior": "阳光自然光照，柔和边缘高光",
    },
    {
        "name": "snowy_game_world",
        "graphic_concept": "角色在雪地游戏世界，雪花漂浮，魔法图标悬空",
        "spatial_structure": "雪地、远山、天空色块简化，轻松幻想",
        "visual_device": "漂浮雪花、魔法小符号、亮点光斑",
        "body_silhouette": "角色行走或跳跃姿态轻盈",
        "outfit_direction": "轻便游戏服装，斗篷或毛衣外套",
        "material_language": "轻棉、毛绒、透明小饰件",
        "color_strategy": "白、淡蓝、粉色点缀",
        "lighting_behavior": "高亮漫射光，雪面反射柔光",
    },
    {
        "name": "floating_balloon_park",
        "graphic_concept": "角色在公园，彩色气球漂浮周围",
        "spatial_structure": "绿地与天空大色块，空间明亮开阔",
        "visual_device": "气球、飘带、发光小物",
        "body_silhouette": "角色轻跳或伸手抓气球",
        "outfit_direction": "日常轻裙或连衣裙",
        "material_language": "棉布、薄纱、亮光小饰件",
        "color_strategy": "明亮黄、粉、天蓝",
        "lighting_behavior": "阳光明亮，柔和阴影",
    },
    {
        "name": "candy_shop_fun",
        "graphic_concept": "角色在糖果店内，糖果漂浮，甜美梦幻",
        "spatial_structure": "店铺简化，糖果大色块作为背景",
        "visual_device": "漂浮糖果、彩色光点、玻璃罐反光",
        "body_silhouette": "角色伸手拿糖果或欢快跳跃",
        "outfit_direction": "可爱短裙+毛衣或短外套",
        "material_language": "棉布、丝带、透明塑料",
        "color_strategy": "粉红、亮黄、薄荷绿",
        "lighting_behavior": "柔和棚光，角色脸部明亮",
    },
    {
        "name": "sunny_rooftop_meeting",
        "graphic_concept": "角色在屋顶，阳光洒下，风轻吹头发",
        "spatial_structure": "天空大色块简化，屋顶元素少量作为点缀",
        "visual_device": "漂浮小花、发光小配件、风吹发丝",
        "body_silhouette": "角色站立或轻跳，手自然摆放",
        "outfit_direction": "轻薄外套+高腰裤/短裙",
        "material_language": "棉布、薄纱、柔软丝带",
        "color_strategy": "蓝天白云主调，角色色点缀",
        "lighting_behavior": "阳光明亮柔和，脸部可读",
    },
    {
        "name": "cherry_blossom_walk",
        "graphic_concept": "角色走在樱花树下，花瓣飘落",
        "spatial_structure": "浅色地面与天空色块，樱花形成前景与背景层",
        "visual_device": "花瓣、柔光粉色光点、轻微风动",
        "body_silhouette": "轻轻回头或抬手触花",
        "outfit_direction": "日常短裙或连衣裙，轻薄外套",
        "material_language": "棉布、薄纱、丝带",
        "color_strategy": "粉红、奶白、淡绿",
        "lighting_behavior": "自然光，柔和光影",
    },
    {
        "name": "afternoon_tea_room",
        "graphic_concept": "角色在下午茶房，桌上甜点与茶具，温馨梦幻",
        "spatial_structure": "桌椅与窗外色块简化，突出角色",
        "visual_device": "茶具、糕点、光斑、发光装饰",
        "body_silhouette": "坐姿或轻侧身，手握茶杯",
        "outfit_direction": "优雅裙装或轻礼服",
        "material_language": "丝绸、棉布、陶瓷光泽",
        "color_strategy": "淡粉、奶白、亮黄",
        "lighting_behavior": "柔和光线，角色脸部明亮",
    }
]

OUTFIT_DIRECTIONS = [plan["outfit_direction"] for plan in ART_DIRECTION_PLANS]

PLAN_TAGS = {
    "heart_signal_closeup": {"closeup", "viewer_interaction", "romance", "high_ctr"},
    "summer_mint_afterglow": {"airy", "summer", "soft_emotion", "clean_color"},
    "idol_stage_dream": {"idol", "performance", "high_color", "viewer_interaction"},
    "moon_confession_fantasy": {"romance", "night", "dream", "viewer_interaction"},
    "floating_room_daydream": {"dream", "floating", "intimate", "soft_emotion"},
    "neon_call_night": {"night_call", "viewer_interaction", "screen_glow", "intimate"},
    "candy_sky_poster": {"poster", "high_color", "thumbnail", "fantasy"},
    "ritual_star_idol": {"ritual", "fantasy", "symbolic", "character_aura"},
    "ultra_minimal_character_poster": {"minimal", "thumbnail", "character_icon", "clean_color"},
    "dream_mist_portrait": {"dream", "soft_emotion", "minimal", "character_aura"},
    "fairytale_pop_storybook": {"fairytale", "high_color", "thumbnail", "cute"},
    "clean_idol_studio_shot": {"studio", "minimal", "thumbnail", "character_icon"},
    "modern_guofeng_character_poster": {"guofeng", "poster", "symbolic", "clean_color"},
}

CHARACTER_PLAN_WEIGHTS = {
    "千夏": {
        "summer_mint_afterglow": 9,
        "floating_room_daydream": 3,
        "heart_signal_closeup": 5,
        "candy_sky_poster": 5,
        "moon_confession_fantasy": 4,
        "neon_call_night": 3,
        "idol_stage_dream": 2,
        "ritual_star_idol": 1,
        "ultra_minimal_character_poster": 5,
        "dream_mist_portrait": 7,
        "fairytale_pop_storybook": 5,
        "clean_idol_studio_shot": 5,
        "modern_guofeng_character_poster": 1,
        "magical_library_day": 0,
    },
    "南宫": {
        "neon_call_night": 8,
        "heart_signal_closeup": 5,
        "ritual_star_idol": 7,
        "moon_confession_fantasy": 3,
        "candy_sky_poster": 4,
        "idol_stage_dream": 4,
        "floating_room_daydream": 3,
        "summer_mint_afterglow": 2,
        "ultra_minimal_character_poster": 5,
        "dream_mist_portrait": 3,
        "fairytale_pop_storybook": 2,
        "clean_idol_studio_shot": 6,
        "modern_guofeng_character_poster": 5,
    },
    "爱芮": {
        "idol_stage_dream": 10,
        "heart_signal_closeup": 8,
        "candy_sky_poster": 8,
        "neon_call_night": 6,
        "floating_room_daydream": 4,
        "moon_confession_fantasy": 3,
        "summer_mint_afterglow": 3,
        "ritual_star_idol": 0,
        "ultra_minimal_character_poster": 4,
        "dream_mist_portrait": 4,
        "fairytale_pop_storybook": 7,
        "clean_idol_studio_shot": 7,
        "modern_guofeng_character_poster": 2,
    },
    "丹": {
        "floating_room_daydream": 9,
        "moon_confession_fantasy": 7,
        "summer_mint_afterglow": 6,
        "candy_sky_poster": 2,
        "heart_signal_closeup": 2,
        "neon_call_night": 0,
        "ritual_star_idol": 2,
        "idol_stage_dream": 0,
        "ultra_minimal_character_poster": 8,
        "dream_mist_portrait": 9,
        "fairytale_pop_storybook": 2,
        "clean_idol_studio_shot": 4,
        "modern_guofeng_character_poster": 6,
    },
    "星见雅": {
        "ritual_star_idol": 9,
        "moon_confession_fantasy": 7,
        "neon_call_night": 5,
        "heart_signal_closeup": 4,
        "candy_sky_poster": 4,
        "idol_stage_dream": 3,
        "summer_mint_afterglow": 2,
        "floating_room_daydream": 2,
        "ultra_minimal_character_poster": 5,
        "dream_mist_portrait": 4,
        "fairytale_pop_storybook": 1,
        "clean_idol_studio_shot": 5,
        "modern_guofeng_character_poster": 8,
    },
    "仪玄": {
        "ritual_star_idol": 10,
        "neon_call_night": 7,
        "moon_confession_fantasy": 6,
        "heart_signal_closeup": 5,
        "candy_sky_poster": 4,
        "floating_room_daydream": 3,
        "idol_stage_dream": 3,
        "summer_mint_afterglow": 1,
        "ultra_minimal_character_poster": 5,
        "dream_mist_portrait": 4,
        "fairytale_pop_storybook": 1,
        "clean_idol_studio_shot": 5,
        "modern_guofeng_character_poster": 9,
    },
}

ACTION_STYLES = [
    {
        "name": "direct_eye_contact",
        "tags": {"viewer_interaction", "closeup", "high_ctr"},
        "body_silhouette": "角色直视 viewer，脸和眼睛是第一焦点，构图以膝上或三分之二身为主，保留肩线、腰线和手部姿态",
        "personality_logic": "用对视建立关系，让观众感觉角色正在看自己，而不是远处摆拍",
        "support_rule": "头发大形、眼睛、发饰、肩线、腰线提示和手部小动作要清楚，缩略图也能读脸",
        "avoid_rule": "不要把人物画太小，不要背对镜头，不要让背景抢走眼神",
    },
    {
        "name": "near_camera_whisper",
        "tags": {"viewer_interaction", "romance", "intimate"},
        "body_silhouette": "角色轻靠近画面中心，像要说悄悄话，肩线、脸部和膝上姿态形成亲近构图，不向镜头压迫",
        "personality_logic": "制造安全亲密感和幻想空间，不靠直白身体暗示",
        "support_rule": "手可以靠近嘴边、耳机或胸前，但不能遮住脸和角色识别点",
        "avoid_rule": "不要成熟化风险，不要高风险服装，不要把视觉焦点集中在身体局部",
    },
    {
        "name": "idol_business_smile",
        "tags": {"idol", "performance", "high_ctr"},
        "body_silhouette": "角色以膝上或三分之二身构图营业微笑，手部动作以扶耳机、轻握麦克风、整理发饰或放在胸前为主，不做指向屏幕的动作",
        "personality_logic": "强化偶像感、点击欲和社交传播亲和力",
        "support_rule": "表情、发饰、服装轮廓、腰线提示和角色色必须在小图里很清楚",
        "avoid_rule": "不要普通证件照，不要僵硬正面站姿，不要廉价自拍滤镜",
    },
    {
        "name": "dreamy_side_glance",
        "tags": {"dream", "soft_emotion", "character_aura"},
        "body_silhouette": "角色侧身回头或半转身，发丝和衣摆轻轻漂浮，眼神有故事感",
        "personality_logic": "用情绪而不是真实动作推动画面，像 Pixiv 收藏向角色图",
        "support_rule": "轮廓要优美，脸部不能被头发完全遮住",
        "avoid_rule": "不要电影截图感，不要复杂建筑透视，不要人物离镜头太远",
    },
    {
        "name": "earpiece_call_gaze",
        "tags": {"night_call", "viewer_interaction", "screen_glow"},
        "body_silhouette": "角色扶耳机、轻碰耳饰或像正在语音通话，视线和 viewer 连接；不出现手持设备",
        "personality_logic": "制造深夜陪伴、秘密聊天和社交平台停滑感，但不依赖手机道具",
        "support_rule": "柔和屏幕光或聊天光晕只服务脸和眼睛，不让 UI 杂乱",
        "avoid_rule": "不要手机，不要手持矩形设备，不要大量文字，不要真实 app 界面",
    },
    {
        "name": "floating_daydream_pose",
        "tags": {"floating", "dream", "soft_emotion"},
        "body_silhouette": "角色在梦境物件中轻坐、半躺或微漂浮，姿态轻盈但身体结构清楚",
        "personality_logic": "表现不合理的美和角色内心世界，而不是物理真实",
        "support_rule": "漂浮物只围绕角色人格展开，不能变成随机杂物",
        "avoid_rule": "不要全身过小，不要复杂房间透视，不要 AI 细节噪音",
    },
    {
        "name": "symbolic_center_pose",
        "tags": {"symbolic", "fantasy", "thumbnail"},
        "body_silhouette": "角色位于视觉符号中心，姿态从容，背后有巨大圆形、星图或光环",
        "personality_logic": "让角色像封面主视觉，世界从她的气质中长出来",
        "support_rule": "大符号要托举角色，不要压小角色；脸、肩线、腰线和膝上姿态必须可读",
        "avoid_rule": "不要 AAA key visual，不要西式概念图废墟，不要把角色变成比例尺",
    },
]

CHARACTER_ACTION_WEIGHTS = {
    "千夏": {
        "direct_eye_contact": 6,
        "near_camera_whisper": 2,
        "dreamy_side_glance": 8,
        "floating_daydream_pose": 8,
        "earpiece_call_gaze": 1,
        "idol_business_smile": 3,
        "symbolic_center_pose": 5,
    },
    "南宫": {
        "direct_eye_contact": 7,
        "earpiece_call_gaze": 4,
        "near_camera_whisper": 1,
        "symbolic_center_pose": 8,
        "dreamy_side_glance": 6,
        "idol_business_smile": 2,
        "floating_daydream_pose": 4,
    },
    "爱芮": {
        "idol_business_smile": 10,
        "direct_eye_contact": 6,
        "near_camera_whisper": 2,
        "earpiece_call_gaze": 2,
        "floating_daydream_pose": 6,
        "dreamy_side_glance": 5,
        "symbolic_center_pose": 6,
    },
    "丹": {
        "dreamy_side_glance": 8,
        "floating_daydream_pose": 8,
        "near_camera_whisper": 0,
        "direct_eye_contact": 5,
        "symbolic_center_pose": 4,
        "earpiece_call_gaze": 0,
        "idol_business_smile": 0,
    },
    "星见雅": {
        "symbolic_center_pose": 9,
        "direct_eye_contact": 7,
        "dreamy_side_glance": 6,
        "near_camera_whisper": 1,
        "earpiece_call_gaze": 1,
        "idol_business_smile": 2,
        "floating_daydream_pose": 2,
    },
    "仪玄": {
        "symbolic_center_pose": 10,
        "earpiece_call_gaze": 2,
        "direct_eye_contact": 6,
        "near_camera_whisper": 0,
        "dreamy_side_glance": 5,
        "floating_daydream_pose": 3,
        "idol_business_smile": 2,
    },
}

COOLDOWN_TAG_BLOCKS = {
    "viewer_interaction": {"viewer_interaction", "closeup"},
    "closeup": {"closeup", "viewer_interaction"},
    "romance": {"romance", "intimate"},
    "intimate": {"romance", "intimate"},
    "idol": {"idol", "performance"},
    "performance": {"idol", "performance"},
    "dream": {"dream", "floating"},
    "floating": {"dream", "floating"},
    "night_call": {"night_call", "screen_glow"},
    "screen_glow": {"night_call", "screen_glow"},
    "symbolic": {"symbolic", "ritual"},
    "high_color": {"high_color", "poster"},
    "minimal": {"minimal", "character_icon"},
}


CHARACTER_OUTFIT_VARIATIONS = {
    "丹": [
        "月白短披肩 + 浅粉内搭 + 银蓝细腰带 + 轻薄裙裤，保留安静未来感但不要像固定圣女制服",
        "透明感短风衣 + 奶白高腰短裙裤 + 星形发卡呼应，整体像收藏级梦境私服",
        "柔软针织开衫 + 浅紫吊带内搭 + 云朵感短裙，偏居家梦境但保持清爽轮廓",
        "未来学院感短外套 + 干净领结 + 银灰百褶裙裤，弱化圣堂感，强化青春空气感",
        "轻量机能披肩 + 粉白短夹克 + 蓝银小扣件，只有少量未来细节，不堆机械零件",
        "现代改良国风短披帛 + 淡粉盘扣上衣 + 奶白裙裤，国风只做轮廓和材质，不变古装",
        "睡前通话感宽松衬衫外套 + 软质短裙裤 + 小星星袜饰，安静亲近但不过度日常",
        "摄影棚干净套装：短款白色外套 + 浅粉内搭 + 银灰腰线，适合封面级角色图",
        "梦境水色连帽短外套 + 透明小饰件 + 浅色裙裤，像雨后空气，不重复圣女披肩",
        "浅色偶像练习室私服：短夹克 + 柔软百褶裙裤 + 细银饰，保留丹的淡漠感",
        "极简海报服装：无装饰纯色上衣 + 一处星形小扣 + 清楚腰线，用色块而不是复杂服饰出效果",
        "薄纱叠层短外套 + 轻盈不对称裙摆 + 透明书本小配件，梦幻但不固定成白袍",
    ],
}


CHARACTER_PROPAGATION_PROFILES = {
    "南宫": {
        "official_core": "天才队长、舞台控制者、节奏调度、小恶魔式压迫感；她知道自己处于画面中心。",
        "propagation_translation": "playful controller idol：她不是向 viewer 撒娇，而是在调度 viewer，把观众拉进自己的节奏里。",
        "viewer_relationship": "轻挑衅对视、主导镜头、像已经看穿 viewer；关系感是“你被她锁定/选中”。",
        "interaction_rule": "她调度 viewer。画面关系是命令、锁定、控场和轻挑衅，不是撒娇或求关注。",
        "thumbnail_strategy": "脸 + 黑发齐刘海 + 粉色渐变短双马尾 + 坏笑 + 科技光环/猫发夹/背后光片 + 中性背景里的粉黑小面积强记忆点；背后光片为可选符号，不固定成背翼形态。",
        "thumbnail_modes": ["膝上控场型", "表情命令型", "符号锁定型", "极简头像型"],
        "primary_hook_symbols": ["科技光环", "节奏 UI", "猫发夹", "坏笑表情"],
        "secondary_support_symbols": ["背后小型机械光片", "粉黑舞台光", "心跳波形"],
        "fantasy_symbols": ["节奏线", "combo UI", "心跳波形", "粉黑舞台光", "背后小型机械光片", "猫元素", "环绕式科技光环"],
        "safe_sensuality": "可以有小恶魔挑衅和镜头主导感，但不要走害羞软妹或直白身体暗示。",
        "preferred_hooks": {"neon_call_night", "ritual_star_idol", "idol_stage_dream", "ultra_minimal_character_poster", "clean_idol_studio_shot", "modern_guofeng_character_poster"},
        "preferred_actions": {"direct_eye_contact", "dreamy_side_glance", "symbolic_center_pose"},
        "suppressed_misreads": ["害羞软妹", "普通粉黑主播", "普通 JK 日常", "低幼萌妹", "普通粉毛偶像", "可爱甜笑自拍", "无目的大脸自拍"],
    },
    "爱芮": {
        "official_core": "高能量舞台偶像、粉丝互动、梦境/妄想扩散、电子偶像式传播。",
        "propagation_translation": "high-energy idol romance signal：她主动靠近 viewer，用舞台感、直播感和恋爱营业感制造停滑。",
        "viewer_relationship": "像正在对 viewer 做一场只属于一个人的偶像营业；粉丝被点名、被靠近、被回应。",
        "interaction_rule": "她主动营业 viewer。画面关系是扑向观众、回应粉丝、制造恋爱信号，不是调度或压迫 viewer。",
        "thumbnail_strategy": "脸 + 粉色双马尾 + 黑色挑染刘海 + 爱心 UI + 耳机发饰 + 粉色舞台背光/机械光片 + 明亮粉黑色块；背后光片为可选符号，不固定成背翼形态。",
        "thumbnail_modes": ["表情营业型", "膝上舞台型", "小道具互动型", "高色块海报型"],
        "primary_hook_symbols": ["爱心环", "麦克风", "直播 UI", "wink/对视"],
        "secondary_support_symbols": ["粉色舞台背光", "耳机线", "idol spotlight"],
        "fantasy_symbols": ["爱心轨道", "粉黑霓虹", "漂浮歌词 UI", "直播弹幕气泡", "耳机线", "小恶魔尾巴暗示", "idol spotlight"],
        "safe_sensuality": "允许安全恋爱感、锁骨、耳机线、轻微汗光和镜头交流；吸引力来自心动和互动，不来自过度身体展示。",
        "preferred_hooks": {"idol_stage_dream", "heart_signal_closeup", "candy_sky_poster", "neon_call_night", "fairytale_pop_storybook", "clean_idol_studio_shot"},
        "preferred_actions": {"idol_business_smile", "direct_eye_contact", "symbolic_center_pose"},
        "suppressed_misreads": ["普通粉毛萌妹", "低气压神性", "大远景孤独感", "直白身体暗示", "只靠服装刺激制造吸引力"],
    },
    "千夏": {
        "official_core": "严格贴合参考图身份：薄荷绿中短层次发、后发自然散开、偏右小揪发和大号薄荷蝴蝶结、厚重不对称刘海、黑色心形耳饰、粉金渐变瞳。她是紧张但认真、清透、努力装镇定的青春陪伴感角色。",
        "propagation_translation": "mint clear companion：她不是强营业角色，也不靠学习记录类道具定义角色，而是让 viewer 感到清透、认真、慢慢靠近。",
        "viewer_relationship": "像在夏日空气里小心靠近 viewer；安静、清透、紧张但真诚的陪伴感。",
        "interaction_rule": "她小心靠近 viewer。画面关系是陪伴、递出情绪、慢慢靠近，不是强营业或攻击性自拍。",
        "thumbnail_strategy": "脸 + 薄荷中短层次发 + 偏右小揪发 + 大号薄荷蝴蝶结 + 厚重不对称刘海 + 心形耳饰 + 清透夏日大色块。",
        "thumbnail_modes": ["参考图还原型", "清透膝上型", "窗边陪伴型", "极简薄荷头像型"],
        "primary_hook_symbols": ["大号薄荷蝴蝶结", "偏右小揪发", "心形耳饰", "薄荷色风"],
        "secondary_support_symbols": ["透明饮料", "水光", "发光云"],
        "fantasy_symbols": ["大号薄荷蝴蝶结", "偏右小揪发", "心形耳饰", "透明饮料", "薄荷色风", "水面反射", "发光云", "透明窗帘"],
        "safe_sensuality": "以青春陪伴和空气感为主，可以亲近但不要强自拍压脸、成熟魅惑或偶像大营业。",
        "preferred_hooks": {"summer_mint_afterglow", "floating_room_daydream", "heart_signal_closeup", "candy_sky_poster", "dream_mist_portrait", "fairytale_pop_storybook"},
        "preferred_actions": {"dreamy_side_glance", "direct_eye_contact", "floating_daydream_pose", "symbolic_center_pose"},
        "suppressed_misreads": ["普通元气偶像", "粉色强营业甜妹", "成熟魅惑角色", "暗黑工业感", "低幼卖萌", "学习记录类道具场景", "桌面记录场景", "双马尾化", "普通短发化", "丢失大号薄荷蝴蝶结"],
    },
    "丹": {
        "official_core": "项目原创人格：浅粉短发、粉紫眼、安静温柔、略淡漠、未来感与透明梦境气质；服装不能固定成同一套圣女制服。",
        "propagation_translation": "quiet sacred dream poster：她不主动营业，而是用安静、梦境、神性和距离感制造收藏欲。",
        "viewer_relationship": "像从安静梦境里看向 viewer；半距离感、透明未来感、淡淡情绪。",
        "interaction_rule": "她安静凝视 viewer。画面关系是梦境里的轻微注视和收藏感，不是主动营业、自拍或暧昧邀约。",
        "thumbnail_strategy": "脸 + 浅粉短发 + 粉紫眼 + 白银光环/羽毛/月亮/水面 + 大面积干净浅色。",
        "thumbnail_modes": ["安静大脸型", "枕头梦境型", "浅色收藏海报型", "极简圣洁头像型"],
        "primary_hook_symbols": ["枕头梦境", "羽毛", "白银光环", "月亮"],
        "secondary_support_symbols": ["星形发卡", "透明书本", "水面"],
        "fantasy_symbols": ["白银光环", "羽毛", "水面", "月亮", "镜面", "星形发卡", "轻机械模块", "透明圣堂", "梦境云层"],
        "safe_sensuality": "不做强营业、不做高风险暧昧；吸引力来自安静神性、收藏海报感和不完全属于现实的距离。避免成熟御姐化、过度强调身材和身体局部焦点。",
        "preferred_hooks": {"moon_confession_fantasy", "floating_room_daydream", "summer_mint_afterglow", "ultra_minimal_character_poster", "dream_mist_portrait", "modern_guofeng_character_poster"},
        "preferred_actions": {"dreamy_side_glance", "floating_daydream_pose", "direct_eye_contact"},
        "suppressed_misreads": ["普通白毛圣女", "成熟御姐化", "过度强调身材", "自拍主播", "粉色偶像营业", "高风险暧昧", "身体局部焦点"],
    },
    "星见雅": {
        "official_core": "冷静严肃的剑客气质，黑色长直发、厚重齐刘海、黑色兽耳、红眼是核心记忆点；刀线或武器意象是可选强化符号，不要求每张出现实体武器。",
        "propagation_translation": "cool blade heroine icon：她的传播钩子是冷静、危险、优雅和一眼记住的黑红剪影。",
        "viewer_relationship": "她不是热情营业，而是用极稳的对视让 viewer 感到被判断、被锁定。",
        "interaction_rule": "她锁定 viewer。画面关系是冷静判断和危险吸引，不是甜美互动。",
        "thumbnail_strategy": "脸 + 黑长直齐刘海 + 黑色兽耳 + 红眼 + 黑红高辨识幻想符号；可用刀线、红色光轨或月形剪影强化压迫感，不固定实体武器。",
        "thumbnail_modes": ["黑红大脸型", "刀线符号型", "冷静半身型", "极简黑红头像型"],
        "primary_hook_symbols": ["红眼", "黑色兽耳", "黑红月亮", "红色刀线光轨"],
        "secondary_support_symbols": ["细红光轨", "风中长发", "星图圆环"],
        "fantasy_symbols": ["刀线高光", "黑红月亮", "兽耳剪影", "细红光轨", "星图圆环", "风中长发"],
        "safe_sensuality": "保持冷艳和剑客压迫，不做软妹化、卖萌化或廉价魅惑。",
        "preferred_hooks": {"ritual_star_idol", "moon_confession_fantasy", "neon_call_night", "heart_signal_closeup", "modern_guofeng_character_poster", "clean_idol_studio_shot"},
        "preferred_actions": {"symbolic_center_pose", "direct_eye_contact", "dreamy_side_glance"},
        "suppressed_misreads": ["短发", "卷发", "蓬松偶像发型", "丢失黑色兽耳识别", "普通武器少女模板", "软妹化"],
    },
    "仪玄": {
        "official_core": "银白长发、黑色波浪/闪电状发饰、金/琥珀眼、成熟从容是核心记忆点；黑色灵鸟是可选神秘符号，不要求每张都实体出现。",
        "propagation_translation": "mature occult charm signal：她用从容、戏谑和灵鸟符号制造神秘吸引力。",
        "viewer_relationship": "像在轻松掌控 viewer 的注意力；不是强营业，而是成熟、游刃有余、带一点戏谑。",
        "interaction_rule": "她轻松掌控 viewer。画面关系是成熟从容、戏谑和神秘吸引，不是甜妹营业。",
        "thumbnail_strategy": "脸 + 银白长发 + 黑色闪电发饰 + 金色眼睛 + 金黑高识别幻想符号；可用灵鸟剪影、羽状黑影或金色术光强化神秘感。",
        "thumbnail_modes": ["金黑大脸型", "灵鸟符号型", "成熟半身型", "极简银白头像型"],
        "primary_hook_symbols": ["金色眼睛", "黑色闪电发饰", "金色术光", "灵鸟剪影"],
        "secondary_support_symbols": ["符号圆环", "银白长发光边", "夜色星图"],
        "fantasy_symbols": ["黑色灵鸟", "金色术光", "黑色闪电线", "符号圆环", "银白长发光边", "夜色星图"],
        "safe_sensuality": "可以成熟、有距离、有压迫，但不要少女化、甜妹化或过度暧昧化。",
        "preferred_hooks": {"ritual_star_idol", "neon_call_night", "moon_confession_fantasy", "heart_signal_closeup", "modern_guofeng_character_poster", "clean_idol_studio_shot"},
        "preferred_actions": {"symbolic_center_pose", "direct_eye_contact", "dreamy_side_glance"},
        "suppressed_misreads": ["短发", "少女化", "过度甜美", "丢失黑色发饰识别", "普通神秘法师模板"],
    },
}


def outfit_variation_for(character_name: str, plan_name: str | None = None) -> str:
    character = _primary_character(character_name)
    variations = CHARACTER_OUTFIT_VARIATIONS.get(character)
    if not variations:
        return ""
    return random.choice(variations)


def propagation_profile_for(character_name: str) -> dict:
    character = _primary_character(character_name)
    return CHARACTER_PROPAGATION_PROFILES.get(character, CHARACTER_PROPAGATION_PROFILES["丹"])


def _profile_adjusted_weight(item_name: str, base_weight: int, preferred: set[str]) -> int:
    weight = int(base_weight)
    if item_name in preferred:
        weight += 5
    return weight


def choose_art_plan(character_name: str | None = None, recent_tags: list[str] | None = None) -> dict:
    character = _primary_character(character_name or "丹")
    profile = propagation_profile_for(character)
    weights_by_name = CHARACTER_PLAN_WEIGHTS.get(character, CHARACTER_PLAN_WEIGHTS["丹"])
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for plan in ART_DIRECTION_PLANS:
        tags = PLAN_TAGS.get(plan["name"], set())
        if tags & blocked:
            continue
        weight = weights_by_name.get(plan["name"], 1)
        if weight <= 0:
            continue
        candidates.append(plan)
        weights.append(_profile_adjusted_weight(plan["name"], weight, profile["preferred_hooks"]))
    if not candidates:
        candidates = [plan for plan in ART_DIRECTION_PLANS if weights_by_name.get(plan["name"], 1) > 0]
        weights = [
            _profile_adjusted_weight(plan["name"], weights_by_name.get(plan["name"], 1), profile["preferred_hooks"])
            for plan in candidates
        ]
    return _weighted_choice(candidates, weights)


def choose_action_style(character_name: str, recent_tags: list[str] | None = None) -> dict:
    character = _primary_character(character_name)
    profile = propagation_profile_for(character)
    weights_by_name = CHARACTER_ACTION_WEIGHTS.get(character, CHARACTER_ACTION_WEIGHTS["丹"])
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for action in ACTION_STYLES:
        if action["tags"] & blocked:
            continue
        weight = weights_by_name.get(action["name"], 0)
        if weight <= 0:
            continue
        candidates.append(action)
        weights.append(_profile_adjusted_weight(action["name"], weight, profile["preferred_actions"]))
    if not candidates:
        candidates = [action for action in ACTION_STYLES if weights_by_name.get(action["name"], 0) > 0]
        weights = [
            _profile_adjusted_weight(action["name"], weights_by_name.get(action["name"], 0), profile["preferred_actions"])
            for action in candidates
        ]
    return _weighted_choice(candidates, weights)


# ---------------------------------------------------------------------------
# Extra scene / outfit theme expansion
# 追加位置建议：放在 art_direction_options.py 文件末尾。
# 只追加新场景、新标签、新角色权重、新服装变体；不改 build_prompt、动作逻辑和自动化脚本。
# ---------------------------------------------------------------------------

EXTRA_SCENE_PLANS = [{'name': 'neon_call_night',
  'graphic_concept': '深夜通话感角色图：屏幕光、耳机线和小型聊天光晕把 viewer 拉进一对一陪伴场景',
  'spatial_structure': '夜色房间或城市窗边被压成蓝紫色块，背景只保留柔和灯点和窗外光斑，角色占据膝上到三分之二身主视觉',
  'visual_device': 'primary hook 只选一个：发光耳机线 / 通话光晕 / 窗边夜色；secondary support 只选一个：小聊天气泡 / 柔蓝补光 / 远处灯点',
  'body_silhouette': '角色轻扶耳机或发饰，视线连接 viewer，手部动作靠近脸侧或胸前，保持清楚五指结构',
  'outfit_direction': '深夜通话感私服：宽松短外套、柔软内搭、高腰裙裤、耳机或发饰小配件，轮廓亲近但干净',
  'material_language': '柔软棉布、磨砂亚克力、耳机线微光、细小金属扣',
  'color_strategy': '蓝紫夜色托脸，角色识别色集中在头发、发饰、领口或耳机线，整体干净不脏暗',
  'lighting_behavior': '柔和屏幕光照亮脸和眼睛，边缘有轻微夜色反光，暗部保持透明'},
 {'name': 'arcade_prize_date',
  'graphic_concept': '游戏厅约会感：夹娃娃机、奖品灯箱和角色笑意形成高点击二次元日常',
  'spatial_structure': '游戏厅背景被简化成粉蓝灯箱、大色块机器和少量圆形高光，不展开复杂店内透视',
  'visual_device': 'primary hook 只选一个：毛绒奖品 / 游戏币 / 发光按钮；secondary support 只选一个：粉蓝灯箱 / 小星点 / 透明亚克力反光',
  'body_silhouette': '角色膝上或三分之二身靠近机器侧边，手握小奖品或游戏币，姿态轻快但不冲镜头',
  'outfit_direction': '游戏厅约会私服：短款夹克、轻甜内搭、高腰短裙或裙裤、厚底鞋袜和一个小型玩具配饰',
  'material_language': '亮面贴纸、透明亚克力、柔软毛绒、棉质短外套',
  'color_strategy': '粉蓝、奶白、亮黄和角色主色形成明亮记忆点，背景亮但不抢脸',
  'lighting_behavior': '灯箱柔光和店内漫射光混合，眼睛与发色高光清楚'},
 {'name': 'gacha_capsule_corner',
  'graphic_concept': '扭蛋角落的收集欲：透明胶囊、迷你奖品和角色表情构成可收藏画面',
  'spatial_structure': '扭蛋机圆形阵列变成背景图形，机器细节压缩成圆点节奏和大色块',
  'visual_device': 'primary hook 只选一个：透明扭蛋胶囊 / 小奖品 / 圆形按钮；secondary support 只选一个：机器圆阵列 / 彩色贴纸 / 柔光反射',
  'body_silhouette': '角色半蹲或侧身回头，手里轻握胶囊，脸和发型保持第一视觉锚点',
  'outfit_direction': '轻快街头可爱私服：短卫衣或短夹克、高腰裙裤、彩色袜饰和一个圆形小配件',
  'material_language': '透明塑料、亮面贴纸、软棉布、少量金属边',
  'color_strategy': '糖果色圆点背景配角色识别色，色彩明亮但层级清楚',
  'lighting_behavior': '店内柔光加透明胶囊小高光，脸部干净明亮'},
 {'name': 'game_ui_battle_select',
  'graphic_concept': '游戏角色选择界面感：角色像被选中进入队伍，UI 只作为干净图形支撑',
  'spatial_structure': '背景是抽象选择界面、发光卡片框和角色色块，不出现真实游戏文字或 logo',
  'visual_device': 'primary hook 只选一个：选中框 / 能量卡片 / 角色图标光环；secondary support 只选一个：细 UI 线 / 圆形按钮 / 半透明面板',
  'body_silhouette': '角色三分之二身或膝上站在卡片框前，姿态像封面主视觉，表情明确',
  'outfit_direction': '游戏活动限定服：短披肩、收腰外套、裙摆或裙裤、少量发光边和角色专属小徽章',
  'material_language': '半透明面板、亮面织物、细金属饰件、柔软内搭',
  'color_strategy': '角色主色加一种高对比辅助色，UI 降低透明度，只托出人物轮廓',
  'lighting_behavior': '前方柔光保证脸部，背后选择框提供轮廓光，不做硬核科幻厚重感'},
 {'name': 'rpg_town_square_festival',
  'graphic_concept': '明亮 RPG 小镇节日：彩旗、摊位和幻想小物围绕角色，像游戏活动插画',
  'spatial_structure': '小镇广场被压成圆形喷泉、彩旗和浅色屋顶色块，透视简化，角色是主视觉',
  'visual_device': 'primary hook 只选一个：节日彩旗 / 小喷泉 / 活动徽章；secondary support 只选一个：摊位灯 / 花瓣 / 软色块',
  'body_silhouette': '角色站在画面中近景或轻侧身，手持小甜点、花束或活动徽章，姿态清楚',
  'outfit_direction': '幻想小镇节日服：短斗篷或小披肩、蝴蝶结、轻裙摆或裙裤、柔软靴袜组合',
  'material_language': '棉麻、软皮革、丝带、少量金属小扣',
  'color_strategy': '奶白、天空蓝、暖黄和角色色形成快乐但不低幼的游戏节日感',
  'lighting_behavior': '晴天柔光和节日小灯点，脸部与眼睛最亮'},
 {'name': 'pixel_cloud_savepoint',
  'graphic_concept': '像素云存档点：云朵、发光存档水晶和角色安静站姿形成游戏幻想封面',
  'spatial_structure': '天空、云层和平台被平面化成大色块，存档点作为唯一幻想装置',
  'visual_device': 'primary hook 只选一个：存档水晶 / 像素云 / 发光平台；secondary support 只选一个：小星点 / 方块光粒 / 柔色圆环',
  'body_silhouette': '角色站立、轻坐或侧身回头，身体轮廓稳定，画面有可爱游戏 UI 空气但没有文字',
  'outfit_direction': '云端游戏冒险服：轻短外套、柔软裙裤、小披肩或袜靴，带一点像素色块装饰',
  'material_language': '柔软布料、半透明水晶、方块光粒、雾面渐变',
  'color_strategy': '天空蓝、奶白、淡紫和角色识别色组成清爽高记忆色盘',
  'lighting_behavior': '云层漫射光包裹角色，存档水晶只提供小范围补光'},
 {'name': 'storybook_castle_balcony',
  'graphic_concept': '童话城堡阳台：圆窗、花藤和天空色块托出角色，不做复杂古堡背景',
  'spatial_structure': '阳台栏杆、圆窗和花藤被设计成简洁图形框，背景只保留天空和远处城堡剪影',
  'visual_device': 'primary hook 只选一个：圆窗 / 小皇冠 / 花藤；secondary support 只选一个：云朵 / 星点 / 飘带',
  'body_silhouette': '角色膝上到三分之二身倚在阳台边，轻回头或微笑，动作优雅清楚',
  'outfit_direction': '童话约会小礼服：短披肩、简洁领口、轻盈裙摆或裙裤、一个小皇冠或花饰重点',
  'material_language': '薄纱、软缎、丝带、圆润金属小饰件',
  'color_strategy': '奶白、淡粉、天空蓝或浅金与角色色融合，画面明亮柔软',
  'lighting_behavior': '童话棚光和天空柔光并存，脸与发型最清楚'},
 {'name': 'fairy_tale_bookshop',
  'graphic_concept': '童话书店约会：发光绘本、书页小精灵和角色眼神形成温柔收藏感',
  'spatial_structure': '书架被压成暖色大色块，前景只保留一本发光书或小书签作为核心装置',
  'visual_device': 'primary hook 只选一个：发光绘本 / 书签丝带 / 小精灵光点；secondary support 只选一个：暖色书架 / 窗光 / 小花纹',
  'body_silhouette': '角色坐在书店角落或轻靠书架，手部轻扶书页，表情安静亲近',
  'outfit_direction': '书店约会私服：柔软针织、短外套、高腰裙裤、书签或小蝴蝶结配饰',
  'material_language': '纸张暖光、针织、棉布、细丝带、磨砂玻璃',
  'color_strategy': '奶茶色、浅粉、薄荷或淡紫承托角色发色，整体温暖不昏暗',
  'lighting_behavior': '窗边自然光加绘本微光，眼睛和脸部保持清楚'},
 {'name': 'blooming_flower_cart',
  'graphic_concept': '街角花车日常：花束、透明包装纸和角色发色形成柔软高收藏插画',
  'spatial_structure': '街角背景简化成花车、伞棚和浅色墙面，花朵作为大色块而不是碎细节',
  'visual_device': 'primary hook 只选一个：大花束 / 透明包装纸 / 小花车；secondary support 只选一个：软伞棚 / 花瓣 / 暖色光斑',
  'body_silhouette': '角色抱花、侧身回头或站在花车旁，手部被花束自然简化，脸部不被遮挡',
  'outfit_direction': '花车日常服：短开衫、轻衬衫、高腰裙裤、透明花束包装与小发饰呼应',
  'material_language': '棉布、薄纱、透明包装纸、柔软花瓣、木质小车色块',
  'color_strategy': '花色只保留两三组主色，角色色是第一记忆点，背景保持浅色空气',
  'lighting_behavior': '午后柔光和花束反射光，脸部明亮，阴影干净'},
 {'name': 'seaside_date_kiosk',
  'graphic_concept': '海边小卖部约会：汽水、海风和蓝白遮阳棚让角色变成夏日封面',
  'spatial_structure': '海、天空和小卖部棚顶压成三层色块，空间开阔但角色占据主视觉',
  'visual_device': 'primary hook 只选一个：透明汽水瓶 / 蓝白遮阳棚 / 海风发丝；secondary support 只选一个：波光 / 小贝壳 / 云朵',
  'body_silhouette': '角色坐在高脚凳、靠近柜台或轻回头，手持汽水，姿态清爽自然',
  'outfit_direction': '海边约会私服：短衬衫、轻薄外套、高腰裙裤、凉鞋或轻运动鞋，透明小饰件点缀',
  'material_language': '棉麻、透明玻璃、湿润波光、轻薄布料',
  'color_strategy': '海蓝、奶白、淡黄和角色色形成高明度夏日记忆',
  'lighting_behavior': '海边明亮漫射光，发丝和眼睛有清楚高光'},
 {'name': 'aquarium_blue_date',
  'graphic_concept': '水族馆蓝色约会：鱼群光影和角色侧脸制造安静心动感',
  'spatial_structure': '巨大水槽被简化成蓝色发光墙，鱼群只做剪影节奏，角色靠近前景',
  'visual_device': 'primary hook 只选一个：鱼群剪影 / 水波光 / 透明水母；secondary support 只选一个：蓝色光墙 / 小气泡 / 柔亮边光',
  'body_silhouette': '角色侧身看向水槽或回头看 viewer，手部靠近玻璃但不贴近镜头',
  'outfit_direction': '水族馆约会服：柔软短外套、轻裙摆或裙裤、透明蓝色小饰件和干净领口',
  'material_language': '玻璃反射、软针织、透明亚克力、水波光纹',
  'color_strategy': '深浅蓝作为环境，角色发色和眼睛是第一阅读点，局部用暖色制造心动感',
  'lighting_behavior': '水波柔光从侧面包裹脸和头发，背景保持干净蓝色'},
 {'name': 'train_window_weekend',
  'graphic_concept': '周末电车窗边日常：窗外流动色块和角色安静表情形成旅行前一刻',
  'spatial_structure': '车窗、座椅和窗外风景压缩成横向色块，空间清楚但不写实堆细节',
  'visual_device': 'primary hook 只选一个：车窗反光 / 小票根 / 旅行饮料；secondary support 只选一个：窗外云 / 座椅色块 / 柔光线',
  'body_silhouette': '角色坐在窗边或侧身回头，手部轻握票根或饮料，姿态稳定亲近',
  'outfit_direction': '周末出行私服：短外套、柔软上衣、高腰裙裤、肩包或小票根配饰，清楚腰线和领口',
  'material_language': '棉布、软皮肩带、玻璃反光、纸张小物',
  'color_strategy': '奶白、浅蓝、灰粉或角色色组合，形成舒适日常封面',
  'lighting_behavior': '窗边大面积自然光，脸和眼睛明亮，车厢暗部简化'},
 {'name': 'laundry_sun_room',
  'graphic_concept': '阳光洗衣房日常：白衬布、泡泡和光斑形成干净生活感二次元画面',
  'spatial_structure': '洗衣房被简化成白色布料、圆形洗衣机窗和阳光色块，背景不杂乱',
  'visual_device': 'primary hook 只选一个：白衬布 / 圆形洗衣机窗 / 泡泡；secondary support 只选一个：阳光光斑 / 小夹子 / 柔色墙面',
  'body_silhouette': '角色抱着柔软衣物或坐在洗衣篮旁，手被布料自然简化，表情明亮亲近',
  'outfit_direction': '清洁感居家私服：宽松短衬衫、柔软内搭、高腰短裤或软裙、袜饰和小发夹',
  'material_language': '白棉布、柔软毛巾、透明泡泡、磨砂塑料圆窗',
  'color_strategy': '白、奶油黄、浅蓝和角色色形成干净生活感，不变灰脏',
  'lighting_behavior': '午后阳光和室内柔光，布料反光托亮脸部'},
 {'name': 'bakery_morning_window',
  'graphic_concept': '清晨面包店约会：暖光、纸袋和玻璃橱窗让角色有柔软生活气',
  'spatial_structure': '橱窗、木质柜台和街景被压成暖色块，食物只做少量图形点缀',
  'visual_device': 'primary hook 只选一个：面包纸袋 / 橱窗反光 / 小托盘；secondary support 只选一个：晨光 / 暖色灯点 / 细小花纹',
  'body_silhouette': '角色轻靠柜台或抱纸袋回头，手部动作简单，表情温柔清楚',
  'outfit_direction': '清晨约会私服：短开衫、柔软衬衫、高腰裙裤、围巾或小包作为一个重点配饰',
  'material_language': '纸袋纹理、针织、棉布、玻璃暖反光',
  'color_strategy': '奶油棕、暖白、淡粉或角色色构成温柔食物系色盘',
  'lighting_behavior': '清晨窗光加面包店暖光，脸部不偏黄，眼睛保持通透'},
 {'name': 'theme_park_twilight',
  'graphic_concept': '游乐园黄昏约会：旋转木马灯、气球和角色表情形成高传播幻想日常',
  'spatial_structure': '游乐设施被压成圆形灯点和大色块剪影，背景梦幻但不拥挤',
  'visual_device': 'primary hook 只选一个：旋转木马灯 / 气球 / 游乐票；secondary support 只选一个：黄昏天空 / 小星灯 / 彩色旗帜',
  'body_silhouette': '角色站在灯点前或侧身回头，手握气球绳或票根，姿态清楚甜美',
  'outfit_direction': '游乐园约会服：短外套、轻裙摆或裙裤、发饰和小包，整体明亮可爱但有设计感',
  'material_language': '亮面小饰件、柔软布料、纸票、气球反光',
  'color_strategy': '黄昏橙粉、奶白、蓝紫和角色色形成梦幻停滑色彩',
  'lighting_behavior': '黄昏逆光加游乐园小灯补光，脸和发型保持第一阅读'},
 {'name': 'rainy_clear_umbrella_date',
  'graphic_concept': '雨天透明伞约会：水滴、伞面反光和角色眼神形成温柔心动图',
  'spatial_structure': '街道背景压成浅灰蓝色块和少量灯点，透明伞是主要空间框架',
  'visual_device': 'primary hook 只选一个：透明雨伞 / 水滴 / 小雨靴；secondary support 只选一个：路灯光斑 / 湿润地面 / 柔蓝空气',
  'body_silhouette': '角色握伞站立或轻回头，手部被伞柄简化，身体稳定，脸不被伞骨遮挡',
  'outfit_direction': '雨天约会私服：防水短外套、柔软裙裤、设计感雨靴或袜靴、一个透明小配饰',
  'material_language': '透明 PVC、湿润布料、柔软针织、细小水滴高光',
  'color_strategy': '浅灰蓝雨色配角色识别色，局部暖光制造约会感，不进入暗黑雨夜',
  'lighting_behavior': '阴天柔光和路灯微暖补光，透明伞反光托出脸部'},
 {'name': 'pajama_game_party',
  'graphic_concept': '居家游戏会：手柄、抱枕和零食小物围绕角色，形成轻松可爱的直播前画面',
  'spatial_structure': '房间被简化成沙发、地毯和屏幕色块，物件数量少而清楚，角色占画面主体',
  'visual_device': 'primary hook 只选一个：游戏手柄 / 抱枕 / 发光屏幕色块；secondary support 只选一个：小零食 / 贴纸 / 柔光灯串',
  'body_silhouette': '角色坐在地毯或沙发边，手持手柄或抱枕，表情有陪玩感，手部不复杂张开',
  'outfit_direction': '居家游戏私服：宽松短外套、软质短裤或裙裤、袜子、可爱发夹或小抱枕配饰',
  'material_language': '毛绒、棉布、磨砂塑料手柄、柔光灯串',
  'color_strategy': '奶油白、粉蓝、薰衣草紫和角色色组成舒适高点击色盘',
  'lighting_behavior': '室内柔光加屏幕冷光，脸和眼睛比屏幕更清楚'},
 {'name': 'idol_practice_mirror_clean',
  'graphic_concept': '偶像练习室的干净瞬间：镜面、毛巾和水瓶形成努力感，而不是舞台大爆炸',
  'spatial_structure': '练习室镜面和地面线条被简化成干净几何，背景只有少量反射色块',
  'visual_device': 'primary hook 只选一个：镜面反射 / 练习水瓶 / 毛巾；secondary support 只选一个：地面光线 / 简洁音响 / 柔色墙面',
  'body_silhouette': '角色膝上到三分之二身，刚练习完轻微回头或整理发饰，身体线条清楚',
  'outfit_direction': '偶像练习室私服：短运动外套、修身内搭、高腰裙裤、干净运动鞋袜和一个小毛巾配饰',
  'material_language': '弹力布、棉质毛巾、镜面反射、磨砂水瓶',
  'color_strategy': '白、浅灰、角色主色和一个高纯点缀色，干净专业但不男性化',
  'lighting_behavior': '练习室柔光和镜面补光，脸部清楚，身体结构稳定'},
 {'name': 'planetarium_soft_date',
  'graphic_concept': '天文馆柔软约会：星空穹顶、座椅暗色块和角色眼神形成安静幻想感',
  'spatial_structure': '星空穹顶变成大面积圆弧色块，座椅只保留简洁暗部轮廓，角色靠近前景',
  'visual_device': 'primary hook 只选一个：星空穹顶 / 小星图票根 / 投影光点；secondary support 只选一个：圆弧光线 / 暖色座椅 / 小星点',
  'body_silhouette': '角色坐在座椅边或侧身回头，手握票根或轻触发饰，姿态安静亲近',
  'outfit_direction': '天文馆约会服：轻披肩、柔软短外套、高腰裙裤、星形小饰件和干净领口',
  'material_language': '软缎、针织、纸质票根、投影柔光、细小星形饰件',
  'color_strategy': '深蓝紫星空配角色识别色和少量暖粉或金色，暗部干净透明',
  'lighting_behavior': '穹顶投影弱光加脸部柔暖补光，眼睛高光清楚'},
 {'name': 'fantasy_cooking_class',
  'graphic_concept': '幻想料理教室：甜点、魔法蒸汽和角色认真表情形成日常可爱传播图',
  'spatial_structure': '厨房背景压成浅色柜台、圆形盘子和柔和蒸汽，食物只保留一两个主形',
  'visual_device': 'primary hook 只选一个：小蛋糕 / 发光蒸汽 / 搅拌碗；secondary support 只选一个：围裙丝带 / 圆盘色块 / 小星点',
  'body_silhouette': '角色站在柜台前或轻侧身，手持搅拌器、盘子或小蛋糕，手部动作简单清楚',
  'outfit_direction': '料理课日常服：短袖上衣、轻围裙、高腰裙裤、袖口和发饰形成可爱重点',
  'material_language': '棉布围裙、陶瓷光泽、奶油质感、柔软蒸汽光',
  'color_strategy': '奶白、淡黄、浅粉和角色色形成甜点系明亮画面',
  'lighting_behavior': '厨房柔光和甜点反光，脸部明亮，蒸汽不遮挡五官'}]

ART_DIRECTION_PLANS.extend(EXTRA_SCENE_PLANS)
OUTFIT_DIRECTIONS = [plan["outfit_direction"] for plan in ART_DIRECTION_PLANS]

PLAN_TAGS.update({'neon_call_night': {'viewer_interaction', 'night_call', 'screen_glow', 'intimate'},
 'arcade_prize_date': {'game', 'viewer_interaction', 'date', 'daily', 'high_color'},
 'gacha_capsule_corner': {'game', 'collectible', 'daily', 'cute', 'high_color'},
 'game_ui_battle_select': {'thumbnail', 'poster', 'ui', 'game', 'symbolic'},
 'rpg_town_square_festival': {'game', 'daily', 'festival', 'high_color', 'fairytale'},
 'pixel_cloud_savepoint': {'dream', 'soft_emotion', 'sky', 'game', 'symbolic'},
 'storybook_castle_balcony': {'soft_emotion', 'romance', 'date', 'fairytale'},
 'fairy_tale_bookshop': {'bookshop', 'quiet', 'soft_emotion', 'date', 'fairytale'},
 'blooming_flower_cart': {'soft_emotion', 'flower', 'date', 'daily'},
 'seaside_date_kiosk': {'date', 'daily', 'airy', 'clean_color', 'summer'},
 'aquarium_blue_date': {'aquarium', 'soft_emotion', 'date', 'blue_light'},
 'train_window_weekend': {'travel', 'soft_emotion', 'quiet', 'daily'},
 'laundry_sun_room': {'soft_emotion', 'clean_color', 'home', 'daily'},
 'bakery_morning_window': {'soft_emotion', 'date', 'daily', 'warm_light'},
 'theme_park_twilight': {'romance', 'date', 'high_color', 'theme_park'},
 'rainy_clear_umbrella_date': {'soft_emotion', 'clean_color', 'rain', 'date'},
 'pajama_game_party': {'soft_emotion', 'home', 'game', 'intimate'},
 'idol_practice_mirror_clean': {'clean_color', 'practice', 'idol', 'daily'},
 'planetarium_soft_date': {'dream', 'night', 'romance', 'date'},
 'fantasy_cooking_class': {'soft_emotion', 'daily', 'cute', 'warm_light'}})

EXTRA_CHARACTER_PLAN_WEIGHTS = {'千夏': {'arcade_prize_date': 3,
        'gacha_capsule_corner': 3,
        'game_ui_battle_select': 2,
        'rpg_town_square_festival': 4,
        'pixel_cloud_savepoint': 6,
        'storybook_castle_balcony': 4,
        'fairy_tale_bookshop': 6,
        'blooming_flower_cart': 7,
        'seaside_date_kiosk': 8,
        'aquarium_blue_date': 6,
        'train_window_weekend': 7,
        'laundry_sun_room': 6,
        'bakery_morning_window': 5,
        'theme_park_twilight': 4,
        'rainy_clear_umbrella_date': 6,
        'pajama_game_party': 5,
        'idol_practice_mirror_clean': 4,
        'planetarium_soft_date': 5,
        'fantasy_cooking_class': 5,
        'neon_call_night': 3},
 '南宫': {'arcade_prize_date': 5,
        'gacha_capsule_corner': 4,
        'game_ui_battle_select': 8,
        'rpg_town_square_festival': 5,
        'pixel_cloud_savepoint': 4,
        'storybook_castle_balcony': 5,
        'fairy_tale_bookshop': 3,
        'blooming_flower_cart': 3,
        'seaside_date_kiosk': 3,
        'aquarium_blue_date': 4,
        'train_window_weekend': 4,
        'laundry_sun_room': 2,
        'bakery_morning_window': 3,
        'theme_park_twilight': 5,
        'rainy_clear_umbrella_date': 4,
        'pajama_game_party': 5,
        'idol_practice_mirror_clean': 6,
        'planetarium_soft_date': 5,
        'fantasy_cooking_class': 2,
        'neon_call_night': 8},
 '爱芮': {'arcade_prize_date': 8,
        'gacha_capsule_corner': 7,
        'game_ui_battle_select': 6,
        'rpg_town_square_festival': 8,
        'pixel_cloud_savepoint': 5,
        'storybook_castle_balcony': 7,
        'fairy_tale_bookshop': 4,
        'blooming_flower_cart': 5,
        'seaside_date_kiosk': 6,
        'aquarium_blue_date': 4,
        'train_window_weekend': 3,
        'laundry_sun_room': 3,
        'bakery_morning_window': 5,
        'theme_park_twilight': 9,
        'rainy_clear_umbrella_date': 3,
        'pajama_game_party': 7,
        'idol_practice_mirror_clean': 8,
        'planetarium_soft_date': 4,
        'fantasy_cooking_class': 6,
        'neon_call_night': 6},
 '丹': {'arcade_prize_date': 1,
       'gacha_capsule_corner': 2,
       'game_ui_battle_select': 3,
       'rpg_town_square_festival': 2,
       'pixel_cloud_savepoint': 7,
       'storybook_castle_balcony': 6,
       'fairy_tale_bookshop': 7,
       'blooming_flower_cart': 5,
       'seaside_date_kiosk': 4,
       'aquarium_blue_date': 7,
       'train_window_weekend': 6,
       'laundry_sun_room': 7,
       'bakery_morning_window': 5,
       'theme_park_twilight': 3,
       'rainy_clear_umbrella_date': 7,
       'pajama_game_party': 6,
       'idol_practice_mirror_clean': 2,
       'planetarium_soft_date': 8,
       'fantasy_cooking_class': 4,
       'neon_call_night': 0},
 '星见雅': {'arcade_prize_date': 1,
         'gacha_capsule_corner': 1,
         'game_ui_battle_select': 5,
         'rpg_town_square_festival': 2,
         'pixel_cloud_savepoint': 2,
         'storybook_castle_balcony': 4,
         'fairy_tale_bookshop': 2,
         'blooming_flower_cart': 1,
         'seaside_date_kiosk': 1,
         'aquarium_blue_date': 3,
         'train_window_weekend': 3,
         'laundry_sun_room': 1,
         'bakery_morning_window': 1,
         'theme_park_twilight': 2,
         'rainy_clear_umbrella_date': 4,
         'pajama_game_party': 1,
         'idol_practice_mirror_clean': 2,
         'planetarium_soft_date': 6,
         'fantasy_cooking_class': 1,
         'neon_call_night': 5},
 '仪玄': {'arcade_prize_date': 1,
        'gacha_capsule_corner': 1,
        'game_ui_battle_select': 6,
        'rpg_town_square_festival': 2,
        'pixel_cloud_savepoint': 2,
        'storybook_castle_balcony': 4,
        'fairy_tale_bookshop': 3,
        'blooming_flower_cart': 1,
        'seaside_date_kiosk': 1,
        'aquarium_blue_date': 3,
        'train_window_weekend': 2,
        'laundry_sun_room': 1,
        'bakery_morning_window': 1,
        'theme_park_twilight': 2,
        'rainy_clear_umbrella_date': 3,
        'pajama_game_party': 1,
        'idol_practice_mirror_clean': 2,
        'planetarium_soft_date': 6,
        'fantasy_cooking_class': 1,
        'neon_call_night': 7}}
for character_name, plan_weights in EXTRA_CHARACTER_PLAN_WEIGHTS.items():
    CHARACTER_PLAN_WEIGHTS.setdefault(character_name, {}).update(plan_weights)

EXTRA_CHARACTER_OUTFIT_VARIATIONS = {'丹': ['水族馆蓝光短披肩 + 奶白内搭 + 透明蓝色小饰件 + 柔软裙裤，保持安静透明感',
       '天文馆约会轻披肩 + 星形小扣 + 浅粉高腰裙裤，像安静梦境收藏海报',
       '雨天透明伞短外套 + 银蓝细腰线 + 柔软袜靴，清爽而不固定成圣女制服',
       '居家游戏宽松短衬衫 + 云朵抱枕配饰 + 浅色软裙裤，亲近但保持淡漠气质',
       '童话书店针织短开衫 + 书签丝带 + 奶白裙裤，温柔但不过度日常化',
       '云端存档点轻短外套 + 半透明水晶小扣 + 浅色裙裤，强化未来梦境感'],
 '千夏': ['薄荷夏日短衬衫 + 奶白高腰裙裤 + 透明饮料小配饰，清透青春感',
        '花车日常短开衫 + 浅色裙裤 + 小花束配饰，保留薄荷空气和陪伴感',
        '周末电车轻外套 + 小票根配饰 + 柔软袜鞋，安静出行感',
        '海边约会蓝白轻衬衫 + 高腰短裙裤 + 透明小饰件，清爽但不强营业'],
 '南宫': ['游戏选择界面限定短披肩 + 粉黑收腰外套 + 半透明 UI 小徽章，控场感清楚',
        '游戏厅约会短夹克 + 高腰裙裤 + 小奖品挂件，轻挑衅但不甜腻',
        '深夜通话黑粉短外套 + 发光耳机线 + 清楚腰线，像锁定 viewer 的私密频道',
        '练习室短运动外套 + 细节腰带 + 猫发夹呼应，聪明从容的队长私服'],
 '爱芮': ['游乐园约会短夹克 + 亮色裙摆 + 气球小配饰，偶像营业感强',
        '游戏厅高色块短外套 + 毛绒奖品挂件 + 厚底鞋袜，粉丝互动感',
        '居家游戏宽松外套 + 可爱手柄配饰 + 软质短裙裤，直播前的亲近感',
        '偶像练习室短运动外套 + 水瓶或毛巾配饰 + 高腰裙裤，努力感和舞台感兼具']}
for character_name, outfit_list in EXTRA_CHARACTER_OUTFIT_VARIATIONS.items():
    CHARACTER_OUTFIT_VARIATIONS.setdefault(character_name, []).extend(outfit_list)

EXTRA_PROFILE_PREFERRED_HOOKS = {'千夏': {'blooming_flower_cart',
        'fairy_tale_bookshop',
        'pixel_cloud_savepoint',
        'rainy_clear_umbrella_date',
        'seaside_date_kiosk',
        'train_window_weekend'},
 '南宫': {'arcade_prize_date',
        'game_ui_battle_select',
        'idol_practice_mirror_clean',
        'neon_call_night',
        'pajama_game_party'},
 '爱芮': {'arcade_prize_date',
        'gacha_capsule_corner',
        'idol_practice_mirror_clean',
        'pajama_game_party',
        'rpg_town_square_festival',
        'theme_park_twilight'},
 '丹': {'aquarium_blue_date',
       'fairy_tale_bookshop',
       'laundry_sun_room',
       'pixel_cloud_savepoint',
       'planetarium_soft_date',
       'rainy_clear_umbrella_date'},
 '星见雅': {'game_ui_battle_select', 'planetarium_soft_date', 'rainy_clear_umbrella_date', 'neon_call_night'},
 '仪玄': {'game_ui_battle_select', 'planetarium_soft_date', 'neon_call_night', 'storybook_castle_balcony'}}
for character_name, hook_names in EXTRA_PROFILE_PREFERRED_HOOKS.items():
    if character_name in CHARACTER_PROPAGATION_PROFILES:
        CHARACTER_PROPAGATION_PROFILES[character_name]["preferred_hooks"].update(hook_names)


# ---------------------------------------------------------------------------
# Character-first safety layer
#
# Keep this block after all plan/profile expansions so it can gate future added
# scenes too. New characters can opt in by adding profile data and, when needed,
# required identity tokens or forbidden plans below.
# ---------------------------------------------------------------------------

CHARACTER_REQUIRED_IDENTITY_TOKENS = {
    "丹": [
        "浅粉色短发",
        "不对称空气感厚刘海",
        "粉紫色眼睛",
        "银白细头环 / 蓝银星形发卡 / 耳侧轻机械模块 / 透明蓝银小光片，至少出现一个",
    ],
    "星见雅": [
        "黑色长直发",
        "厚重整齐齐刘海",
        "黑色兽耳",
        "锐利红色眼瞳",
        "红色刀线 / 太刀柄 / 刀鞘 / 武士绳结，至少出现一个",
    ],
}

CHARACTER_FORBIDDEN_PLANS = {
    "星见雅": {
        "arcade_prize_date",
        "bakery_morning_window",
        "blooming_flower_cart",
        "fantasy_cooking_class",
        "laundry_sun_room",
        "pajama_game_party",
        "seaside_date_kiosk",
        "theme_park_twilight",
    },
    "丹": {
        "arcade_prize_date",
        "gacha_capsule_corner",
        "idol_practice_mirror_clean",
        "neon_call_night",
        "theme_park_twilight",
    },
}

CHARACTER_VIEWER_DISTANCE = {
    "爱芮": "close / idol interaction：可以更靠近 viewer，强调偶像营业、心动、收藏欲。",
    "南宫": "medium-close / teasing control：可以近，但关系是控场、锁定和轻挑衅。",
    "千夏": "medium / shy companion：保持青春陪伴感，靠近但不压迫镜头。",
    "丹": "medium-distant / quiet healing：保持透明、安静、轻未来距离感，不强营业，不贴脸。",
    "星见雅": "distant / pressure gaze：保持凛然压迫、冷感距离和被审视感，不软化成约会少女。",
    "仪玄": "ritual / mature mystery：保持仪式感、神秘距离和成熟牵引，不变成甜妹互动。",
}

CHARACTER_PLAN_WEIGHT_FLOOR = 1


def required_identity_tokens_for(character_name: str) -> list[str]:
    character = _primary_character(character_name)
    return CHARACTER_REQUIRED_IDENTITY_TOKENS.get(character, [])


def viewer_distance_for(character_name: str) -> str:
    character = _primary_character(character_name)
    return CHARACTER_VIEWER_DISTANCE.get(
        character,
        "medium / character-first：新增角色默认保持中距离，先稳身份，再增加互动强度。",
    )


def _allowed_plan_for_character(character: str, plan_name: str) -> bool:
    return plan_name not in CHARACTER_FORBIDDEN_PLANS.get(character, set())


def choose_art_plan(character_name: str | None = None, recent_tags: list[str] | None = None) -> dict:
    character = _primary_character(character_name or "丹")
    profile = propagation_profile_for(character)
    weights_by_name = CHARACTER_PLAN_WEIGHTS.get(character, CHARACTER_PLAN_WEIGHTS["丹"])
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for plan in ART_DIRECTION_PLANS:
        plan_name = plan["name"]
        if not _allowed_plan_for_character(character, plan_name):
            continue
        tags = PLAN_TAGS.get(plan_name, set())
        if tags & blocked:
            continue
        weight = weights_by_name.get(plan_name, CHARACTER_PLAN_WEIGHT_FLOOR)
        if weight <= 0:
            continue
        candidates.append(plan)
        weights.append(_profile_adjusted_weight(plan_name, weight, profile["preferred_hooks"]))
    if not candidates:
        candidates = [
            plan for plan in ART_DIRECTION_PLANS
            if _allowed_plan_for_character(character, plan["name"])
            and weights_by_name.get(plan["name"], CHARACTER_PLAN_WEIGHT_FLOOR) > 0
        ]
        weights = [
            _profile_adjusted_weight(
                plan["name"],
                weights_by_name.get(plan["name"], CHARACTER_PLAN_WEIGHT_FLOOR),
                profile["preferred_hooks"],
            )
            for plan in candidates
        ]
    if not candidates:
        candidates = ART_DIRECTION_PLANS[:]
        weights = [1 for _ in candidates]
    return _weighted_choice(candidates, weights)

CHARACTER_REQUIRED_IDENTITY_TOKENS.update({
    "叶瞬光": [
        "云岿山修行者气质",
        "剑 / 剑光 / 剑穗，至少出现一个",
        "温柔可靠的师姐感",
        "清亮、承担型保护者气场",
    ],
    "席德": [
        "机械改造元素",
        "蓝紫电弧 / 电路纹，至少出现一个",
        "老席德或大型机械伙伴痕迹",
        "花朵反差与天真危险感",
    ],
    "橘福福": [
        "虎系元素 / 虎纹 / 虎耳或虎尾气质，至少出现一个",
        "火属性暖光",
        "云岿山武修气质",
        "虎威或虎形装置 / 伏魔符纸，至少出现一个",
    ],
})

CHARACTER_FORBIDDEN_PLANS.update({
    "叶瞬光": {"arcade_prize_date", "gacha_capsule_corner", "pajama_game_party", "theme_park_twilight"},
    "席德": {"bakery_morning_window", "blooming_flower_cart", "laundry_sun_room", "seaside_date_kiosk", "rainy_clear_umbrella_date"},
    "橘福福": {"planetarium_soft_date", "fairy_tale_bookshop", "laundry_sun_room", "aquarium_blue_date"},
})

CHARACTER_VIEWER_DISTANCE.update({
    "叶瞬光": "medium / protective senior sister：保持温柔可靠的保护距离，可以回身看向 viewer，但不贴脸营业。",
    "席德": "medium-close / innocent dangerous demo：可以靠近展示机械，但手和装置不要冲镜头，危险感来自电光和机械伙伴。",
    "橘福福": "medium-close / energetic action：可以更有动势和亲近感，但必须保留虎系火光与云岿山武修气质。",
})

# Late apply: the V3 section above redefines the profile dictionaries, so apply
# the new character data and stricter gates again at the very end.
CHARACTER_PROPAGATION_PROFILES.update(NEW_CHARACTER_PROPAGATION_PROFILES)

for character_name, outfit_list in NEW_CHARACTER_OUTFIT_VARIATIONS.items():
    CHARACTER_OUTFIT_VARIATIONS.setdefault(character_name, []).extend(outfit_list)

for character_name, plan_weights in NEW_CHARACTER_PLAN_WEIGHTS.items():
    CHARACTER_PLAN_WEIGHTS.setdefault(character_name, {}).update(plan_weights)

STRICT_PLAN_CHARACTERS = {"丹", "星见雅", "仪玄", "叶瞬光", "席德", "橘福福"}

CHARACTER_FORBIDDEN_TAGS = {
    "丹": {"idol", "practice", "theme_park", "gacha", "collectible"},
    "星见雅": {"cute", "theme_park", "home", "daily", "flower"},
    "仪玄": {"cute", "home", "domestic_daily", "theme_park"},
    "叶瞬光": {"cute", "theme_park", "gacha", "home"},
    "席德": {"soft_emotion", "flower", "warm_light"},
    "橘福福": {"quiet", "blue_light", "aquarium"},
}


def _default_plan_weight_for(character: str) -> int:
    return 0 if character in STRICT_PLAN_CHARACTERS else CHARACTER_PLAN_WEIGHT_FLOOR


def _allowed_plan_for_character(character: str, plan_name: str) -> bool:
    if plan_name in CHARACTER_FORBIDDEN_PLANS.get(character, set()):
        return False
    plan_tags = PLAN_TAGS.get(plan_name, set())
    forbidden_tags = CHARACTER_FORBIDDEN_TAGS.get(character, set())
    return not (plan_tags & forbidden_tags)


def choose_art_plan(character_name: str | None = None, recent_tags: list[str] | None = None) -> dict:
    character = _primary_character(character_name or "丹")
    profile = propagation_profile_for(character)
    weights_by_name = CHARACTER_PLAN_WEIGHTS.get(character, CHARACTER_PLAN_WEIGHTS["丹"])
    default_weight = _default_plan_weight_for(character)
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for plan in ART_DIRECTION_PLANS:
        plan_name = plan["name"]
        if not _allowed_plan_for_character(character, plan_name):
            continue
        tags = PLAN_TAGS.get(plan_name, set())
        if tags & blocked:
            continue
        weight = weights_by_name.get(plan_name, default_weight)
        if weight <= 0:
            continue
        candidates.append(plan)
        weights.append(_profile_adjusted_weight(plan_name, weight, profile["preferred_hooks"]))
    if not candidates:
        candidates = [
            plan for plan in ART_DIRECTION_PLANS
            if _allowed_plan_for_character(character, plan["name"])
            and weights_by_name.get(plan["name"], default_weight) > 0
        ]
        weights = [
            _profile_adjusted_weight(
                plan["name"],
                weights_by_name.get(plan["name"], default_weight),
                profile["preferred_hooks"],
            )
            for plan in candidates
        ]
    if not candidates:
        candidates = [
            plan for plan in ART_DIRECTION_PLANS
            if _allowed_plan_for_character(character, plan["name"])
        ] or ART_DIRECTION_PLANS[:]
        weights = [1 for _ in candidates]
    return _weighted_choice(candidates, weights)

# ---------------------------------------------------------------------------
# Final user-owned style plans
# These two plans preserve the user's favorite prompt language as selectable
# ART_DIRECTION_PLANS instead of only global rendering guidance.
# ---------------------------------------------------------------------------
USER_FAVORITE_STYLE_PLANS = [
    {
        "name": "reference_soft_lineart_reinterpretation",
        "graphic_concept": "uploaded reference image reinterpreted as a clean lightweight hand-drawn anime illustration, focused on character identity, collectible charm, and soft fantasy appeal",
        "spatial_structure": "simple airy illustration space with uncluttered background shapes, character kept as the clear center of attention, no copied reference composition, no heavy cinematic environment",
        "visual_device": "thin elegant lineart, sketch-like contour rhythm, clear color blocks, soft watercolor / colored pencil / pale marker feeling, one memorable character-color accent",
        "body_silhouette": "medium to knee-up character framing, natural relaxed pose, both arms readable and simple, hands either resting naturally, holding small safe accessory, or partly hidden by clothing without distortion",
        "outfit_direction": "preserve the reference outfit color identity while allowing a lighter anime fashion reinterpretation: clean simplified layers, soft ribbons or small accessories, clear clothing color separation, no over-complex material noise",
        "material_language": "low-to-medium saturation hand-drawn finish, clean anime linework, simple cel shading, soft flat colors, reduced texture complexity, no thick paint, no glossy 3D skin",
        "color_strategy": "gentle but not washed out; cream skin tones, clear main clothing color, small blush and soft accent colors; avoid gray fog, whitewashed pastel, diluted outfit colors, and full-frame single hot color backgrounds",
        "lighting_behavior": "soft diffuse studio-like anime light, mild rim light only when useful, minimal hard shadow, fresh light-novel illustration clarity",
    },
    {
        "name": "intimate_anime_photo_crop",
        "graphic_concept": "high-end anime photography style character visual with intimate viewer relationship, cheerful youthful emotion, strong facial charm, and mobile-wallpaper appeal",
        "spatial_structure": "medium-close to three-quarter character framing with face as the focal point but enough torso and outfit visible; background is a softly blurred town street, balcony, garden path, or sunset outdoor space",
        "visual_device": "eyes to smile to hair flow visual path, soft bokeh, golden-hour warmth, clean negative space around the face, candid light-novel photo feeling without copying phone-selfie logic",
        "body_silhouette": "three-quarter angle, slight below-eye-level or eye-level view, natural shoulders and waist visible, hands kept small and calm: one hand near chest, hair, sleeve, bag strap, or out of frame; no hand reaching toward the lens",
        "outfit_direction": "date-photo / light-novel portrait fashion: neat layered outfit, soft collar or shoulder detail, character-specific color accents, enough lower-body or waist information to avoid repeated bust-only images",
        "material_language": "clean anime lineart, soft watercolor-anime hybrid shading, delicate eyelashes, glossy but controlled eyes, transparent anime skin rendering, no realistic skin texture or heavy cinematic grading",
        "color_strategy": "warm sunset highlights balanced with soft cool shadows; background hues stay lower saturation than the character; avoid magenta/pink full-screen backgrounds unless broken by cream, sky blue, gray, or warm neutral space",
        "lighting_behavior": "natural golden-hour ambient light, gentle hair rim light, soft depth of field, minimal clutter, emotional warmth over realism",
    },
]

_existing_plan_names = {plan["name"] for plan in ART_DIRECTION_PLANS}
for _plan in USER_FAVORITE_STYLE_PLANS:
    if _plan["name"] not in _existing_plan_names:
        ART_DIRECTION_PLANS.append(_plan)
        _existing_plan_names.add(_plan["name"])

OUTFIT_DIRECTIONS = [plan["outfit_direction"] for plan in ART_DIRECTION_PLANS]

PLAN_TAGS.update({
    "reference_soft_lineart_reinterpretation": {"user_favorite", "soft_lineart", "light_novel", "reference_identity", "clean_color"},
    "intimate_anime_photo_crop": {"user_favorite", "anime_photo", "soft_emotion", "viewer_interaction", "golden_hour"},
})

for _character_name in list(CHARACTER_PLAN_WEIGHTS):
    CHARACTER_PLAN_WEIGHTS.setdefault(_character_name, {})["reference_soft_lineart_reinterpretation"] = 4
    CHARACTER_PLAN_WEIGHTS.setdefault(_character_name, {})["intimate_anime_photo_crop"] = 3

for _profile in CHARACTER_PROPAGATION_PROFILES.values():
    _profile.setdefault("preferred_hooks", set()).update({
        "reference_soft_lineart_reinterpretation",
        "intimate_anime_photo_crop",
    })

# ---------------------------------------------------------------------------
# Final feedback plan: white infinity room
# Added after all overrides so the plan is present in the effective V3 pool.
# ---------------------------------------------------------------------------
WHITE_INFINITY_ROOM_PLAN_FINAL = {
    "name": "white_infinity_room",
    "graphic_concept": "a pure white infinite room where the character, silhouette, and one small symbolic accent become the entire visual hook; clean social anime poster feeling",
    "spatial_structure": "endless white / warm gray / soft cream space with no visible wall clutter, only subtle floor shadow or circular platform to ground the character without swallowing them",
    "visual_device": "large negative space, crisp character silhouette, one floating minimal symbol, low-contrast geometric shadow, strong thumbnail readability through shape rather than noisy background",
    "body_silhouette": "single character in full-body, thigh-up, or clean three-quarter standing pose; calm readable limbs, natural hands, no lens-reaching hand, no complex crossed fingers",
    "outfit_direction": "minimal high-end outfit with character-specific color accents: white, gray, cream, black, or pale neutral base plus one recognizable identity color; avoid locking everyone into the same costume",
    "material_language": "smooth cloth, matte surfaces, clean lineart, very light glow, no heavy texture, no metallic overload, no studio product-render feeling",
    "color_strategy": "mostly white / warm gray / cream space, character color used as small controlled accent; avoid full-frame hot pink, magenta, neon background, or same-hue background matching the character accent",
    "lighting_behavior": "soft shadowless gallery light, gentle floor contact shadow, clean edge light around hair and outfit, quiet but memorable minimalism",
}

if not any(plan["name"] == WHITE_INFINITY_ROOM_PLAN_FINAL["name"] for plan in ART_DIRECTION_PLANS):
    ART_DIRECTION_PLANS.append(WHITE_INFINITY_ROOM_PLAN_FINAL)

OUTFIT_DIRECTIONS = [plan["outfit_direction"] for plan in ART_DIRECTION_PLANS]

PLAN_TAGS["white_infinity_room"] = {"minimal", "white_space", "character_icon", "clean_color", "user_feedback"}

for _character_name in list(CHARACTER_PLAN_WEIGHTS):
    CHARACTER_PLAN_WEIGHTS.setdefault(_character_name, {})["white_infinity_room"] = 3

for _character_name in ["荳ｹ", "蜊怜ｮｫ", "莉ｪ邇・", "譏溯ｧ・寉", "蟶ｭ蠕ｷ"]:
    CHARACTER_PLAN_WEIGHTS.setdefault(_character_name, {})["white_infinity_room"] = 6

for _profile in CHARACTER_PROPAGATION_PROFILES.values():
    _profile.setdefault("preferred_hooks", set()).add("white_infinity_room")

# ---------------------------------------------------------------------------
# Final outfit variation experiment
# Keep this block at the end. It overrides outfit_variation_for without touching
# identity locks, so it is easy to remove if the result drifts too far.
# ---------------------------------------------------------------------------
OUTFIT_EPISODE_POOL = [
    "episode outfit: soft daily private clothes, loose cardigan, simple skirt or shorts, small character-color accessory; clearly different from the default reference costume",
    "episode outfit: light novel date outfit, clean layered top, neat waist detail, coordinated socks or boots, character identity colors kept only as accents",
    "episode outfit: fantasy idol stage-lite costume, asymmetrical ribbon detail, compact decorative trim, readable silhouette, not a cosplay copy of the reference outfit",
    "episode outfit: airy studio dress / long shirt layer, matte fabric, minimal jewelry, soft movement in sleeves or hem, face and hair identity unchanged",
    "episode outfit: modern street casual, cropped jacket or soft hoodie layer, simple pleated bottom, one iconic charm attached to bag / belt / collar",
    "episode outfit: storybook formal casual, small capelet or shawl, gentle collar shape, polished shoes, elegant but not heavy palace costume",
    "episode outfit: clean summer outfit, pale inner layer, light outer shirt, short skirt or shorts, breathable fabric, no repeated school-uniform look",
    "episode outfit: rainy-day transparent coat or soft trench, muted neutral base, one vivid character-color lining, hands kept simple and visible",
    "episode outfit: white-room minimal fashion, cream / gray / black base, one bold identity-color stripe or accessory, high-end poster silhouette",
    "episode outfit: RPG town casual fantasy, travel shawl, small pouch, simple boots, festival accent, character personality over armor complexity",
    "episode outfit: aquarium date styling, blue-white light fabric, translucent small accessory, gentle layered skirt or culotte, calm reflective mood",
    "episode outfit: practice-room casual, fitted but safe dance top, loose warm-up jacket, sporty skirt or shorts, clean idol rehearsal feeling",
]

PLAN_OUTFIT_ADAPTER = {
    "aquarium_blue_date": "scene adapter: add blue-white transparent details and water-reflection softness, avoid paper / pen / creator props",
    "rainy_clear_umbrella_date": "scene adapter: add raincoat, soft trench, clear umbrella color echo, keep hands simple and not gripping complex objects",
    "idol_practice_mirror_clean": "scene adapter: add rehearsal wear or warm-up jacket, not full performance costume every time",
    "rpg_town_square_festival": "scene adapter: add festival ribbon, town-travel layer, small pouch or charm, avoid armor overload",
    "storybook_castle_balcony": "scene adapter: add light capelet, storybook collar, soft formal trim, avoid heavy royal costume",
    "game_ui_battle_select": "scene adapter: add compact action-fashion details and clean UI-like color blocking, no weapon requirement unless character identity needs it",
    "theme_park_twilight": "scene adapter: add date-park outer layer, small glowing accessory, playful but safe silhouette",
    "white_infinity_room": "scene adapter: simplify into white / gray / cream minimal fashion with one strong identity accent",
    "reference_soft_lineart_reinterpretation": "scene adapter: preserve reference color memory but redesign outfit as a lighter illustration episode outfit",
    "intimate_anime_photo_crop": "scene adapter: use soft date-photo clothing with visible collar / waist / shoulder detail, avoid pure bust-only framing",
}

CHARACTER_OUTFIT_PUSH = {
    "荳ｹ": [
        "Dan-specific variation: replace default sacred dress with quiet future-casual white jacket, sea-blue inner layer, soft skirt-pants, and one small halo / water accent",
        "Dan-specific variation: minimal gallery outfit, cream long shirt, pale aqua sash, matte boots, calm sacred mood without repeating the same dress",
        "Dan-specific variation: rainy-day gentle coat, muted mint-gray palette, transparent hood edge, elegant but daily enough to feel new",
    ],
    "蜊・､・": [
        "Chinatsu-specific variation: keep mint hair silhouette from reference, use fresh mint daily outfit, bow and heart-earring identity preserved, no artist / paper / pen props",
        "Chinatsu-specific variation: soft summer date clothes, pale green cardigan, simple skirt, large bow kept, natural companion mood",
    ],
    "譏溯ｧ・寉": [
        "Miyabi-specific variation: black-red modern coat dress or rain-night formal wear, ears and black long hair preserved, no forced sword unless the scene truly benefits",
        "Miyabi-specific variation: minimalist dark heroine fashion, clean red accent line, strong silhouette without weapon dependency",
    ],
}

_BASE_OUTFIT_VARIATION_FOR = outfit_variation_for


def outfit_variation_for(character_name: str, plan_name: str | None = None) -> str:
    character = _primary_character(character_name)
    parts = []

    character_push = CHARACTER_OUTFIT_PUSH.get(character, [])
    if character_push and random.random() < 0.75:
        parts.append(random.choice(character_push))
    else:
        original = _BASE_OUTFIT_VARIATION_FOR(character_name, plan_name)
        if original:
            parts.append(original)

    if random.random() < 0.9 or not parts:
        parts.append(random.choice(OUTFIT_EPISODE_POOL))

    adapter = PLAN_OUTFIT_ADAPTER.get(plan_name or "")
    if adapter:
        parts.append(adapter)

    parts.append(
        "outfit rule: keep face, hairstyle, eye shape, signature hair accessory, and personality identity stable; clothing is an episode variation, not the fixed default costume; avoid exact same outfit across images"
    )
    return " / ".join(parts)


# ---------------------------------------------------------------------------
# Final identity separation patch: Miyabi vs Yeshunguang
# This patch prevents the model from collapsing both sword girls into the same
# black-haired beast-ear archetype.
# ---------------------------------------------------------------------------
CHARACTER_REQUIRED_IDENTITY_TOKENS.setdefault("星见雅", []).extend([
    "星见雅必须是黑色长直发、厚重齐刘海、黑色尖兽耳、锐利红眼的冷感剑客",
    "星见雅使用黑 / 墨绿 / 红色刀线的冷色武士剪影",
    "星见雅明确不是叶瞬光：不要棕褐长发、不要暖棕大尾巴、不要红色发带、不要白金云岿山师姐服、不要温柔护送感",
])
CHARACTER_REQUIRED_IDENTITY_TOKENS.setdefault("叶瞬光", []).extend([
    "叶瞬光必须是暖棕 / 焦糖色长发，带棕褐色兽耳和蓬松大棕尾",
    "叶瞬光必须有红色发带 / 红绳 / 红色小花饰之一，红色眼睛，白色云岿山修行服配黑金或黄玉点缀",
    "叶瞬光明确不是星见雅：不要黑长直姬发、不要黑色尖兽耳、不要黑绿冷色武士制服、不要冷酷压迫审视感、不要红黑太刀少女模板",
])

if "星见雅" in CHARACTER_PROPAGATION_PROFILES:
    CHARACTER_PROPAGATION_PROFILES["星见雅"]["official_core"] += " 她必须和叶瞬光区分：黑发、黑尖兽耳、红眼、冷色武士剪影是星见雅；不要画成棕发红绳白金云岿山师姐。"
    CHARACTER_PROPAGATION_PROFILES["星见雅"].setdefault("suppressed_misreads", []).extend([
        "叶瞬光化", "棕褐长发", "暖棕大尾巴", "红色发带", "白金云岿山师姐服", "温柔护送感",
    ])
if "叶瞬光" in CHARACTER_PROPAGATION_PROFILES:
    CHARACTER_PROPAGATION_PROFILES["叶瞬光"]["official_core"] += " 她必须和星见雅区分：暖棕长发、棕褐兽耳、蓬松大棕尾、红绳/红花饰、白金云岿山服是叶瞬光；不要画成黑发黑耳冷感武士。"
    CHARACTER_PROPAGATION_PROFILES["叶瞬光"].setdefault("suppressed_misreads", []).extend([
        "星见雅化", "黑长直姬发", "黑色尖兽耳", "黑绿冷色武士制服", "冷酷压迫审视感", "红黑太刀少女模板",
    ])

CHARACTER_OUTFIT_PUSH.setdefault("星见雅", []).extend([
    "Miyabi-specific variation: black / dark-teal modern blade coat, black straight hair and black sharp beast ears preserved, red eye pressure, explicitly not brown-haired Yeshunguang",
    "Miyabi-specific variation: minimalist dark sword heroine fashion, clean red blade-line accent, no brown tail, no red ribbon, no white-gold mountain senior-sister outfit",
])
CHARACTER_OUTFIT_PUSH.setdefault("叶瞬光", []).extend([
    "Yeshunguang-specific variation: white cloud-mountain practitioner outfit, black-gold / yellow-jade details, red ribbon or red cord, warm brown hair and large brown tail preserved",
    "Yeshunguang-specific variation: gentle senior-sister travel outfit, white outer layer, dark inner line, red tassel, sword cord, warm brown beast ears and fluffy tail clearly different from Miyabi",
    "Yeshunguang-specific variation: rain-stone-step guardian outfit, pale robe jacket, red hair ribbon, sword tassel, soft brown tail, protective warmth not cold pressure",
])
