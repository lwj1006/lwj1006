import random


OUTFIT_DIRECTIONS = [
    "reference-faithful outfit with small fashionable variation",
    "clean light-novel casual outfit, character palette stays recognizable",
    "transparent summer jacket over a sporty camisole, fresh and polished",
    "cafe maid remix outfit, neat apron, ribbons, cute and clean",
    "romantic flower bridal dress, elegant veil or bouquet, clean and elegant",
    "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
    "elegant black stockings outfit, refined fashion styling, graceful pose",
    "white blouse and black stockings, clean heroine styling",
    "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
    "soft bakery or cafe casual outfit, warm and simple",
    "minimal sunny studio outfit, face and hair identity as the main focus",
    "clean pure-white studio outfit, simple silhouette, character colors as the only accent",
    "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
]


ANTI_SAFE_COMPOSITION = []


CHARACTER_PROFILES = {
    "南宫": {
        "official_core": "黑发短双马尾，发尾粉色渐变，齐刘海，粉色眼睛，猫咪发夹，俏皮。",
        "identity_tokens": ["short black twin tails with pink gradient tips", "straight blunt bangs", "pink eyes", "cat hairpin"],
        "viewer_relationship": "像在悄悄观察观众，表情聪明、轻微挑衅，但不夸张。",
        "thumbnail_strategy": "黑粉发色和猫咪小饰品必须在小图里仍然清楚。",
        "interaction_rule": "允许对视、侧身回头、轻笑；避免手指指向镜头。",
        "color_anchor": "black, pink, clean white",
    },
    "爱芮": {
        "official_core": "高饱和粉色双马尾，黑色挑染刘海，明亮粉蓝眼睛，偶像感、元气感强。",
        "identity_tokens": ["vivid pink twin tails", "black streak in bangs", "pink-blue bright eyes", "idol-like hair accessories"],
        "viewer_relationship": "像正在和观众营业互动，亲近、明亮、有舞台感。",
        "thumbnail_strategy": "粉色双马尾和明亮眼睛是第一识别点。",
        "interaction_rule": "允许挥手、微笑、转身看向观众；避免自拍道具和伸手贴镜头。",
        "color_anchor": "hot pink, cyan, clean black",
    },
    "千夏": {
        "official_core": "薄荷中短层次发 + 大号薄荷蝴蝶结 + 不对称刘海，侧边小发束，粉金色眼睛，表情轻、眼神干净。",
        "identity_tokens": ["mint gray-green short layered hair", "large mint bow", "soft asymmetrical bangs", "pink-gold eyes"],
        "viewer_relationship": "轻轻看向观众，嘴角很小，肩颈放松。",
        "thumbnail_strategy": "薄荷发色、蝴蝶结、清透眼睛必须稳定，不要改成普通长发角色。",
        "interaction_rule": "允许坐姿、窗边回头、自然整理头发；避免纸笔和创作者设定。",
        "color_anchor": "mint, pale gold, soft white",
    },
    "丹": {
        "official_core": "浅粉短发，空气感碎刘海，粉紫眼睛，小银蓝发饰，脸部留白多。",
        "identity_tokens": ["pale pink short layered hair", "airy uneven bangs", "pink-purple eyes", "small silver-blue hair accessory"],
        "viewer_relationship": "轻轻看向观众，表情小，身体动作少。",
        "thumbnail_strategy": "浅粉短发和透明感眼睛必须稳定，服装可以变化。",
        "interaction_rule": "允许站立、坐姿、侧脸、轻微回头；避免固定同一套服装。",
        "color_anchor": "pale pink, violet, silver blue",
    },
    "星见雅": {
        "official_core": "黑色长直发，姬发式齐刘海，尖锐黑色兽耳，红色眼睛，一侧细编发。",
        "identity_tokens": ["long straight black hair", "hime-cut blunt bangs", "sharp black animal ears", "red eyes", "single side braid detail"],
        "viewer_relationship": "正面或侧面看向观众，表情少，眼睛和发型轮廓清楚。",
        "thumbnail_strategy": "黑长直、黑兽耳、红眼和一侧细编发是核心；刀鞘或红线只是小点缀。",
        "interaction_rule": "允许刀鞘、红色线条、远处剑影；避免复杂手部持物。",
        "color_anchor": "black, red, white",
    },
    "仪玄": {
        "official_core": "银白长发，柔软呆毛，黑色雷纹或波纹发饰，金色眼睛，长袖或垂坠衣摆。",
        "identity_tokens": ["long silver-white hair", "small ahoge", "black wave or lightning-shaped hair ornament", "golden eyes"],
        "viewer_relationship": "正面或侧身看向观众，手部靠近袖口或胸前，动作慢。",
        "thumbnail_strategy": "银白长发和金眼必须清晰，背景不要压过人物。",
        "interaction_rule": "允许手在胸前、袖摆自然下垂、侧身凝视；避免复杂手势。",
        "color_anchor": "silver white, black, gold",
    },
    "叶瞬光": {
        "official_core": "暖棕长发，深色内层发，红色眼睛，红色发带或花形发饰，白黑金服装，人类耳朵。",
        "identity_tokens": ["long warm brown hair", "dark inner hair layers", "red eyes", "red ribbon or flower hair accessory", "white black gold outfit", "human ears only"],
        "viewer_relationship": "回头看向观众，表情轻，手部和肩线放松。",
        "thumbnail_strategy": "暖棕长发、深色内层发、红眼、红色发饰和白黑金服装要稳定；不要添加动物耳朵、尾巴，也不要变成黑发红眼冷角色。",
        "interaction_rule": "允许红绳、细长饰带、清亮光痕或小型刀剑配饰作为点缀；不要强制手持武器，不要加入动物耳朵、尾巴、固定宗门或山门元素。",
        "color_anchor": "warm brown, red, ivory, black gold",
    },
    "席德": {
        "official_core": "浅青蓝短发，后侧明显蓝色大辫子，青绿色眼睛，白灰机械改造服，机械手臂，黄橙线缆，OBOL小队。",
        "identity_tokens": ["short light cyan-blue hair", "large blue back braid", "green or teal-green eyes", "white gray mechanical bodysuit", "exposed mechanical arm parts", "orange-yellow cable accents", "OBOL Squad operator"],
        "viewer_relationship": "把机械部件靠近身边展示，眼睛睁大，表情轻。",
        "thumbnail_strategy": "浅青蓝短发、蓝色大辫子、青绿色眼睛、白灰机械服和机械手臂必须清楚；不要变成普通蓝发校园少女。",
        "interaction_rule": "机械手臂、线缆和机能服是身份核心；滑板车、锤形武器和任何手持物件都不是固定设定，默认不要出现；避免普通花园少女、普通军服少女和纯机器人化。",
        "color_anchor": "light cyan blue, white gray, teal green, orange yellow",
    },
    "橘福福": {
        "official_core": "金橙短发，黄绿色眼睛，虎耳与蓬松虎尾，红白节庆装饰，动作幅度大的人形少女。",
        "identity_tokens": ["golden-orange short hair", "green or yellow-green eyes", "small tiger ears", "large fluffy tiger tail", "red festive accessory", "human girl, not animalized"],
        "viewer_relationship": "回头笑或向前跑，虎尾形成大弧线，画面偏暖。",
        "thumbnail_strategy": "金橙发、黄绿色眼睛、虎耳、蓬松虎尾和红白装饰要稳定；不要变成虎兽人。",
        "interaction_rule": "允许奔跑、回头笑、节庆武术动作、虎尾动势；避免真实虎脸、虎口鼻、虎爪兽腿、完整虎皮套装。",
        "color_anchor": "golden orange, yellow green, warm white, red",
    },
}


