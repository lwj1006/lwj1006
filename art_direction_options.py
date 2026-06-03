import random


OUTFIT_DIRECTIONS = [
    "reference-faithful outfit with small fashionable variation",
    "clean light-novel casual outfit, character palette stays recognizable",
    "young casual tops: white short T-shirt, cropped hoodie, sleeveless tank, or off-shoulder knit",
    "clean Adidas-inspired sporty date outfit: pale lavender cropped hoodie or sleeveless cropped athletic tank, classic three white stripe accents, short skirt or shorts",
    "clean Yonex-inspired sporty date outfit: cropped hoodie or sleeveless cropped athletic tank, short skirt or shorts, tiny blue-green stripe accent",
    "soft date outfit: fitted cardigan, simple camisole or blouse, A-line skirt, small shoulder bag, clean and youthful",
    "cafe maid remix outfit, neat apron, ribbons, cute and clean",
    "romantic flower bridal dress, elegant veil or bouquet, clean and elegant",
    "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
    "rare refined dark-hosiery fashion outfit, restrained and non-fetishized",
    "clean youthful casual outfit, blouse or light cardigan, no stocking emphasis",
    "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
    "soft bakery or cafe casual outfit, warm and simple",
    "minimal sunny studio outfit, face and hair identity as the main focus",
    "clean pure-white studio outfit, simple silhouette, character colors as the only accent",
    "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
    "pure white sundress with a straw hat, fresh summer date mood",
    "medium-short blue-and-white gingham shirt over a white tank top, denim shorts; shirt worn either tied into a small front-bottom bow or open and unbuttoned",
    "soft light-blue windbreaker jacket, white low-neck tank top, athletic shorts, round-frame glasses",
    "thin white off-shoulder long T-shirt, green camisole inner layer visible at neckline, shorts",
    "lace off-shoulder dress with puff sleeves, clean romantic styling",
    "bright red short one-piece dress, youthful clean date styling",
    "five-sleeve white light-sport T-shirt with gray shorts or denim shorts",
    "white lace long dress as the main element, freely designed elegant silhouette, paired with white high heels",
]


ANTI_SAFE_COMPOSITION = []


