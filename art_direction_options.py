import random


OUTFIT_DIRECTIONS = [
    "reference-faithful outfit with small fashionable variation",
    "clean light-novel casual outfit, character palette stays recognizable",
    "transparent summer jacket over a sporty camisole, fresh and polished",
    "cafe maid remix outfit, neat apron, ribbons, cute and clean",
    "romantic flower bridal dress, elegant veil or bouquet, non-adult",
    "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
    "elegant black stockings outfit, refined fashion styling, no explicit posing",
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
        "official_core": "薄荷中短层次发 + 大号薄荷蝴蝶结 + 不对称刘海 薄荷灰绿，柔软分层发型，侧边小发束与大蝴蝶结，粉金色眼睛，清爽安静。",
        "identity_tokens": ["mint gray-green short layered hair", "large mint bow", "soft asymmetrical bangs", "pink-gold eyes"],
        "viewer_relationship": "像安静陪伴观众，温柔、干净、带一点害羞。",
        "thumbnail_strategy": "薄荷发色、蝴蝶结、清透眼睛必须稳定，不要改成普通长发角色。",
        "interaction_rule": "允许坐姿、窗边回头、自然整理头发；避免纸笔和创作者设定。",
        "color_anchor": "mint, pale gold, soft white",
    },
    "丹": {
        "official_core": "浅粉短发，空气感碎刘海，粉紫眼睛，安静、透明。",
        "identity_tokens": ["pale pink short layered hair", "airy uneven bangs", "pink-purple eyes", "small silver-blue hair accessory"],
        "viewer_relationship": "像从安静梦境里看向观众，神秘但亲近。",
        "thumbnail_strategy": "浅粉短发和透明感眼睛必须稳定，服装可以变化。",
        "interaction_rule": "允许站立、坐姿、侧脸、轻微回头；避免固定同一套服装。",
        "color_anchor": "pale pink, violet, silver blue",
    },
    "星见雅": {
        "official_core": "黑色长直发，姬发式齐刘海，尖锐黑色兽耳，红色眼睛，冷静、锋利。",
        "identity_tokens": ["long straight black hair", "hime-cut blunt bangs", "sharp black animal ears", "red eyes"],
        "viewer_relationship": "像冷静地看穿观众，距离感强但角色存在感清楚。",
        "thumbnail_strategy": "黑长直、黑兽耳、红眼是核心；剑可以作为气质符号但不是必须手持。",
        "interaction_rule": "允许刀鞘、红色线条、远处剑影；避免复杂手部持物。",
        "color_anchor": "black, red, white",
    },
    "仪玄": {
        "official_core": "银白长发，柔软呆毛，黑色雷纹或波纹发饰，金色眼睛，成熟安静。",
        "identity_tokens": ["long silver-white hair", "small ahoge", "black wave hair ornament", "golden eyes"],
        "viewer_relationship": "像平静地邀请观众进入仪式，沉稳、有神秘感。",
        "thumbnail_strategy": "银白长发和金眼必须清晰，背景不要压过人物。",
        "interaction_rule": "允许手在胸前、袖摆自然下垂、侧身凝视；避免复杂手势。",
        "color_anchor": "silver white, black, gold",
    },
    "叶瞬光": {
        "official_core": "暖棕长发，棕色兽耳，蓬松棕色尾巴，红色眼睛，红色发带或花饰，温柔可靠。",
        "identity_tokens": ["warm brown long hair", "brown animal ears", "fluffy brown tail", "red eyes", "red ribbon or flower accessory"],
        "viewer_relationship": "像温柔地回头照看观众，亲和但有守护感。",
        "thumbnail_strategy": "暖棕发色、棕色兽耳和尾巴要稳定，不要变成黑发红眼冷剑士。",
        "interaction_rule": "剑是可选符号，不强制手持；避免固定宗门或山门元素。",
        "color_anchor": "warm brown, red, ivory",
    },
    "席德": {
        "official_core": "天蓝色发头发 后面有大麻花辫，蓝紫色眼睛，带少量蓝紫光纹与异质感，天真但危险的少女。",
        "identity_tokens": ["silver-gray short hair", "blue-violet eyes", "subtle blue-violet light marks", "innocent dangerous expression"],
        "viewer_relationship": "像天真地展示一个不可思议的小秘密，表情无辜但气氛有轻微危险感。",
        "thumbnail_strategy": "银灰发、蓝紫眼睛和细小光纹必须清楚，避免普通校园少女化。",
        "interaction_rule": "允许花朵、玻璃糖纸、蓝紫小光点；避免复杂硬质装置和多手结构。",
        "color_anchor": "silver gray, blue violet, soft white",
    },
    "橘福福": {
        "official_core": "橘色发色，明亮金橙眼睛，虎纹或虎主题小饰品，活泼、可靠、热烈的少女气质。",
        "identity_tokens": ["short orange hair", "golden-orange eyes", "tiger-themed accessory", "warm lively expression"],
        "viewer_relationship": "像元气地把观众拉进热闹场面，亲近、明亮、行动感强。",
        "thumbnail_strategy": "橘发、金橙眼、虎主题识别要稳定，避免被背景同化。",
        "interaction_rule": "允许奔跑、回头笑、舞台动作；避免固定宗门或山门元素。",
        "color_anchor": "orange, gold, white",
    },
}