GENERIC_PROFILE = {
    "official_core": "严格保留上传参考图中的发型、发色、眼睛、核心饰品、脸型和表情距离。",
    "identity_tokens": ["reference hairstyle", "reference hair color", "reference eyes", "reference accessories"],
    "viewer_relationship": "让角色像真实拥有自己的日常和情绪，亲近但不做作。",
    "thumbnail_strategy": "缩小后仍然能读出发型、眼睛、主色和核心饰品。",
    "interaction_rule": "动作自然，手部简单，不使用复杂持物。",
    "color_anchor": "reference main colors, clean white, soft black",
}


ART_DIRECTION_PLANS = [
    {
        "name": "trend_mirror_studio",
        "graphic_concept": "明亮练习室或镜面房，清爽潮流感，角色像刚结束练习后看向观众。",
        "spatial_structure": "大镜子、浅色地面、窗光和少量圆形灯点，背景不拥挤。",
        "visual_device": "镜面反射和窗光让角色发型、发饰、脸部更醒目。",
        "body_silhouette": "近景膝上或坐姿，角色占画面大，手靠近脸颊或自然放松。",
        "outfit_direction": "transparent summer jacket over a sporty camisole, fresh and polished",
        "material_language": "半透明外套、运动内搭、黑色肩带、小挂件、玻璃反光。",
        "color_strategy": "角色主色成为画面主色，奶白和少量黑色压住画面。",
        "lighting_behavior": "高亮窗光，皮肤和头发有清爽高光，不能油腻。",
        "tags": ["trend_lifestyle", "mirror", "studio", "close_character"],
    },
    {
        "name": "capsule_toy_corner",
        "graphic_concept": "潮玩扭蛋角，透明玩具球和浅色背景制造可收藏感。",
        "spatial_structure": "透明玩具球、浅色圆形墙面、少量小玩偶，环境像可爱的潮玩店一角。",
        "visual_device": "圆形玩具球和角色眼睛互相呼应，形成强缩略图记忆点。",
        "body_silhouette": "半身到膝上近景，可递出一个小玩具球，但手不要贴镜头过大。",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "透明塑料、柔软外套、小饰品、糖果色点缀。",
        "color_strategy": "浅色背景配角色主色，玩具颜色只做小面积点缀。",
        "lighting_behavior": "柔和高调灯光，眼睛和发丝最清晰。",
        "tags": ["trend_lifestyle", "toy", "pastel", "close_character"],
    },
    {
        "name": "graphic_poster_studio",
        "graphic_concept": "干净平面海报棚拍，角色主色、符号和大字母色块形成传播感。",
        "spatial_structure": "浅色背景、大色块、简单几何图形和少量不可读装饰字母。",
        "visual_device": "大色块和角色主色做成视觉标志，像角色个人海报。",
        "body_silhouette": "坐姿或跪坐，膝上到全身之间，脸和发饰最清楚。",
        "outfit_direction": "cafe maid remix outfit, neat apron, ribbons, cute and clean",
        "material_language": "白布、黑色边线、丝带、轻量鞋袜、小挂件。",
        "color_strategy": "白底或浅色底，角色主色占主导，黑色只负责压线。",
        "lighting_behavior": "干净棚拍光，无强阴影。",
        "tags": ["trend_lifestyle", "poster", "graphic", "close_character"],
    },
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
        "tags": ["cafe", "window", "warm_light", "daily"],
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
        "tags": ["bakery", "morning", "warm_light", "daily"],
    },
    {
        "name": "open_grassland_breeze",
        "graphic_concept": "开阔草原微风，清爽自然色和角色轮廓优先。",
        "spatial_structure": "低矮草地、远处柔和地平线、少量小花，不堆复杂景物。",
        "visual_device": "风吹发丝和衣摆形成轻方向线。",
        "body_silhouette": "站姿或轻步行走，三分之二身到全身之间，动作稳定。",
        "outfit_direction": "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
        "material_language": "轻薄布料、草叶、小花、柔软发丝。",
        "color_strategy": "草地绿色低饱和，角色主色保持明确，不被背景吞掉。",
        "lighting_behavior": "晴天漫射光，整体明亮但不过曝。",
        "tags": ["grassland", "breeze", "natural_light", "daily"],
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
        "tags": ["flower_field", "afternoon", "dream", "nature"],
    },
    {
        "name": "picnic_under_tree",
        "graphic_concept": "树荫野餐，低矮餐布、藤篮、饮料杯和近距离回头表情优先。",
        "spatial_structure": "野餐布、篮子、树荫、远处草地，画面简洁。",
        "visual_device": "格纹野餐布形成图形底，树影轻轻压住背景。",
        "body_silhouette": "自然坐姿或跪坐，双手放在膝边、篮子旁或衣摆上。",
        "outfit_direction": "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
        "material_language": "棉布、藤篮、草地、轻柔树影。",
        "color_strategy": "浅绿、奶油白和角色主色组合，整体清爽。",
        "lighting_behavior": "树荫斑驳光，但脸部不能被遮暗。",
        "tags": ["picnic", "tree_shadow", "soft_daylight", "nature"],
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
        "tags": ["greenhouse", "flower", "natural_light", "nature"],
    },
    {
        "name": "bookstore_cafe_corner",
        "graphic_concept": "书店咖啡角，书架竖线、圆桌、杯子、翻开的书和窗边暖光组成画面。",
        "spatial_structure": "书架、圆桌、暖灯、窗边座位，书脊不出现可读文字。",
        "visual_device": "书架竖线和圆桌形成稳定构图。",
        "body_silhouette": "坐姿或站在书架旁，手部放松，不拿复杂道具。",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "纸张、木架、针织、柔软发丝。",
        "color_strategy": "暖木色和浅奶油色托住角色主色。",
        "lighting_behavior": "柔和室内灯加窗边自然光。",
        "tags": ["bookstore", "cafe", "quiet", "daily"],
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
        "tags": ["sweets", "pastel_room", "soft_light", "daily"],
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
        "tags": ["garden", "tea_table", "fairy_tale", "daily"],
    },
    {
        "name": "flower_bridal_garden",
        "graphic_concept": "花嫁感花园插画，浪漫、干净、明亮，重点是角色脸和发型。",
        "spatial_structure": "浅色花门、白色纱帘、花束和草地，布景轻量不拥挤。",
        "visual_device": "头纱、花束和花门形成柔和外框。",
        "body_silhouette": "站姿或坐姿，三分之二身，双手自然捧花或放在裙摆旁。",
        "outfit_direction": "romantic flower bridal dress, elegant veil or bouquet, clean and elegant",
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
        "outfit_direction": "cafe maid remix outfit, neat apron, ribbons, cute and clean",
        "material_language": "围裙、蝴蝶结、棉布、陶瓷杯、甜点。",
        "color_strategy": "黑白女仆服作为稳定色块，角色发色和眼睛必须更突出。",
        "lighting_behavior": "午后咖啡店柔光，眼睛和脸最清楚。",
        "tags": ["maid", "cafe", "sweets", "warm_light"],
    },
    {
        "name": "black_stockings_tea_room",
        "graphic_concept": "精致茶室时装插画，黑丝作为优雅服装元素，姿态干净高级。",
        "spatial_structure": "小茶桌、椅子、浅色窗帘和花瓶，空间简洁柔和。",
        "visual_device": "黑白服装对比和角色发色形成强识别。",
        "body_silhouette": "坐姿或侧身站姿，腿部姿态自然，手部简单清楚。",
        "outfit_direction": "elegant black stockings outfit, refined fashion styling, graceful pose",
        "material_language": "黑色长袜、轻裙摆、白衬衫、丝带、柔软布料。",
        "color_strategy": "黑白服装压住画面，背景用奶油白和浅木色，角色主色清楚。",
        "lighting_behavior": "柔和室内自然光，避免强烈阴影。",
        "tags": ["black_stockings", "tea_room", "fashion", "soft_light"],
    },
    {
        "name": "sunny_seaside_train",
        "graphic_concept": "晴天海边列车，夏日旅行感、透明饮料和窗外蓝色海面。",
        "spatial_structure": "列车座位、明亮窗户、海面和天空，车厢元素保持干净。",
        "visual_device": "窗框、海平线和饮料杯形成清爽生活感。",
        "body_silhouette": "坐姿膝上近景，角色占比大，手部动作简单。",
        "outfit_direction": "transparent summer jacket over a sporty camisole, fresh and polished",
        "material_language": "透明外套、白色短装、玻璃杯、贴纸、小包挂件。",
        "color_strategy": "蓝天和角色主色互相衬托，黑色肩带或小包负责压色。",
        "lighting_behavior": "强烈但柔和的晴天窗光，皮肤高光清爽。",
        "tags": ["seaside", "train", "summer", "close_character"],
    },
]