CHARACTER_PROFILES = {
    "南宫": {
        "official_core": "short black twin tails with pink gradient tips, straight blunt bangs, pink eyes, cat hairpin, playful but clean expression.",
        "identity_tokens": ["short black twin tails with pink gradient tips", "straight blunt bangs", "pink eyes", "cat hairpin"],
        "viewer_relationship": "clever presence, slightly playful, never exaggerated; gaze can meet the lens or drift away naturally.",
        "thumbnail_strategy": "black-pink hair color and the small cat accessory must stay readable at thumbnail size.",
        "interaction_rule": "side glance, eyes-away moment, natural eye contact, or a small smile are fine; avoid always forcing a camera-facing pose or pointing fingers toward the camera.",
        "color_anchor": "black, pink, clean white",
    },
    "爱芮": {
        "official_core": "vivid pink twin tails, black streak in bangs, bright pink-blue eyes, idol-like accessories, energetic stage presence.",
        "identity_tokens": ["vivid pink twin tails", "black streak in bangs", "pink-blue bright eyes", "idol-like hair accessories"],
        "viewer_relationship": "bright and friendly, like a clean idol-stage interaction.",
        "thumbnail_strategy": "pink twin tails and bright eyes are the first recognition points.",
        "interaction_rule": "waving, smiling, or moving through the scene are fine; avoid selfie props, deliberate lens-facing poses, and hands reaching into the lens.",
        "color_anchor": "hot pink, cyan, clean black",
    },
    "千夏": {
        "official_core": "mint gray-green short layered hair, large mint bow, soft asymmetrical bangs, small side hair bundle, pink-gold eyes, light clean gaze.",
        "identity_tokens": ["mint gray-green short layered hair", "large mint bow", "soft asymmetrical bangs", "pink-gold eyes"],
        "viewer_relationship": "gentle gaze, very small smile, relaxed neck and shoulders.",
        "thumbnail_strategy": "mint hair, large bow, and clear eyes must stay stable; do not turn her into a generic long-haired character.",
        "interaction_rule": "seated pose, window-side glance, or naturally adjusting hair are fine; avoid paper, pen, creator-desk, or illustrator setup motifs.",
        "color_anchor": "mint, pale gold, soft white",
    },
    "丹": {
        "official_core": "pale pink short layered hair, airy uneven bangs, pink-purple eyes, small silver-blue hair accessory, soft open face.",
        "identity_tokens": ["pale pink short layered hair", "airy uneven bangs", "pink-purple eyes", "small silver-blue hair accessory"],
        "viewer_relationship": "quiet gaze, subtle expression, low-intensity body motion.",
        "thumbnail_strategy": "pale pink short hair and transparent-looking eyes must stay stable; styling may vary.",
        "interaction_rule": "standing, seated, front three-quarter, or gentle side-angle poses are fine; avoid locking her into one repeated visual formula.",
        "color_anchor": "pale pink, violet, silver blue",
    },
    "星见雅": {
        "official_core": "long straight black hair, hime-cut blunt bangs, sharp black animal ears, red eyes, single side braid detail.",
        "identity_tokens": ["long straight black hair", "hime-cut blunt bangs", "sharp black animal ears", "red eyes", "single side braid detail"],
        "viewer_relationship": "front or side gaze with a restrained expression; eyes and hair silhouette stay clear.",
        "thumbnail_strategy": "long black hair, black animal ears, red eyes, and one side braid are core; sheath or red-line details are only optional accents.",
        "interaction_rule": "small sheath-like accent, red line motif, or distant blade-shaped shadow may appear; avoid complex hand-held objects.",
        "color_anchor": "black, red, white",
    },
    "仪玄": {
        "official_core": "long silver-white hair, soft ahoge, black wave or lightning-shaped hair ornament, golden eyes.",
        "identity_tokens": ["long silver-white hair", "small ahoge", "black wave or lightning-shaped hair ornament", "golden eyes"],
        "viewer_relationship": "front or side gaze, slow calm movement, hands relaxed near the body or chest.",
        "thumbnail_strategy": "silver-white hair and golden eyes must remain clear; background should not overpower identity.",
        "interaction_rule": "hands near chest, relaxed posture, or side gaze are fine; avoid complex gestures.",
        "color_anchor": "silver white, black, gold",
    },
    "叶瞬光": {
        "official_core": "long warm brown hair, dark inner hair layers, red eyes, red ribbon or flower hair accessory, human ears only.",
        "identity_tokens": ["long warm brown hair", "dark inner hair layers", "red eyes", "red ribbon or flower hair accessory", "human ears only"],
        "viewer_relationship": "quiet off-camera attention, light expression, relaxed hands and shoulder line.",
        "thumbnail_strategy": "warm brown hair, dark inner layers, red eyes, and red accessory must stay stable; do not add animal ears or tail.",
        "interaction_rule": "red cord, slim ribbon, clean light streak, or small distant blade-like ornament may be an accent; do not force a hand-held weapon, sect gate, mountain temple, animal ears, or tail.",
        "color_anchor": "warm brown, red, ivory, black gold",
    },
    "席德": {
        "official_core": "short light cyan-blue hair, large blue back braid, green or teal-green eyes, mechanical arm parts, orange-yellow cable accents.",
        "identity_tokens": ["short light cyan-blue hair", "large blue back braid", "green or teal-green eyes", "mechanical arm parts", "orange-yellow cable accents"],
        "viewer_relationship": "mechanical parts stay close to the body, eyes open and clear, expression light.",
        "thumbnail_strategy": "cyan-blue short hair, blue back braid, teal-green eyes, mechanical arm, and orange-yellow cable accents must stay clear; do not turn her into a generic blue-haired girl.",
        "interaction_rule": "mechanical arm and cables are identity anchors; scooter, hammer weapon, extra fixed design details, and hand-held items are not fixed identity and should be absent by default; avoid generic garden girl or full robot transformation.",
        "color_anchor": "light cyan blue, teal green, orange yellow, clean white",
    },
    "橘福福": {
        "official_core": "golden-orange short hair, yellow-green eyes, small tiger ears, large fluffy tiger tail, red-white festive accessory, energetic human girl.",
        "identity_tokens": ["golden-orange short hair", "green or yellow-green eyes", "small tiger ears", "large fluffy tiger tail", "red festive accessory", "human girl, not animalized"],
        "viewer_relationship": "moving forward or caught mid-motion with a smile, tail forming a large arc, warm image mood.",
        "thumbnail_strategy": "golden-orange hair, yellow-green eyes, tiger ears, fluffy tail, and red-white accessory must stay stable; do not turn her into a tiger beast-person.",
        "interaction_rule": "running, side attention, festive motion, and tail movement are fine; avoid realistic tiger face, animal muzzle, animal legs, claws, or full animal transformation.",
        "color_anchor": "golden orange, yellow green, warm white, red",
    },
    "柚叶": {
        "official_core": "vivid coral-red hair, straight bangs, long thick red side braid or large side ponytail mass, green-yellow eyes, round brown ear-like hair accessories, small fang.",
        "identity_tokens": ["vivid coral-red hair", "straight bangs", "long thick red side braid or large side ponytail mass", "green-yellow eyes", "round brown ear-like hair accessories", "small fang"],
        "viewer_relationship": "lively expression and natural motion; gaze may meet the lens or drift aside.",
        "thumbnail_strategy": "coral-red hair mass, green-yellow eyes, round brown hair accessories, and small fang must stay readable.",
        "interaction_rule": "a subtle tanuki-like motif may appear as a tiny accessory or mood cue; do not animalize her, add animal face details, or force large props.",
        "color_anchor": "coral red, green yellow, dark brown, soft pink",
    },
    "爱丽丝": {
        "official_core": "soft blonde long twin-tail hair, long pointed pink head accessory, warm orange-red eyes, white round disk hair ornaments, red cylindrical hair ties near the hair ends.",
        "identity_tokens": ["soft blonde long twin-tail hair", "long pointed pink head accessory", "warm orange-red eyes", "white round disk hair ornaments", "red cylindrical hair ties near the hair ends"],
        "viewer_relationship": "natural expression, relaxed posture, and clean eye readability.",
        "thumbnail_strategy": "blonde twin-tail silhouette, long pointed pink head accessory, warm orange-red eyes, white round disks, and red hair-end ties must stay clear.",
        "interaction_rule": "head tilt, seated pose, small daily gesture, or side glance are fine; keep the long twin-tail silhouette and round hair ornaments clear, and avoid forcing tools or fixed role details.",
        "color_anchor": "blonde, warm orange red, soft white, muted red",
    },
    "普罗米娅": {
        "official_core": "deep blue-purple hair, heavy side-swept bangs covering one eye, visible violet eye, long segmented braid.",
        "identity_tokens": ["deep blue-purple hair", "side-swept bangs covering one eye", "violet eye", "long segmented braid"],
        "viewer_relationship": "front three-quarter, gentle side angle, half-hidden face, or natural gaze direction are fine.",
        "thumbnail_strategy": "blue-purple hair, one-eye-covered bangs, visible violet eye, and segmented braid must stay clear.",
        "interaction_rule": "front three-quarter framing, gentle side angle, or half-hidden face is fine; avoid forcing fixed role details, heavy covering layers, mechanical props, or hand-held objects.",
        "color_anchor": "deep blue, violet, black, silver",
    },
    "薇薇安": {
        "official_core": "pale lavender long wavy hair, elf ears, red eyes, small ahoge, dark purple bow-like hair accent.",
        "identity_tokens": ["pale lavender long wavy hair", "elf ears", "red eyes", "small ahoge", "dark purple hair accent"],
        "viewer_relationship": "graceful posture and natural gaze, without locking expression or outfit.",
        "thumbnail_strategy": "lavender wavy hair, elf ears, red eyes, ahoge, and dark purple hair accent must stay readable.",
        "interaction_rule": "side gaze, gentle hand pose, or soft curved silhouette may appear; avoid forcing large props, fixed role details, or fantasy role.",
        "color_anchor": "lavender, dark purple, red, soft white",
    },
    "安比": {
        "official_core": "short silver-white hair, yellow-orange eyes, small black-and-gold hair ornament, orange-yellow accent ribbon or streak.",
        "identity_tokens": ["short silver-white hair", "yellow-orange eyes", "black-and-gold hair ornament", "orange-yellow accent"],
        "viewer_relationship": "clear eyes and compact silhouette, with expression allowed to vary naturally.",
        "thumbnail_strategy": "silver-white short hair, yellow-orange eyes, and black-gold hair ornament must stay stable.",
        "interaction_rule": "side attention or action-ready posture are fine; expression may vary naturally, and hand-held objects or combat details should not be forced.",
        "color_anchor": "silver white, yellow orange, black, gray",
    },
    "可琳": {
        "official_core": "mint green twin tails, straight bangs, purple eyes, round X-shaped hair ornaments.",
        "identity_tokens": ["mint green twin tails", "straight bangs", "purple eyes", "round X-shaped hair ornaments"],
        "viewer_relationship": "natural expression and simple readable posture.",
        "thumbnail_strategy": "mint twin tails, purple eyes, and X-shaped hair ornaments must stay clear.",
        "interaction_rule": "small hand gesture, quiet pose, or natural side glance are fine; keep her expression and posture natural, and avoid forcing large hand-held objects or fixed role details.",
        "color_anchor": "mint green, purple, black, soft gray",
    },
    "艾莲": {
        "official_core": "short dark navy-black hair with red-pink underside, red eyes, silver hair clips, shark tail or shark-fin silhouette.",
        "identity_tokens": ["short dark navy-black hair", "red-pink underside hair", "red eyes", "silver hair clips", "shark tail or shark-fin silhouette"],
        "viewer_relationship": "natural gaze and relaxed expression, with clear hair silhouette.",
        "thumbnail_strategy": "dark navy short hair, red-pink underside, red eyes, silver clips, and shark-tail silhouette must stay readable.",
        "interaction_rule": "side glance, casual pose, or restrained motion are fine; expression may vary naturally, and hand-held objects, fixed role details, or leg-focused framing should not be forced.",
        "color_anchor": "dark navy, red pink, red, white",
    },
    "琉音": {
        "official_core": "black-and-white split hair, twin bun structure, long white braid, dark side ponytail, bright gold-green eyes, round headphone-like accessories.",
        "identity_tokens": ["black-and-white split hair", "twin bun structure", "long white braid", "dark side ponytail", "gold-green eyes", "round headphone-like accessories"],
        "viewer_relationship": "lively expression and rhythmic silhouette, without forcing props.",
        "thumbnail_strategy": "black-white split hair, twin buns, long white braid, dark ponytail, and gold-green eyes must stay readable.",
        "interaction_rule": "cheerful pose or music-like rhythm is fine; avoid forcing performance props or fixed role details.",
        "color_anchor": "black, white, gold green, teal, red",
    },
    "耀嘉音": {
        "official_core": "very long dark teal hair, swept bangs, pale pink eyes, pearl-like headband, elegant earrings.",
        "identity_tokens": ["very long dark teal hair", "swept bangs", "pale pink eyes", "pearl-like headband", "elegant earrings"],
        "viewer_relationship": "natural expression and composed posture, without locking personality.",
        "thumbnail_strategy": "dark teal long hair, swept bangs, pale pink eyes, pearl-like headband, and earrings must stay readable.",
        "interaction_rule": "graceful hand pose or side gaze are fine; avoid forcing long hand-held props, heavy accessory styling, fixed formal styling, or fixed expression.",
        "color_anchor": "dark teal, pale pink, pearl white, gold",
    },
}


