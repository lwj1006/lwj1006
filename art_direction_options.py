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
        "body_silhouette": "角色主动向镜头压近，手臂、衣摆或翅膀形成外扩轮廓，但只有一个前景爆点，不让全画面同时爆炸",
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
        "body_silhouette": "角色半身或膝上靠近镜头，眼神直视 viewer，一只手自然靠近画面边缘但不遮脸",
        "outfit_direction": "社交平台头像级偶像服装：短外套、蝴蝶结、耳机、细腰线和高识别小配件",
        "material_language": "柔软布料、透明亚克力、发光小饰件、轻薄丝带",
        "color_strategy": "高记忆角色色占主导，背景用互补色托脸，缩略图先读到眼睛和发色",
        "lighting_behavior": "脸部明亮，眼睛高光清楚，边缘有梦境柔光，不做真实摄影暗部",
    },
    {
        "name": "summer_mint_afterglow",
        "graphic_concept": "薄荷夏日空气从角色周围生长，风、透明饮料、窗帘和水光形成清凉幻想",
        "spatial_structure": "浅色房间、天台或海边被压成大色块，空间不复杂，只服务清透情绪",
        "visual_device": "primary hook 只选一个：薄荷色风 / 乐谱或耳机线 / 透明饮料；secondary support 只选一个：窗帘 / 水光 / 发光云",
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
        "body_silhouette": "角色面向 viewer 做营业感动作，身体打开但不夸张擦边",
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
        "body_silhouette": "角色坐在窗边、回头对视或轻轻靠近镜头，像在对 viewer 说悄悄话",
        "outfit_direction": "夜色约会感服装：轻礼服外套、短裙或裙裤、精致领口和柔软披肩",
        "material_language": "软缎、薄纱、月光边缘、透明宝石小饰件",
        "color_strategy": "深蓝紫夜色加角色发色高光，局部暖粉或金色制造恋爱记忆点",
        "lighting_behavior": "月光和柔暖补光并存，暗部保持干净，不进入恐怖或废墟气质",
    },
    {
        "name": "floating_room_daydream",
        "graphic_concept": "房间、书本、枕头、小物件和云朵轻微漂浮，表现角色的白日梦人格空间",
        "spatial_structure": "真实房间被改造成梦境平面，透视可以不合理，但画面必须可爱、清楚、可收藏",
        "visual_device": "primary hook 只选一个：抱枕梦境 / 漂浮书本 / 窗外超现实天空；secondary support 只选一个：云朵 / 贴纸 / 耳机线",
        "body_silhouette": "角色坐、趴或半躺在画面中央偏近位置，表情要有亲近感",
        "outfit_direction": "居家幻想私服：宽松短外套、可爱内搭、短裙或软裤、袜子和小发饰",
        "material_language": "柔软棉布、毛绒、纸张、贴纸、透明光点",
        "color_strategy": "奶油白、粉蓝、薰衣草紫或角色主色形成舒服但显眼的封面感",
        "lighting_behavior": "柔亮室内光，像梦醒前一秒，脸部绝对不能暗",
    },
    {
        "name": "neon_call_night",
        "graphic_concept": "深夜通话、直播或私信气氛，角色像正在和 viewer 形成秘密关系",
        "spatial_structure": "背景是简化的夜色屏幕、聊天窗口和霓虹色块，不做复杂城市写实",
        "visual_device": "primary hook 只选一个：手机屏幕光 / 耳机通话 / 近景眼神；secondary support 只选一个：聊天气泡 / 少量弹幕光点 / 半透明 UI",
        "body_silhouette": "角色拿手机或扶耳机看向 viewer，距离亲近，有深夜陪伴感",
        "outfit_direction": "夜间社交私服：短外套、宽松上衣、细项链、耳机或小型科技饰件",
        "material_language": "柔软针织、屏幕玻璃、透明 UI、微发光饰件",
        "color_strategy": "黑夜只作为衬托，脸部用粉紫、蓝青或角色色点亮，禁止脏灰暗部",
        "lighting_behavior": "屏幕光照亮眼睛和脸侧，背景霓虹克制但有点击欲望",
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
        "lighting_behavior": "整体明亮，角色脸和上半身是第一焦点，不追求真实阴影",
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
        "graphic_concept": "超级简约角色海报：只保留角色脸、发型大形、一个专属符号和一块高记忆纯色背景",
        "spatial_structure": "没有真实空间，背景是干净纯色、轻微渐变或单一大色块；角色半身到胸像构图，绝不变成远景小人",
        "visual_device": "primary hook 只选一个：角色专属发饰 / 一个小道具 / 一个简洁图形符号；secondary support 只允许一条细线、一个小光点或一块纯色",
        "body_silhouette": "角色正面或三分之二半身，脸、眼睛、头发轮廓和发饰极清楚，姿态克制但有情绪",
        "outfit_direction": "极简但有角色识别的上半身服装：干净领口、明确肩线、一个小配饰或一处角色色",
        "material_language": "平滑色块、干净线稿、少量柔光、无复杂材质",
        "color_strategy": "最多两到三种主色，角色专属色必须一眼记住，背景不抢脸",
        "lighting_behavior": "柔亮均匀光，眼睛和脸部最清楚，不追求真实阴影和复杂光效",
    },
    {
        "name": "dream_mist_portrait",
        "graphic_concept": "梦幻感角色近景：像半醒梦里的角色图，只保留柔雾、眼神、发丝和一个人格化幻想符号",
        "spatial_structure": "空间几乎融化成浅色雾面背景，角色胸像到半身占画面主体，边缘可有少量漂浮光尘但不形成复杂场景",
        "visual_device": "primary hook 只选一个：月亮 / 羽毛 / 发光云 / 透明耳机线；secondary support 只选一个：薄雾色块 / 小星点 / 柔光圆",
        "body_silhouette": "角色微侧脸或轻回头，肩颈线干净，表情安静但有被收藏的情绪余韵",
        "outfit_direction": "柔软轻薄的角色上半身服装，领口和发饰清楚，避免复杂层叠和大型机械装饰",
        "material_language": "透明薄纱、柔软棉感、轻微珠光、雾面渐变",
        "color_strategy": "低噪声高记忆浅色系，角色色作为第一阅读点，背景只负责托出脸和眼睛",
        "lighting_behavior": "大面积柔光包裹，眼睛高光清楚，阴影极浅，不做电影暗调",
    },
    {
        "name": "fairytale_pop_storybook",
        "graphic_concept": "童话感社交插画：角色像从一本发光绘本里跳出来，画面可爱但不低幼",
        "spatial_structure": "背景是扁平化绘本舞台、窗框、糖果云或小花园的一小角，绝不展开复杂建筑透视",
        "visual_device": "primary hook 只选一个：绘本窗框 / 小皇冠 / 糖果云 / 花环；secondary support 只选一个：小星点 / 丝带 / 软色块",
        "body_silhouette": "角色半身或膝上构图，动作轻快，有明确表情和手势，缩略图先读到脸和发型",
        "outfit_direction": "童话偶像感服装：小披肩、蝴蝶结、短裙边或领结只保留一个重点，不做全身堆装饰",
        "material_language": "柔软布料、绘本质感色块、少量亮片、圆润干净线条",
        "color_strategy": "高明度但控制色数，最多三种主色，避免全画面彩虹噪音",
        "lighting_behavior": "明亮童话棚光，脸部和发色最清楚，背景像舞台布景一样轻",
    },
    {
        "name": "clean_idol_studio_shot",
        "graphic_concept": "摄影棚式二次元角色图：不是写实摄影，而是干净棚拍感的角色商业头像",
        "spatial_structure": "纯色无缝背景、简洁地台或一块软阴影，角色半身到膝上，画面结构极清楚",
        "visual_device": "primary hook 只选一个：角色专属道具 / 发饰 / 手势 / 眼神；secondary support 只选一个：背景色块 / 柔影 / 小型补光边",
        "body_silhouette": "角色姿态稳定，肩线、腰线和脸部表情清楚，像可以直接用于社交平台封面或头像",
        "outfit_direction": "干净精修的角色服装，上半身识别度优先，少量配饰集中在脸周和领口",
        "material_language": "平滑布料、干净皮肤光、克制高光、少量透明或金属小件",
        "color_strategy": "单一背景主色配角色识别色，强缩略图读取，避免复杂环境抢戏",
        "lighting_behavior": "柔和棚拍主光加轻边光，眼睛、脸和发型是绝对焦点",
    },
    {
        "name": "modern_guofeng_character_poster",
        "graphic_concept": "现代国风角色海报：用留白、墨色线条和一个东方意象强化角色人格，不做古装旅游照",
        "spatial_structure": "背景是大面积宣纸感留白、圆窗、折扇弧线或水墨色块，角色半身占主视觉",
        "visual_device": "primary hook 只选一个：圆月窗 / 折扇弧线 / 墨色花枝 / 玉饰；secondary support 只选一个：淡墨云气 / 细金线 / 水纹",
        "body_silhouette": "角色正面或三分之二半身，姿态克制，手部动作像轻握扇、整理发饰或安静回眸",
        "outfit_direction": "现代改良国风服装：盘扣、短披帛、云肩或玉饰只保留一个重点，并保持角色原本发型和人格",
        "material_language": "丝缎、宣纸纹理、淡墨、细金线、玉石小饰件",
        "color_strategy": "一块角色识别色 + 墨色/米白/淡金支撑，不能变成传统厚重古风杂色",
        "lighting_behavior": "清透柔光，脸部现代二次元插画感明确，水墨元素只做气氛不压角色",
    },
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
        "floating_room_daydream": 7,
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
        "modern_guofeng_character_poster": 3,
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
        "body_silhouette": "角色直视 viewer，脸和眼睛是第一焦点，上半身占画面较大比例",
        "personality_logic": "用对视建立关系，让观众感觉角色正在看自己，而不是远处摆拍",
        "support_rule": "头发大形、眼睛、发饰和手部小动作必须清楚，缩略图也能读脸",
        "avoid_rule": "不要把人物画太小，不要背对镜头，不要让背景抢走眼神",
    },
    {
        "name": "near_camera_whisper",
        "tags": {"viewer_interaction", "romance", "intimate"},
        "body_silhouette": "角色轻靠近镜头，像要说悄悄话，肩线和脸部形成亲近构图",
        "personality_logic": "制造安全亲密感和幻想空间，不走低级擦边",
        "support_rule": "手可以靠近嘴边、耳机或胸前，但不能遮住脸和角色识别点",
        "avoid_rule": "不要成人化，不要裸露风险，不要夸张身体凝视",
    },
    {
        "name": "idol_business_smile",
        "tags": {"idol", "performance", "high_ctr"},
        "body_silhouette": "角色以半身或膝上构图营业微笑，手势可爱但不俗套",
        "personality_logic": "强化偶像感、点击欲和社交传播亲和力",
        "support_rule": "表情、发饰、服装上半身和角色色必须在小图里很清楚",
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
        "name": "phone_call_gaze",
        "tags": {"night_call", "viewer_interaction", "screen_glow"},
        "body_silhouette": "角色拿手机、扶耳机或像正在直播通话，视线和 viewer 连接",
        "personality_logic": "制造深夜陪伴、秘密聊天和社交平台停滑感",
        "support_rule": "屏幕光只服务脸和眼睛，不让 UI 杂乱",
        "avoid_rule": "不要大量文字，不要真实 app 界面，不要让手机挡脸",
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
        "support_rule": "大符号要托举角色，不要压小角色；脸和上半身必须可读",
        "avoid_rule": "不要 AAA key visual，不要西式概念图废墟，不要把角色变成比例尺",
    },
]