ART_DIRECTION_PLANS.extend([
    {
        "name": "pure_white_character_focus",
        "graphic_concept": "纯白背景角色主视觉，去掉复杂场景，让人物身份、发型、眼睛和服装成为全部重点。",
        "spatial_structure": "无缝纯白背景，只有少量柔和投影和角色主色小图形点缀，不出现真实地点。",
        "visual_device": "大面积白底、角色主色、少量黑色线条形成清楚缩略图。",
        "body_silhouette": "近景膝上或三分之二身，角色占画面大，姿势自然稳定。",
        "outfit_direction": "clean pure-white studio outfit, simple silhouette, character colors as the only accent",
        "material_language": "干净布料、少量丝带、小饰品、柔软发丝。",
        "color_strategy": "白色占主导，角色自己的主色作为唯一强记忆点，避免背景抢戏。",
        "lighting_behavior": "高调柔光，脸部和眼睛极清楚，不能发灰或发脏。",
        "tags": ["pure_white", "studio", "minimal", "close_character"],
    },
    {
        "name": "zero_gravity_fairy_tale_call",
        "graphic_concept": "童话通话场景的无重力版本，像角色在柔软梦境里悬浮接听一段秘密通话。",
        "spatial_structure": "浅色童话房间或云朵空间，枕头、花瓣、书页、丝带、小玩偶轻轻漂浮。",
        "visual_device": "漂浮物围绕角色形成圆形节奏，视线回到角色脸和眼睛。",
        "body_silhouette": "人物轻微悬浮，身体自然蜷曲或侧躺在空中，手部简单，不做复杂持物。",
        "outfit_direction": "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
        "material_language": "轻纱、丝带、云朵、花瓣、柔软玩偶、微光粒子。",
        "color_strategy": "浅色童话背景配角色主色，整体清透，避免杂乱高饱和。",
        "lighting_behavior": "柔和梦境光，轮廓轻盈，脸部保持清楚。",
        "tags": ["zero_gravity", "fairy_tale", "phone_call_mood", "floating"],
    },
    {
        "name": "zero_gravity_fairy_garden",
        "graphic_concept": "无重力童话花园，角色像漂浮在花瓣和阳光之间，轻盈、梦幻、可收藏。",
        "spatial_structure": "浅色花园、云朵、花瓣、透明泡泡和小型童话装饰物漂浮，空间不拥挤。",
        "visual_device": "花瓣和泡泡形成上升流线，强化人物悬浮感。",
        "body_silhouette": "角色悬浮在画面中央或稍偏上，膝上到全身之间，四肢放松自然。",
        "outfit_direction": "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
        "material_language": "轻纱、花瓣、透明泡泡、丝带、柔软发丝。",
        "color_strategy": "花色只做点缀，角色主色必须是画面记忆点。",
        "lighting_behavior": "明亮自然柔光，边缘有轻微发光空气感。",
        "tags": ["zero_gravity", "fairy_tale", "flower", "floating"],
    },
])