GENERIC_PROFILE = {
    "official_core": "strictly preserve the uploaded reference hairstyle, hair color, eyes, core accessories, face shape, and expression distance.",
    "identity_tokens": ["reference hairstyle", "reference hair color", "reference eyes", "reference accessories"],
    "viewer_relationship": "make the character feel like they have a real daily life and emotion, close but not artificial.",
    "thumbnail_strategy": "hair shape, eyes, main colors, and core accessories must remain readable when scaled down.",
    "interaction_rule": "natural action, simple hands, no complex hand-held objects.",
    "color_anchor": "reference main colors, clean white, soft black",
}


SHOT_SCALE_OPTIONS = [
    {
        "name": "full_body_readable",
        "description": "full-body framing, head-to-toe visible when possible, character occupies a medium-large readable area as the clear subject",
        "weight": 2.3,
    },
    {
        "name": "knee_up_medium",
        "description": "knee-up or thigh-up framing, character is clearly larger than a distant figure, face, hair, outfit silhouette, and hands are readable",
        "weight": 3.0,
    },
    {
        "name": "waist_up_half_body",
        "description": "waist-up or half-body framing, face and upper body become the main read while the scene still frames the character",
        "weight": 2.4,
    },
    {
        "name": "bust_close",
        "description": "bust shot, face, eyes, hair silhouette, shoulders, and main accessories are prominent; keep enough background to preserve the selected scene",
        "weight": 1.2,
    },
    {
        "name": "close_upper_body",
        "description": "close upper-body framing, face and identity details dominate; background appears as layered atmosphere rather than empty space",
        "weight": 0.8,
    },
]