GENERIC_PROFILE = {
    "official_core": "严格保留上传参考图中的发型、发色、眼睛、核心饰品、脸型和气质。",
    "identity_tokens": ["reference hairstyle", "reference hair color", "reference eyes", "reference accessories"],
    "viewer_relationship": "让角色像真实拥有自己的日常和情绪，亲近但不做作。",
    "thumbnail_strategy": "缩小后仍然能读出发型、眼睛、主色和核心饰品。",
    "interaction_rule": "动作自然，手部简单，不使用复杂持物。",
    "color_anchor": "the character's own main colors, clean white, soft black",
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
        "graphic_concept": "树荫野餐，温柔陪伴感和角色亲近度优先。",
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
        "graphic_concept": "书店咖啡角，安静生活感和柔和知识气氛。",
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
        "outfit_direction": "romantic flower bridal dress, elegant veil or bouquet, non-adult",
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
        "graphic_concept": "精致茶室时装插画，黑丝作为优雅服装元素，不做成人化姿态。",
        "spatial_structure": "小茶桌、椅子、浅色窗帘和花瓶，空间简洁柔和。",
        "visual_device": "黑白服装对比和角色发色形成强识别。",
        "body_silhouette": "坐姿或侧身站姿，腿部姿态自然，手部简单清楚。",
        "outfit_direction": "elegant black stockings outfit, refined fashion styling, no explicit posing",
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
    {
        "name": "holding_small_cute_prop",
        "body_silhouette": "轻轻拿着小甜点、饮料、花束、书或透明玩具球，手部保持小比例且清楚。",
        "tags": ["small_prop", "stable_hands"],
    },
]


ACTION_STYLES.append(
    {
        "name": "post_workout_stretch",
        "body_silhouette": "运动后拉伸动作，坐姿或单膝跪姿，身体微微前倾，肩颈和腰线放松，手部自然扶膝盖、鞋带或地面。",
        "tags": ["stretch", "sporty", "stable_hands"],
    }
)


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
    return dict(_weighted_choice(ACTION_STYLES, recent_tags=recent_tags, weights=weights))


def choose_plan_and_action(character_name, recent_tags=None):
    plan = choose_art_plan(character_name, recent_tags)
    action = choose_action_style(character_name, recent_tags)
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
    return "medium-close to three-quarter body framing, character occupies a large part of the image"


def outfit_variation_for(character_name, outfit_direction=None):
    profile = _profile_for(character_name)
    base = outfit_direction if outfit_direction in OUTFIT_DIRECTIONS else random.choice(OUTFIT_DIRECTIONS)
    return (
        f"{base}; adapt the outfit to the current character's own palette: {profile['color_anchor']}; "
        "never change the character's hairstyle, hair color, eye color, or core accessories"
    )