ART_DIRECTION_PLANS.extend([
    {
        "name": "guofeng_decorative_kv",
        "graphic_concept": "国风装饰 KV，不做门派叙事；纸伞、窗棂、绢花、红绳和玉色小饰品围绕角色形成清楚画面。",
        "spatial_structure": "浅色庭院或室内屏风空间，角色在中景，前景可有纸伞边缘、花枝或红绳轻遮挡，但脸、眼睛和发型必须清楚。",
        "visual_device": "圆形纸伞、窗棂格线、细红绳和绢花形成重复图形节奏，不能变成山门、宗门或剑修场景。",
        "body_silhouette": "三分之二身或膝上构图，侧身回头或坐姿，手部靠近袖口、花枝或小饰品。",
        "outfit_direction": "reference-faithful outfit with small fashionable variation",
        "material_language": "绢布、纸伞、玉饰、红绳、浅金纹样、木窗格、薄纱袖口。",
        "color_strategy": "暖白、浅金、玉色和角色主色做干净对比，红色只作细线点缀。",
        "lighting_behavior": "柔和窗光穿过窗棂，在脸、发丝和衣摆上留下浅色切光。",
        "tags": ["guofeng", "decorative", "window_frame", "ribbon", "soft_light", "kv"],
    },
])


ART_DIRECTION_PLANS.extend([
    {
        "name": "afternoon_cafe_large_negative_space",
        "graphic_concept": "light-novel CG style afternoon cafe interior; the image reads first as warm window light, cream wall color blocks, wooden table planes, and quiet air, then the character appears as a small emotional point inside the space",
        "spatial_structure": "wide composition with large negative space; character placed off-center near one corner or window edge; foreground table edge, chair back, or curtain can partially block the view; clear perspective from floor, table, and window frame",
        "visual_device": "open book, half-finished drink, dessert plate, flower vase, and tabletop sunlight form a clear daily story",
        "body_silhouette": "small to medium figure, seated sideways or turned back slightly, not centered, calm expression and natural hands near the table",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "wood grain, ceramic cup, paper book pages, sheer curtain, soft fabric, small reflective highlights on glass",
        "color_strategy": "large soft blocks of cream, honey, pale wood, and the character palette; low clutter, readable silhouette",
        "lighting_behavior": "strong afternoon window beam cuts across the room; soft bounced light keeps the face readable without making the character the only subject",
        "tags": ["cafe", "negative_space", "corner_composition", "window_frame", "story_props", "warm_light", "novel_cg"],
    },
    {
        "name": "library_corner_sunset_silence",
        "graphic_concept": "quiet library corner as an anime novel CG; shelves, amber dust light, and rectangular shadow shapes are the main thumbnail design",
        "spatial_structure": "deep corner perspective with bookcases forming a frame; character sits or stands near the lower third, partly hidden by shelf edge or desk lamp; large empty wall or floor area remains visible",
        "visual_device": "opened books, stacked notes, bookmark ribbon, tea cup, and sunset strip on the desk guide the eye",
        "body_silhouette": "back view or looking back over shoulder; face may be smaller but identity hair shape and eyes remain clear when visible",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "paper, wood shelf, brass lamp, matte cloth, dust in light, quiet floor reflection",
        "color_strategy": "large warm amber and muted green-brown blocks, with the character colors used as the final focal accent",
        "lighting_behavior": "low sunset light through a high window, hard rectangular cuts on shelf and floor, soft shadow around the character",
        "tags": ["library", "corner_composition", "back_view", "large_space", "story_props", "sunset", "novel_cg"],
    },
    {
        "name": "classroom_sunset_doorframe",
        "graphic_concept": "after-school classroom anime screenshot feeling; desks, blackboard, doorway frame, and orange light establish the scene before the character",
        "spatial_structure": "view from hallway through a doorframe or window frame; character placed near frame edge or half out of frame; rows of desks create perspective and reading order",
        "visual_device": "open notebook, pencil case, drink carton, loose paper, and moving curtain show a recent after-school moment",
        "body_silhouette": "standing by the window, back turned or slight over-shoulder glance; relaxed posture, no centered idol pose",
        "outfit_direction": "white blouse and black stockings, clean heroine styling",
        "material_language": "chalkboard matte surface, varnished desk wood, fabric curtain, paper, school bag strap",
        "color_strategy": "large orange sunset block, pale classroom wall, dark desk grid, and a clean character-color accent",
        "lighting_behavior": "strong horizontal sunset beam cuts across desks and character; face can be partly rim-lit instead of front-lit",
        "tags": ["classroom", "doorframe", "window_frame", "back_view", "sunset", "story_props", "novel_cg"],
    },
    {
        "name": "balcony_breeze_half_out_frame",
        "graphic_concept": "home balcony breeze scene; curtain, sky, railing, and white interior wall carry the first read, character is an emotional note near the edge",
        "spatial_structure": "interior looking toward balcony or balcony looking inward; character half out of frame or placed low in one side; doorframe and curtain create foreground layers",
        "visual_device": "wind-blown curtain, small plant pot, sandals, glass with condensation, and reflected floor light create domestic narrative",
        "body_silhouette": "side or back silhouette, looking outside or glancing back; hair and accessories move lightly in wind",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "thin curtain, glass door, metal railing, ceramic pot, polished floor reflection, soft cotton",
        "color_strategy": "large white and sky-blue color fields with one warm accent from the character or prop",
        "lighting_behavior": "bright exterior light, interior in pale shade, thin rim light on hair and shoulder",
        "tags": ["balcony", "large_space", "half_out_frame", "foreground_occlusion", "breeze", "daily", "novel_cg"],
    },
    {
        "name": "greenhouse_terrace_reflection",
        "graphic_concept": "flower greenhouse terrace with glass reflections; plants, window grids, and pale green light define the image more than the pose",
        "spatial_structure": "layered glasshouse perspective; character placed behind plants or reflected faintly in glass; foreground leaves partially cover edges without hiding identity essentials",
        "visual_device": "flower bouquet, watering can, small sweets tray, folded ribbon, and sun patches on tile floor build a small daily scene",
        "body_silhouette": "three-quarter back view or quiet side glance, small figure inside deep space, not centered",
        "outfit_direction": "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "glass, leaf translucency, ceramic tile, bouquet paper, lace or ribbon, soft moisture shine",
        "color_strategy": "large pale green and white blocks, flower colors as controlled accents, character palette preserved",
        "lighting_behavior": "diffused greenhouse light with clear window-grid shadows and soft reflective highlights",
        "tags": ["greenhouse", "terrace", "reflection", "foreground_occlusion", "flower", "large_space", "novel_cg"],
    },
    {
        "name": "white_room_floor_window",
        "graphic_concept": "quiet white room with floor-to-ceiling window; the composition is built from white wall, pale floor reflection, curtain shadow, and one character-color accent",
        "spatial_structure": "very wide white space; character small and off-center near a window, sofa edge, or low table; strong empty areas remain intentionally visible",
        "visual_device": "thin curtain, small jewelry tray, flower stem, glass cup, book, and soft floor reflection create minimal narrative detail",
        "body_silhouette": "sitting on floor or standing near window, profile or back view; calm, cinematic, not posing for camera",
        "outfit_direction": "clean pure-white studio outfit, simple silhouette, character colors as the only accent",
        "material_language": "white cotton, glass, polished floor, thin curtain, small metal accessory, matte wall",
        "color_strategy": "dominant white and pale gray with the character palette as the memory point; no busy background",
        "lighting_behavior": "large soft window light plus one hard curtain-shadow cut across the floor",
        "tags": ["white_room", "floor_window", "negative_space", "large_space", "soft_light", "minimal", "novel_cg"],
    },
    {
        "name": "dessert_shop_mirror_glance",
        "graphic_concept": "small dessert shop with mirror reflection; the viewer first reads pastel wall blocks, display case geometry, and reflected light",
        "spatial_structure": "mirror or glass display shows only a partial reflection of the same single character; no second person, no clone, no picture-in-picture duplicate",
        "visual_device": "cake slices, fork, receipt, flower wrapping, and a half-finished drink create a natural after-moment instead of a staged pose",
        "body_silhouette": "looking back through mirror or over shoulder; hands simple, close to prop or counter, no reaching toward camera",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "glass display, porcelain plate, cream, paper receipt, polished counter, soft knit or blouse fabric",
        "color_strategy": "large pastel wall and cream counter blocks, character colors echoed in one dessert or flower accent",
        "lighting_behavior": "soft shop light with reflective highlights and a clean shadow separation under the counter",
        "tags": ["dessert_shop", "mirror", "reflection", "story_props", "corner_composition", "pastel", "novel_cg"],
    },
    {
        "name": "summer_courtyard_soft_shadow",
        "graphic_concept": "summer courtyard or small garden as a light animation screenshot; tree shadow, white wall, stepping stones, and sky color dominate the thumbnail",
        "spatial_structure": "high or low camera angle with character placed at the edge of the path; foreground leaves, doorframe, or fence line can crop the image",
        "visual_device": "open book on bench, cold drink, flower basket, wind on leaves, and reflected light on stone give the place memory",
        "body_silhouette": "walking away, pausing, or turning back slightly; medium-small figure inside a clear environment",
        "outfit_direction": "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
        "material_language": "stone, leaf shadow, painted wood, glass bottle, paper pages, light summer fabric",
        "color_strategy": "large blocks of white wall, green shade, and pale sky; character palette stays as the emotional accent",
        "lighting_behavior": "bright summer light filtered by leaves, strong shadow pattern across ground and wall",
        "tags": ["summer_courtyard", "garden", "high_low_camera", "foreground_occlusion", "breeze", "story_props", "novel_cg"],
    },
])