ART_DIRECTION_PLANS = [
    {
        "name": "trend_mirror_studio",
        "graphic_concept": "bright practice-room or mirror-studio key visual; the character feels freshly finished with training, caught by the camera during a natural pause",
        "spatial_structure": "large mirror, pale floor, window light, and a few circular lamp dots; keep the background spacious and uncluttered",
        "visual_device": "mirror reflection and window light make the hair silhouette, face, and main accessory read clearly at thumbnail size",
        "body_silhouette": "close knee-up or seated pose, character relatively large in frame, hands relaxed near the face, jacket, or lap",
        "outfit_direction": "young casual tops: white short T-shirt, cropped hoodie, sleeveless tank, or off-shoulder knit",
        "material_language": "clean cotton T-shirt, cropped hoodie fabric, ribbed tank top, soft off-shoulder knit, polished floor reflection, soft hair shine",
        "color_strategy": "character palette controls the image; milky white and small black accents keep the composition clean",
        "lighting_behavior": "bright window light with crisp but soft highlights on skin and hair; no oily or harsh rendering",
        "tags": ["trend_lifestyle", "mirror", "studio", "close_character"],
    },
    {
        "name": "capsule_toy_corner",
        "graphic_concept": "collectible capsule-toy corner; transparent toy balls, pale walls, and small mascot shapes make the character feel like a premium character good",
        "spatial_structure": "transparent capsule balls, light circular wall shapes, and a few tiny toys; the scene stays cute but not crowded",
        "visual_device": "repeating circles echo the eyes and create a strong thumbnail memory point",
        "body_silhouette": "half-body to knee-up framing; a small toy may sit nearby, but hands should not dominate the camera",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "clear plastic, soft jacket fabric, tiny charms, candy-color accents, glossy reflections",
        "color_strategy": "pale background plus character colors; toy colors remain small supporting accents",
        "lighting_behavior": "soft high-key light; eyes and hair edges stay sharp",
        "tags": ["trend_lifestyle", "toy", "pastel", "close_character"],
    },
    {
        "name": "graphic_poster_studio",
        "graphic_concept": "clean graphic poster shoot; character colors, simple symbols, and large unreadable letter blocks create an advertising-poster feeling",
        "spatial_structure": "light background, bold color blocks, simple geometry, and a few decorative non-readable letters",
        "visual_device": "large color fields turn the character palette into a clear visual logo",
        "body_silhouette": "seated or kneeling pose, knee-up to full-body range, face and main accessory remain the first read",
        "outfit_direction": "cafe maid remix outfit, neat apron, ribbons, cute and clean",
        "material_language": "clean cloth, apron edge, ribbons, lightweight shoes, small charms, matte graphic panels",
        "color_strategy": "white or pale base, character color dominant, black used only as controlled line weight",
        "lighting_behavior": "clean studio light with minimal shadow",
        "tags": ["trend_lifestyle", "poster", "graphic", "close_character"],
    },
    {
        "name": "afternoon_cafe_negative_space",
        "graphic_concept": "light-novel CG style afternoon cafe interior; warm window light, cream wall blocks, wooden table planes, and quiet air read before the character",
        "spatial_structure": "wide composition with large negative space; character placed off-center near a corner or window; foreground table edge, chair back, or curtain may partially block the view",
        "visual_device": "half-finished drink, dessert plate, flower vase, receipt slip, and tabletop sunlight form a clear daily story",
        "body_silhouette": "medium readable seated or standing figure, three-quarter front or gentle side angle, calm expression, natural hands near the table",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "wood grain, ceramic cup, folded receipt paper, sheer curtain, soft fabric, small glass highlights",
        "color_strategy": "large soft blocks of cream, honey, pale wood, and character palette; low clutter, readable silhouette",
        "lighting_behavior": "strong afternoon window beam cuts across the room; soft bounced light keeps the face readable",
        "tags": ["cafe", "negative_space", "corner_composition", "window_frame", "story_props", "warm_light", "novel_cg"],
    },
    {
        "name": "small_bakery_morning",
        "graphic_concept": "quiet morning bakery scene; warm shelves, paper bags, and soft pastry shapes support the character without stealing identity",
        "spatial_structure": "bread rack, paper bags, glass case, warm lamps, and a simple walking path; elements stay few and readable",
        "visual_device": "round bread shapes and small warm lamps create a gentle repeated rhythm",
        "body_silhouette": "standing near the counter or shifting attention sideways; hands simple, no complicated held object",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "apron cotton, linen, paper bag, wood shelf, glass case, warm bakery glow",
        "color_strategy": "light brown and cream support the character palette; avoid making the whole image yellow",
        "lighting_behavior": "warm indoor light mixed with soft window light; eyes remain clear",
        "tags": ["bakery", "morning", "warm_light", "daily"],
    },
    {
        "name": "bookstore_cafe_corner",
        "graphic_concept": "bookstore cafe corner; vertical shelves, a round table, cup, small note card, and warm window light build a quiet readable scene",
        "spatial_structure": "bookcases, round table, warm lamp, and window seat; no readable book-spine text",
        "visual_device": "shelf verticals and round table geometry create a stable composition",
        "body_silhouette": "sitting or standing beside shelves, hands relaxed, no complex prop handling",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "paper, wood shelf, knit fabric, warm lamp, soft hair edges",
        "color_strategy": "warm wood and pale cream hold the background while character colors stay distinct",
        "lighting_behavior": "soft indoor lamp mixed with natural window light",
        "tags": ["bookstore", "cafe", "quiet", "daily"],
    },
    {
        "name": "library_corner_sunset_silence",
        "graphic_concept": "quiet library corner as an anime novel CG; shelves, amber dust light, and rectangular shadow shapes are the main thumbnail design",
        "spatial_structure": "deep corner perspective with bookcases forming a frame; character near the lower third, partly hidden by shelf edge or desk lamp; large empty wall or floor remains visible",
        "visual_device": "stacked notes, thin ribbon marker as a small accent, tea cup, desk lamp, and sunset strip on the desk guide the eye",
        "body_silhouette": "three-quarter front, seated reading pause, or side attention inside the library; face, hair shape, and eyes remain readable",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "paper, wood shelf, brass lamp, matte cloth, dust in light, quiet floor reflection",
        "color_strategy": "large warm amber and muted green-brown blocks, with character colors as the final focal accent",
        "lighting_behavior": "low sunset light through a high window, hard rectangular cuts on shelf and floor, soft shadow around the character",
        "tags": ["library", "corner_composition", "large_space", "story_props", "sunset", "novel_cg"],
    },
    {
        "name": "balcony_breeze_half_out_frame",
        "graphic_concept": "home balcony breeze scene; curtain, sky, railing, and white interior wall carry the first read, with the character as an emotional note near the edge",
        "spatial_structure": "interior looking toward balcony or balcony looking inward; character half out of frame or placed low to one side; doorframe and curtain create foreground layers",
        "visual_device": "wind-blown curtain, small plant pot, sandals, glass with condensation, and reflected floor light create domestic narrative",
        "body_silhouette": "front three-quarter or relaxed side angle near the balcony breeze; hair and accessories move lightly in wind while face stays readable",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "thin curtain, glass door, metal railing, ceramic pot, polished floor reflection, soft cotton",
        "color_strategy": "large white and sky-blue color fields with one warm accent from the character or nearby object",
        "lighting_behavior": "bright exterior light, interior in pale shade, thin rim light on hair and shoulder",
        "tags": ["balcony", "large_space", "half_out_frame", "foreground_occlusion", "breeze", "daily", "novel_cg"],
    },
    {
        "name": "summer_courtyard_soft_shadow",
        "graphic_concept": "summer courtyard or small garden as a light animation screenshot; tree shadow, white wall, stepping stones, and sky color dominate the thumbnail",
        "spatial_structure": "high or low camera angle with character placed at the edge of the path; foreground leaves, doorframe, or fence line may crop the image",
        "visual_device": "cold drink, flower basket, folded handkerchief, wind on leaves, and reflected light on stone give the place memory",
        "body_silhouette": "walking, pausing, or shifting attention along the path; medium readable figure inside a clear environment",
        "outfit_direction": "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
        "material_language": "stone, leaf shadow, painted wood, glass bottle, small paper slips, light summer fabric",
        "color_strategy": "large blocks of white wall, green shade, and pale sky; character palette stays as the emotional accent",
        "lighting_behavior": "bright summer light filtered by leaves, strong shadow pattern across ground and wall",
        "tags": ["summer_courtyard", "garden", "high_low_camera", "foreground_occlusion", "breeze", "story_props", "novel_cg"],
    },
    {
        "name": "open_grassland_breeze",
        "graphic_concept": "open grassland breeze scene; clean natural colors and the character silhouette are the priority",
        "spatial_structure": "low grass, soft distant horizon, a few small flowers, and wide sky; avoid piling up scenery",
        "visual_device": "wind through hair and clothing creates a light directional line",
        "body_silhouette": "standing or lightly walking, three-quarter to full-body framing, stable motion",
        "outfit_direction": "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
        "material_language": "light fabric, grass blades, small flowers, soft hair movement",
        "color_strategy": "low-saturation green background; character colors must remain legible and not be swallowed by the grass",
        "lighting_behavior": "bright diffused daylight, luminous but not overexposed",
        "tags": ["grassland", "breeze", "natural_light", "daily"],
    },
    {
        "name": "greenhouse_terrace_reflection",
        "graphic_concept": "flower greenhouse terrace with glass reflections; plants, window grids, and pale green light define the image more than the pose",
        "spatial_structure": "layered glasshouse perspective; character behind plants or faintly reflected in glass; foreground leaves partially cover edges without hiding identity essentials",
        "visual_device": "flower bouquet, watering can, small sweets tray, folded ribbon, and sun patches on tile floor build a small daily scene",
        "body_silhouette": "three-quarter front or quiet side glance, medium readable figure inside deep space, not centered",
        "outfit_direction": "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "glass, leaf translucency, ceramic tile, bouquet paper, lace or ribbon, soft moisture shine",
        "color_strategy": "large pale green and white blocks, flower colors as controlled accents, character palette preserved",
        "lighting_behavior": "diffused greenhouse light with clear window-grid shadows and soft reflective highlights",
        "tags": ["greenhouse", "terrace", "reflection", "foreground_occlusion", "flower", "large_space", "novel_cg"],
    },
    {
        "name": "flower_sea_afternoon",
        "graphic_concept": "afternoon flower field; dreamy but not cluttered, with the character still acting as the main visual subject",
        "spatial_structure": "broad flower field as soft color blocks; only a few blurred foreground flowers",
        "visual_device": "flower color fields frame the character hair color and eyes as the memory point",
        "body_silhouette": "standing, seated, or gentle side-angle facing the flower field; hand may lightly touch a flower branch without covering the face",
        "outfit_direction": "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "petals, light gauze, cotton, hair ornament, moderate detail density",
        "color_strategy": "flower colors support the character palette; avoid filling the image with one high-saturation color",
        "lighting_behavior": "soft afternoon light, clear face, lightly blurred background",
        "tags": ["flower_field", "afternoon", "dream", "nature"],
    },
    {
        "name": "garden_tea_table",
        "graphic_concept": "light fairy-tale garden tea table; refined, gentle, and readable as a daily illustration rather than a dense fantasy scene",
        "spatial_structure": "small tea table, flower hedge, white chair, and pale tablecloth; set dressing remains clear and uncrowded",
        "visual_device": "round tea table and flower-hedge arcs frame the character",
        "body_silhouette": "seated, side glance, or lightly holding the chair back; fingers clear and natural",
        "outfit_direction": "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
        "material_language": "tablecloth, flowers, teacup, soft skirt hem, pale chair paint",
        "color_strategy": "white, pale green, and flower accents support the character's strongest identity colors",
        "lighting_behavior": "clear garden daylight with soft air and no heavy shadow",
        "tags": ["garden", "tea_table", "fairy_tale", "daily"],
    },
    {
        "name": "flower_bridal_garden",
        "graphic_concept": "romantic bridal garden illustration; clean, bright, and focused on the character face, hairstyle, and silhouette",
        "spatial_structure": "pale flower arch, white veil fabric, bouquet, and grass; background is light and not crowded",
        "visual_device": "veil, bouquet, and flower arch create a soft frame around the character",
        "body_silhouette": "standing or seated three-quarter pose, hands naturally near bouquet or skirt",
        "outfit_direction": "romantic flower bridal dress, elegant veil or bouquet, clean and elegant",
        "material_language": "thin veil, flower bouquet, soft white dress, a few ribbons",
        "color_strategy": "white and pale flower colors support character colors without washing out hair or eyes",
        "lighting_behavior": "soft garden daylight, clear face, clean high-key atmosphere",
        "tags": ["bridal", "garden", "flower", "soft_light"],
    },
    {
        "name": "dessert_shop_mirror_glance",
        "graphic_concept": "small dessert shop with mirror reflection; pastel wall blocks, display case geometry, and reflected light read before the pose",
        "spatial_structure": "mirror or glass display shows only a partial reflection of the same single character; no second person, no clone, no picture-in-picture duplicate",
        "visual_device": "cake slices, fork, receipt, flower wrapping, and a half-finished drink create a natural after-moment instead of a staged pose",
        "body_silhouette": "seen through a mirror or side reflection; hands simple and close to counter, no reaching toward camera",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "glass display, porcelain plate, cream, paper receipt, polished counter, soft knit or blouse fabric",
        "color_strategy": "large pastel wall and cream counter blocks, character colors echoed in one dessert or flower accent",
        "lighting_behavior": "soft shop light with reflective highlights and clean shadow separation under the counter",
        "tags": ["dessert_shop", "mirror", "reflection", "story_props", "corner_composition", "pastel", "novel_cg"],
    },
    {
        "name": "city_date_window_stroll",
        "graphic_concept": "casual city date moment with boutique window light, cafe signs without readable text, and soft evening reflections; single character only, the date partner stays implied off-camera",
        "spatial_structure": "street corner, glass storefront, cafe terrace edge, and sidewalk perspective lines; character offset from center as if caught during a walk",
        "visual_device": "small shoulder bag, wrapped dessert box, drink cup, window reflections, and warm shop light make the date mood readable without adding another person",
        "body_silhouette": "walking or pausing near a window, front three-quarter angle preferred; gaze may meet the lens or drift aside naturally, hands simple",
        "outfit_direction": "soft date outfit: fitted cardigan, simple camisole or blouse, A-line skirt, small shoulder bag, clean and youthful",
        "material_language": "soft datewear fabric, small shoulder bag, glass storefront, paper dessert box, polished sidewalk reflection",
        "color_strategy": "warm shop light and cool street shadows frame the character palette; brand or sign shapes must stay non-readable",
        "lighting_behavior": "evening window glow with gentle rim light on hair and shoulders; face remains readable but not front-lit like a studio portrait",
        "tags": ["date", "city", "window_frame", "reflection", "warm_light", "daily", "novel_cg"],
    },
    {
        "name": "park_date_riverside_breeze",
        "graphic_concept": "fresh park date scene by a riverside path; benches, railing, trees, and water reflections set a gentle everyday mood; single character only, no couple pose",
        "spatial_structure": "curving path, riverside railing, bench, tree shadow, and distant water line create depth; character placed to one side in a candid frame",
        "visual_device": "small bouquet, folded scarf, takeout drink, shoulder bag, and wind on hair suggest a date without forcing hand-held objects",
        "body_silhouette": "light walking pause or seated on a bench edge, front three-quarter or relaxed side angle; avoid stiff posed stance",
        "outfit_direction": "soft date outfit: fitted cardigan, simple camisole or blouse, A-line skirt, small shoulder bag, clean and youthful",
        "material_language": "soft casual datewear fabric, small bag, bench wood, leaf shadow, water reflection",
        "color_strategy": "fresh green, white, and pale blue support the character palette; sporty brand-like stripes remain small accents",
        "lighting_behavior": "soft daylight or late-afternoon light through leaves, with clear hair edge and gentle water sparkle",
        "tags": ["date", "park", "riverside", "breeze", "natural_light", "daily", "novel_cg"],
    },
    {
        "name": "pastel_room_sweets",
        "graphic_concept": "soft pastel sweets room; simple, cute, and not childish, with the character face as the clearest detail",
        "spatial_structure": "pale wall, small round table, cake or fruit plate, and minimal background",
        "visual_device": "round table and dessert plate act as small visual anchors",
        "body_silhouette": "standing or seated knee-up framing, hands near cup or naturally lowered",
        "outfit_direction": "minimal sunny studio outfit, face and hair identity as the main focus",
        "material_language": "cream cloth, ceramic, dessert, soft hair accessory",
        "color_strategy": "pale background while character hair color and eyes stay more vivid",
        "lighting_behavior": "soft high-key indoor light; avoid washed-out whites",
        "tags": ["sweets", "pastel_room", "soft_light", "daily"],
    },
    {
        "name": "cafe_maid_afternoon",
        "graphic_concept": "cute clean cafe-maid illustration with a light service feeling, not a costume catalogue pose",
        "spatial_structure": "cafe table, dessert plate, pale wall, and window light; simple background",
        "visual_device": "apron silhouette and dessert plate create a clear memory point",
        "body_silhouette": "standing or seated beside a table, hands naturally near tray, skirt, or tabletop",
        "outfit_direction": "cafe maid remix outfit, neat apron, ribbons, cute and clean",
        "material_language": "apron, bow, cotton cloth, ceramic cup, dessert",
        "color_strategy": "black-and-white maid outfit stays controlled; character hair and eyes must remain stronger than the costume",
        "lighting_behavior": "soft afternoon cafe light; eyes and face remain the sharpest read",
        "tags": ["maid", "cafe", "sweets", "warm_light"],
    },
    {
        "name": "sunny_seaside_train",
        "graphic_concept": "sunny seaside train travel scene; blue sea through the window, clean summer light, and a small drink detail create a fresh travel mood",
        "spatial_structure": "train seat, bright window, sea, and sky; carriage details stay clean",
        "visual_device": "window frame, horizon line, and drink cup create a crisp summer-life composition",
        "body_silhouette": "seated knee-up close framing, character relatively large, hands simple",
        "outfit_direction": "young casual tops: white short T-shirt, cropped hoodie, sleeveless tank, or off-shoulder knit",
        "material_language": "white short T-shirt, cropped hoodie, sleeveless tank top, soft off-shoulder knit, glass cup, stickers, small bag charm",
        "color_strategy": "blue sky and character palette support each other; small black straps or bag details anchor the colors",
        "lighting_behavior": "strong but soft sunny window light with fresh skin highlights",
        "tags": ["seaside", "train", "summer", "close_character"],
    },
    {
        "name": "white_room_floor_window",
        "graphic_concept": "quiet white room with floor-to-ceiling window; white wall, pale floor reflection, curtain shadow, and one character-color accent build the composition",
        "spatial_structure": "very wide white space; character off-center but medium-large and clearly readable near a window, sofa edge, or low table; strong empty areas remain intentionally visible",
        "visual_device": "thin curtain, small jewelry tray, flower stem, glass cup, folded cloth, and soft floor reflection create minimal narrative detail",
        "body_silhouette": "sitting on floor or standing near window, front three-quarter or relaxed side angle, calm and cinematic",
        "outfit_direction": "clean pure-white studio outfit, simple silhouette, character colors as the only accent",
        "material_language": "white cotton, glass, polished floor, thin curtain, small metal accessory, matte wall",
        "color_strategy": "dominant white and pale gray with character palette as the memory point; no busy background",
        "lighting_behavior": "large soft window light plus one hard curtain-shadow cut across the floor",
        "tags": ["white_room", "floor_window", "negative_space", "large_space", "soft_light", "minimal", "novel_cg"],
    },
    {
        "name": "pure_white_character_focus",
        "graphic_concept": "pure white character key visual; remove complex scenery so identity, hairstyle, eyes, and outfit silhouette become the entire focus",
        "spatial_structure": "seamless pure white background with only soft shadow and tiny character-color graphic accents; no real location",
        "visual_device": "large white field, character color, and a few black line accents create a clear thumbnail",
        "body_silhouette": "close knee-up or three-quarter pose, character large in frame, natural stable posture",
        "outfit_direction": "clean pure-white studio outfit, simple silhouette, character colors as the only accent",
        "material_language": "clean cloth, a few ribbons, tiny accessories, soft hair",
        "color_strategy": "white dominates; character colors are the only strong memory point",
        "lighting_behavior": "high-key soft light, face and eyes very clear, no gray or dirty whites",
        "tags": ["pure_white", "studio", "minimal", "close_character"],
    },
    {
        "name": "zero_gravity_fairy_room",
        "graphic_concept": "zero-gravity fairy-tale room; the character floats inside a soft dream space with petals, ribbons, and small toys drifting around",
        "spatial_structure": "pale fairy-tale room or cloud space, pillows, petals, ribbons, paper stars, and small toys floating lightly",
        "visual_device": "floating objects form a circular rhythm that returns the eye to face and eyes",
        "body_silhouette": "character lightly floating, body naturally curled or side-lying in the air, hands simple",
        "outfit_direction": "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
        "material_language": "light gauze, ribbon, cloud shapes, petals, soft toys, tiny glow particles",
        "color_strategy": "pale dream background plus character palette; clear and airy, not cluttered or oversaturated",
        "lighting_behavior": "soft dream light, light silhouette, face remains clear",
        "tags": ["zero_gravity", "fairy_tale", "floating"],
    },
    {
        "name": "zero_gravity_fairy_garden",
        "graphic_concept": "zero-gravity fairy garden; the character floats between petals and sunlight, light, dreamy, and collectible",
        "spatial_structure": "pale garden, cloud shapes, petals, transparent bubbles, and small fairy-tale ornaments floating with plenty of open air",
        "visual_device": "petals and bubbles form an upward flow line that strengthens the floating feeling",
        "body_silhouette": "character floating near center or slightly above center, knee-up to full-body range, limbs relaxed",
        "outfit_direction": "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
        "material_language": "light gauze, petals, transparent bubbles, ribbons, soft hair",
        "color_strategy": "flower colors are accents only; character palette must remain the memory point",
        "lighting_behavior": "bright natural soft light with a slight glowing edge in the air",
        "tags": ["zero_gravity", "fairy_tale", "flower", "floating"],
    },
    {
        "name": "guofeng_decorative_kv",
        "graphic_concept": "decorative guofeng key visual without sect or martial-arts storytelling; paper umbrellas, carved windows, silk flowers, red cords, and jade accents orbit the character",
        "spatial_structure": "pale courtyard or indoor screen space; character in middle distance, with umbrella edge, flower branch, or red cord lightly occluding the foreground while face, eyes, and hairstyle remain clear",
        "visual_device": "umbrella circles, window grids, thin red cords, and silk flowers form repeated graphic rhythm; do not turn into a mountain sect or sword-cultivation scene",
        "body_silhouette": "three-quarter or knee-up composition, side glance or seated pose, hands near sleeve edge, flower branch, or tiny ornament",
        "outfit_direction": "reference-faithful outfit with small fashionable variation",
        "material_language": "silk cloth, paper umbrella, jade ornament, red cord, pale gold pattern, wooden window grid, gauze sleeve",
        "color_strategy": "warm white, pale gold, jade, and character palette; red only as thin accent lines",
        "lighting_behavior": "soft window light through lattice leaves pale cuts on face, hair, and clothing edges",
        "tags": ["guofeng", "decorative", "window_frame", "ribbon", "soft_light", "kv"],
    },
    {
        "name": "overhead_deep_perspective_space",
        "graphic_concept": "high-angle anime CG composition; room plan, floor shape, table edges, and window light pattern are the main thumbnail before the character",
        "spatial_structure": "camera looks down from above or stair height; floor tiles, railing, tabletop lines, or furniture edges create clear depth; character stays medium-readable and offset from center",
        "visual_device": "strong foreground-middle-background separation; the eye follows floor perspective and light shapes before reaching the character",
        "body_silhouette": "medium readable figure seen from above, head, face direction, and hair silhouette readable, relaxed posture",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "floor reflection, table plane, window frame, soft cloth, paper, glass highlight",
        "color_strategy": "large floor or wall color block dominates; character palette is a controlled focal accent",
        "lighting_behavior": "top or window light draws hard geometric cuts across floor and furniture, with soft bounce on the character",
        "tags": ["high_camera", "deep_perspective", "large_space", "negative_space", "novel_cg"],
    },
    {
        "name": "low_angle_foreground_depth",
        "graphic_concept": "low-angle upward anime screenshot composition; camera looks slightly up from floor, table, stairs, or garden-path height while the character stays readable",
        "spatial_structure": "camera near floor, tabletop, stair, chair, or garden path level, looking upward through a foreground edge; midground character remains medium-readable and off-center; background rises behind the character",
        "visual_device": "low foreground object, middle character, and rising window, door, wall, tree, or ceiling line form a readable upward three-depth stack",
        "body_silhouette": "medium readable figure seen from a low upward perspective, front three-quarter or clean side angle preferred, simple hands",
        "outfit_direction": "fresh picnic outfit, short jacket or light cardigan, clear color blocks",
        "material_language": "large blurred foreground edge, polished floor or stone path, glass, curtain, plant leaves, fabric",
        "color_strategy": "foreground shadow mass plus bright background plane; character color sits between them as the second read",
        "lighting_behavior": "low camera catches floor reflection and rim light; strong light direction clarifies depth",
        "tags": ["low_camera", "foreground_depth", "deep_perspective", "foreground_occlusion", "novel_cg"],
    },
    {
        "name": "far_shot_readable_room",
        "graphic_concept": "wide light-novel CG; environment carries emotion while the character remains the readable subject inside a room or terrace",
        "spatial_structure": "longer camera distance with wide room, courtyard, library aisle, cafe floor, or balcony visible; character occupies a medium-readable area near a third or corner",
        "visual_device": "large empty wall, floor, or window area and repeated perspective lines create scale; readable character placement creates quiet warmth or loneliness",
        "body_silhouette": "readable full-body, knee-up, or three-quarter figure; identity kept by face, hair shape, color, and accessory silhouette",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "wall, floor, window, shelf, railing, curtain, table plane, soft reflection",
        "color_strategy": "dominant environment colors with one character-color accent; avoid filling the frame with the body",
        "lighting_behavior": "large soft light field, long shadow, or window beam gives spatial scale",
        "tags": ["far_shot", "readable_subject", "large_space", "negative_space", "deep_perspective", "novel_cg"],
    },
    {
        "name": "telephoto_layered_interior",
        "graphic_concept": "compressed telephoto interior or garden view; multiple vertical layers make the image feel found inside the scene",
        "spatial_structure": "camera looks through shelves, curtains, plants, doorframes, or glass; foreground and background stack tightly while character remains off-center",
        "visual_device": "repeating frames and soft occlusion create depth; character appears between layers, not flat in front",
        "body_silhouette": "front three-quarter or relaxed side view, partial crop allowed, face and identity hair/accessory cues remain visible",
        "outfit_direction": "soft bakery or cafe casual outfit, warm and simple",
        "material_language": "glass reflection, curtain layers, shelf edges, leaves, ceramic, paper, soft cloth",
        "color_strategy": "stacked muted color planes; one sharper character-color accent controls the focal point",
        "lighting_behavior": "compressed light bands, reflected highlights, and soft shadow layers separate foreground, character, and background",
        "tags": ["telephoto", "layered_space", "foreground_occlusion", "reflection", "deep_perspective", "novel_cg"],
    },
    {
        "name": "black_stockings_tea_room",
        "graphic_concept": "rare refined tea-room fashion illustration; black stockings appear only as a restrained styling element, not the main theme",
        "spatial_structure": "small tea table, chair, pale curtain, and flower vase; simple soft room with no leg-focused framing",
        "visual_device": "controlled black-and-white clothing contrast supports character colors without dominating the thumbnail",
        "body_silhouette": "seated or side-standing pose, natural leg posture, hands simple and clear; no fetish framing",
        "outfit_direction": "rare refined dark-hosiery fashion outfit, restrained and non-fetishized",
        "material_language": "thin dark stockings, light skirt hem, white blouse, ribbon, soft cloth",
        "color_strategy": "black-and-white outfit stays secondary; background uses cream and pale wood, character colors remain primary",
        "lighting_behavior": "soft indoor natural light, no harsh shadow or dramatic leg emphasis",
        "tags": ["black_stockings", "tea_room", "fashion", "soft_light"],
    },
]


