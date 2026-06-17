import random


ART_DIRECTION_PLANS = [
    {
        "name": "black_frame_pressure",
        "graphic_concept": "巨大黑色机械框景压缩空间，角色不在画面中心，黑白剪影先成立",
        "spatial_structure": "狭窄纵向机械框架与倾斜玻璃切割画面，前景黑色结构占画面约三分之一",
        "visual_device": "半透明显示器、黑色框架、斜向光带共同形成画面骨架",
        "body_silhouette": "角色蹲坐或半跪在画面下方，身体形成紧凑三角轮廓，一只手靠近前景形成近大远小",
        "outfit_direction": "工业救援制服：短外套、束带、反光条、轻量护具和实用口袋，设计清楚但不繁复",
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
        "outfit_direction": "未来通勤装：短款结构外套、高腰下装、简洁领口、轻机能腰带",
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
        "outfit_direction": "设计师外套造型：大廓形短外套、内搭、腰部束带或简洁短裙/短裤",
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
        "outfit_direction": "轻量学院机能装：短外套、衬衫或内搭、非固定色短裙/短裤、运动鞋或厚底鞋",
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
        "outfit_direction": "街头轻机能：短夹克、层次内搭、工装短裤或不规则半裙、可见鞋子设计",
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
        "outfit_direction": "柔软日常设计款：短上衣、轻薄外套、简洁下装，有一个明确领口或袖口设计点",
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
        "outfit_direction": "运动实验装：短款上衣、轻运动外套、机能短裙或短裤、清楚鞋袜设计",
        "material_language": "弹力运动布、半透明外层、轻量塑料扣、细反光边",
        "color_strategy": "主色从服装主题决定，可用灰白、冷蓝、深海绿或低饱和黑；角色识别色只做小面积强调",
        "lighting_behavior": "近景高光柔和，背景光点克制，不做廉价 RGB",
    },
    {
        "name": "telephoto_compression",
        "graphic_concept": "长焦镜头压缩空间，巨大背景结构贴近人物，画面拒绝开阔感",
        "spatial_structure": "巨型月亮、工业塔、桥墩或全息广告牌占据大部分背景，人物被远景结构压住",
        "visual_device": "极度虚化的铁丝网、雨滴、栏杆或前景碎片切过画面，背景逆光形成清楚轮廓光",
        "body_silhouette": "角色半身、膝上或收敛站姿，动作幅度很小，主要靠眼神、肩线和局部手部动作建立压迫感",
        "outfit_direction": "防风高领、战术披风、修身外套或轻量护具，保留角色核心特征但减少碎饰",
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
        "outfit_direction": "下半身机能风增强：防水工装裤、重型战术靴、搭扣、短外套或贴身内搭",
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
        "outfit_direction": "流线型机能服、轻量夹克、长带或可读的运动鞋靴，强调速度而不是复杂装饰",
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


WEATHER_ATMOSPHERE = [
    {
        "name": "normal_clear_air",
        "prompt_concept": "正常清透空气，不加入强天气介质，让空间结构和角色动作成为主导",
        "tags": {"normal_air"},
        "weight": 6,
    },
    {
        "name": "volumetric_dust",
        "prompt_concept": "丁达尔光尘埃，空气中有细小浮尘，适合废墟、楼梯、机械框架和静态压迫空间",
        "tags": {"dust", "hazy", "quiet"},
        "weight": 2,
    },
    {
        "name": "heavy_rain_droplets",
        "prompt_concept": "暴雨与镜头水珠，强调湿润质感、雨线、潮湿衣料边缘和地面反光",
        "tags": {"rain", "wet", "reflection", "dark_mood"},
        "weight": 2,
    },
    {
        "name": "thick_fog",
        "prompt_concept": "浓雾让背景白化，远景信息被吞没，适合巨大空间留白、孤独感和拒绝感",
        "tags": {"fog", "large_space", "quiet", "low_visibility"},
        "weight": 2,
    },
    {
        "name": "clear_clinical",
        "prompt_concept": "无尘室般的冷锐空气，边缘清楚、阴影干净，带审视感和压迫感",
        "tags": {"clinical", "cold", "hard_geometry"},
        "weight": 1,
    },
]


CAMERA_LENSES = [
    {
        "name": "14mm_ultra_wide",
        "prompt_concept": "14mm 超广角，强透视和边缘拉伸，只在舞台侵入、速度感或前景压迫时使用",
        "match_names": {"stage_intrusion", "foreground_hand_intrusion", "kinetic_motion_blur"},
        "tags": {"wide_angle", "foreground_pressure"},
    },
    {
        "name": "35mm_environmental",
        "prompt_concept": "35mm 环境人像镜头，角色与空间关系清楚，适合视觉装置参与构图",
        "match_names": {"black_frame_pressure", "tilted_glass_cut", "neon_puddle_reflection", "controlled_command"},
        "tags": {"environmental_lens"},
    },
    {
        "name": "50mm_standard",
        "prompt_concept": "50mm 标准镜头，接近人眼视角，纪实、稳定、不过分夸张",
        "match_names": {"quiet_observation", "defensive_fold", "weighted_recline", "plant_shadow_mask"},
        "tags": {"standard_lens"},
    },
    {
        "name": "85mm_portrait_compression",
        "prompt_concept": "85mm 轻长焦，压缩背景但保留人物姿态，适合克制、冷静和拒绝感",
        "match_names": {"over_shoulder_departure", "large_space_stillness", "blade_stillness", "occult_command"},
        "tags": {"telephoto", "compressed"},
    },
    {
        "name": "200mm_telephoto",
        "prompt_concept": "200mm 长焦，空间强烈压缩，背景贴近人物，适合蓄势、半拔刃和巨大背景压迫",
        "match_names": {"telephoto_compression", "half_drawn_tension"},
        "tags": {"telephoto", "compressed", "background_pressure"},
    },
]


LIGHTING_STRATEGIES = [
    {
        "name": "plan_native_lighting",
        "prompt_concept": "沿用本张视觉企划本身的光影逻辑，不额外覆盖光线",
        "match_names": set(),
        "tags": {"native_lighting"},
        "weight": 5,
    },
    {
        "name": "chiaroscuro_drama",
        "prompt_concept": "强烈单侧光，脸部一侧进入阴影，明暗结构清楚，适合压迫、蓄势和刀刃停顿",
        "match_names": {"blade_stillness", "half_drawn_tension", "quiet_observation", "telephoto_compression"},
        "tags": {"chiaroscuro", "high_contrast", "deep_shadow"},
        "weight": 2,
    },
    {
        "name": "diffused_melancholy",
        "prompt_concept": "阴天漫反射柔光，反差较低，情绪安静、湿润、略带忧郁",
        "match_names": {"post_combat_exhaustion", "large_space_stillness", "over_shoulder_departure", "thick_fog"},
        "tags": {"diffused", "melancholy", "low_contrast"},
        "weight": 2,
    },
    {
        "name": "clinical_harsh",
        "prompt_concept": "冷硬顶光与锋利阴影边缘，像无尘室或审讯灯，带审视感和压迫感",
        "match_names": {"black_frame_pressure", "occult_command", "clear_clinical"},
        "tags": {"clinical", "hard_light", "cold"},
        "weight": 1,
    },
    {
        "name": "wet_reflection_gel",
        "prompt_concept": "冷暖反射光从潮湿地面反打人物，控制霓虹感，只保留少量边缘色彩",
        "match_names": {"neon_puddle_reflection", "heavy_rain_droplets", "stage_intrusion"},
        "tags": {"reflection_light", "rain", "controlled_neon"},
        "weight": 1,
    },
]


def choose_weather_atmosphere(plan: dict, action: dict, recent_tags: list[str] | None = None) -> dict:
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    plan_tags = PLAN_TAGS.get(plan["name"], set())
    action_tags = action.get("tags", set())
    for weather in WEATHER_ATMOSPHERE:
        tags = weather.get("tags", set())
        if tags & blocked:
            continue
        weight = int(weather.get("weight", 1))
        if tags & plan_tags or tags & action_tags:
            weight += 2
        if plan["name"] == "neon_puddle_reflection" and weather["name"] == "heavy_rain_droplets":
            weight += 3
        if "large_space" in action_tags and weather["name"] == "thick_fog":
            weight += 2
        candidates.append(weather)
        weights.append(weight)
    return _weighted_choice(candidates, weights)


def choose_camera_lens(plan: dict, action: dict) -> dict:
    names = {plan["name"], action["name"]}
    suitable = [lens for lens in CAMERA_LENSES if lens["match_names"] & names]
    if suitable:
        return random.choice(suitable)
    return next(lens for lens in CAMERA_LENSES if lens["name"] == "50mm_standard")


def choose_lighting_strategy(plan: dict, action: dict, weather: dict) -> dict:
    names = {plan["name"], action["name"], weather["name"]}
    candidates = []
    weights = []
    for lighting in LIGHTING_STRATEGIES:
        weight = int(lighting.get("weight", 1))
        if lighting["match_names"] & names:
            weight += 3
        candidates.append(lighting)
        weights.append(weight)
    return _weighted_choice(candidates, weights)


INFORMATION_BALANCE_STRATEGIES = [
    {
        "name": "protagonist_dominant_75",
        "label": "主角型",
        "prompt_concept": "画面信息分配约为：75% 角色，10% 图形结构，5% 空间装置，10% 留白与节奏。人物是绝对主角，空间只负责托举角色魅力。",
        "director_note": "适合验证角色魅力、服装和脸部识别，不要让背景抢戏。",
        "tags": {"protagonist_focus", "character_heavy"},
        "weight": 5,
    },
    {
        "name": "character_cover_60",
        "label": "角色封面型",
        "prompt_concept": "画面信息分配约为：60% 角色，20% 图形结构，10% 空间装置，10% 留白与节奏。角色足够大，但仍保留封面式图形设计。",
        "director_note": "适合半身到膝上构图，角色存在感强，图形结构不消失。",
        "tags": {"protagonist_focus", "cover_balance"},
        "weight": 6,
    },
    {
        "name": "fashion_feature_55",
        "label": "服装展示型",
        "prompt_concept": "画面信息分配约为：55% 角色，15% 图形结构，10% 空间装置，20% 服装轮廓与材质节奏。重点看服装剪裁、腰线、袖口、鞋靴和整体女性向设计。",
        "director_note": "适合检验换装效果，人物不能只剩脸，服装上半身和腰线必须清楚。",
        "tags": {"protagonist_focus", "fashion_focus"},
        "weight": 4,
    },
    {
        "name": "classic_balance_40",
        "label": "平衡封面型",
        "prompt_concept": "画面信息分配约为：40% 角色，25% 图形结构，20% 空间装置，15% 留白与节奏。角色、空间和图形共同成立，保持商业封面感。",
        "director_note": "适合多数 art direction，既不变成纯写真，也不让空间压过角色。",
        "tags": {"balanced"},
        "weight": 8,
    },
    {
        "name": "graphic_first_30",
        "label": "图形优先型",
        "prompt_concept": "画面信息分配约为：30% 角色，35% 图形结构，20% 空间装置，15% 留白与节奏。先读到大形、切割、圆环、阴影或几何结构，再读到角色。",
        "director_note": "适合强图形企划，角色是画面的一部分，不是唯一目的。",
        "tags": {"graphic_layout", "balanced"},
        "weight": 5,
    },
    {
        "name": "space_dominant_20",
        "label": "空间主导型",
        "prompt_concept": "画面信息分配约为：20% 角色，30% 图形结构，30% 空间装置，20% 留白与节奏。空间情绪先成立，角色像进入巨大场域里的演员。",
        "director_note": "适合巨大空间、建筑、神殿、竖井和空旷场景。",
        "tags": {"large_space", "space_focus"},
        "weight": 4,
    },
    {
        "name": "extreme_negative_space_15",
        "label": "极端留白型",
        "prompt_concept": "画面信息分配约为：15% 角色，20% 图形结构，20% 空间装置，45% 留白与节奏。角色可以很小，留白必须有压迫、孤独或仪式感。",
        "director_note": "适合丹、巨大空间和作者性 KV，不适合每张都用。",
        "tags": {"large_space", "negative_space", "quiet"},
        "weight": 2,
    },
    {
        "name": "device_driven_35",
        "label": "装置驱动型",
        "prompt_concept": "画面信息分配约为：35% 角色，20% 图形结构，30% 空间装置，15% 留白与节奏。玻璃、栏杆、线缆、纸张、镜面或布料装置必须参与构图。",
        "director_note": "适合视觉装置强的企划，让装置服务角色，不要变成杂物展示。",
        "tags": {"device_focus", "foreground_pressure"},
        "weight": 4,
    },
    {
        "name": "emotion_stillness_25",
        "label": "情绪静止型",
        "prompt_concept": "画面信息分配约为：25% 角色，20% 图形结构，25% 空间装置，30% 留白与节奏。动作很小，情绪由空气、距离、光线和支撑重量表达。",
        "director_note": "适合低能量动作，避免大手、漂浮和镜头互动。",
        "tags": {"quiet", "low_energy", "negative_space"},
        "weight": 4,
    },
]


CHARACTER_INFORMATION_BALANCE_WEIGHTS = {
    "千夏": {
        "protagonist_dominant_75": 5,
        "character_cover_60": 7,
        "fashion_feature_55": 5,
        "classic_balance_40": 7,
        "graphic_first_30": 4,
        "space_dominant_20": 3,
        "extreme_negative_space_15": 2,
        "device_driven_35": 5,
        "emotion_stillness_25": 6,
    },
    "南宫": {
        "protagonist_dominant_75": 5,
        "character_cover_60": 6,
        "fashion_feature_55": 4,
        "classic_balance_40": 7,
        "graphic_first_30": 6,
        "space_dominant_20": 4,
        "extreme_negative_space_15": 2,
        "device_driven_35": 6,
        "emotion_stillness_25": 4,
    },
    "爱芮": {
        "protagonist_dominant_75": 7,
        "character_cover_60": 8,
        "fashion_feature_55": 5,
        "classic_balance_40": 6,
        "graphic_first_30": 5,
        "space_dominant_20": 3,
        "extreme_negative_space_15": 1,
        "device_driven_35": 5,
        "emotion_stillness_25": 2,
    },
    "丹": {
        "protagonist_dominant_75": 4,
        "character_cover_60": 5,
        "fashion_feature_55": 4,
        "classic_balance_40": 6,
        "graphic_first_30": 5,
        "space_dominant_20": 8,
        "extreme_negative_space_15": 7,
        "device_driven_35": 4,
        "emotion_stillness_25": 8,
    },
    "星见雅": {
        "protagonist_dominant_75": 5,
        "character_cover_60": 6,
        "fashion_feature_55": 3,
        "classic_balance_40": 7,
        "graphic_first_30": 6,
        "space_dominant_20": 5,
        "extreme_negative_space_15": 3,
        "device_driven_35": 4,
        "emotion_stillness_25": 5,
    },
    "仪玄": {
        "protagonist_dominant_75": 5,
        "character_cover_60": 6,
        "fashion_feature_55": 4,
        "classic_balance_40": 7,
        "graphic_first_30": 5,
        "space_dominant_20": 5,
        "extreme_negative_space_15": 3,
        "device_driven_35": 5,
        "emotion_stillness_25": 5,
    },
}


def choose_information_balance(character_name: str, plan: dict, action: dict, recent_tags: list[str] | None = None) -> dict:
    primary = _primary_character(character_name)
    character_weights = CHARACTER_INFORMATION_BALANCE_WEIGHTS.get(primary, {})
    plan_tags = PLAN_TAGS.get(plan["name"], set())
    action_tags = action.get("tags", set())
    blocked = _blocked_tags(recent_tags)
    candidates = []
    weights = []
    for strategy in INFORMATION_BALANCE_STRATEGIES:
        tags = strategy.get("tags", set())
        if tags & blocked:
            continue
        weight = int(strategy.get("weight", 1)) + int(character_weights.get(strategy["name"], 0))
        if "large_space" in plan_tags and {"space_focus", "negative_space"} & tags:
            weight += 4
        if "foreground_pressure" in plan_tags and "device_focus" in tags:
            weight += 3
        if "graphic_layout" in plan_tags and "graphic_layout" in tags:
            weight += 3
        if "quiet" in action_tags and {"negative_space", "low_energy"} & tags:
            weight += 3
        if "stage" in plan_tags or action["name"] == "stage_intrusion":
            if "protagonist_focus" in tags:
                weight += 3
        if plan["name"] in {"small_figure_large_space", "negative_space_monolith", "cracked_white_room"}:
            if strategy["name"] in {"space_dominant_20", "extreme_negative_space_15", "emotion_stillness_25"}:
                weight += 4
        candidates.append(strategy)
        weights.append(max(1, weight))
    return _weighted_choice(candidates, weights)


def choose_develop_combo(character_name: str, recent_tags: list[str] | None = None) -> dict:
    plan, action = choose_plan_and_action(character_name, recent_tags)
    combo_tags = [*(recent_tags or []), *PLAN_TAGS.get(plan["name"], set()), *action.get("tags", set())]
    weather = choose_weather_atmosphere(plan, action, combo_tags)
    lens = choose_camera_lens(plan, action)
    lighting = choose_lighting_strategy(plan, action, weather)
    information_balance = choose_information_balance(character_name, plan, action, combo_tags)
    return {
        "art_plan": plan,
        "action_style": action,
        "weather_atmosphere": weather,
        "camera_lens": lens,
        "lighting_strategy": lighting,
        "information_balance": information_balance,
    }


def collect_develop_cooldown_tags(
    plan: dict,
    action: dict,
    weather: dict,
    lens: dict,
    lighting: dict,
    information_balance: dict | None = None,
) -> list[str]:
    tags = set(collect_cooldown_tags(plan, action))
    tags.update(weather.get("tags", set()))
    tags.update(lens.get("tags", set()))
    tags.update(lighting.get("tags", set()))
    if information_balance:
        tags.update(information_balance.get("tags", set()))
    return sorted(tags)


# ---------------------------------------------------------------------------
# Fenjue develop expansion pack
#
# This block intentionally extends the stable develop engine without replacing
# its proven selector functions. The goal is to make the experimental branch
# behave like an art-direction lab: more spatial grammar, more character-driven
# action, and richer photographic control.
# ---------------------------------------------------------------------------

EXTRA_ART_DIRECTION_PLANS = [
    {
        "name": "negative_space_monolith",
        "graphic_concept": "巨大的单色墙体或光面立柱压住画面，角色只占小体积，靠孤独感和比例关系成立",
        "spatial_structure": "垂直巨墙、极端留白、狭小角色落点，空间像沉默的纪念碑",
        "visual_device": "巨大平面、锐利投影、极小人物、地面反射形成安静但有重量的图形",
        "body_silhouette": "角色低能量站立或停步，身体不迎合镜头，衣摆只做极小幅度运动",
        "outfit_direction": "极简长外套、窄腰线、少量金属扣或透明边缘，服装为大空间让位",
        "material_language": "哑光布料、光滑墙面、冷白玻璃、少量磨砂金属",
        "color_strategy": "大面积低饱和冷白或灰蓝，角色识别色只作为眼睛、发饰和小型扣件出现",
        "lighting_behavior": "高处柔和天光，大面积阴影，人物边缘保持清楚但不过亮",
    },
    {
        "name": "mirror_corridor_recursion",
        "graphic_concept": "镜面走廊反复切分角色轮廓，空间像多层记忆回声",
        "spatial_structure": "两侧镜面、玻璃门、斜向走廊形成重复框景，角色被切成几个节奏块",
        "visual_device": "镜中局部反射、半透明玻璃边、错位倒影、斜向透视线",
        "body_silhouette": "角色侧身停在走廊节点，手不伸向镜头，视线从反射里回看",
        "outfit_direction": "干净都市机能外套或轻礼服混搭，轮廓利落，适合镜面切割",
        "material_language": "冷玻璃、镜面金属、哑光衣料、少量透明薄膜",
        "color_strategy": "银灰、冷蓝、低饱和角色点缀，避免彩虹反光泛滥",
        "lighting_behavior": "走廊侧光和镜面二次反射，光线被玻璃分层",
    },
    {
        "name": "overhead_map_layout",
        "graphic_concept": "极高俯视像地图一样组织画面，角色成为图面中的清晰符号",
        "spatial_structure": "地面网格、楼梯平台、圆形地标或透明地板从上方展开",
        "visual_device": "地面线条、散落纸张、影子和角色身体共同形成平面设计",
        "body_silhouette": "角色坐、躺或停步在图形节点上，身体轮廓必须像图标一样可读",
        "outfit_direction": "上半身设计简洁，下装和鞋靴形成清楚外轮廓，避免碎饰淹没俯视图",
        "material_language": "磨砂地面、玻璃砖、纸张、轻薄尼龙",
        "color_strategy": "浅底色配一个清晰主色点，保证缩小后仍能读出人物",
        "lighting_behavior": "顶部大面积漫射光，影子成为构图的一部分",
    },
    {
        "name": "vertical_billboard_cut",
        "graphic_concept": "巨型竖向广告牌或灯箱裁切角色，现代城市版式感强",
        "spatial_structure": "巨大灯箱、窄巷、竖向钢架和人物形成错位比例",
        "visual_device": "竖向光块、暗部墙面、前景电线、半遮挡灯箱边缘",
        "body_silhouette": "角色贴近灯箱边缘行走或停顿，背部和肩线被竖向光带切开",
        "outfit_direction": "城市夜行机能服、短外套、腰包或细带，但不要变成赛博杂物堆",
        "material_language": "湿润墙面、塑料灯箱、磨砂尼龙、黑色金属",
        "color_strategy": "冷暗底色加一处暖色灯箱，角色默认色降到小面积识别点",
        "lighting_behavior": "侧面灯箱光为主，背景城市光低存在感",
    },
    {
        "name": "subway_platform_crosswind",
        "graphic_concept": "地铁进站风把衣摆和头发压成横向流线，空间速度感来自风而不是伸手",
        "spatial_structure": "长站台、轨道线、屏蔽门和远处车灯形成深透视",
        "visual_device": "横向风线、模糊列车灯、站台边缘、衣摆弧线",
        "body_silhouette": "角色站稳或半转身，重心抓地，头发和衣摆被侧风拉开",
        "outfit_direction": "防风短外套、内搭、工装短裙或长裤，鞋靴要有支撑感",
        "material_language": "防风布、橡胶鞋底、站台金属、玻璃门反射",
        "color_strategy": "灰蓝站台底色，加一处角色色和一处信号灯色",
        "lighting_behavior": "顶部冷白灯和列车侧光交替，脸部保持可读",
    },
    {
        "name": "ruined_chapel_backlight",
        "graphic_concept": "破损礼拜堂的巨大窗洞从背后照亮角色，圣洁与废墟同时存在",
        "spatial_structure": "破碎拱窗、斜倒梁柱、地面碎片，角色处在光洞边缘",
        "visual_device": "拱形框景、灰尘光束、碎玻璃、长阴影",
        "body_silhouette": "角色静立、跪坐或靠在残墙旁，动作小但情绪重",
        "outfit_direction": "简化礼服、战术外套或圣女感机能服，避免传统奇幻厚重装甲",
        "material_language": "粗糙石面、薄纱、磨损金属、干燥尘埃",
        "color_strategy": "灰白废墟中保留一条清晰角色色，不做全图梦幻粉紫",
        "lighting_behavior": "强背光、柔和尘埃、脸部弱补光",
    },
    {
        "name": "archive_room_paper_storm",
        "graphic_concept": "纸张和档案像风暴一样绕过角色，但背景仍保持图形秩序",
        "spatial_structure": "档案柜、桌面、纸张轨迹和窄窗构成室内风场",
        "visual_device": "飞纸、夹子、透明文件袋、桌面投影",
        "body_silhouette": "角色护住文件、低头穿过纸阵或坐在桌边，动作服务人格而非镜头",
        "outfit_direction": "学院机能、衬衫外套、束带短裙或宽松长裤，强调袖口和领口",
        "material_language": "纸张、棉布、透明文件袋、旧木桌或金属柜",
        "color_strategy": "纸张暖白和空间灰为主，角色色只做文件标记、发饰、眼睛",
        "lighting_behavior": "窗边斜光切过纸张，空气中有轻微尘埃",
    },
    {
        "name": "server_cathedral",
        "graphic_concept": "服务器机柜像教堂立柱排列，角色被科技空间压缩成仪式感剪影",
        "spatial_structure": "高耸机柜、冷光线缆、狭窄通道和头顶桥架形成垂直秩序",
        "visual_device": "线缆弧线、点状指示灯、黑色前景框、远处冷光门",
        "body_silhouette": "角色低能量行走或停在通道中央，手部动作极小，气质压住画面",
        "outfit_direction": "冷感战术外套、短披肩、紧凑腰线或长靴，避免全身科幻装甲",
        "material_language": "黑色机柜、冷玻璃、哑光皮革、线缆",
        "color_strategy": "深灰黑和冷蓝为主，角色识别色只作小型发光点",
        "lighting_behavior": "机柜边缘冷光、顶部窄光，强控制暗部",
    },
    {
        "name": "rooftop_water_tank",
        "graphic_concept": "屋顶水箱和围栏形成巨大圆柱与斜线，角色处于城市边缘",
        "spatial_structure": "水箱、天线、围栏、远处城市低轮廓，天空留白大",
        "visual_device": "圆柱阴影、栏杆线、晾衣绳或电线切割画面",
        "body_silhouette": "角色坐在水箱底座或靠围栏，动作有重量，不漂浮",
        "outfit_direction": "日常外套、运动鞋、轻机能配件，服装要像能真实坐在屋顶",
        "material_language": "旧水泥、锈蚀金属、棉布、橡胶鞋底",
        "color_strategy": "天空灰蓝或晚霞米橙为主，角色色克制点缀",
        "lighting_behavior": "黄昏低角度长阴影，脸部轻微反光",
    },
    {
        "name": "underpass_shadow_slice",
        "graphic_concept": "高架桥下的巨大阴影把画面切成黑白两块，角色处于明暗边界",
        "spatial_structure": "桥墩、斜坡、涂鸦墙和远处小光口组成压缩空间",
        "visual_device": "大阴影、粗糙墙面、斜向护栏、地面反光",
        "body_silhouette": "角色靠墙、插兜或低头站在阴影边缘，动作内收",
        "outfit_direction": "街头机能外套、宽松裤或短裙加厚鞋，配件少但轮廓硬",
        "material_language": "混凝土、雨后地面、尼龙、磨砂金属",
        "color_strategy": "黑灰与一处角色色对撞，避免可爱色全铺",
        "lighting_behavior": "桥下暗部大块面，远处光源打出窄边缘光",
    },
    {
        "name": "frozen_escalator_diagonal",
        "graphic_concept": "停止运行的扶梯斜线贯穿画面，角色被放进强烈对角结构",
        "spatial_structure": "扶梯、玻璃护栏、楼层空洞和反射地面构成连续斜线",
        "visual_device": "扶手带、金属台阶、玻璃倒影、上下楼层切片",
        "body_silhouette": "角色坐在扶梯台阶或站在斜线上，身体顺着对角线压缩",
        "outfit_direction": "城市通勤与舞台感混搭，短外套、腰线、鞋靴清楚",
        "material_language": "金属台阶、玻璃、哑光衣料、橡胶扶手",
        "color_strategy": "中性商场灰白为主，角色色作为扶梯节奏点",
        "lighting_behavior": "室内冷光和玻璃反射，避免商业写真平光",
    },
    {
        "name": "aquarium_blue_silence",
        "graphic_concept": "巨大水族箱蓝色光面压过画面，角色像被水下世界观察",
        "spatial_structure": "水族箱玻璃、鱼影、蓝色暗部和窄走道形成静态深度",
        "visual_device": "水波纹、鱼群剪影、玻璃反光、人物倒影",
        "body_silhouette": "角色侧身贴近玻璃或坐在暗处，动作安静，视线不必直视镜头",
        "outfit_direction": "轻薄外套或简洁裙裤，面料被蓝光统一，配件极少",
        "material_language": "水面光、玻璃、哑光布料、少量金属",
        "color_strategy": "深蓝和水绿色为主，角色固有色被水光压低",
        "lighting_behavior": "水波 caustics 投在脸和衣服上，整体低噪点",
    },
    {
        "name": "cable_forest_tangle",
        "graphic_concept": "大量线缆像森林枝条一样形成前景和背景，角色被工业线条包围",
        "spatial_structure": "线缆、吊架、设备箱、窄通道组成复杂但有秩序的空间",
        "visual_device": "粗线缆前景、细线缆背景、局部小灯、黑色框景",
        "body_silhouette": "角色穿过线缆或在其间停住，身体动作小，空间压迫强",
        "outfit_direction": "战术背心、短夹克、束带或护腕，但细节控制在少数焦点",
        "material_language": "橡胶线缆、金属扣、尼龙、磨损塑料",
        "color_strategy": "黑灰工业底色，角色色像信号灯一样少量出现",
        "lighting_behavior": "点状设备光和窄顶光，让线缆成为暗部图形",
    },
    {
        "name": "ceremonial_gate_symmetry_break",
        "graphic_concept": "近似对称的仪式门框被角色偏位打破，庄重但不死板",
        "spatial_structure": "巨门、台阶、垂帘或灯柱形成轴线，角色偏离中心造成张力",
        "visual_device": "门框、垂直帘、地面轴线、单侧强光",
        "body_silhouette": "角色站在轴线旁或回身离开，动作收敛，气场由空间放大",
        "outfit_direction": "仪式感外套、长裙摆或短披肩，但避免厚重宫廷化",
        "material_language": "石材、薄帘、金属边、哑光布",
        "color_strategy": "低饱和金、黑、白或冷灰，角色色作为破坏对称的点",
        "lighting_behavior": "门后背光和单侧补光，强调整体轴线",
    },
    {
        "name": "elevator_shaft_depth",
        "graphic_concept": "电梯井或竖井的深度形成坠落感，角色处在边缘而非中心",
        "spatial_structure": "竖向井道、钢索、维护平台、远处光点向下消失",
        "visual_device": "垂直钢索、平台边缘、黑色深处、警示灯点",
        "body_silhouette": "角色蹲在平台边、扶着栏杆或背对深井，必须有重量支撑",
        "outfit_direction": "维护服感机能外套、硬鞋、腰带或手套，动作可信",
        "material_language": "冷金属、磨损漆面、橡胶、暗玻璃",
        "color_strategy": "深灰竖井加一处高明度安全色或角色色",
        "lighting_behavior": "上方窄光和深处反光，压出纵深",
    },
    {
        "name": "laundry_rooftop_wind",
        "graphic_concept": "屋顶晾晒布料被风拉成巨大平面，角色在日常空间里被图形包围",
        "spatial_structure": "晾衣绳、床单、屋顶围墙和天空形成多层半透明平面",
        "visual_device": "白布前景、夹子、小旗、天空留白、衣料投影",
        "body_silhouette": "角色穿过布料或坐在矮墙边，动作自然低能量",
        "outfit_direction": "日常轻外套、衬衫、宽松裤或短裙，设计感藏在领口袖口",
        "material_language": "棉布、阳光、旧水泥、塑料夹",
        "color_strategy": "暖白和天空蓝为主，小面积角色色像生活物件",
        "lighting_behavior": "午后硬度适中的阳光，布料透光形成柔影",
    },
    {
        "name": "moonlit_blade_plain",
        "graphic_concept": "空旷地面、低月光和一条刀线构成极简剑客视觉",
        "spatial_structure": "开阔平面、低矮远景、月亮或冷光源压在背景",
        "visual_device": "刀鞘直线、月光边缘、地面长影、少量风尘",
        "body_silhouette": "角色半拔刀或背身停步，动作极小但杀气清楚",
        "outfit_direction": "和风战术外套、腰间绳结、护臂、简洁长靴",
        "material_language": "刀鞘漆面、粗布、皮革、冷金属",
        "color_strategy": "黑白灰和冷月蓝为主，红橙眼睛或小饰件成为唯一高纯点",
        "lighting_behavior": "月光侧逆光，脸部暗而可读",
    },
    {
        "name": "talisman_black_bird_orbit",
        "graphic_concept": "符纸和黑色灵鸟围绕角色形成轨道，空间像术式启动前一秒",
        "spatial_structure": "空旷室内或屋顶，符纸轨迹和黑鸟剪影形成圆形动线",
        "visual_device": "符纸、黑鸟、金色细线、半透明术式圆环",
        "body_silhouette": "角色站立或侧坐，手势小而有掌控感，不做夸张施法动作",
        "outfit_direction": "东方术法与都市战术混搭，修身外套、护臂、流苏少量出现",
        "material_language": "纸、黑羽、金属、哑光黑布",
        "color_strategy": "黑金白为主，眼睛和符纹提供高纯焦点",
        "lighting_behavior": "金色符光从低处扫过，背景保持克制",
    },
    {
        "name": "empty_stage_after_show",
        "graphic_concept": "演出结束后的空舞台比角色更大，聚光灯余温和散落物件讲故事",
        "spatial_structure": "空舞台、撤下的灯架、地面胶带、远处幕布和空座位",
        "visual_device": "单束残余聚光、麦克风支架剪影、地面反光、纸屑",
        "body_silhouette": "角色坐在舞台边或背对空座位，动作不营业",
        "outfit_direction": "舞台服退场状态：外套半披、鞋靴清楚、装饰减少",
        "material_language": "舞台木地板、黑幕、灯架金属、亮片极少",
        "color_strategy": "暗场暖黑为主，角色色作为残余光里的小亮点",
        "lighting_behavior": "一束舞台余光和大面积暗部，让情绪落下来",
    },
    {
        "name": "cracked_white_room",
        "graphic_concept": "纯白房间被裂缝和阴影切开，角色像在干净空间里出现微小失衡",
        "spatial_structure": "白墙、白地、裂纹、折角和极少家具形成抽象空间",
        "visual_device": "裂缝线、白色块面、单个椅子或台座、人物投影",
        "body_silhouette": "角色坐在地面、靠墙或半跪，动作小，心理压力由空间表达",
        "outfit_direction": "极简白灰服装或低饱和外套，腰线和鞋靴必须清楚",
        "material_language": "白墙、哑光地面、棉布、轻金属",
        "color_strategy": "白灰主导，角色发色和眼睛成为唯一温度",
        "lighting_behavior": "高亮但不过曝，裂缝和投影提供结构",
    },
]

ART_DIRECTION_PLANS.extend(EXTRA_ART_DIRECTION_PLANS)

PLAN_TAGS.update({
    "negative_space_monolith": {"large_space", "quiet", "static", "hard_geometry"},
    "mirror_corridor_recursion": {"reflection", "glass", "depth", "quiet"},
    "overhead_map_layout": {"overhead", "graphic_layout", "static"},
    "vertical_billboard_cut": {"urban", "hard_geometry", "compressed"},
    "subway_platform_crosswind": {"wind", "grounded", "depth"},
    "ruined_chapel_backlight": {"dust", "large_space", "backlight", "quiet"},
    "archive_room_paper_storm": {"paper", "wind", "medium_energy"},
    "server_cathedral": {"hard_geometry", "dark_mood", "compressed", "clinical"},
    "rooftop_water_tank": {"grounded", "large_space", "quiet"},
    "underpass_shadow_slice": {"hard_geometry", "dark_mood", "grounded"},
    "frozen_escalator_diagonal": {"diagonal", "grounded", "glass"},
    "aquarium_blue_silence": {"blue", "quiet", "reflection", "water"},
    "cable_forest_tangle": {"hard_geometry", "dark_mood", "foreground_pressure"},
    "ceremonial_gate_symmetry_break": {"large_space", "static", "backlight"},
    "elevator_shaft_depth": {"depth", "hard_geometry", "grounded"},
    "laundry_rooftop_wind": {"wind", "soft_curve", "daily"},
    "moonlit_blade_plain": {"blade", "quiet", "static", "dark_mood"},
    "talisman_black_bird_orbit": {"occult", "bird", "controlled", "medium_energy"},
    "empty_stage_after_show": {"stage", "quiet", "low_energy"},
    "cracked_white_room": {"large_space", "quiet", "clinical", "static"},
})


def _apply_character_plan_expansion() -> None:
    updates = {
        "千夏": {
            "archive_room_paper_storm": 8,
            "stair_perspective": 8,
            "underpass_shadow_slice": 5,
            "frozen_escalator_diagonal": 6,
            "rooftop_water_tank": 5,
            "subway_platform_crosswind": 6,
            "overhead_map_layout": 5,
            "laundry_rooftop_wind": 4,
            "cable_forest_tangle": 3,
            "negative_space_monolith": 3,
        },
        "南宫": {
            "server_cathedral": 8,
            "cable_forest_tangle": 7,
            "underpass_shadow_slice": 6,
            "vertical_billboard_cut": 6,
            "elevator_shaft_depth": 6,
            "mirror_corridor_recursion": 5,
            "empty_stage_after_show": 5,
            "frozen_escalator_diagonal": 4,
            "telephoto_compression": 5,
            "black_frame_pressure": 8,
        },
        "爱芮": {
            "empty_stage_after_show": 7,
            "ceremonial_gate_symmetry_break": 5,
            "overhead_map_layout": 5,
            "vertical_billboard_cut": 4,
            "laundry_rooftop_wind": 5,
            "subway_platform_crosswind": 4,
            "negative_space_monolith": 3,
            "high_view_floating": 4,
            "foreground_hand_intrusion": 2,
            "cracked_white_room": 3,
        },
        "丹": {
            "negative_space_monolith": 10,
            "cracked_white_room": 9,
            "ruined_chapel_backlight": 8,
            "aquarium_blue_silence": 7,
            "ceremonial_gate_symmetry_break": 6,
            "mirror_corridor_recursion": 6,
            "small_figure_large_space": 10,
            "plant_shadow_mask": 6,
            "rooftop_water_tank": 3,
            "archive_room_paper_storm": 3,
        },
        "星见雅": {
            "moonlit_blade_plain": 10,
            "telephoto_compression": 8,
            "underpass_shadow_slice": 7,
            "server_cathedral": 5,
            "vertical_billboard_cut": 6,
            "mirror_corridor_recursion": 5,
            "ceremonial_gate_symmetry_break": 5,
            "negative_space_monolith": 6,
            "elevator_shaft_depth": 4,
            "ruined_chapel_backlight": 4,
        },
        "仪玄": {
            "talisman_black_bird_orbit": 10,
            "server_cathedral": 6,
            "ruined_chapel_backlight": 6,
            "mirror_corridor_recursion": 5,
            "telephoto_compression": 6,
            "ceremonial_gate_symmetry_break": 7,
            "cable_forest_tangle": 4,
            "negative_space_monolith": 5,
            "underpass_shadow_slice": 4,
            "cracked_white_room": 4,
        },
    }
    for character, weights in updates.items():
        CHARACTER_PLAN_WEIGHTS.setdefault(character, {}).update(weights)


_apply_character_plan_expansion()

EXTRA_ACTION_STYLES = [
    {
        "name": "low_guard_wait",
        "tags": {"grounded", "controlled", "no_reach", "medium_energy"},
        "body_silhouette": "角色重心下压，双脚稳定，手臂贴近身体形成低位防备轮廓",
        "personality_logic": "不是攻击瞬间，而是等待对方先动，适合冷静、掌控型角色",
        "support_rule": "必须看出脚底抓地和膝盖受力，身体有真实重量",
        "avoid_rule": "不要冲向镜头，不要大幅张开手臂，不要漂浮",
    },
    {
        "name": "kneeling_recovery",
        "tags": {"grounded", "support", "low_energy", "quiet", "heavy_weight"},
        "body_silhouette": "单膝或双膝接触地面，肩线放松，手撑地或搭在膝上形成恢复姿态",
        "personality_logic": "战后或情绪低潮后的短暂停顿，画面靠重量和呼吸感成立",
        "support_rule": "膝盖、手掌或墙面必须承担身体重量",
        "avoid_rule": "不要舞台营业，不要轻飘飘，不要跳跃或伸手",
    },
    {
        "name": "hairpin_turn",
        "tags": {"turn", "medium_energy", "no_reach", "wind"},
        "body_silhouette": "角色像刚刚被叫住一样急停转身，头发和衣摆落后身体半拍",
        "personality_logic": "用转身动作制造瞬间性，但不靠手伸向镜头",
        "support_rule": "一只脚作为旋转轴，另一只脚轻微离开或刚落地",
        "avoid_rule": "不要正面站定，不要自拍回头，不要前景大手",
    },
    {
        "name": "object_shadow_hide",
        "tags": {"quiet", "foreground_pressure", "no_reach", "shadow"},
        "body_silhouette": "角色被栏杆、帘子、玻璃或植物阴影遮住一部分身体，只露出眼神和肩线",
        "personality_logic": "用遮挡制造观察感和距离感，适合内向、疏离或危险角色",
        "support_rule": "遮挡物必须成为构图结构，不只是装饰",
        "avoid_rule": "不要完全无遮挡正脸，不要过度表演",
    },
    {
        "name": "distant_walkaway",
        "tags": {"no_reach", "depth", "quiet", "reject", "small_figure"},
        "body_silhouette": "角色向画面深处走去，背影或侧背影为主，只有头部轻微回看或完全不回头",
        "personality_logic": "让空间和离场感成为叙事，不向观众讨好",
        "support_rule": "脚步方向必须和空间透视线一致",
        "avoid_rule": "不要正面迎接镜头，不要微笑营业，不要分身",
    },
    {
        "name": "seated_edge_drop",
        "tags": {"grounded", "support", "quiet", "edge"},
        "body_silhouette": "角色坐在平台、窗台、楼梯或舞台边缘，一条腿下垂，另一条腿收起",
        "personality_logic": "动作有重量，有等待感，适合把角色固定进空间",
        "support_rule": "臀部和手掌必须有明确支撑面",
        "avoid_rule": "不要漂浮，不要躺平刷屏，不要伸手",
    },
    {
        "name": "one_step_pause",
        "tags": {"grounded", "depth", "quiet", "medium_energy"},
        "body_silhouette": "角色迈出一步后停住，身体微微前倾但不冲刺，鞋靴和地面关系清楚",
        "personality_logic": "用即将行动的犹豫感替代夸张动作",
        "support_rule": "前脚承重，后脚保持平衡，衣摆顺着动作轻微移动",
        "avoid_rule": "不要跑跳，不要高速动效，不要前景大手",
    },
    {
        "name": "blade_sheath_click",
        "tags": {"blade", "controlled", "no_reach", "tension", "grounded"},
        "body_silhouette": "角色一手扶刀鞘或刀柄，动作停在收刀或半出鞘的一瞬间，身体极稳",
        "personality_logic": "杀气来自克制和静止，不直接挥砍",
        "support_rule": "双脚稳定，肩颈线紧但动作幅度小",
        "avoid_rule": "不要完全拔刀大挥砍，不要爆炸特效，不要跳跃",
    },
    {
        "name": "occult_bird_perch",
        "tags": {"occult", "bird", "controlled", "quiet", "no_reach"},
        "body_silhouette": "角色手臂或肩头停着黑色灵鸟，身体静止，视线像在命令画面外的事物",
        "personality_logic": "术式不靠大动作，而靠旁观者感和上位气质",
        "support_rule": "鸟、手臂、肩线构成小型焦点三角",
        "avoid_rule": "不要夸张施法姿势，不要大量鸟群淹没画面",
    },
    {
        "name": "paper_scatter_reachless",
        "tags": {"paper", "wind", "medium_energy", "no_reach"},
        "body_silhouette": "纸张飞起，角色用身体避开或护住资料，手臂收在身体附近",
        "personality_logic": "动态来自环境，不来自角色向镜头进攻",
        "support_rule": "身体与纸张风向相反，形成清楚张力",
        "avoid_rule": "不要伸手抓镜头，不要全身漂浮",
    },
    {
        "name": "railing_balance",
        "tags": {"grounded", "support", "edge", "medium_energy", "no_reach"},
        "body_silhouette": "角色单手扶栏杆或坐在栏杆旁，身体重心和栏杆形成斜向平衡",
        "personality_logic": "用边缘感制造紧张，不用大动作",
        "support_rule": "栏杆必须承重，腿部和鞋靴位置可信",
        "avoid_rule": "不要悬空飞行，不要前景大手",
    },
    {
        "name": "wall_slide_down",
        "tags": {"grounded", "support", "low_energy", "quiet", "heavy_weight"},
        "body_silhouette": "角色背靠墙缓慢滑坐，膝盖弯曲，肩线和头部低下来",
        "personality_logic": "强调疲惫、沉默、失落或战后空白",
        "support_rule": "墙面和地面必须同时提供支撑",
        "avoid_rule": "不要笑得营业，不要轻飘飘，不要伸手",
    },
    {
        "name": "eye_only_threat",
        "tags": {"controlled", "quiet", "tension", "no_reach"},
        "body_silhouette": "身体几乎不动，只用眼神、下颌和肩颈角度制造压迫感",
        "personality_logic": "适合高位角色，危险感来自少动作",
        "support_rule": "姿态必须稳定，构图和光影承担主要张力",
        "avoid_rule": "不要夸张表情，不要挥手，不要冲镜头",
    },
    {
        "name": "coat_wrap_defense",
        "tags": {"quiet", "defensive", "soft_curve", "no_reach"},
        "body_silhouette": "角色用外套、披肩或围巾包住身体，轮廓收缩成防御形态",
        "personality_logic": "动作表达保护自己、犹豫或寒冷，而不是展示服装",
        "support_rule": "衣物包裹必须形成清楚大形，不要碎布乱飞",
        "avoid_rule": "不要布料龙卷风，不要身体大幅展开",
    },
    {
        "name": "floor_reflection_stare",
        "tags": {"reflection", "grounded", "quiet", "no_reach"},
        "body_silhouette": "角色低头看向地面倒影或水面，身体和倒影形成上下关系",
        "personality_logic": "把情绪放在自我观察或沉默里",
        "support_rule": "地面、水面或玻璃必须承担视觉焦点的一部分",
        "avoid_rule": "不要看镜头营业，不要高能动作",
    },
    {
        "name": "hands_behind_back",
        "tags": {"quiet", "controlled", "no_reach", "static"},
        "body_silhouette": "角色双手背在身后或藏在外套里，肩线放松，姿态干净",
        "personality_logic": "用克制、隐藏和轻微距离感替代手部表演",
        "support_rule": "身体重心必须自然，头部与肩部关系清楚",
        "avoid_rule": "不要伸手，不要手靠脸，不要摆拍剪刀手",
    },
    {
        "name": "threshold_pause",
        "tags": {"depth", "quiet", "static", "no_reach"},
        "body_silhouette": "角色停在门框、窗框或台阶边界，半个身体在光里、半个在暗里",
        "personality_logic": "表现进入或离开前一秒的心理停顿",
        "support_rule": "门框或边界必须成为画面结构",
        "avoid_rule": "不要冲出画面，不要大动作",
    },
]

ACTION_STYLES.extend(EXTRA_ACTION_STYLES)


def _apply_character_action_expansion() -> None:
    updates = {
        "千夏": {
            "defensive_fold": 9,
            "seated_edge_drop": 8,
            "paper_scatter_reachless": 8,
            "coat_wrap_defense": 7,
            "wall_slide_down": 6,
            "railing_balance": 6,
            "one_step_pause": 5,
            "hands_behind_back": 5,
            "distant_walkaway": 4,
            "floor_reflection_stare": 4,
        },
        "南宫": {
            "controlled_command": 8,
            "eye_only_threat": 8,
            "low_guard_wait": 6,
            "object_shadow_hide": 6,
            "threshold_pause": 6,
            "hands_behind_back": 6,
            "railing_balance": 5,
            "over_shoulder_departure": 5,
            "seated_edge_drop": 4,
            "stage_intrusion": 2,
        },
        "爱芮": {
            "stage_intrusion": 5,
            "hairpin_turn": 7,
            "one_step_pause": 5,
            "seated_edge_drop": 5,
            "railing_balance": 5,
            "hands_behind_back": 3,
            "large_space_stillness": 4,
            "floor_reflection_stare": 3,
            "coat_wrap_defense": 3,
            "foreground_hand_intrusion": 2,
        },
        "丹": {
            "large_space_stillness": 10,
            "floor_reflection_stare": 8,
            "threshold_pause": 8,
            "wall_slide_down": 7,
            "coat_wrap_defense": 7,
            "object_shadow_hide": 6,
            "distant_walkaway": 6,
            "seated_edge_drop": 6,
            "hands_behind_back": 5,
            "one_step_pause": 4,
        },
        "星见雅": {
            "blade_sheath_click": 10,
            "half_drawn_tension": 9,
            "low_guard_wait": 8,
            "eye_only_threat": 7,
            "over_shoulder_departure": 6,
            "post_combat_exhaustion": 4,
            "threshold_pause": 5,
            "distant_walkaway": 5,
            "object_shadow_hide": 4,
            "hands_behind_back": 4,
        },
        "仪玄": {
            "occult_bird_perch": 10,
            "eye_only_threat": 8,
            "over_shoulder_departure": 7,
            "threshold_pause": 6,
            "hands_behind_back": 6,
            "low_guard_wait": 5,
            "floor_reflection_stare": 5,
            "post_combat_exhaustion": 3,
            "paper_scatter_reachless": 4,
            "object_shadow_hide": 5,
        },
    }
    for character, weights in updates.items():
        CHARACTER_ACTION_WEIGHTS.setdefault(character, {}).update(weights)


_apply_character_action_expansion()

COOLDOWN_TAG_BLOCKS.update({
    "grounded": {"floating", "wide_angle"},
    "support": {"floating", "explosive"},
    "small_figure": {"wide_angle", "foreground_pressure", "reach"},
    "blade": {"stage", "soft_curve"},
    "occult": {"stage", "soft_curve"},
    "paper": {"explosive"},
    "edge": {"floating"},
    "hard_geometry": {"soft_curve"},
    "static": {"explosive", "reach", "motion_blur"},
})

WEATHER_ATMOSPHERE.extend([
    {
        "name": "blue_hour_haze",
        "prompt_concept": "蓝调时刻的薄雾，城市边缘变成柔和蓝灰色块，情绪安静但不阴沉",
        "tags": {"hazy", "blue", "quiet"},
        "weight": 3,
    },
    {
        "name": "snow_silence",
        "prompt_concept": "细雪和低噪点冷空气，背景声音像被吸收，适合静态与孤独空间",
        "tags": {"snow", "quiet", "large_space"},
        "weight": 2,
    },
    {
        "name": "ash_fall",
        "prompt_concept": "缓慢落灰或燃尽纸屑，空气干燥，画面带战后余温",
        "tags": {"ash", "dust", "low_energy"},
        "weight": 2,
    },
    {
        "name": "dry_heat_shimmer",
        "prompt_concept": "远景热浪轻微扭曲，空气干燥，空间边缘有折射感",
        "tags": {"heat", "large_space"},
        "weight": 1,
    },
    {
        "name": "window_condensation",
        "prompt_concept": "窗面凝结水汽与指痕，室内外温差让玻璃变成情绪屏障",
        "tags": {"glass", "wet", "quiet"},
        "weight": 3,
    },
    {
        "name": "sea_mist",
        "prompt_concept": "海风带来的盐雾和低饱和水汽，远景被蓝白空气吞掉",
        "tags": {"fog", "blue", "large_space"},
        "weight": 2,
    },
    {
        "name": "fluorescent_dust",
        "prompt_concept": "室内荧光灯下漂浮的微尘，空间冷、旧、略有压迫",
        "tags": {"dust", "clinical", "cold"},
        "weight": 2,
    },
    {
        "name": "after_rain_clear",
        "prompt_concept": "雨后放晴的干净空气，地面仍有反光，颜色清楚但不过饱和",
        "tags": {"rain", "reflection", "clear"},
        "weight": 3,
    },
    {
        "name": "smoke_after_battle",
        "prompt_concept": "战斗后残留的低矮烟雾，前景暗部轻微吞没地面",
        "tags": {"smoke", "dark_mood", "low_energy"},
        "weight": 2,
    },
    {
        "name": "floating_pollen",
        "prompt_concept": "逆光中的细小花粉和微粒，空气温柔但保持构图克制",
        "tags": {"pollen", "soft_curve", "quiet"},
        "weight": 2,
    },
    {
        "name": "icy_breath",
        "prompt_concept": "冷空气中微弱白色呼气，情绪低温，人物动作更慢",
        "tags": {"cold", "quiet", "low_energy"},
        "weight": 2,
    },
    {
        "name": "paper_dust",
        "prompt_concept": "纸张摩擦带起的细尘和纸屑，适合档案室、练习室和创作场景",
        "tags": {"paper", "dust", "medium_energy"},
        "weight": 2,
    },
    {
        "name": "storm_front_light",
        "prompt_concept": "暴雨前的低压空气，天空偏暗但边缘有强烈冷白光",
        "tags": {"dark_mood", "wind", "backlight"},
        "weight": 2,
    },
    {
        "name": "indoor_stale_air",
        "prompt_concept": "封闭室内的沉闷空气，光线低流动，适合压迫型空间",
        "tags": {"compressed", "quiet", "dark_mood"},
        "weight": 2,
    },
    {
        "name": "twilight_smog",
        "prompt_concept": "黄昏城市雾霾，远景灯点被空气压扁，空间有疲惫感",
        "tags": {"hazy", "urban", "low_energy"},
        "weight": 2,
    },
    {
        "name": "halo_backscatter",
        "prompt_concept": "强背光在空气粒子上形成柔和 halo，但控制光晕，不让画面失控",
        "tags": {"backlight", "hazy", "large_space"},
        "weight": 2,
    },
    {
        "name": "lens_mist",
        "prompt_concept": "镜头边缘轻微水汽，焦点仍清楚，边缘被柔化",
        "tags": {"wet", "foreground_pressure", "quiet"},
        "weight": 1,
    },
    {
        "name": "dry_wind_grit",
        "prompt_concept": "干风带起细沙和颗粒，衣摆和头发有真实风阻",
        "tags": {"wind", "dust", "grounded"},
        "weight": 2,
    },
    {
        "name": "glass_prism_air",
        "prompt_concept": "玻璃折射让空气出现淡淡棱镜色，但只在边缘和焦点附近出现",
        "tags": {"glass", "reflection", "clinical"},
        "weight": 2,
    },
    {
        "name": "silent_whiteout",
        "prompt_concept": "背景被白色空气吞没，只保留少量边界线和人物轮廓",
        "tags": {"large_space", "fog", "quiet", "clinical"},
        "weight": 2,
    },
])

CAMERA_LENSES.extend([
    {
        "name": "24mm_low_angle_environment",
        "prompt_concept": "24mm 低机位环境镜头，空间压迫比手部前景更重要，适合建筑和楼梯",
        "match_names": {"stair_perspective", "server_cathedral", "elevator_shaft_depth", "low_guard_wait"},
        "tags": {"wide_angle", "environmental_lens", "grounded"},
    },
    {
        "name": "28mm_documentary_wide",
        "prompt_concept": "28mm 纪实广角，保留环境信息但避免夸张大手，像现场抓拍",
        "match_names": {"subway_platform_crosswind", "archive_room_paper_storm", "one_step_pause"},
        "tags": {"environmental_lens"},
    },
    {
        "name": "40mm_story_lens",
        "prompt_concept": "40mm 叙事镜头，人物和空间权重均衡，适合安静故事性画面",
        "match_names": {"plant_shadow_mask", "rooftop_water_tank", "threshold_pause", "coat_wrap_defense"},
        "tags": {"standard_lens", "story_lens"},
    },
    {
        "name": "70mm_soft_compression",
        "prompt_concept": "70mm 柔和压缩，背景靠近但不糊成纯色，适合中景情绪图",
        "match_names": {"aquarium_blue_silence", "mirror_corridor_recursion", "floor_reflection_stare"},
        "tags": {"telephoto", "compressed"},
    },
    {
        "name": "100mm_macro_detail",
        "prompt_concept": "100mm 细节镜头，压住动作，只突出眼神、手套、刀柄、发饰等局部焦点",
        "match_names": {"eye_only_threat", "blade_sheath_click", "occult_bird_perch"},
        "tags": {"telephoto", "detail_focus", "static"},
    },
    {
        "name": "135mm_stage_compression",
        "prompt_concept": "135mm 舞台压缩，角色与远处灯架或空间装置贴近，减少透视变形",
        "match_names": {"empty_stage_after_show", "stage_intrusion", "telephoto_compression"},
        "tags": {"telephoto", "compressed", "stage"},
    },
    {
        "name": "300mm_extreme_flatten",
        "prompt_concept": "300mm 极端长焦压扁空间，背景巨大图形几乎贴在角色身后",
        "match_names": {"telephoto_compression", "negative_space_monolith", "moonlit_blade_plain"},
        "tags": {"telephoto", "compressed", "background_pressure"},
    },
    {
        "name": "overhead_orthographic",
        "prompt_concept": "近似正交的高角度俯视，像平面设计稿一样组织人物和地面元素",
        "match_names": {"overhead_map_layout", "high_view_floating", "floor_reflection_stare"},
        "tags": {"overhead", "graphic_layout"},
    },
    {
        "name": "dutch_angle_35mm",
        "prompt_concept": "35mm 倾斜构图，画面有不稳定感，但人物身体结构仍保持可信",
        "match_names": {"tilted_glass_cut", "frozen_escalator_diagonal", "hairpin_turn"},
        "tags": {"environmental_lens", "diagonal"},
    },
    {
        "name": "ground_level_24mm",
        "prompt_concept": "贴近地面的 24mm 镜头，强调鞋靴、台阶、积水和支撑重量",
        "match_names": {"neon_puddle_reflection", "seated_edge_drop", "kneeling_recovery", "wall_slide_down"},
        "tags": {"wide_angle", "grounded", "reflection"},
    },
    {
        "name": "reflection_split_lens",
        "prompt_concept": "透过反光表面分割画面，本体与倒影同时存在但不制造分身",
        "match_names": {"mirror_corridor_recursion", "floor_reflection_stare", "neon_puddle_reflection"},
        "tags": {"reflection", "glass"},
    },
    {
        "name": "through_object_long_lens",
        "prompt_concept": "隔着栏杆、玻璃、植物或线缆的长焦窥视感，前景遮挡压低侵略性",
        "match_names": {"object_shadow_hide", "cable_forest_tangle", "plant_shadow_mask", "aquarium_blue_silence"},
        "tags": {"telephoto", "foreground_pressure", "quiet"},
    },
    {
        "name": "surveillance_camera_flat",
        "prompt_concept": "监控摄像头般的扁平高位视角，冷静、疏离、拒绝美少女自拍感",
        "match_names": {"server_cathedral", "underpass_shadow_slice", "hands_behind_back"},
        "tags": {"overhead", "clinical", "static"},
    },
    {
        "name": "handheld_snapshot_35mm",
        "prompt_concept": "35mm 手持抓拍感，构图略偏但不凌乱，适合日常瞬间和转身动作",
        "match_names": {"hairpin_turn", "laundry_rooftop_wind", "subway_platform_crosswind"},
        "tags": {"environmental_lens", "medium_energy"},
    },
    {
        "name": "architectural_shift_lens",
        "prompt_concept": "建筑移轴镜头，垂直线稳定，空间宏大但不过度畸变",
        "match_names": {"negative_space_monolith", "ruined_chapel_backlight", "ceremonial_gate_symmetry_break", "cracked_white_room"},
        "tags": {"large_space", "hard_geometry", "static"},
    },
])

LIGHTING_STRATEGIES.extend([
    {
        "name": "moonlit_edge",
        "prompt_concept": "冷月光从侧后方切出人物边缘，正面保持低亮度但眼神可读",
        "match_names": {"moonlit_blade_plain", "blade_sheath_click", "over_shoulder_departure"},
        "tags": {"backlight", "dark_mood", "quiet"},
        "weight": 2,
    },
    {
        "name": "sodium_vapor_backstreet",
        "prompt_concept": "街巷钠灯形成脏暖色边缘光，暗部保持灰蓝，适合城市压迫感",
        "match_names": {"underpass_shadow_slice", "vertical_billboard_cut", "rooftop_water_tank"},
        "tags": {"urban", "dark_mood", "hard_light"},
        "weight": 2,
    },
    {
        "name": "fluorescent_overhead",
        "prompt_concept": "冷白荧光顶灯制造疲惫和审视感，眼窝和衣褶有轻微硬阴影",
        "match_names": {"server_cathedral", "archive_room_paper_storm", "fluorescent_dust"},
        "tags": {"clinical", "cold", "hard_light"},
        "weight": 2,
    },
    {
        "name": "underlight_reflection",
        "prompt_concept": "地面、水面或玻璃从下方反光，脸部被低位柔光轻轻托起",
        "match_names": {"neon_puddle_reflection", "floor_reflection_stare", "after_rain_clear"},
        "tags": {"reflection_light", "reflection", "wet"},
        "weight": 2,
    },
    {
        "name": "storm_flash_slice",
        "prompt_concept": "暴风前的瞬间闪光切出锐利轮廓，背景暗而前景有短促亮面",
        "match_names": {"storm_front_light", "subway_platform_crosswind", "hairpin_turn"},
        "tags": {"backlight", "high_contrast", "wind"},
        "weight": 1,
    },
    {
        "name": "silhouette_backlight",
        "prompt_concept": "强背光让角色先成为剪影，再用少量反光恢复脸部和服装边缘",
        "match_names": {"large_space_stillness", "negative_space_monolith", "ruined_chapel_backlight", "distant_walkaway"},
        "tags": {"backlight", "large_space", "static"},
        "weight": 3,
    },
    {
        "name": "projector_cut_light",
        "prompt_concept": "投影机或窗格光把身体切成几块，光影像版式一样参与构图",
        "match_names": {"plant_shadow_mask", "cracked_white_room", "object_shadow_hide"},
        "tags": {"graphic_layout", "shadow", "hard_geometry"},
        "weight": 2,
    },
    {
        "name": "glass_prism_caustics",
        "prompt_concept": "玻璃和晶体产生克制的棱镜折射，只在焦点边缘形成彩色碎光",
        "match_names": {"tilted_glass_cut", "mirror_corridor_recursion", "glass_prism_air", "cracked_white_room"},
        "tags": {"glass", "reflection_light", "clinical"},
        "weight": 2,
    },
    {
        "name": "paper_lantern_soft",
        "prompt_concept": "纸灯或暖白间接光柔化边缘，情绪安静，避免偶像写真甜腻",
        "match_names": {"archive_room_paper_storm", "ceremonial_gate_symmetry_break", "paper_scatter_reachless"},
        "tags": {"paper", "diffused", "quiet"},
        "weight": 2,
    },
    {
        "name": "emergency_red_low",
        "prompt_concept": "低位红色警示灯只扫过小面积，不让全图变成廉价红黑",
        "match_names": {"server_cathedral", "cable_forest_tangle", "elevator_shaft_depth"},
        "tags": {"dark_mood", "hard_light"},
        "weight": 1,
    },
    {
        "name": "dawn_blue_gradient",
        "prompt_concept": "清晨蓝白渐变光，远处亮、近处冷，适合安静的出发前一秒",
        "match_names": {"rooftop_water_tank", "distant_walkaway", "one_step_pause", "blue_hour_haze"},
        "tags": {"blue", "quiet", "diffused"},
        "weight": 2,
    },
    {
        "name": "late_sunset_long_shadow",
        "prompt_concept": "傍晚低角度长阴影拉伸空间，人物不靠动作也有叙事感",
        "match_names": {"rooftop_water_tank", "underpass_shadow_slice", "subway_platform_crosswind"},
        "tags": {"shadow", "grounded", "large_space"},
        "weight": 2,
    },
    {
        "name": "aquarium_blue_caustic",
        "prompt_concept": "水族箱蓝光和水波纹在脸和衣服上缓慢移动，情绪安静疏离",
        "match_names": {"aquarium_blue_silence"},
        "tags": {"blue", "reflection_light", "quiet", "water"},
        "weight": 3,
    },
    {
        "name": "blade_flash_line",
        "prompt_concept": "刀线反光只作为一条极细高光出现，强化危险感而不进入战斗画面",
        "match_names": {"blade_stillness", "blade_sheath_click", "half_drawn_tension", "moonlit_blade_plain"},
        "tags": {"blade", "hard_light", "static"},
        "weight": 3,
    },
    {
        "name": "talisman_gold_flicker",
        "prompt_concept": "符纸和金色术光局部闪动，黑色灵鸟与暗部保持克制",
        "match_names": {"occult_command", "occult_bird_perch", "talisman_black_bird_orbit"},
        "tags": {"occult", "bird", "reflection_light"},
        "weight": 3,
    },
    {
        "name": "monitor_face_glow",
        "prompt_concept": "屏幕光只照亮眼睛和脸侧，背景设备保持暗部图形",
        "match_names": {"server_cathedral", "cable_forest_tangle", "eye_only_threat"},
        "tags": {"clinical", "dark_mood", "reflection_light"},
        "weight": 2,
    },
    {
        "name": "stage_afterglow",
        "prompt_concept": "演出结束后的残余聚光，暖光很小，周围暗部吞没多余信息",
        "match_names": {"empty_stage_after_show", "stage_intrusion"},
        "tags": {"stage", "low_energy", "dark_mood"},
        "weight": 2,
    },
    {
        "name": "white_room_overexposure_control",
        "prompt_concept": "白房间高亮但不爆掉，靠裂缝、阴影和人物边缘维持结构",
        "match_names": {"cracked_white_room", "silent_whiteout", "clear_clinical"},
        "tags": {"clinical", "large_space", "diffused"},
        "weight": 2,
    },
    {
        "name": "rain_noir_rim",
        "prompt_concept": "雨夜黑色暗部和细窄轮廓光，湿润边缘清楚但不霓虹泛滥",
        "match_names": {"heavy_rain_droplets", "neon_puddle_reflection", "vertical_billboard_cut"},
        "tags": {"rain", "dark_mood", "backlight"},
        "weight": 2,
    },
    {
        "name": "dust_ray_cathedral",
        "prompt_concept": "高处光束穿过尘埃，像教堂空间一样庄重，人物被空间放大",
        "match_names": {"ruined_chapel_backlight", "volumetric_dust", "ceremonial_gate_symmetry_break"},
        "tags": {"dust", "large_space", "backlight"},
        "weight": 2,
    },
])


def _soften_outfits_toward_feminine_design() -> None:
    replacements = {
        "未来通勤装": "未来感女性通勤装",
        "轻量学院机能装": "女性向学院轻机能套装",
        "街头轻机能": "女性向街头轻机能",
        "运动实验装": "女性向运动实验套装",
        "防风高领、战术披风、修身外套或轻量护具": "防风高领内搭、收腰短披肩、修身短外套或轻量装饰护片",
        "哑光战术面料": "哑光高级衣料",
        "下半身机能风增强：防水工装裤、重型战术靴、搭扣、短外套或贴身内搭": "下半身女性向机能风：防水短外套、高腰半裙或修身短裤、精致厚底短靴、细搭扣、贴身内搭",
        "流线型机能服、轻量夹克、长带或可读的运动鞋靴": "流线型女性运动套装、短款轻夹克、飘带或可读的精致运动鞋靴",
        "城市夜行机能服": "城市夜行女性剪裁短外套",
        "防风短外套、内搭、工装短裙或长裤": "防风短外套、贴身内搭、高腰短裙或垂坠裙裤",
        "战术外套或圣女感机能服": "收腰短外套或圣女感轻礼服",
        "学院机能、衬衫外套、束带短裙或宽松长裤": "学院感衬衫外套、束带短裙、不规则半裙或垂坠裙裤",
        "冷感战术外套": "冷感收腰短外套",
        "街头机能外套、宽松裤或短裙加厚鞋": "街头女性短外套、垂坠裙裤或短裙搭配精致厚底鞋",
        "战术背心、短夹克、束带或护腕": "短款背心式上衣、收腰短夹克、细束带或精致袖饰",
        "维护服感机能外套、硬鞋、腰带或手套": "收腰机能短外套、精致厚底鞋、细腰带或短手套",
        "和风战术外套、腰间绳结、护臂、简洁长靴": "和风收腰短外套、腰间绳结、精致袖饰、简洁长靴",
        "东方术法与都市战术混搭": "东方术法与都市女性剪裁混搭",
        "护臂": "精致袖饰",
        "外骨骼": "轻量装饰骨架",
        "厚重装甲": "厚重装甲感",
        "工装": "轻工装感",
        "战术": "轻战术感",
        "机能": "轻机能",
        "维修服": "工作感短外套",
        "重型": "精致",
        "粗糙金属磨损": "做旧金属细节",
        "硬质扣件": "精致扣件",
        "橡胶鞋底": "厚底鞋底",
        "橡胶、": "厚底鞋细节、",
    }
    feminine_rule = (
        "整体保持女性向高级服装设计：收腰、短外套、裙装或裙裤比例、精致鞋靴和柔软材质优先；"
        "硬质元素只作为少量点缀。"
    )
    for plan in ART_DIRECTION_PLANS:
        outfit = plan.get("outfit_direction", "")
        material = plan.get("material_language", "")
        for old, new in replacements.items():
            outfit = outfit.replace(old, new)
            material = material.replace(old, new)
        if feminine_rule not in outfit:
            outfit = f"{outfit}；{feminine_rule}"
        plan["outfit_direction"] = outfit
        plan["material_language"] = material


_soften_outfits_toward_feminine_design()


# ---------------------------------------------------------------------------
# Fenjue master director system
#
# The develop branch is no longer a flat random prompt composer. Each visual
# plan first resolves to a director class; that class becomes the visual
# constitution for action language, atmosphere, lens, lighting, information
# balance, and complexity budget.
# ---------------------------------------------------------------------------

PLAN_DIRECTOR_CLASS = {
    "plant_shadow_mask": "quiet_emotion",
    "aquarium_blue_silence": "quiet_emotion",
    "rooftop_water_tank": "quiet_emotion",
    "laundry_rooftop_wind": "quiet_emotion",
    "empty_stage_after_show": "quiet_emotion",
    "small_figure_large_space": "graphic_static",
    "negative_space_monolith": "architectural_pressure",
    "cracked_white_room": "graphic_static",
    "high_view_floating": "graphic_static",
    "overhead_map_layout": "graphic_static",
    "ceremonial_gate_symmetry_break": "ritual_space",
    "ruined_chapel_backlight": "ritual_space",
    "server_cathedral": "ritual_space",
    "talisman_black_bird_orbit": "ritual_space",
    "foreground_hand_intrusion": "stage_dynamic",
    "kinetic_motion_blur": "stage_dynamic",
    "cloth_s_curve": "stage_dynamic",
    "subway_platform_crosswind": "documentary_motion",
    "archive_room_paper_storm": "documentary_motion",
    "neon_puddle_reflection": "documentary_motion",
    "stair_perspective": "architectural_pressure",
    "black_frame_pressure": "architectural_pressure",
    "underpass_shadow_slice": "architectural_pressure",
    "frozen_escalator_diagonal": "architectural_pressure",
    "elevator_shaft_depth": "architectural_pressure",
    "cable_forest_tangle": "architectural_pressure",
    "tilted_glass_cut": "cinematic_compression",
    "telephoto_compression": "cinematic_compression",
    "vertical_billboard_cut": "cinematic_compression",
    "mirror_corridor_recursion": "cinematic_compression",
    "moonlit_blade_plain": "blade_pressure",
}

DIRECTOR_CLASSES = {
    "quiet_emotion": {
        "label": "quiet emotion / 安静情绪",
        "constitution": "主导演是呼吸感、重量、微动作和观察距离；所有模块必须压低侵略性，让角色在安静空间中可读。",
        "allowed_actions": {
            "quiet_observation", "weighted_recline", "defensive_fold", "kneeling_recovery",
            "object_shadow_hide", "distant_walkaway", "seated_edge_drop", "one_step_pause",
            "wall_slide_down", "coat_wrap_defense", "floor_reflection_stare",
            "hands_behind_back", "threshold_pause",
        },
        "allowed_weather": {
            "normal_clear_air", "blue_hour_haze", "floating_pollen", "window_condensation",
            "icy_breath", "snow_silence", "indoor_stale_air", "after_rain_clear",
            "thick_fog",
        },
        "allowed_lens": {
            "40mm_story_lens", "50mm_standard", "70mm_soft_compression",
            "through_object_long_lens", "reflection_split_lens", "85mm_portrait_compression",
        },
        "allowed_lighting": {
            "plan_native_lighting", "diffused_melancholy", "dawn_blue_gradient",
            "projector_cut_light", "paper_lantern_soft", "aquarium_blue_caustic",
            "late_sunset_long_shadow",
        },
        "allowed_information_balance": {
            "classic_balance_40", "graphic_first_30", "emotion_stillness_25",
            "fashion_feature_55", "character_cover_60",
        },
        "forbidden_tags": {"blade", "stage", "explosive", "motion_blur", "wide_angle", "reach"},
        "complexity_budget": {
            "max_particle_layers": 2,
            "max_foreground_devices": 2,
            "max_reflection_systems": 3,
            "max_secondary_motion": 1,
        },
    },
    "graphic_static": {
        "label": "graphic static / 静态图形",
        "constitution": "主导演是大形、留白、平面构成和静态压迫；动作只做尺度与情绪，不许抢走图形秩序。",
        "allowed_actions": {
            "large_space_stillness", "distant_walkaway", "threshold_pause",
            "hands_behind_back", "eye_only_threat", "object_shadow_hide",
            "wall_slide_down", "kneeling_recovery",
        },
        "allowed_weather": {
            "normal_clear_air", "silent_whiteout", "thick_fog", "clear_clinical",
            "blue_hour_haze", "snow_silence", "halo_backscatter",
        },
        "allowed_lens": {
            "architectural_shift_lens", "overhead_orthographic", "300mm_extreme_flatten",
            "85mm_portrait_compression", "50mm_standard",
        },
        "allowed_lighting": {
            "plan_native_lighting", "silhouette_backlight", "white_room_overexposure_control",
            "projector_cut_light", "dust_ray_cathedral", "diffused_melancholy",
        },
        "allowed_information_balance": {
            "graphic_first_30", "space_dominant_20", "extreme_negative_space_15",
            "emotion_stillness_25", "classic_balance_40",
        },
        "forbidden_tags": {"stage", "explosive", "motion_blur", "reach", "wide_angle"},
        "complexity_budget": {
            "max_particle_layers": 1,
            "max_foreground_devices": 2,
            "max_reflection_systems": 1,
            "max_secondary_motion": 0,
        },
    },
    "architectural_pressure": {
        "label": "architectural pressure / 建筑压迫",
        "constitution": "主导演是结构压力、硬边框、纵深和空间支配；角色必须被空间压住，但不能被装置吞没。",
        "allowed_actions": {
            "low_guard_wait", "one_step_pause", "threshold_pause", "hands_behind_back",
            "object_shadow_hide", "railing_balance", "seated_edge_drop",
            "eye_only_threat", "large_space_stillness", "distant_walkaway",
        },
        "allowed_weather": {
            "normal_clear_air", "indoor_stale_air", "fluorescent_dust", "volumetric_dust",
            "twilight_smog", "dry_wind_grit", "clear_clinical",
        },
        "allowed_lens": {
            "24mm_low_angle_environment", "28mm_documentary_wide", "35mm_environmental",
            "architectural_shift_lens", "surveillance_camera_flat", "40mm_story_lens",
        },
        "allowed_lighting": {
            "plan_native_lighting", "clinical_harsh", "fluorescent_overhead",
            "sodium_vapor_backstreet", "late_sunset_long_shadow", "emergency_red_low",
            "silhouette_backlight",
        },
        "allowed_information_balance": {
            "classic_balance_40", "graphic_first_30", "device_driven_35",
            "space_dominant_20", "character_cover_60",
        },
        "forbidden_tags": {"soft_curve", "floating", "stage", "explosive"},
        "complexity_budget": {
            "max_particle_layers": 1,
            "max_foreground_devices": 4,
            "max_reflection_systems": 1,
            "max_secondary_motion": 1,
        },
    },
    "stage_dynamic": {
        "label": "stage dynamic / 舞台动势",
        "constitution": "主导演是表演能量、前景侵入、动势和镜头占有；允许冲击，但必须保住身体结构和角色识别。",
        "allowed_actions": {
            "stage_intrusion", "hairpin_turn", "one_step_pause", "foreground_hand_intrusion",
            "railing_balance", "paper_scatter_reachless", "low_guard_wait",
        },
        "allowed_weather": {
            "normal_clear_air", "storm_front_light", "dry_wind_grit", "after_rain_clear",
            "paper_dust", "lens_mist",
        },
        "allowed_lens": {
            "14mm_ultra_wide", "24mm_low_angle_environment", "28mm_documentary_wide",
            "35mm_environmental", "dutch_angle_35mm", "handheld_snapshot_35mm",
        },
        "allowed_lighting": {
            "plan_native_lighting", "storm_flash_slice", "wet_reflection_gel",
            "stage_afterglow", "rain_noir_rim", "late_sunset_long_shadow",
        },
        "allowed_information_balance": {
            "protagonist_dominant_75", "character_cover_60", "fashion_feature_55",
            "classic_balance_40", "device_driven_35",
        },
        "forbidden_tags": {"large_space", "negative_space", "static", "low_energy"},
        "complexity_budget": {
            "max_particle_layers": 1,
            "max_foreground_devices": 2,
            "max_reflection_systems": 1,
            "max_secondary_motion": 2,
        },
    },
    "cinematic_compression": {
        "label": "cinematic compression / 电影压缩",
        "constitution": "主导演是长焦压迫、背景贴近、局部紧张和冷静危险感；动作幅度小，张力来自镜头压缩。",
        "allowed_actions": {
            "eye_only_threat", "blade_sheath_click", "half_drawn_tension",
            "low_guard_wait", "over_shoulder_departure", "hands_behind_back",
            "object_shadow_hide", "threshold_pause",
        },
        "allowed_weather": {
            "normal_clear_air", "blue_hour_haze", "twilight_smog", "smoke_after_battle",
            "indoor_stale_air", "glass_prism_air", "window_condensation",
        },
        "allowed_lens": {
            "70mm_soft_compression", "85mm_portrait_compression", "100mm_macro_detail",
            "135mm_stage_compression", "200mm_telephoto", "300mm_extreme_flatten",
            "through_object_long_lens",
        },
        "allowed_lighting": {
            "plan_native_lighting", "chiaroscuro_drama", "moonlit_edge",
            "blade_flash_line", "monitor_face_glow", "rain_noir_rim",
            "glass_prism_caustics",
        },
        "allowed_information_balance": {
            "character_cover_60", "fashion_feature_55", "classic_balance_40",
            "graphic_first_30", "device_driven_35",
        },
        "forbidden_tags": {"stage", "explosive", "wide_angle", "floating"},
        "complexity_budget": {
            "max_particle_layers": 1,
            "max_foreground_devices": 4,
            "max_reflection_systems": 3,
            "max_secondary_motion": 1,
        },
    },
    "blade_pressure": {
        "label": "blade pressure / 刀线压迫",
        "constitution": "主导演是刀线、静止杀气和拔刀前一秒；任何天气和光效都只能服务极细张力，不进入战斗特效。",
        "allowed_actions": {
            "blade_sheath_click", "half_drawn_tension", "blade_stillness",
            "eye_only_threat", "low_guard_wait", "threshold_pause",
            "over_shoulder_departure",
        },
        "allowed_weather": {
            "normal_clear_air", "blue_hour_haze", "icy_breath", "smoke_after_battle",
            "silent_whiteout", "ash_fall",
        },
        "allowed_lens": {
            "100mm_macro_detail", "200mm_telephoto", "300mm_extreme_flatten",
            "85mm_portrait_compression", "through_object_long_lens",
        },
        "allowed_lighting": {
            "plan_native_lighting", "moonlit_edge", "blade_flash_line",
            "chiaroscuro_drama", "silhouette_backlight",
        },
        "allowed_information_balance": {
            "character_cover_60", "classic_balance_40", "graphic_first_30",
            "emotion_stillness_25",
        },
        "forbidden_tags": {"stage", "explosive", "soft_curve", "wide_angle", "motion_blur"},
        "complexity_budget": {
            "max_particle_layers": 1,
            "max_foreground_devices": 1,
            "max_reflection_systems": 0,
            "max_secondary_motion": 1,
        },
    },
    "ritual_space": {
        "label": "ritual space / 仪式空间",
        "constitution": "主导演是仪式秩序、符号、空间层级和上位控制；奇观可以存在，但必须少而准。",
        "allowed_actions": {
            "occult_bird_perch", "occult_command", "eye_only_threat",
            "threshold_pause", "hands_behind_back", "distant_walkaway",
            "large_space_stillness", "low_guard_wait",
        },
        "allowed_weather": {
            "normal_clear_air", "halo_backscatter", "volumetric_dust", "ash_fall",
            "silent_whiteout", "fluorescent_dust", "indoor_stale_air",
        },
        "allowed_lens": {
            "architectural_shift_lens", "85mm_portrait_compression",
            "100mm_macro_detail", "135mm_stage_compression",
            "surveillance_camera_flat", "300mm_extreme_flatten",
        },
        "allowed_lighting": {
            "plan_native_lighting", "talisman_gold_flicker", "dust_ray_cathedral",
            "silhouette_backlight", "clinical_harsh", "monitor_face_glow",
        },
        "allowed_information_balance": {
            "classic_balance_40", "graphic_first_30", "space_dominant_20",
            "device_driven_35", "emotion_stillness_25",
        },
        "forbidden_tags": {"stage", "soft_curve", "motion_blur", "wide_angle"},
        "complexity_budget": {
            "max_particle_layers": 2,
            "max_foreground_devices": 2,
            "max_reflection_systems": 1,
            "max_secondary_motion": 2,
        },
    },
    "documentary_motion": {
        "label": "documentary motion / 纪实动势",
        "constitution": "主导演是现场感、可相信的风和一次性瞬间；环境可以动，角色不能散架。",
        "allowed_actions": {
            "paper_scatter_reachless", "hairpin_turn", "one_step_pause",
            "railing_balance", "floor_reflection_stare", "distant_walkaway",
            "seated_edge_drop", "low_guard_wait",
        },
        "allowed_weather": {
            "normal_clear_air", "after_rain_clear", "dry_wind_grit", "paper_dust",
            "storm_front_light", "heavy_rain_droplets", "lens_mist",
        },
        "allowed_lens": {
            "28mm_documentary_wide", "35mm_environmental", "handheld_snapshot_35mm",
            "ground_level_24mm", "reflection_split_lens", "40mm_story_lens",
        },
        "allowed_lighting": {
            "plan_native_lighting", "underlight_reflection", "paper_lantern_soft",
            "storm_flash_slice", "rain_noir_rim", "fluorescent_overhead",
        },
        "allowed_information_balance": {
            "character_cover_60", "classic_balance_40", "device_driven_35",
            "fashion_feature_55", "graphic_first_30",
        },
        "forbidden_tags": {"floating", "large_space", "negative_space"},
        "complexity_budget": {
            "max_particle_layers": 2,
            "max_foreground_devices": 2,
            "max_reflection_systems": 1,
            "max_secondary_motion": 3,
        },
    },
}

DEFAULT_DIRECTOR_CLASS = "architectural_pressure"


ENERGY_PROFILES = {
    "bright_airy": {
        "label": "明亮空气感",
        "constitution": "默认给画面保留空气、干净色块和生命力；压迫感来自构图，不来自脏暗和废弃感。",
        "preferred_weather": {"normal_clear_air", "floating_pollen", "after_rain_clear", "blue_hour_haze"},
        "preferred_lighting": {
            "plan_native_lighting", "dawn_blue_gradient", "late_sunset_long_shadow",
            "paper_lantern_soft", "diffused_melancholy",
        },
        "forbidden_tags": {"smoke", "smog", "stale", "ash", "dirty", "ruin", "dark_mood"},
        "max_low_pressure_score": 0,
    },
    "clean_tension": {
        "label": "干净张力",
        "constitution": "高级、清洁、有张力；允许压迫和暗部，但不能变成废弃、潮湿、灰败或战后衰败。",
        "preferred_weather": {"normal_clear_air", "after_rain_clear", "blue_hour_haze", "glass_prism_air", "clear_clinical"},
        "preferred_lighting": {
            "plan_native_lighting", "projector_cut_light", "silhouette_backlight",
            "blade_flash_line", "dawn_blue_gradient", "late_sunset_long_shadow",
        },
        "forbidden_tags": {"smog", "stale", "dirty", "post_battle"},
        "max_low_pressure_score": 1,
    },
    "luxury_shadow": {
        "label": "高级暗部",
        "constitution": "暗部可以存在，但必须像时装大片或高级 KV；禁止霉味、废墟、脏旧和低气压衰败。",
        "preferred_weather": {"normal_clear_air", "window_condensation", "glass_prism_air", "blue_hour_haze"},
        "preferred_lighting": {
            "chiaroscuro_drama", "glass_prism_caustics", "moonlit_edge",
            "monitor_face_glow", "projector_cut_light", "plan_native_lighting",
        },
        "forbidden_tags": {"dirty", "ruin", "stale", "smog", "ash"},
        "max_low_pressure_score": 1,
    },
    "editorial_melancholy": {
        "label": "杂志感轻忧郁",
        "constitution": "允许安静、低饱和和轻微忧郁，但画面仍要干净、可收藏、有角色魅力。",
        "preferred_weather": {"normal_clear_air", "blue_hour_haze", "window_condensation", "icy_breath", "snow_silence"},
        "preferred_lighting": {
            "diffused_melancholy", "dawn_blue_gradient", "moonlit_edge",
            "late_sunset_long_shadow", "plan_native_lighting",
        },
        "forbidden_tags": {"dirty", "ruin", "stale", "smog", "post_battle"},
        "max_low_pressure_score": 1,
    },
    "low_pressure_decay": {
        "label": "低气压衰败实验",
        "constitution": "实验性低气压、废墟、烟尘、旧工业和战后余味；只作为 develop 实验低频出现。",
        "preferred_weather": {"smoke_after_battle", "twilight_smog", "indoor_stale_air", "ash_fall"},
        "preferred_lighting": {"sodium_vapor_backstreet", "fluorescent_overhead", "rain_noir_rim", "dust_ray_cathedral"},
        "forbidden_tags": set(),
        "max_low_pressure_score": 99,
    },
}

DEFAULT_ENERGY_PROFILE = "clean_tension"

PLAN_ENERGY_PROFILE = {
    "plant_shadow_mask": "bright_airy",
    "laundry_rooftop_wind": "bright_airy",
    "rooftop_water_tank": "clean_tension",
    "aquarium_blue_silence": "clean_tension",
    "small_figure_large_space": "clean_tension",
    "negative_space_monolith": "clean_tension",
    "cracked_white_room": "clean_tension",
    "high_view_floating": "bright_airy",
    "overhead_map_layout": "clean_tension",
    "tilted_glass_cut": "luxury_shadow",
    "mirror_corridor_recursion": "luxury_shadow",
    "vertical_billboard_cut": "luxury_shadow",
    "telephoto_compression": "luxury_shadow",
    "moonlit_blade_plain": "clean_tension",
    "ceremonial_gate_symmetry_break": "clean_tension",
    "server_cathedral": "clean_tension",
    "talisman_black_bird_orbit": "clean_tension",
    "empty_stage_after_show": "editorial_melancholy",
    "ruined_chapel_backlight": "low_pressure_decay",
    "underpass_shadow_slice": "low_pressure_decay",
    "cable_forest_tangle": "low_pressure_decay",
    "neon_puddle_reflection": "low_pressure_decay",
    "elevator_shaft_depth": "low_pressure_decay",
}

LOW_PRESSURE_TAGS = {
    "ruin", "dark_mood", "smoke", "smog", "stale", "ash", "post_battle",
    "dirty", "abandoned", "low_pressure",
}

LOW_PRESSURE_NAME_TAGS = {
    "ruined_chapel_backlight": {"ruin", "abandoned", "low_pressure"},
    "underpass_shadow_slice": {"dirty", "low_pressure"},
    "cable_forest_tangle": {"dirty", "low_pressure"},
    "neon_puddle_reflection": {"wet", "dark_mood", "low_pressure"},
    "elevator_shaft_depth": {"dark_mood", "low_pressure"},
    "server_cathedral": {"clinical"},
    "negative_space_monolith": set(),
    "twilight_smog": {"smog", "low_pressure"},
    "indoor_stale_air": {"stale", "low_pressure"},
    "smoke_after_battle": {"smoke", "post_battle", "low_pressure"},
    "ash_fall": {"ash", "post_battle"},
    "fluorescent_dust": {"dust", "clinical"},
    "volumetric_dust": {"dust"},
    "heavy_rain_droplets": {"rain", "wet"},
    "rain_noir_rim": {"rain", "dark_mood"},
    "sodium_vapor_backstreet": {"dirty", "dark_mood"},
    "fluorescent_overhead": {"clinical"},
    "emergency_red_low": {"dark_mood"},
    "dust_ray_cathedral": {"dust"},
}


def _apply_xhs_default_plan_bias() -> None:
    """Keep low-pressure plans as experiments, but reduce their default batch frequency."""
    low_pressure_multipliers = {
        "ruined_chapel_backlight": 0.35,
        "underpass_shadow_slice": 0.45,
        "cable_forest_tangle": 0.4,
        "neon_puddle_reflection": 0.45,
        "elevator_shaft_depth": 0.5,
    }
    xhs_boost = {
        "plant_shadow_mask": 1.35,
        "laundry_rooftop_wind": 1.3,
        "rooftop_water_tank": 1.25,
        "tilted_glass_cut": 1.2,
        "mirror_corridor_recursion": 1.15,
        "aquarium_blue_silence": 1.2,
        "ceremonial_gate_symmetry_break": 1.15,
        "cracked_white_room": 1.15,
        "vertical_billboard_cut": 1.1,
    }
    for weights in CHARACTER_PLAN_WEIGHTS.values():
        for name, multiplier in low_pressure_multipliers.items():
            if name in weights:
                weights[name] = max(1, int(round(weights[name] * multiplier)))
        for name, multiplier in xhs_boost.items():
            if name in weights:
                weights[name] = max(1, int(round(weights[name] * multiplier)))


_apply_xhs_default_plan_bias()


def resolve_director_class(plan: dict) -> dict:
    class_name = PLAN_DIRECTOR_CLASS.get(plan["name"], DEFAULT_DIRECTOR_CLASS)
    director = dict(DIRECTOR_CLASSES[class_name])
    director["name"] = class_name
    return director


def resolve_energy_profile(plan: dict, director: dict) -> dict:
    profile_name = PLAN_ENERGY_PROFILE.get(plan["name"], DEFAULT_ENERGY_PROFILE)
    if profile_name == "low_pressure_decay" and director["name"] in {"quiet_emotion", "stage_dynamic"}:
        profile_name = DEFAULT_ENERGY_PROFILE
    profile = dict(ENERGY_PROFILES[profile_name])
    profile["name"] = profile_name
    return profile


def _by_name(items: list[dict]) -> dict[str, dict]:
    return {item["name"]: item for item in items}


def _tags_for_item(item: dict, extra_tags: set[str] | None = None) -> set[str]:
    tags = set(item.get("tags", set()))
    tags.update(extra_tags or set())
    return tags


def _directed_candidates(
    items: list[dict],
    allowed_names: set[str],
    forbidden_tags: set[str],
    blocked: set[str],
    item_extra_tags: dict[str, set[str]] | None = None,
) -> list[dict]:
    candidates = []
    item_extra_tags = item_extra_tags or {}
    for item in items:
        if allowed_names and item["name"] not in allowed_names:
            continue
        tags = _tags_for_item(item, item_extra_tags.get(item["name"]))
        if tags & forbidden_tags:
            continue
        if tags & blocked:
            continue
        candidates.append(item)
    return candidates


def _weighted_director_choice(candidates: list[dict], base_weights: dict[str, int] | None = None) -> dict:
    if not candidates:
        raise ValueError("director choice requires at least one candidate")
    base_weights = base_weights or {}
    weights = [
        max(1, int(item.get("weight", 1)) + int(base_weights.get(item["name"], 0)))
        for item in candidates
    ]
    return _weighted_choice(candidates, weights)


def _choose_action_for_director(
    character_name: str,
    plan: dict,
    director: dict,
    recent_tags: list[str] | None = None,
) -> dict:
    character = _primary_character(character_name)
    character_weights = CHARACTER_ACTION_WEIGHTS.get(character, CHARACTER_ACTION_WEIGHTS["丹"])
    blocked = _blocked_tags(recent_tags)
    candidates = _directed_candidates(
        ACTION_STYLES,
        director["allowed_actions"],
        director["forbidden_tags"],
        blocked,
    )
    weighted = []
    weights = []
    plan_tags = PLAN_TAGS.get(plan["name"], set())
    for action in candidates:
        weight = int(character_weights.get(action["name"], 0))
        if weight <= 0:
            continue
        action_tags = action.get("tags", set())
        if action_tags & plan_tags:
            weight += 2
        if action["name"] in director["allowed_actions"]:
            weight += 2
        weighted.append(action)
        weights.append(max(1, weight))
    if not weighted:
        weighted = candidates or [action for action in ACTION_STYLES if character_weights.get(action["name"], 0) > 0]
        weights = [max(1, int(character_weights.get(action["name"], 1))) for action in weighted]
    return _weighted_choice(weighted, weights)


def _choose_weather_for_director(
    plan: dict,
    action: dict,
    director: dict,
    energy_profile: dict,
    recent_tags: list[str] | None = None,
) -> dict:
    blocked = _blocked_tags(recent_tags)
    candidates = _directed_candidates(
        WEATHER_ATMOSPHERE,
        director["allowed_weather"],
        director["forbidden_tags"] | energy_profile["forbidden_tags"],
        blocked,
    )
    if not candidates:
        candidates = _directed_candidates(
            WEATHER_ATMOSPHERE,
            director["allowed_weather"],
            director["forbidden_tags"],
            blocked,
        )
    plan_tags = PLAN_TAGS.get(plan["name"], set())
    action_tags = action.get("tags", set())
    weights = []
    for weather in candidates:
        weight = int(weather.get("weight", 1))
        if weather.get("tags", set()) & (plan_tags | action_tags):
            weight += 2
        if weather["name"] in energy_profile["preferred_weather"]:
            weight += 4
        weights.append(max(1, weight))
    if not candidates:
        return next(weather for weather in WEATHER_ATMOSPHERE if weather["name"] == "normal_clear_air")
    return _weighted_choice(candidates, weights)


def _choose_lens_for_director(plan: dict, action: dict, director: dict) -> dict:
    names = {plan["name"], action["name"]}
    candidates = [
        lens for lens in CAMERA_LENSES
        if lens["name"] in director["allowed_lens"]
        and not (lens.get("tags", set()) & director["forbidden_tags"])
    ]
    matched = [lens for lens in candidates if lens.get("match_names", set()) & names]
    if matched:
        return random.choice(matched)
    if candidates:
        return random.choice(candidates)
    return next(lens for lens in CAMERA_LENSES if lens["name"] == "50mm_standard")


def _choose_lighting_for_director(plan: dict, action: dict, weather: dict, director: dict, energy_profile: dict) -> dict:
    names = {plan["name"], action["name"], weather["name"]}
    candidates = [
        lighting for lighting in LIGHTING_STRATEGIES
        if lighting["name"] in director["allowed_lighting"]
        and not (lighting.get("tags", set()) & (director["forbidden_tags"] | energy_profile["forbidden_tags"]))
    ]
    if not candidates:
        candidates = [
            lighting for lighting in LIGHTING_STRATEGIES
            if lighting["name"] in director["allowed_lighting"]
            and not (lighting.get("tags", set()) & director["forbidden_tags"])
        ]
    if not candidates:
        return next(lighting for lighting in LIGHTING_STRATEGIES if lighting["name"] == "plan_native_lighting")
    weights = []
    for lighting in candidates:
        weight = int(lighting.get("weight", 1))
        if lighting.get("match_names", set()) & names:
            weight += 3
        if lighting["name"] in energy_profile["preferred_lighting"]:
            weight += 4
        weights.append(max(1, weight))
    return _weighted_choice(candidates, weights)


def _choose_information_balance_for_director(
    character_name: str,
    plan: dict,
    action: dict,
    director: dict,
    recent_tags: list[str] | None = None,
) -> dict:
    primary = _primary_character(character_name)
    character_weights = CHARACTER_INFORMATION_BALANCE_WEIGHTS.get(primary, {})
    blocked = _blocked_tags(recent_tags)
    candidates = _directed_candidates(
        INFORMATION_BALANCE_STRATEGIES,
        director["allowed_information_balance"],
        set(),
        blocked,
    )
    if not candidates:
        candidates = INFORMATION_BALANCE_STRATEGIES
    plan_tags = PLAN_TAGS.get(plan["name"], set())
    action_tags = action.get("tags", set())
    weights = []
    for strategy in candidates:
        tags = strategy.get("tags", set())
        weight = int(strategy.get("weight", 1)) + int(character_weights.get(strategy["name"], 0))
        if strategy["name"] in director["allowed_information_balance"]:
            weight += 1
        if "large_space" in plan_tags and {"space_focus", "negative_space"} & tags:
            weight += 3
        if "foreground_pressure" in plan_tags and "device_focus" in tags:
            weight += 2
        if "quiet" in action_tags and {"negative_space", "low_energy"} & tags:
            weight += 2
        weights.append(max(1, weight))
    return _weighted_choice(candidates, weights)


COMPLEXITY_TAG_COSTS = {
    "particle_layers": {"rain", "snow", "dust", "ash", "fog", "hazy", "pollen", "smoke", "paper"},
    "foreground_devices": {"foreground_pressure", "glass", "hard_geometry", "paper", "bird", "occult"},
    "reflection_systems": {"reflection", "glass", "wet", "water", "reflection_light"},
    "secondary_motion": {"wind", "motion_blur", "speed", "floating", "cloth_flow", "paper", "bird"},
}


def _complexity_counts(*items: dict) -> dict[str, int]:
    counts = {key: 0 for key in COMPLEXITY_TAG_COSTS}
    for item in items:
        if not item:
            continue
        item_tags = set(item.get("tags", set()))
        if "name" in item:
            item_tags.update(PLAN_TAGS.get(item["name"], set()))
        for key, tags in COMPLEXITY_TAG_COSTS.items():
            if item_tags & tags:
                counts[key] += 1
    return counts


def _item_all_tags(item: dict) -> set[str]:
    tags = set(item.get("tags", set()))
    if "name" in item:
        tags.update(PLAN_TAGS.get(item["name"], set()))
        tags.update(LOW_PRESSURE_NAME_TAGS.get(item["name"], set()))
    return tags


def low_pressure_score(*items: dict) -> int:
    score = 0
    for item in items:
        if not item:
            continue
        tags = _item_all_tags(item)
        score += len(tags & LOW_PRESSURE_TAGS)
    return score


def _preferred_item(
    items: list[dict],
    preferred_names: set[str],
    allowed_names: set[str],
    forbidden_tags: set[str],
    fallback_name: str,
) -> dict:
    candidates = [
        item for item in items
        if item["name"] in preferred_names
        and (not allowed_names or item["name"] in allowed_names)
        and not (_item_all_tags(item) & forbidden_tags)
    ]
    if candidates:
        return _weighted_director_choice(candidates)
    allowed = [
        item for item in items
        if item["name"] in allowed_names
        and not (_item_all_tags(item) & forbidden_tags)
    ]
    if allowed:
        return _weighted_director_choice(allowed)
    return next(item for item in items if item["name"] == fallback_name)


def _apply_energy_profile(
    plan: dict,
    action: dict,
    weather: dict,
    lens: dict,
    lighting: dict,
    information_balance: dict,
    director: dict,
    energy_profile: dict,
) -> tuple[dict, dict, dict]:
    score = low_pressure_score(plan, action, weather, lens, lighting, information_balance)
    max_score = int(energy_profile["max_low_pressure_score"])
    adjusted = False
    if score > max_score:
        weather = _preferred_item(
            WEATHER_ATMOSPHERE,
            energy_profile["preferred_weather"],
            director["allowed_weather"],
            director["forbidden_tags"] | energy_profile["forbidden_tags"],
            "normal_clear_air",
        )
        lighting = _preferred_item(
            LIGHTING_STRATEGIES,
            energy_profile["preferred_lighting"],
            director["allowed_lighting"],
            director["forbidden_tags"] | energy_profile["forbidden_tags"],
            "plan_native_lighting",
        )
        adjusted = True
    final_score = low_pressure_score(plan, action, weather, lens, lighting, information_balance)
    return weather, lighting, {
        "profile": energy_profile["name"],
        "label": energy_profile["label"],
        "low_pressure_score": final_score,
        "max_low_pressure_score": max_score,
        "adjusted": adjusted,
    }


def _apply_complexity_budget(
    plan: dict,
    action: dict,
    weather: dict,
    lens: dict,
    lighting: dict,
    information_balance: dict,
    director: dict,
) -> tuple[dict, dict, dict, dict]:
    budget = dict(director["complexity_budget"])
    counts = _complexity_counts(plan, action, weather, lens, lighting, information_balance)
    over_budget = [
        key for key, count in counts.items()
        if count > budget.get(f"max_{key}", 99)
    ]
    if not over_budget:
        return weather, lens, lighting, {"budget": budget, "counts": counts, "over_budget": []}

    if counts["particle_layers"] > budget["max_particle_layers"]:
        weather = next(item for item in WEATHER_ATMOSPHERE if item["name"] == "normal_clear_air")
    if counts["reflection_systems"] > budget["max_reflection_systems"]:
        non_reflection_lenses = [
            item for item in CAMERA_LENSES
            if item["name"] in director["allowed_lens"]
            and not (item.get("tags", set()) & {"reflection", "glass", "wet"})
        ]
        if non_reflection_lenses:
            lens = random.choice(non_reflection_lenses)
        non_reflection_lighting = [
            item for item in LIGHTING_STRATEGIES
            if item["name"] in director["allowed_lighting"]
            and not (item.get("tags", set()) & {"reflection", "reflection_light", "water", "glass", "wet"})
        ]
        if non_reflection_lighting:
            lighting = _weighted_director_choice(non_reflection_lighting)
    if counts["foreground_devices"] > budget["max_foreground_devices"]:
        plain_lighting = next(item for item in LIGHTING_STRATEGIES if item["name"] == "plan_native_lighting")
        lighting = plain_lighting
    if counts["secondary_motion"] > budget["max_secondary_motion"]:
        still_lenses = [
            item for item in CAMERA_LENSES
            if item["name"] in director["allowed_lens"]
            and not (item.get("tags", set()) & {"wide_angle", "medium_energy"})
        ]
        if still_lenses:
            lens = random.choice(still_lenses)

    final_counts = _complexity_counts(plan, action, weather, lens, lighting, information_balance)
    final_over_budget = [
        key for key, count in final_counts.items()
        if count > budget.get(f"max_{key}", 99)
    ]
    return weather, lens, lighting, {
        "budget": budget,
        "counts": final_counts,
        "over_budget": final_over_budget,
    }


def choose_develop_combo(character_name: str, recent_tags: list[str] | None = None) -> dict:
    plan = choose_art_plan(character_name, recent_tags)
    director = resolve_director_class(plan)
    energy_profile = resolve_energy_profile(plan, director)
    director_tags = [director["name"], *PLAN_TAGS.get(plan["name"], set())]
    action = _choose_action_for_director(character_name, plan, director, [*(recent_tags or []), *director_tags])
    combo_tags = [*(recent_tags or []), *director_tags, *action.get("tags", set())]
    weather = _choose_weather_for_director(plan, action, director, energy_profile, combo_tags)
    lens = _choose_lens_for_director(plan, action, director)
    lighting = _choose_lighting_for_director(plan, action, weather, director, energy_profile)
    information_balance = _choose_information_balance_for_director(
        character_name,
        plan,
        action,
        director,
        combo_tags,
    )
    weather, lighting, energy_state = _apply_energy_profile(
        plan,
        action,
        weather,
        lens,
        lighting,
        information_balance,
        director,
        energy_profile,
    )
    weather, lens, lighting, complexity = _apply_complexity_budget(
        plan,
        action,
        weather,
        lens,
        lighting,
        information_balance,
        director,
    )
    return {
        "art_plan": plan,
        "director_class": director,
        "energy_profile": energy_profile,
        "energy_state": energy_state,
        "action_style": action,
        "weather_atmosphere": weather,
        "camera_lens": lens,
        "lighting_strategy": lighting,
        "information_balance": information_balance,
        "complexity_budget": complexity,
    }


def collect_develop_cooldown_tags(
    plan: dict,
    action: dict,
    weather: dict,
    lens: dict,
    lighting: dict,
    information_balance: dict | None = None,
    director_class: dict | None = None,
    complexity_budget: dict | None = None,
    energy_profile: dict | None = None,
    energy_state: dict | None = None,
) -> list[str]:
    tags = set(collect_cooldown_tags(plan, action))
    tags.update(weather.get("tags", set()))
    tags.update(lens.get("tags", set()))
    tags.update(lighting.get("tags", set()))
    if information_balance:
        tags.update(information_balance.get("tags", set()))
    if director_class:
        tags.add(director_class.get("name", "unknown_director"))
    if energy_profile:
        tags.add(energy_profile.get("name", "unknown_energy"))
    if energy_state and energy_state.get("low_pressure_score", 0) > energy_state.get("max_low_pressure_score", 99):
        tags.add("low_pressure_over_budget")
    if complexity_budget:
        tags.update(f"complexity_{key}" for key in complexity_budget.get("over_budget", []))
    return sorted(tags)