ART_DIRECTION_PLANS.extend([
    {
        "name": "overhead_deep_perspective_space",
        "graphic_concept": "high-angle anime CG composition; the room plan, floor shape, table edges, and window light pattern are the main thumbnail before the character",
        "spatial_structure": "camera looks down from above or from a stair/loft height; floor tiles, desk rows, railing, or tabletop lines create clear depth; character is small and offset from center",
        "visual_device": "strong foreground-middle-background separation; the eye follows floor perspective and light shapes before reaching the character",
        "body_silhouette": "small figure seen from above, head and hair silhouette readable, relaxed posture, not posing toward camera",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "floor reflection, table plane, window frame, soft cloth, paper, glass highlight",
        "color_strategy": "large floor or wall color block dominates; character palette is a controlled focal accent",
        "lighting_behavior": "top or window light draws hard geometric cuts across floor and furniture, with soft bounce on the character",
        "tags": ["high_camera", "deep_perspective", "large_space", "negative_space", "novel_cg"],
    },
    {
        "name": "low_angle_foreground_depth",
        "graphic_concept": "low-angle anime screenshot composition; foreground objects are large, the character sits deeper in space, and ceiling/window verticals give scale",
        "spatial_structure": "camera near floor, tabletop, chair level, or garden path level; foreground edge is big and slightly cropped; midground character is off-center; background recedes clearly",
        "visual_device": "foreground object, middle character, and far window/door/plant layer form a readable three-depth stack",
        "body_silhouette": "medium-small figure seen through low perspective, back/side/over-shoulder angle preferred, simple hands",
        "outfit_direction": "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
        "material_language": "large blurred foreground edge, polished floor or stone path, glass, curtain, plant leaves, fabric",
        "color_strategy": "foreground shadow mass plus bright background plane; character color sits between them as the second read",
        "lighting_behavior": "low camera catches floor reflection and rim light; strong light direction clarifies depth",
        "tags": ["low_camera", "foreground_depth", "deep_perspective", "foreground_occlusion", "novel_cg"],
    },
    {
        "name": "far_shot_small_figure_room",
        "graphic_concept": "far-shot light-novel CG; the environment carries the emotion, with the character as a small memory point inside a readable room or terrace",
        "spatial_structure": "long distance from camera; wide room, courtyard, library aisle, cafe floor, or balcony space visible; character occupies a small part of the frame near a third or corner",
        "visual_device": "large empty wall/floor/window area and repeated perspective lines create scale; small silhouette placement creates loneliness or quiet warmth",
        "body_silhouette": "small full-body or three-quarter figure, back view or side view, identity kept by hair shape, color, and accessory silhouette",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "wall, floor, window, shelf, railing, curtain, table plane, soft reflection",
        "color_strategy": "dominant environment colors with one character-color accent; avoid filling the frame with the body",
        "lighting_behavior": "large soft light field, long shadow, or window beam gives spatial scale",
        "tags": ["far_shot", "small_figure", "large_space", "negative_space", "deep_perspective", "novel_cg"],
    },
    {
        "name": "telephoto_layered_interior",
        "graphic_concept": "compressed telephoto interior or garden view; multiple vertical layers make the image look found inside the scene",
        "spatial_structure": "camera looks through shelves, curtains, plants, doorframes, or glass; foreground and background stack tightly while character remains off-center",
        "visual_device": "repeating frames and soft occlusion create depth; character appears between layers, not flat in front",
        "body_silhouette": "side or back view, partial crop allowed, face not required to dominate as long as identity hair and accessory cues remain visible",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "glass reflection, curtain layers, shelf edges, leaves, ceramic, paper, soft cloth",
        "color_strategy": "stacked muted color planes; one sharper character-color accent controls the focal point",
        "lighting_behavior": "compressed light bands, reflected highlights, and soft shadow layers separate foreground, character, and background",
        "tags": ["telephoto", "layered_space", "foreground_occlusion", "reflection", "deep_perspective", "novel_cg"],
    },
])


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
        "body_silhouette": "坐姿，膝上到全身之间，双手自然放在膝边或座位上。",
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
    {
        "name": "holding_small_cute_prop",
        "body_silhouette": "轻轻拿着小甜点、饮料、花束、书或透明玩具球，手部保持小比例且清楚。",
        "tags": ["small_prop", "stable_hands"],
    },
    {
        "name": "looking_back_from_edge",
        "body_silhouette": "off-center figure near the image edge, back turned or three-quarter back view, softly looking back over shoulder; identity hair shape and eyes remain readable but the room and light lead the image",
        "tags": ["back_view", "edge_framing", "story_pose"],
    },
    {
        "name": "half_hidden_by_foreground",
        "body_silhouette": "character partly screened by foreground curtain, plant, shelf, table edge, or doorframe; natural relaxed posture, simple hands, no camera-facing pose",
        "tags": ["foreground_occlusion", "half_out_frame", "story_pose"],
    },
    {
        "name": "quiet_prop_after_moment",
        "body_silhouette": "character caught after an action: closing a book, setting down a cup, turning from the window, or pausing beside a table; emotion is quiet and cinematic",
        "tags": ["story_props", "after_moment", "simple_hand"],
    },
    {
        "name": "tiny_figure_in_depth",
        "body_silhouette": "small figure placed deep in the room or path; full environment remains visible, body does not fill the frame, silhouette and hair/accessory shape carry identity",
        "tags": ["small_figure", "far_shot", "deep_perspective", "story_pose"],
    },
    {
        "name": "camera_looking_down",
        "body_silhouette": "seen from a high angle, head and shoulders/floor relation readable; pose stays simple so the perspective and space are the main effect",
        "tags": ["high_camera", "deep_perspective", "story_pose"],
    },
    {
        "name": "camera_from_low_foreground",
        "body_silhouette": "seen from low foreground height through a table edge, floor, plant, or railing; character is midground and off-center, not frontally staged",
        "tags": ["low_camera", "foreground_depth", "story_pose"],
    },
]