ACTION_STYLES = [
    {
        "name": "steady_eye_contact",
        "body_silhouette": "natural direct-eye-contact moment, slight side turn or relaxed pause, hands resting near sides, jacket edge, or skirt edge; avoid stiff front-facing portrait pose",
        "tags": ["eye_contact", "stable_pose", "simple_hand"],
    },
    {
        "name": "gentle_side_glance",
        "body_silhouette": "three-quarter side angle with eyes drifting away from the camera, hair moving naturally, hands relaxed and readable",
        "tags": ["side_glance", "stable_pose"],
    },
    {
        "name": "seated_quiet_pose",
        "body_silhouette": "quiet seated pose, knee-up to full-body range, both hands naturally near knees, seat, or clothing edge",
        "tags": ["seated", "stable_hands"],
    },
    {
        "name": "walking_forward",
        "body_silhouette": "light walking motion, clear body balance, arms swinging naturally with simple readable hands",
        "tags": ["walking", "stable_hands"],
    },
    {
        "name": "adjusting_hair",
        "body_silhouette": "one hand lightly adjusting hair, the other hand relaxed downward, complete readable fingers",
        "tags": ["hair_touch", "simple_hand"],
    },
    {
        "name": "hands_near_chest",
        "body_silhouette": "both hands near collarbone, neckline, or upper chest area in a modest relaxed way, fingers clear and not tangled",
        "tags": ["hands_visible", "simple_hand"],
    },
    {
        "name": "nearby_small_scene_prop",
        "body_silhouette": "a small dessert, drink, bouquet, note card, or toy sits nearby as scene detail; hands stay simple and do not need to hold the object",
        "tags": ["small_prop", "story_props", "stable_hands"],
    },
    {
        "name": "looking_back_from_edge",
        "body_silhouette": "rare turn-back moment near the image edge; use sparingly, face still readable, and avoid making this the default body direction",
        "tags": ["back_view", "edge_framing", "story_pose"],
    },
    {
        "name": "unaware_candid_moment",
        "body_silhouette": "candid moment as if the camera arrived unexpectedly; character is not posing, gaze may briefly meet the lens or stay on window, table, floor light, or scene detail",
        "tags": ["candid", "eyes_away", "story_pose", "stable_hands"],
    },
    {
        "name": "interrupted_daily_motion",
        "body_silhouette": "caught mid-daily motion, just before or after a small action; body weight is natural, gaze can be slightly off-camera or briefly toward the camera, no deliberate portrait pose",
        "tags": ["candid", "after_moment", "eyes_away", "story_pose"],
    },
    {
        "name": "three_quarter_observed_from_distance",
        "body_silhouette": "front three-quarter observation or soft side-angle variation; character attention mostly stays inside the scene, with optional natural eye contact if composition supports it",
        "tags": ["three_quarter", "natural_gaze", "far_shot", "story_pose"],
    },
    {
        "name": "half_hidden_by_foreground",
        "body_silhouette": "character partly screened by foreground curtain, plant, shelf, table edge, or doorframe; natural relaxed posture, simple hands, no camera-facing pose",
        "tags": ["foreground_occlusion", "half_out_frame", "story_pose"],
    },
    {
        "name": "quiet_prop_after_moment",
        "body_silhouette": "character caught after an action: setting down a cup, turning from the window, adjusting a sleeve, or pausing beside a table; emotion is quiet and cinematic",
        "tags": ["story_props", "after_moment", "simple_hand"],
    },
    {
        "name": "readable_figure_in_depth",
        "body_silhouette": "readable figure placed within the room or path; environment remains visible while the character stays large enough for identity details",
        "tags": ["readable_subject", "far_shot", "deep_perspective", "story_pose"],
    },
    {
        "name": "camera_looking_down",
        "body_silhouette": "occasional moderate high-angle view; head, face, shoulders, and hair remain readable, with controlled floor space",
        "tags": ["high_camera", "deep_perspective", "story_pose"],
    },
    {
        "name": "camera_from_low_foreground",
        "body_silhouette": "low-angle upward shot from floor, table, stair, chair, or garden-path height; foreground edge is near camera while the character remains medium-readable in the midground",
        "tags": ["low_camera", "foreground_depth", "story_pose"],
    },
    {
        "name": "clean_crouching_pose",
        "body_silhouette": "clean crouching pose with knees bent and body weight low, hands naturally near knee, skirt edge, floor, or shoe; keep the angle modest and composition-led",
        "tags": ["crouching", "low_pose", "stable_hands", "story_pose"],
    },
]