CHARACTER_ACTION_WEIGHTS = {
    "千夏": {
        "direct_eye_contact": 6,
        "near_camera_whisper": 5,
        "dreamy_side_glance": 8,
        "floating_daydream_pose": 7,
        "phone_call_gaze": 4,
        "idol_business_smile": 3,
        "symbolic_center_pose": 2,
    },
    "南宫": {
        "direct_eye_contact": 8,
        "phone_call_gaze": 8,
        "near_camera_whisper": 3,
        "symbolic_center_pose": 7,
        "dreamy_side_glance": 5,
        "idol_business_smile": 2,
        "floating_daydream_pose": 3,
    },
    "爱芮": {
        "idol_business_smile": 10,
        "direct_eye_contact": 8,
        "near_camera_whisper": 6,
        "phone_call_gaze": 5,
        "floating_daydream_pose": 5,
        "dreamy_side_glance": 4,
        "symbolic_center_pose": 4,
    },
    "丹": {
        "dreamy_side_glance": 8,
        "floating_daydream_pose": 8,
        "near_camera_whisper": 2,
        "direct_eye_contact": 5,
        "symbolic_center_pose": 4,
        "phone_call_gaze": 0,
        "idol_business_smile": 0,
    },
    "星见雅": {
        "symbolic_center_pose": 9,
        "direct_eye_contact": 7,
        "dreamy_side_glance": 6,
        "near_camera_whisper": 4,
        "phone_call_gaze": 4,
        "idol_business_smile": 2,
        "floating_daydream_pose": 2,
    },
    "仪玄": {
        "symbolic_center_pose": 10,
        "phone_call_gaze": 7,
        "direct_eye_contact": 6,
        "near_camera_whisper": 5,
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


CHARACTER_PROPAGATION_PROFILES = {
    "南宫": {
        "official_core": "天才队长、舞台控制者、节奏调度、小恶魔式压迫感；她知道自己处于画面中心。",
        "propagation_translation": "playful controller idol：她不是向 viewer 撒娇，而是在调度 viewer，把观众拉进自己的节奏里。",
        "viewer_relationship": "轻挑衅对视、主导镜头、像已经看穿 viewer；关系感是“你被她锁定/选中”。",
        "interaction_rule": "她调度 viewer。画面关系是命令、锁定、控场和轻挑衅，不是撒娇或求关注。",
        "thumbnail_strategy": "脸 + 黑发齐刘海 + 粉色渐变短双马尾 + 坏笑 + 科技光环/机械小翅膀 + 粉黑大色块。",
        "thumbnail_modes": ["半身控场型", "大脸命令型", "符号锁定型", "极简头像型"],
        "primary_hook_symbols": ["科技光环", "节奏 UI", "猫发夹", "坏笑手势"],
        "secondary_support_symbols": ["机械小翅膀", "粉黑舞台光", "心跳波形"],
        "fantasy_symbols": ["节奏线", "combo UI", "心跳波形", "粉黑舞台光", "机械小翅膀", "猫元素", "环绕式科技光环"],
        "safe_sensuality": "可以有小恶魔挑衅和镜头主导感，但不要走害羞软妹或低级擦边。",
        "preferred_hooks": {"neon_call_night", "ritual_star_idol", "idol_stage_dream", "ultra_minimal_character_poster", "clean_idol_studio_shot", "modern_guofeng_character_poster"},
        "preferred_actions": {"direct_eye_contact", "phone_call_gaze", "symbolic_center_pose"},
        "suppressed_misreads": ["害羞软妹", "普通粉黑主播", "普通 JK 日常", "低幼萌妹", "普通粉毛偶像", "可爱甜笑自拍", "无目的大脸自拍"],
    },
    "爱芮": {
        "official_core": "高能量舞台偶像、粉丝互动、梦境/妄想扩散、电子偶像式传播。",
        "propagation_translation": "high-energy idol romance signal：她主动靠近 viewer，用舞台感、直播感和恋爱营业感制造停滑。",
        "viewer_relationship": "像正在对 viewer 做一场只属于一个人的偶像营业；粉丝被点名、被靠近、被回应。",
        "interaction_rule": "她主动营业 viewer。画面关系是扑向观众、回应粉丝、制造恋爱信号，不是调度或压迫 viewer。",
        "thumbnail_strategy": "大脸/半身 + 粉色双马尾 + 黑色挑染刘海 + 爱心 UI + 耳机发饰 + 粉色机械翅膀 + 明亮粉黑色块。",
        "thumbnail_modes": ["大脸营业型", "半身舞台型", "手势互动型", "高色块海报型"],
        "primary_hook_symbols": ["爱心环", "麦克风", "直播 UI", "wink/对视"],
        "secondary_support_symbols": ["粉色机械翅膀", "耳机线", "idol spotlight"],
        "fantasy_symbols": ["爱心轨道", "粉黑霓虹", "漂浮歌词 UI", "直播弹幕气泡", "耳机线", "小恶魔尾巴暗示", "idol spotlight"],
        "safe_sensuality": "允许安全恋爱感、锁骨、耳机线、贴近镜头、轻微汗光；吸引力来自心动和互动，不来自成人化暴露。",
        "preferred_hooks": {"idol_stage_dream", "heart_signal_closeup", "candy_sky_poster", "neon_call_night", "fairytale_pop_storybook", "clean_idol_studio_shot"},
        "preferred_actions": {"idol_business_smile", "direct_eye_contact", "near_camera_whisper", "phone_call_gaze"},
        "suppressed_misreads": ["普通粉毛萌妹", "低气压神性", "大远景孤独感", "硬擦边", "只靠露肤制造吸引力"],
    },
    "千夏": {
        "official_core": "作曲/音乐创作者、紧张但认真、想把情绪传达给大家、梦境与舞台背后的内向能量。",
        "propagation_translation": "mint emotional composer comfort：她不是强营业角色，而是让 viewer 觉得她在慢慢靠近。",
        "viewer_relationship": "像把刚写好的旋律小心翼翼递给 viewer；安静、清透、紧张但真诚的陪伴感。",
        "interaction_rule": "她小心靠近 viewer。画面关系是陪伴、递出情绪、慢慢靠近，不是强营业或攻击性自拍。",
        "thumbnail_strategy": "脸 + 薄荷中短层次发 + 大号薄荷蝴蝶结 + 不对称刘海 + 心形耳饰 + 耳机/乐谱/风 + 清透夏日大色块。",
        "thumbnail_modes": ["清透半身型", "窗边陪伴型", "音乐符号型", "极简薄荷头像型"],
        "primary_hook_symbols": ["大号薄荷蝴蝶结", "漂浮乐谱", "耳机线", "薄荷色风"],
        "secondary_support_symbols": ["透明饮料", "水光", "发光云"],
        "fantasy_symbols": ["漂浮乐谱", "耳机线", "透明饮料", "薄荷色风", "水面反射", "发光云", "小型音符 UI", "透明窗帘"],
        "safe_sensuality": "以青春陪伴和空气感为主，可以亲近但不要强自拍压脸、成熟性感或偶像大营业。",
        "preferred_hooks": {"summer_mint_afterglow", "floating_room_daydream", "heart_signal_closeup", "candy_sky_poster", "dream_mist_portrait", "fairytale_pop_storybook"},
        "preferred_actions": {"dreamy_side_glance", "direct_eye_contact", "floating_daydream_pose", "near_camera_whisper"},
        "suppressed_misreads": ["普通元气偶像", "粉色强营业甜妹", "成熟性感角色", "暗黑工业感", "低幼卖萌"],
    },
    "丹": {
        "official_core": "项目原创人格：浅粉短发、粉紫眼、安静温柔、略淡漠、未来圣女感。",
        "propagation_translation": "quiet sacred dream poster：她不主动营业，而是用安静、梦境、神性和距离感制造收藏欲。",
        "viewer_relationship": "像从安静梦境里看向 viewer；半距离感、透明未来感、淡淡情绪。",
        "interaction_rule": "她安静凝视 viewer。画面关系是梦境里的轻微注视和收藏感，不是主动营业、自拍或性感邀约。",
        "thumbnail_strategy": "脸 + 浅粉短发 + 粉紫眼 + 白银光环/羽毛/月亮/水面 + 大面积干净浅色。",
        "thumbnail_modes": ["安静大脸型", "枕头梦境型", "浅色收藏海报型", "极简圣洁头像型"],
        "primary_hook_symbols": ["枕头梦境", "羽毛", "白银光环", "月亮"],
        "secondary_support_symbols": ["星形发卡", "透明书本", "水面"],
        "fantasy_symbols": ["白银光环", "羽毛", "水面", "月亮", "镜面", "星形发卡", "轻机械模块", "透明圣堂", "梦境云层"],
        "safe_sensuality": "不做强营业、不做微色情；吸引力来自安静神性、收藏海报感和不完全属于现实的距离。避免成熟御姐圣女、大胸成人化和身体焦点。",
        "preferred_hooks": {"moon_confession_fantasy", "floating_room_daydream", "summer_mint_afterglow", "ultra_minimal_character_poster", "dream_mist_portrait", "modern_guofeng_character_poster"},
        "preferred_actions": {"dreamy_side_glance", "floating_daydream_pose", "direct_eye_contact"},
        "suppressed_misreads": ["普通白毛圣女", "成熟御姐圣女", "大胸成人化", "自拍主播", "粉色偶像营业", "强微色情", "身体曲线焦点"],
    },
    "星见雅": {
        "official_core": "冷静严肃的剑客气质，黑色长直发、厚重齐刘海、黑色兽耳、红眼和太刀是核心记忆点。",
        "propagation_translation": "cool blade heroine icon：她的传播钩子是冷静、危险、优雅和一眼记住的黑红剪影。",
        "viewer_relationship": "她不是热情营业，而是用极稳的对视让 viewer 感到被判断、被锁定。",
        "interaction_rule": "她锁定 viewer。画面关系是冷静判断和危险吸引，不是甜美互动。",
        "thumbnail_strategy": "脸 + 黑长直齐刘海 + 黑色兽耳 + 红眼 + 太刀/刀线 + 黑红高辨识幻想符号。",
        "thumbnail_modes": ["黑红大脸型", "刀线符号型", "冷静半身型", "极简黑红头像型"],
        "primary_hook_symbols": ["红眼", "太刀刀线", "黑色兽耳", "黑红月亮"],
        "secondary_support_symbols": ["细红光轨", "风中长发", "星图圆环"],
        "fantasy_symbols": ["刀线高光", "黑红月亮", "兽耳剪影", "细红光轨", "星图圆环", "风中长发"],
        "safe_sensuality": "保持冷艳和剑客压迫，不做软妹化、卖萌化或低级性感。",
        "preferred_hooks": {"ritual_star_idol", "moon_confession_fantasy", "neon_call_night", "heart_signal_closeup", "modern_guofeng_character_poster", "clean_idol_studio_shot"},
        "preferred_actions": {"symbolic_center_pose", "direct_eye_contact", "dreamy_side_glance"},
        "suppressed_misreads": ["短发", "卷发", "蓬松偶像发型", "丢失兽耳", "丢失太刀", "软妹化"],
    },
    "仪玄": {
        "official_core": "银白长发、黑色波浪/闪电状发饰、金/琥珀眼、成熟从容、黑色灵鸟。",
        "propagation_translation": "mature occult charm signal：她用从容、戏谑和灵鸟符号制造神秘吸引力。",
        "viewer_relationship": "像在轻松掌控 viewer 的注意力；不是强营业，而是成熟、游刃有余、带一点戏谑。",
        "interaction_rule": "她轻松掌控 viewer。画面关系是成熟从容、戏谑和神秘吸引，不是甜妹营业。",
        "thumbnail_strategy": "脸 + 银白长发 + 黑色闪电发饰 + 金色眼睛 + 黑色灵鸟 + 金黑高识别幻想符号。",
        "thumbnail_modes": ["金黑大脸型", "灵鸟符号型", "成熟半身型", "极简银白头像型"],
        "primary_hook_symbols": ["黑色灵鸟", "黑色闪电发饰", "金色眼睛", "金色术光"],
        "secondary_support_symbols": ["符号圆环", "银白长发光边", "夜色星图"],
        "fantasy_symbols": ["黑色灵鸟", "金色术光", "黑色闪电线", "符号圆环", "银白长发光边", "夜色星图"],
        "safe_sensuality": "可以成熟、有距离、有压迫，但不要少女化、甜妹化或成人化擦边。",
        "preferred_hooks": {"ritual_star_idol", "neon_call_night", "moon_confession_fantasy", "heart_signal_closeup", "modern_guofeng_character_poster", "clean_idol_studio_shot"},
        "preferred_actions": {"symbolic_center_pose", "phone_call_gaze", "direct_eye_contact", "near_camera_whisper"},
        "suppressed_misreads": ["短发", "少女化", "过度甜美", "丢失黑色发饰", "丢失黑色灵鸟"],
    },
}


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