ACTION_STYLES.append(
    {
        "name": "post_workout_stretch",
        "body_silhouette": "运动后拉伸动作，坐姿或单膝跪姿，身体微微前倾，肩颈和腰线放松，手部自然扶膝盖、鞋带或地面。",
        "tags": ["stretch", "sporty", "stable_hands"],
    }
)


VISUAL_MOTIF_SYSTEMS = [
    {
        "name": "moonlit_toy_window_kv",
        "motifs": "plush toys, tiny rabbits, floating petals, ribbons, candles, crystal charms, translucent glass beads",
        "layering": "foreground candles and ribbons; midground character woven into hair and fabric flow; background cathedral-like moonlit window and soft toys",
        "shape_rhythm": "large window arc, S-shaped hair flow, ribbon curves, circular candle lights, repeated petal dots",
        "light_bloom": "cool blue moonlight cut by warm candle bloom, candy reflections on hair edges, soft overexposed rim highlights",
        "poetic_line": "a cathedral-like moonlit window filled with floating petals and soft glowing toys, ribbons and tiny ornaments drifting through the air like fragments of a dream",
    },
    {
        "name": "pastel_lolita_decorative_kv",
        "motifs": "lace, bows, flower trays, glass dessert cups, pearl chains, butterflies, small ribbon cards without text",
        "layering": "foreground lace ribbon and dessert glass; midground character and outfit details; background soft color panels and ornamental frames",
        "shape_rhythm": "rounded boxes, bow loops, skirt waves, pearl chains, flower circles, logo-like silhouette",
        "light_bloom": "milky pastel bloom, warm cream highlights crossing cool mint or lavender shadows, glossy candy reflections",
        "poetic_line": "a sweet decorative anime KV with lace ribbons, pearl chains, butterflies, and glass desserts arranged around the character",
    },
    {
        "name": "fairy_tale_anniversary_kv",
        "motifs": "storybook pages, glowing butterflies, flower petals, ribbons, tiny crowns, paper stars, crystal drops, soft dolls",
        "layering": "foreground book pages and petals; midground character floating through decorative rhythm; background giant storybook window or flower arch",
        "shape_rhythm": "storybook rectangle, flower arch curve, S-shaped hair, drifting ribbon spiral, repeated star and butterfly marks",
        "light_bloom": "golden fairy light against cool blue or pale green air, edge glow, translucent bloom, small sparkling overexposure",
        "poetic_line": "a fairy-tale anniversary key visual where storybook pages, glowing butterflies, and tiny ornaments orbit the character in a soft circular stage",
    },
    {
        "name": "candy_air_parlor_kv",
        "motifs": "transparent candy jars, cream flowers, curled ribbons, glass marbles, paper confetti, plush mascots, floating bubbles",
        "layering": "foreground glass candy and confetti; midground character framed by ribbons; background soft parlor shelves, window light, and blurred ornaments",
        "shape_rhythm": "jar circles, bubble dots, ribbon curls, hair S-curve, repeated small mascot silhouettes",
        "light_bloom": "cold cyan shadows crossed with peach-pink candy highlights, glass bloom, bright rim cuts, airy haze",
        "poetic_line": "a candy-colored parlor world where glass jars, plush mascots, and floating bubbles become the visual rhythm around the character",
    },
    {
        "name": "guofeng_ribbon_window_kv",
        "motifs": "paper umbrella, silk flowers, thin red cords, jade charms, carved window grid, translucent gauze",
        "layering": "foreground umbrella edge or red cord; midground character framed by gauze and hair flow; background pale window grid and soft garden light",
        "shape_rhythm": "umbrella circle, window rectangles, ribbon lines, flower dots, S-shaped hair flow",
        "light_bloom": "warm white window light with pale gold reflection, small red cord accents, clean jade-green shadows",
        "poetic_line": "a decorative guofeng key visual where umbrella arcs, red cords, silk flowers, and window-grid light arrange the character like an elegant collectible illustration",
    },
]