ACTION_STYLES.append(
    {
        "name": "post_workout_stretch",
        "body_silhouette": "clean athletic cool-down stretch, seated or one-knee pose, modest body angle, shoulders relaxed, hands naturally near knee, shoe, or floor; avoid suggestive framing",
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
        "name": "pastel_lace_decorative_kv",
        "motifs": "lace, bows, flower trays, glass dessert cups, pearl chains, butterflies, small ribbon cards without text",
        "layering": "foreground lace ribbon and dessert glass; midground character and outfit details; background soft color panels and ornamental frames",
        "shape_rhythm": "rounded boxes, bow loops, skirt waves, pearl chains, flower circles, logo-like silhouette",
        "light_bloom": "milky pastel bloom, warm cream highlights crossing cool mint or lavender shadows, glossy candy reflections",
        "poetic_line": "a sweet decorative anime KV with lace ribbons, pearl chains, butterflies, and glass desserts arranged around the character",
    },
    {
        "name": "fairy_tale_anniversary_kv",
        "motifs": "glowing butterflies, flower petals, ribbons, tiny crowns, paper stars, crystal drops, soft plush ornaments, decorative window cards",
        "layering": "foreground petals and ribbon cards; midground character floating through decorative rhythm; background giant arched window or flower arch",
        "shape_rhythm": "arched window curve, flower arch curve, S-shaped hair, drifting ribbon spiral, repeated star and butterfly marks",
        "light_bloom": "golden fairy light against cool blue or pale green air, edge glow, translucent bloom, small sparkling overexposure",
        "poetic_line": "a fairy-tale anniversary key visual where glowing butterflies, ribbons, flower petals, and tiny ornaments orbit the character in a soft circular stage",
    },
    {
        "name": "candy_air_parlor_kv",
        "motifs": "small glass dessert accents, cream flowers, curled ribbons, glass marbles, paper confetti, tiny plush accents, floating bubbles",
        "layering": "foreground tiny glass dessert detail and confetti; midground character framed by ribbons; background soft parlor shelves, window light, and blurred ornaments",
        "shape_rhythm": "small glass circles, bubble dots, ribbon curls, hair S-curve, repeated tiny plush silhouettes",
        "light_bloom": "cold cyan shadows crossed with peach-pink candy highlights, glass bloom, bright rim cuts, airy haze",
        "poetic_line": "a soft candy-colored parlor accent where tiny glass dessert details, ribbons, and floating bubbles stay secondary to the character",
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
    "pastel_lace_decorative_kv": {
        "cafe",
        "bakery",
        "dessert_shop",
        "date",
        "city",
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
        "park",
        "greenhouse",
        "zero_gravity",
        "bridal",
        "studio",
    },
    "candy_air_parlor_kv": {
        "dessert_shop",
        "toy",
        "pastel",
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


DAYLIGHT_PLAN_TAGS = {"morning", "afternoon", "summer", "sunset", "warm_light", "natural_light", "seaside"}


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
        if visual["name"] in {"pastel_lace_decorative_kv"}
    ]


def choose_visual_design(recent_tags=None, plan=None):
    return dict(random.choice(_visuals_for_plan(plan)))


def choose_shot_scale(recent_tags=None, plan=None):
    plan_tags = _tags_of(plan or {})
    options = [dict(option) for option in SHOT_SCALE_OPTIONS]
    if plan_tags & {"close_character", "studio", "pure_white", "white_room"}:
        bonuses = {
            "knee_up_medium": 0.7,
            "waist_up_half_body": 0.9,
            "bust_close": 0.45,
            "close_upper_body": 0.25,
        }
    elif plan_tags & {"far_shot", "readable_subject", "deep_perspective", "large_space"}:
        bonuses = {
            "full_body_readable": 0.65,
            "knee_up_medium": 0.55,
            "waist_up_half_body": 0.25,
        }
    else:
        bonuses = {
            "full_body_readable": 0.25,
            "knee_up_medium": 0.55,
            "waist_up_half_body": 0.45,
            "bust_close": 0.15,
        }

    weighted = []
    for option in options:
        weighted.append((max(option["weight"] + bonuses.get(option["name"], 0.0), 0.2), option))
    total = sum(weight for weight, _ in weighted)
    pick = random.random() * total
    cursor = 0.0
    for weight, option in weighted:
        cursor += weight
        if pick <= cursor:
            return option
    return weighted[-1][1]


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
    "柚叶",
    "爱丽丝",
    "普罗米娅",
    "薇薇安",
    "安比",
    "可琳",
    "艾莲",
    "琉音",
    "耀嘉音",
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
    "席德": {"nearby_small_scene_prop"},
}


NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES = {
    "overhead_deep_perspective_space": 1.65,
    "low_angle_foreground_depth": 3.4,
    "far_shot_readable_room": 2.2,
    "telephoto_layered_interior": 3.2,
    "afternoon_cafe_negative_space": 3.2,
    "library_corner_sunset_silence": 3.0,
    "balcony_breeze_half_out_frame": 3.0,
    "greenhouse_terrace_reflection": 2.8,
    "white_room_floor_window": 2.8,
    "guofeng_decorative_kv": 2.9,
    "dessert_shop_mirror_glance": 2.8,
    "city_date_window_stroll": 2.6,
    "park_date_riverside_breeze": 2.5,
    "summer_courtyard_soft_shadow": 2.8,
    "bookstore_cafe_corner": 2.4,
    "garden_tea_table": 2.2,
    "pastel_room_sweets": 2.0,
    "small_bakery_morning": 1.9,
    "trend_mirror_studio": 0.7,
    "capsule_toy_corner": 0.8,
    "graphic_poster_studio": 0.55,
    "pure_white_character_focus": 0.75,
    "sunny_seaside_train": 0.6,
    "black_stockings_tea_room": 0.12,
}

NARRATIVE_SPACE_ACTION_WEIGHT_OVERRIDES = {
    "readable_figure_in_depth": 0.75,
    "camera_looking_down": 1.25,
    "camera_from_low_foreground": 3.35,
    "unaware_candid_moment": 3.1,
    "interrupted_daily_motion": 1.7,
    "three_quarter_observed_from_distance": 0.85,
    "looking_back_from_edge": 0.18,
    "half_hidden_by_foreground": 1.15,
    "quiet_prop_after_moment": 1.4,
    "gentle_side_glance": 1.0,
    "seated_quiet_pose": 2.2,
    "nearby_small_scene_prop": 0.9,
    "walking_forward": 2.0,
    "steady_eye_contact": 2.2,
    "hands_near_chest": 1.45,
    "adjusting_hair": 1.6,
    "post_workout_stretch": 0.2,
    "clean_crouching_pose": 1.35,
}


def _apply_weight_overrides(default_weights, character_weights, overrides):
    for item_name, weight in overrides.items():
        default_weights[item_name] = weight
        for weights in character_weights.values():
            weights[item_name] = weight


_apply_weight_overrides(DEFAULT_PLAN_WEIGHTS, CHARACTER_PLAN_WEIGHTS, NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES)
_apply_weight_overrides(DEFAULT_ACTION_WEIGHTS, CHARACTER_ACTION_WEIGHTS, NARRATIVE_SPACE_ACTION_WEIGHT_OVERRIDES)


PLAN_ACTION_COMPATIBILITY = [
    ({"white_room", "pure_white", "minimal"}, {"crouching", "low_pose", "stable_hands", "simple_hand", "eye_contact", "stable_pose", "hair_touch", "hands_visible", "seated", "walking"}),
    ({"high_camera"}, {"high_camera", "deep_perspective", "far_shot", "readable_subject", "eye_contact", "stable_pose", "crouching", "low_pose", "seated"}),
    ({"low_camera", "foreground_depth"}, {"low_camera", "foreground_depth", "eye_contact", "stable_pose", "crouching", "low_pose", "seated", "walking"}),
    ({"far_shot", "readable_subject"}, {"far_shot", "readable_subject", "deep_perspective", "eye_contact", "stable_pose", "crouching", "low_pose", "walking", "seated"}),
    ({"telephoto", "layered_space"}, {"foreground_occlusion", "edge_framing", "simple_hand", "eye_contact", "stable_pose", "crouching", "low_pose", "hair_touch", "hands_visible", "seated"}),
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
        "safe_sensuality": "clean, collectible, non-adult, and non-suggestive.",
        "color_anchor": profile["color_anchor"],
        "propagation_translation": "Character identity is independent from the scene; any character can adapt to lifestyle and cinematic settings without changing species, role, or fixed lore.",
    }


def required_identity_tokens_for(character_name):
    return list(_profile_for(character_name)["identity_tokens"])


def viewer_distance_for(character_name):
    return "camera distance keeps the character at least medium-readable as the clear subject; face, hair silhouette, eyes, outfit shape, and main accessories stay readable"


def outfit_variation_for(character_name, outfit_direction=None):
    profile = _profile_for(character_name)
    base = outfit_direction if outfit_direction in OUTFIT_DIRECTIONS else random.choice(OUTFIT_DIRECTIONS)
    sanrio_detail = ""
    if random.random() < 0.06:
        sanrio_detail = (
            "; optional low-key Sanrio-inspired pastel charm detail, such as a tiny hair clip, "
            "bag charm, sticker, or soft motif; no readable logo and no exact mascot costume"
        )
    eyewear_detail = ""
    if "glasses" not in base.lower() and random.random() < 0.07:
        eyewear_detail = (
            "; optional subtle eyewear accessory, such as round-frame glasses, thin oval glasses, "
            "or lightweight rimless glasses; keep it low-key and do not hide the eyes"
        )
    return (
        f"{base}{sanrio_detail}{eyewear_detail}; adapt to character palette: {profile['color_anchor']}; "
        "keep hairstyle, hair color, eye color, and core accessories"
    )