VISUAL_TAG_COMPATIBILITY = {
    "moonlit_toy_window_kv": {
        "fairy_tale",
        "zero_gravity",
        "dream",
        "night",
        "white_room",
        "flower",
        "toy",
    },
    "pastel_lolita_decorative_kv": {
        "cafe",
        "bakery",
        "dessert_shop",
        "maid",
        "bridal",
        "tea_room",
        "pastel",
        "toy",
        "flower",
        "studio",
    },
    "fairy_tale_anniversary_kv": {
        "fairy_tale",
        "flower",
        "garden",
        "greenhouse",
        "zero_gravity",
        "bridal",
        "studio",
    },
    "candy_air_parlor_kv": {
        "cafe",
        "bakery",
        "dessert_shop",
        "toy",
        "pastel",
        "studio",
    },
    "guofeng_ribbon_window_kv": {
        "guofeng",
        "decorative",
        "window_frame",
        "garden",
        "tea_table",
        "reflection",
        "flower",
    },
}


DAYLIGHT_PLAN_TAGS = {"morning", "afternoon", "summer", "sunset", "warm_light", "natural_light", "classroom", "seaside"}


def _visuals_for_plan(plan=None):
    if not plan:
        return VISUAL_MOTIF_SYSTEMS
    plan_tags = _tags_of(plan)
    compatible = []
    for visual in VISUAL_MOTIF_SYSTEMS:
        allowed_tags = VISUAL_TAG_COMPATIBILITY.get(visual["name"], set())
        if plan_tags & allowed_tags:
            compatible.append(visual)
    if plan_tags & DAYLIGHT_PLAN_TAGS:
        compatible = [
            visual for visual in compatible
            if visual["name"] != "moonlit_toy_window_kv"
        ]
    return compatible or [
        visual for visual in VISUAL_MOTIF_SYSTEMS
        if visual["name"] in {"pastel_lolita_decorative_kv", "candy_air_parlor_kv"}
    ]


def choose_visual_design(recent_tags=None, plan=None):
    return dict(random.choice(_visuals_for_plan(plan)))


KNOWN_CHARACTER_NAMES = [
    "南宫",
    "爱芮",
    "千夏",
    "丹",
    "星见雅",
    "仪玄",
    "叶瞬光",
    "席德",
    "橘福福",
]


PLAN_TAGS = {
    plan["name"]: list(plan.get("tags", []))
    for plan in ART_DIRECTION_PLANS
}


ACTION_TAGS = {
    action["name"]: list(action.get("tags", []))
    for action in ACTION_STYLES
}


DEFAULT_PLAN_WEIGHTS = {
    plan["name"]: 1.0
    for plan in ART_DIRECTION_PLANS
}


DEFAULT_ACTION_WEIGHTS = {
    action["name"]: 1.0
    for action in ACTION_STYLES
}


CHARACTER_PLAN_WEIGHTS = {
    character_name: dict(DEFAULT_PLAN_WEIGHTS)
    for character_name in KNOWN_CHARACTER_NAMES
}


CHARACTER_ACTION_WEIGHTS = {
    character_name: dict(DEFAULT_ACTION_WEIGHTS)
    for character_name in KNOWN_CHARACTER_NAMES
}


CHARACTER_ACTION_EXCLUSIONS = {
    "席德": {"holding_small_cute_prop"},
}


NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES = {
    "overhead_deep_perspective_space": 3.4,
    "low_angle_foreground_depth": 3.4,
    "far_shot_small_figure_room": 3.5,
    "telephoto_layered_interior": 3.2,
    "afternoon_cafe_large_negative_space": 3.2,
    "library_corner_sunset_silence": 3.0,
    "classroom_sunset_doorframe": 3.0,
    "balcony_breeze_half_out_frame": 3.0,
    "greenhouse_terrace_reflection": 2.8,
    "white_room_floor_window": 2.8,
    "guofeng_decorative_kv": 2.9,
    "dessert_shop_mirror_glance": 2.8,
    "summer_courtyard_soft_shadow": 2.8,
    "bookstore_cafe_corner": 2.4,
    "sunny_cafe_window": 2.2,
    "garden_tea_table": 2.2,
    "greenhouse_flower_room": 2.2,
    "pastel_room_sweets": 2.0,
    "small_bakery_morning": 1.9,
    "trend_mirror_studio": 0.7,
    "capsule_toy_corner": 0.8,
    "graphic_poster_studio": 0.55,
    "pure_white_character_focus": 0.75,
    "sunny_seaside_train": 0.6,
}

NARRATIVE_SPACE_ACTION_WEIGHT_OVERRIDES = {
    "tiny_figure_in_depth": 3.2,
    "camera_looking_down": 3.0,
    "camera_from_low_foreground": 3.0,
    "looking_back_from_edge": 2.8,
    "half_hidden_by_foreground": 2.6,
    "quiet_prop_after_moment": 2.6,
    "gentle_side_glance": 1.8,
    "seated_quiet_pose": 1.7,
    "holding_small_cute_prop": 1.6,
    "walking_forward": 1.3,
    "steady_eye_contact": 0.6,
    "hands_near_chest": 0.75,
    "post_workout_stretch": 0.2,
}


def _apply_weight_overrides(default_weights, character_weights, overrides):
    for item_name, weight in overrides.items():
        default_weights[item_name] = weight
        for weights in character_weights.values():
            weights[item_name] = weight


_apply_weight_overrides(DEFAULT_PLAN_WEIGHTS, CHARACTER_PLAN_WEIGHTS, NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES)
_apply_weight_overrides(DEFAULT_ACTION_WEIGHTS, CHARACTER_ACTION_WEIGHTS, NARRATIVE_SPACE_ACTION_WEIGHT_OVERRIDES)


PLAN_ACTION_COMPATIBILITY = [
    ({"high_camera"}, {"high_camera", "deep_perspective", "far_shot", "small_figure", "back_view"}),
    ({"low_camera", "foreground_depth"}, {"low_camera", "foreground_depth", "back_view"}),
    ({"far_shot", "small_figure"}, {"far_shot", "small_figure", "deep_perspective", "back_view"}),
    ({"telephoto", "layered_space"}, {"foreground_occlusion", "edge_framing", "back_view", "simple_hand"}),
]


def _profile_for(character_name):
    return CHARACTER_PROFILES.get(character_name, GENERIC_PROFILE)


def _tags_of(item):
    tags = item.get("tags", [])
    return set(tags if isinstance(tags, list) else list(tags))


def _recent_set(recent_tags=None):
    if not recent_tags:
        return set()
    return set(recent_tags)


def _weighted_choice(items, recent_tags=None, weights=None):
    recent = _recent_set(recent_tags)
    weights = weights or {}
    scored = []
    for item in items:
        score = float(weights.get(item["name"], 1.0))
        score -= len(_tags_of(item) & recent) * 0.55
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
    weights = CHARACTER_PLAN_WEIGHTS.get(character_name or "", DEFAULT_PLAN_WEIGHTS)
    return dict(_weighted_choice(ART_DIRECTION_PLANS, recent_tags=recent_tags, weights=weights))


def choose_action_style(character_name=None, recent_tags=None):
    weights = CHARACTER_ACTION_WEIGHTS.get(character_name or "", DEFAULT_ACTION_WEIGHTS)
    excluded = CHARACTER_ACTION_EXCLUSIONS.get(character_name or "", set())
    action_pool = [
        action for action in ACTION_STYLES
        if action["name"] not in excluded
    ]
    return dict(_weighted_choice(action_pool or ACTION_STYLES, recent_tags=recent_tags, weights=weights))


def _compatible_actions_for_plan(plan):
    plan_tags = _tags_of(plan)
    required_action_tags = set()
    for plan_keys, action_keys in PLAN_ACTION_COMPATIBILITY:
        if plan_tags & plan_keys:
            required_action_tags |= action_keys
    if not required_action_tags:
        return ACTION_STYLES
    compatible = [
        action for action in ACTION_STYLES
        if _tags_of(action) & required_action_tags
    ]
    return compatible or ACTION_STYLES


def choose_compatible_action_style(character_name=None, recent_tags=None, plan=None):
    weights = CHARACTER_ACTION_WEIGHTS.get(character_name or "", DEFAULT_ACTION_WEIGHTS)
    action_pool = _compatible_actions_for_plan(plan or {})
    excluded = CHARACTER_ACTION_EXCLUSIONS.get(character_name or "", set())
    action_pool = [
        action for action in action_pool
        if action["name"] not in excluded
    ]
    return dict(_weighted_choice(action_pool, recent_tags=recent_tags, weights=weights))


def choose_plan_and_action(character_name, recent_tags=None):
    plan = choose_art_plan(character_name, recent_tags)
    action = choose_compatible_action_style(character_name, recent_tags, plan)
    return plan, action


def collect_cooldown_tags(plan, action):
    return sorted(_tags_of(plan) | _tags_of(action))


def propagation_profile_for(character_name):
    profile = _profile_for(character_name)
    return {
        "official_core": profile["official_core"],
        "viewer_relationship": profile["viewer_relationship"],
        "interaction_rule": profile["interaction_rule"],
        "thumbnail_strategy": profile["thumbnail_strategy"],
        "safe_sensuality": "干净、可收藏、不过度成人化。",
        "color_anchor": profile["color_anchor"],
        "propagation_translation": "人物身份独立于场景；任意角色都能适配所有生活潮流场景。",
    }


def required_identity_tokens_for(character_name):
    return list(_profile_for(character_name)["identity_tokens"])


def viewer_distance_for(character_name):
    return "camera distance follows the selected scene; keep face, hair silhouette, eyes, and main accessories readable"


def outfit_variation_for(character_name, outfit_direction=None):
    profile = _profile_for(character_name)
    base = outfit_direction if outfit_direction in OUTFIT_DIRECTIONS else random.choice(OUTFIT_DIRECTIONS)
    return (
        f"{base}; adapt to character palette: {profile['color_anchor']}; "
        "keep hairstyle, hair color, eye color, and core accessories"
    )
