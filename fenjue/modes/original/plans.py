import json
import random
from pathlib import Path

from fenjue.data.outfits.yang_mi import YANG_MI_COLOR_FREE_THEMES, YANG_MI_ORIGINAL_COLOR_THEMES
from fenjue.data.outfits.zhang_wonyoung import ZHANG_WONYOUNG_COLOR_FREE_THEMES, ZHANG_WONYOUNG_ORIGINAL_COLOR_THEMES
from fenjue.data.outfits.zhang_ruonan import ZHANG_RUONAN_COLOR_FREE_THEMES, ZHANG_RUONAN_ORIGINAL_COLOR_THEMES

PROJECT_DIR = Path(__file__).resolve().parent
RUNTIME_CONFIG_PATH = PROJECT_DIR / "config" / "runtime_art_direction.json"
RUNTIME_CONFIG_REVISION = "python-default"


OUTFIT_DIRECTIONS = [
    "character-signature outfit with a small fashionable variation",
    "clean light-novel casual outfit, character palette stays recognizable",
    "clean Adidas-inspired sporty date outfit: sleeveless cropped athletic tank, short pleated sport skirt, classic stripe accents",
    "clean Yonex-inspired sporty date outfit: sleeveless cropped athletic tank, short pleated sport skirt, tiny sporty stripe accent",
    "soft date outfit: cardigan, camisole or blouse, A-line skirt, small shoulder bag, clean and youthful",
    "cafe maid remix outfit, neat apron, ribbons, cute and clean",
    "romantic flower bridal dress, elegant veil or bouquet, clean and elegant",
    "elegant flower-field fantasy outfit, simplified layers, no weapon requirement",
    "clean youthful casual outfit, blouse or light cardigan, no stocking emphasis",
    "soft casual outfit with warm simple styling",
    "minimal sunny studio outfit, face and hair identity as the main focus",
    "clean minimal studio outfit, simple silhouette, palette selected to support character identity",
    "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
    "fresh sundress with a straw hat, summer date mood",
    "medium-short gingham shirt over a tank top, denim shorts; shirt tied into a small front-bottom bow",
    "soft windbreaker jacket, modest crew-neck tank top, athletic shorts, round-frame glasses",
    "thin off-shoulder long T-shirt, camisole inner layer visible at neckline, shorts",
    "lace off-shoulder dress with puff sleeves, clean romantic styling",
    "short one-piece dress, youthful clean date styling",
    "elbow-length sleeve light-sport T-shirt with tailored denim shorts",
    "sailor dress, short sleeves, bow and trim, fitted knee-length summer school-date style",
    "simple camisole, lightweight opaque chiffon off-shoulder sleeves, high-waisted denim shorts, clean summer date style",
    "strap maxi dress, fitted waist, flowing full skirt, elegant lightweight summer style",
    "tank top, oversized cropped hoodie, loose jeans, relaxed casual style",
    "sleeveless top, denim overalls, youthful clean casual style",
    "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
    "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit",
    "academy pinafore dress, shirt, ribbon tie, round glasses, preppy school style",
    "oversized sweater, loose sleeves, cozy homewear, soft casual style",
    "waist-shaped mini dress, lace panels, bell sleeves, boots, idol stagewear",
    "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
    "waist-shaped dress, off-shoulder cut, uneven skirt, romantic cottagecore style",
    "lace dress, ribbon waist, airy garden fairy style",
    "striped swim top under loose cover shirt, clean beach resort style",
    "satin lounge slip dress, lace panel, halter neck, side tie ribbon, relaxed resort-home mood",
    "athleisure activewear set, athletic tank, lightweight sun jacket, running shorts, summer sport mood",
    "layered striped knit top, wrap skirt, preppy luxury styling",
    "striped tank top, pleated mini skirt, tennis-girl summer casual style",
    "ribbed tank top, satin shorts, minimal summer lounge style",
    "long-sleeve cropped active top, high-waist flare yoga pants, soft pilates outfit",
    "simple camisole, high-waist flare pants, balletcore pilates fashion",
    "straight-neck maxi dress, simple straight bodice, loose flowing resort silhouette",
    "straight-neck opaque top with oversized cardigan worn off shoulders, relaxed knit loungewear style",
    "cropped graphic T-shirt, abstract graphic chest print, high-waisted jogger pants, casual streetwear",
    "fantasy evening gown, sleeveless design, modest neckline, clean bodice, flowing layered skirt",
    "spaghetti-strap lightly fitted mini dress, clean silhouette, minimalist cocktail eveningwear",
    "cropped athletic top, fitted short sleeves, plain hem band, clean activewear style",
    "knit halter dress, textured fabric, clean upper-body fit, soft draped summer silhouette",
    "straight-neck tailored mini dress, clean neckline, asymmetric hem, long flowing side panels forming a dramatic trailing train, opaque satin opera gloves, pointed high heels",
    "halter-neck ruffled mini dress, clean bodice, layered cascading ruffles, asymmetric high-low hem, long trailing ruffled panels and ribbon-like tails, mid-calf boots",
    "minimal one-piece swimsuit, modest scoop neckline, standard leg openings, clean fitted silhouette, thin straps wrapping around the upper thighs",
    "retro athletic cheer set, sleeveless high-neck cropped athletic top with large number graphic, matching standard-waist athletic shorts, side stripes, piping and drawstring, semi-opaque polka-dot tights",
    "sleeveless halter-neck blouse, soft draped fabric, scarf-like neck tie detail, loose flowing silhouette, high-waisted wide-leg trousers",
    "sleeveless high-neck blouse, delicate floral embroidery, lightly textured opaque fabric, softly gathered neckline, subtle ruffled shoulder trim",
    "racing crop jacket, motorsport sponsor top, performance event costume",
    "lace mini dress, ribbon neck detail, romantic feminine style",
    "light knit cardigan, soft layered outerwear",
    "striped lounge pants, casual wide-leg pants",
    "athletic crop tank, fitness camisole",
    "high-waist denim mini skirt, casual sporty skirt",
    "ruffled chiffon mini dress, tiered fairy dress, idol rehearsal outfit",
    "oversized zip hoodie, casual rehearsal outerwear",
    "chiffon spaghetti-strap maxi dress, flowing skirt, light luxury feminine dating fashion",
    "layered chiffon dress, soft draped layers, gentle girlfriend city-date fashion",
    "satin wrap dress, gentle waist definition, quiet luxury weekend date styling",
    "clean fitted shirt dress, minimal luxury urban lifestyle fashion",
    "short-sleeve blouse dress, soft mature dating fashion, natural social-media outfit",
    "floral tailored top with high-waist skirt, soft romantic rich-girl styling",
    "lace tailored blouse with delicate panel detail, clean refined feminine fashion",
    "off-shoulder floral tailored top with elegant shoulder line, light luxury dating style",
    "off-shoulder cable-knit sweater, soft knit, gentle girlfriend styling",
    "ribbed off-shoulder knit sweater, clean rich-girl casual fashion",
    "off-shoulder mini dress, refined slim silhouette, weekend city date fashion",
    "pleated mini skirt with fitted blouse, soft intellectual date styling",
    "layered tulle skirt with lightweight blouse, romantic urban lifestyle outfit",
    "high-waist straight-leg jeans with fitted blouse, elegant city walk styling",
    "shoulder-draped striped sweater over fitted blouse, clean rich-girl lifestyle fashion",
    "white floral lace blouse with opaque lining and bell sleeves, paired with light-blue distressed high-waist denim shorts, polished summer street style",
    "white-based blue small-floral wrap dress with a modest V neckline, fitted waist, and soft A-line skirt, fresh garden style",
    "pink ribbed cropped cardigan over a white fitted straight-neck inner top, paired with a black high-waist skirt or trousers, sweet modern styling",
    "blue, cyan, lime, and white striped crochet-knit sleeveless top with medium-wash high-waist straight-leg jeans, colorful creative casual style",
    "black velvet mermaid evening gown with a modest sweetheart neckline and white chiffon shoulder wrap; keep the gown as dense soft-pile low-sheen velvet and the wrap as lightweight airy opaque chiffon, elegant banquet styling",
    "white fitted ribbed tank top with a gray high-waist pleated skirt and small blue ribbon accent, clean youthful preppy style",
    "cream open-knit oversized sweater with restrained red, orange, navy, and light-blue stripes, paired with light-wash denim shorts, creative casual style",
    "white crossover draped sleeveless top with a modest neckline and coordinated white skirt or trousers, minimalist resort styling",
    "light-blue oversized button-up shirt with rolled sleeves and a dark-navy high-waist A-line mini skirt, clean intellectual casual style",
    "white flowing maxi resort dress with a gathered bow-front bodice and relaxed full-length skirt, airy vacation styling",
    "sky-blue seamless athletic top with wide straps and matching high-waist full-length leggings, clean pilates styling",
    "green-and-white small-check oversized button-up shirt with a gray high-waist pleated skirt and restrained colorful scarf accent, playful preppy style",
    "white mock-neck short-sleeve inner top with a tailored gray sleeveless vest and matching straight skirt, modern preppy set",
    "burgundy cropped lightweight windbreaker over a white inner top with a dark-gray high-waist pleated skirt and black sturdy boots, sporty preppy styling",
    "burgundy knit pullover layered over a blue button-up shirt with a dark-green high-waist corduroy straight skirt, cozy retro preppy style",
    "boxy olive-green and gray plaid wool jacket with a matching skirt and simple black fitted inner top, coordinated autumn set",
    "plain black oversized T-shirt with gray wide-leg sweatpants and a light-beige low-profile cap, relaxed travel casual style",
    "white relaxed crew-neck T-shirt with a black asymmetric athletic wrap skirt, clean sporty daily style",
    "navy-and-white striped short-sleeve knit top with a white clean A-line skirt, brown loafers, and restrained preppy styling",
    "white-based red small-floral camisole midi dress with a square neckline, gathered waist, and softly flowing skirt, gentle garden vacation style",
    "floral lace blouse with opaque lining, bell sleeves, and tailored high-waist denim shorts, polished summer street style",
    "small-floral wrap dress with a modest V neckline, fitted waist, and soft A-line skirt, fresh garden style",
    "ribbed cropped cardigan over a fitted straight-neck inner top, paired with a high-waist skirt or trousers, sweet modern styling",
    "striped crochet-knit sleeveless top with high-waist straight-leg jeans, colorful creative casual style",
    "velvet mermaid evening gown with a modest sweetheart neckline and lightweight chiffon shoulder wrap; keep the gown as dense soft-pile low-sheen velvet and the wrap as lightweight airy opaque chiffon, elegant banquet styling",
    "fitted ribbed tank top with a high-waist pleated skirt and small ribbon accent, clean youthful preppy style",
    "oversized multicolor open-knit sweater with relaxed denim shorts, creative casual street style",
    "crossover draped sleeveless top with a modest neckline and coordinated skirt or trousers, minimalist resort styling",
    "oversized button-up shirt with rolled sleeves and a high-waist A-line mini skirt, clean intellectual casual style",
    "flowing maxi resort dress with a gathered bow-front bodice and relaxed full-length skirt, airy vacation styling",
    "seamless athletic top with wide straps and matching high-waist full-length leggings, clean pilates styling",
    "small-check oversized button-up shirt with a high-waist pleated skirt and restrained scarf accent, playful preppy style",
    "mock-neck short-sleeve inner top with a tailored sleeveless vest and matching straight skirt, modern preppy set",
    "cropped lightweight windbreaker over a simple inner top with a high-waist pleated skirt and sturdy boots, sporty preppy styling",
    "knit pullover layered over a button-up shirt with a high-waist corduroy straight skirt, cozy retro preppy style",
    "boxy plaid wool jacket with a matching skirt and simple fitted inner top, coordinated autumn set",
    "plain oversized T-shirt with wide-leg sweatpants and a low-profile cap, relaxed travel casual style",
    "relaxed crew-neck T-shirt with an asymmetric athletic wrap skirt, clean sporty daily style",
    "striped short-sleeve knit top with a clean A-line skirt, loafers, and restrained preppy styling",
    "small-floral camisole midi dress with a square neckline, gathered waist, and softly flowing skirt, gentle garden vacation style",
]

OUTFIT_DIRECTIONS.extend(YANG_MI_ORIGINAL_COLOR_THEMES)
OUTFIT_DIRECTIONS.extend(YANG_MI_COLOR_FREE_THEMES)
OUTFIT_DIRECTIONS.extend(ZHANG_WONYOUNG_ORIGINAL_COLOR_THEMES)
OUTFIT_DIRECTIONS.extend(ZHANG_WONYOUNG_COLOR_FREE_THEMES)
OUTFIT_DIRECTIONS.extend(ZHANG_RUONAN_ORIGINAL_COLOR_THEMES)
OUTFIT_DIRECTIONS.extend(ZHANG_RUONAN_COLOR_FREE_THEMES)

FIXED_COLOR_OUTFIT_DIRECTIONS = (
    set(OUTFIT_DIRECTIONS[-190:-170])
    | set(YANG_MI_ORIGINAL_COLOR_THEMES)
    | set(ZHANG_WONYOUNG_ORIGINAL_COLOR_THEMES)
    | set(ZHANG_RUONAN_ORIGINAL_COLOR_THEMES)
)


ANTI_SAFE_COMPOSITION = []


CHARACTER_PROFILES = {
    "南宫": {
        "official_core": "short black bob with two high curled twin tails whose lower lengths are vivid pink, straight blunt bangs, warm pink-red eyes with orange-gold inner color, and a small gray cat-face hairpin.",
        "identity_tokens": ["short black bob with two high curled twin tails", "vivid pink lower twin-tail lengths", "straight blunt bangs", "warm pink-red eyes with orange-gold inner color", "small gray cat-face hairpin"],
        "viewer_relationship": "clever presence, slightly playful, never exaggerated; gaze can meet the lens or drift away naturally.",
        "thumbnail_strategy": "black-pink hair color and the small cat accessory must stay readable at thumbnail size.",
        "interaction_rule": "side glance, eyes-away moment, natural eye contact, or a small smile are fine; avoid always forcing a camera-facing pose or pointing fingers toward the camera.",
        "color_anchor": "black, pink, clean white",
    },
    "爱芮": {
        "official_core": "vivid pink curled twin tails, one black forelock streak with small teal accent streaks, bright cyan-blue eyes with pink star-like inner highlights, dark ribbon-like twin-tail fittings, and an energetic idol expression.",
        "identity_tokens": ["vivid pink curled twin tails", "black forelock streak with small teal accents", "cyan-blue eyes with pink star-like inner highlights", "dark ribbon-like twin-tail fittings"],
        "viewer_relationship": "bright and friendly, like a clean idol-stage interaction.",
        "thumbnail_strategy": "pink twin tails and bright eyes are the first recognition points.",
        "interaction_rule": "waving, smiling, or moving through the scene are fine; avoid selfie props, deliberate lens-facing poses, and hands reaching into the lens.",
        "color_anchor": "hot pink, cyan, clean black",
    },
    "千夏": {
        "official_core": "pale mint-gray-green asymmetrical high-layered short bob with a rounded airy silhouette, thick separated blunt bangs near the upper eyelids, one partially exposed temple secured by a black hollow triangular clip, several small electronic-style clips on the heavier opposite fringe, and a single mid-high half-up side ponytail secured by a large faceted teal four-point star-shaped ornament; the jaw-to-nape bob has broad grouped locks and feathered outward tips, while the rear layers and ponytail deepen into muted teal with subtle pale lavender-gray tips; multicolored amber-gold and cyan eyes and compact youthful facial features.",
        "identity_tokens": ["pale mint-gray-green jaw-to-nape asymmetrical layered short bob", "thick separated blunt bangs with one exposed temple", "black hollow triangular clip and small electronic-style fringe clips", "single mid-high half-up side ponytail", "large faceted teal four-point star-shaped ponytail ornament, not a bow", "muted teal rear layers with subtle pale lavender-gray tips", "multicolored amber-gold and cyan eyes"],
        "viewer_relationship": "warm friendly eye contact, soft cheerful smile, approachable and slightly playful expression.",
        "thumbnail_strategy": "the compact mint short-bob foundation, strongly asymmetrical half-up side ponytail, faceted teal four-point star ornament, fringe clips, and clear multicolored eyes must stay stable; never turn the ornament into a bow or the short bob into long hair or a full high ponytail.",
        "interaction_rule": "small daily gestures, hands relaxed near the sides or sleeves, subtle cute reactions, and relaxed seated poses.",
        "color_anchor": "pale mint gray-green, muted teal, pale lavender gray, amber gold, cyan",
    },
    "丹": {
        "official_core": "saturated rose-pink layered face-framing hair with a rounded shoulder-length silhouette, long sweeping asymmetrical bangs, vivid magenta-violet faceted eyes, two small silver star hair clips, a large blue-violet folded ribbon structure at the rear, and exactly one permanent pair of low-set wings anchored symmetrically at the left and right rear waist at upper-hip level, never at the shoulder blades or upper back. Each wing projects laterally and slightly backward from its waist root, fans across the outer hip, then sweeps downward beside the outer thigh. The canonical state may be pale white-lilac layered feathers or dark indigo feather-mechanical construction.",
        "identity_tokens": ["saturated rose-pink layered hair", "rounded shoulder-length face-framing silhouette", "long sweeping asymmetrical bangs", "vivid magenta-violet faceted eyes", "two small silver star hair clips", "large blue-violet rear ribbon structure", "exactly one pair of low-set wings rooted at the left and right rear waist", "wing roots at upper-hip level, never shoulder-blade or upper-back wings", "wings extending outward from the waist and sweeping downward beside the outer thighs"],
        "viewer_relationship": "calm self-assurance with a soft knowing smile or composed side gaze; feminine and poised rather than timid or childlike.",
        "thumbnail_strategy": "the rose-pink layered hair silhouette, sweeping fringe, luminous magenta-violet eyes, silver star clips, blue-violet rear ribbon, and the low waist-level root or descending side silhouette of both wings must remain recognizable whenever the crop includes the waist.",
        "interaction_rule": "Treat the wings as a permanent character structure independent of clothing or scene props. Preserve exactly two wings with separate roots on the left and right rear waist, aligned around the upper hips with a clear center-back gap. They never grow from the shoulders, shoulder blades, spine, or upper back. From each waist root, the short upper section extends laterally and slightly backward before the feather mass curves down beside the outer thigh; the relaxed compact silhouette reaches roughly knee level, while an expanded action form may extend farther. Use either pale white-lilac layered feather wings or dark indigo feather-mechanical wings for one coherent canonical state; never combine states into extra wings, duplicate the pair, attach them to the arms, or reduce them to shoulder ornaments.",
        "color_anchor": "rose pink, magenta violet, silver, blue violet, white lilac or dark indigo",
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
        "official_core": "a tall adult woman with elegant elongated proportions, a relatively small head, long neck, balanced long torso, high waist, long well-shaped legs, long silver-white hair, soft ahoge, black wave or lightning-shaped hair ornament, and golden eyes.",
        "identity_tokens": ["tall adult woman with elegant elongated proportions", "relatively small head, long neck, balanced long torso, high waist, and long well-shaped legs", "long silver-white hair", "small ahoge", "black wave or lightning-shaped hair ornament", "golden eyes"],
        "viewer_relationship": "front or side gaze, slow calm movement, hands relaxed near the body or chest.",
        "thumbnail_strategy": "her mature graceful silhouette, relatively small head, high waist, long legs, silver-white hair, and golden eyes must remain clear; never compress her into petite, compact, chibi-like, short-torsoed, or short-legged proportions.",
        "interaction_rule": "hands near chest, relaxed posture, or side gaze are fine; avoid complex gestures.",
        "color_anchor": "silver white, black, gold",
    },
    "叶瞬光": {
        "official_core": "very long layered warm chestnut-brown outer hair with deep indigo-black inner layers, thick rounded bangs, two tall triangular crown hair tufts made entirely of brown hair, red eyes, a slim red-white headband, a large red rear ribbon bow, and small red knot ornaments; human ears, no animal ears.",
        "identity_tokens": ["very long layered warm chestnut-brown outer hair", "deep indigo-black inner hair layers", "thick rounded bangs", "two triangular crown hair tufts made of hair, not ears", "red eyes", "slim red-white headband", "large red rear ribbon bow and small red knot ornaments", "human ears, no animal ears"],
        "viewer_relationship": "quiet off-camera attention, light expression, relaxed hands and shoulder line.",
        "thumbnail_strategy": "warm chestnut-brown outer hair, indigo-black inner layers, triangular crown hair tufts, red eyes, red-white headband, rear bow, and small red knot ornaments must stay stable; never turn the hair tufts into animal ears.",
        "interaction_rule": "the pointed crown shapes are hair locks, not biological ears. Do not infer or force a tail from the large flowing hair silhouette. Preserve the red-white headband and red ribbon-knot ornaments, never replace them with flowers, and ignore the white-haired companion visible in one group reference. Do not force a hand-held weapon, sect gate, or mountain temple.",
        "color_anchor": "warm brown, red, ivory, black gold",
    },
    "席德": {
        "official_core": "short light cyan-blue layered hair, one large dark-blue braided ponytail at the back, luminous green and cyan eyes, clearly visible white-gray mechanical forearm parts, and orange-yellow cable accents.",
        "identity_tokens": ["short light cyan-blue layered hair", "one large dark-blue braided back ponytail", "luminous green and cyan eyes", "visible white-gray mechanical forearm parts", "orange-yellow cable accents"],
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
        "official_core": "vivid coral-red bob with straight bangs and two extremely long thick segmented low braids tied near the ends, green-yellow eyes, round brown mechanical hair ornaments, and a small fang.",
        "identity_tokens": ["vivid coral-red bob with straight bangs", "two extremely long thick segmented low braids", "green-yellow eyes", "round brown mechanical hair ornaments", "small fang"],
        "viewer_relationship": "lively expression and natural motion; gaze may meet the lens or drift aside.",
        "thumbnail_strategy": "coral-red twin-braid silhouette, green-yellow eyes, round brown hair ornaments, and small fang must stay readable.",
        "interaction_rule": "keep her lively human silhouette with clear human face, human hands, and human legs. Natural motion, side attention, or a small hand gesture are fine; do not add an animal muzzle, paws, biological animal ears, unrelated animal anatomy, or forced large props.",
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
        "official_core": "short dark navy-black layered bob with a vivid red-pink underside, red eyes, and two silver hair clips.",
        "identity_tokens": ["short dark navy-black layered bob", "vivid red-pink underside hair", "red eyes", "two silver hair clips"],
        "viewer_relationship": "natural gaze and relaxed expression, with clear hair silhouette.",
        "thumbnail_strategy": "dark navy short hair, red-pink underside, red eyes, and two silver clips must stay readable.",
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
        "official_core": "very long voluminous deep teal-black hair, short straight choppy bangs across the forehead, cheek-length curved side locks, narrow pale pink-red eyes, a wide white pearl-silver jeweled headband with small diamond studs, and large gold hoop earrings with green jade beads.",
        "identity_tokens": ["very long voluminous deep teal-black hair", "short straight choppy bangs", "cheek-length curved side locks", "narrow pale pink-red eyes", "wide white pearl-silver jeweled headband with diamond studs", "large gold hoop earrings with green jade beads"],
        "viewer_relationship": "confident narrow-eyed gaze, softly angular adult anime face, poised smile, and elegant self-assured posture.",
        "thumbnail_strategy": "deep teal-black hair, short choppy bangs, pink-red narrow eyes, wide white jeweled headband, and gold-green hoop earrings must remain readable.",
        "interaction_rule": "the jeweled headband and gold-green hoop earrings are permanent identity anchors. Staff, stage props, black corset costume, red jacket, white performance sleeves, weapons, and character-reference poses are not fixed identity and must not transfer into photoset clothing.",
        "color_anchor": "dark teal, pale pink, pearl white, gold",
    },
    "柏妮思": {
        "official_core": "light blonde short hair, high side twin tails attached with golden twin-tail holders, fluffy outward-curving twin tails, thick fluffy bangs, voluminous front hair, partially eye-covering bangs, red-orange eyes, energetic smile, lively and carefree atmosphere, sporty youthful appearance.",
        "identity_tokens": [
            "light blonde short hair",
            "high side twin tails",
            "golden twin-tail holders",
            "fluffy outward-curving twin tails",
            "thick fluffy bangs",
            "red-orange eyes"
        ],
        "viewer_relationship": "bright direct eye contact, cheerful grin, energetic and welcoming expression, playful and approachable personality, as if inviting the viewer into the fun.",
        "thumbnail_strategy": "high side twin tails, golden twin-tail holders, fluffy bangs, and red-orange eyes must stay stable; do not turn her into a generic blonde girl, long-haired character, mature cool beauty, or horned character.",
        "interaction_rule": "playful gestures, casual movement, excited reactions, leaning forward, waving, laughing, energetic body language, spontaneous cute antics, naturally interacting with people, animals, or the environment.",
        "personality_anchor": "big friendly puppy energy, accident-prone but lucky, chaotic good personality, warm-hearted troublemaker, naturally lovable and optimistic.",
        "color_anchor": "gold, black, red-orange, warm cream"
    },
    "妮可": {
        "official_core": "long fluffy pink twin tails, black ribbon twin-tail bows, bright green eyes, layered pink bangs, confident smile, street-smart and charismatic atmosphere, fashionable urban girl appearance.",
        "identity_tokens": [
            "long fluffy pink twin tails",
            "black ribbon twin-tail bows",
            "bright green eyes",
            "layered pink bangs",
            "pink hair"
        ],
        "viewer_relationship": "confident eye contact, playful grin, clever and persuasive expression, as if she is already negotiating a deal with the viewer.",
        "thumbnail_strategy": "long pink twin tails, black ribbon bows, layered pink bangs, and bright green eyes must stay stable; do not turn her into a generic pink-haired girl, idol character, or elegant princess.",
        "interaction_rule": "confident poses, playful gestures, finger-pointing, peace signs, counting money, negotiating, showing off, teasing expressions, relaxed leader-like body language, naturally taking charge of the situation.",
        "personality_anchor": "street-smart entrepreneur, money-loving but soft-hearted, debt-ridden genius, resourceful survivor, charming trickster, reliable leader beneath a greedy exterior.",
        "color_anchor": "pink, black, white, neon yellow-green"
    },
    "简": {
        "official_core": "short layered black bob with gray highlights, pointed elf ears with multiple silver piercings, turquoise-green eyes, long dark-crimson rear hair extension, segmented gray rat tail with a metallic arrow-shaped tip.",
        "identity_tokens": ["short layered black bob with gray highlights", "pointed elf ears with multiple silver piercings", "turquoise-green eyes", "long dark-crimson rear hair extension", "segmented gray rat tail with metallic arrow-shaped tip"],
        "viewer_relationship": "playful confident presence with a natural front, three-quarter, or side gaze; keep the eyes, ears, hair silhouette, and tail readable.",
        "thumbnail_strategy": "black-gray bob, turquoise-green eyes, pierced elf ears, crimson rear hair extension, and segmented rat tail must stay clear; outfit and undercover gear may vary.",
        "interaction_rule": "small teasing expression or relaxed stance is fine; keep hands object-free and naturally below shoulder level, and avoid complex undercover or tactical props.",
        "color_anchor": "black, dark crimson, gray, silver, turquoise green",
    },
    "月城柳": {
        "official_core": "soft pink shoulder-length to medium-long hair with side-swept bangs, violet-pink eyes, thin dark rectangular glasses, black mechanical side hair ornament with a circular cable, and a small teal ribbon accent.",
        "identity_tokens": ["soft pink shoulder-length to medium-long hair with side-swept bangs", "violet-pink eyes", "thin dark rectangular glasses", "black mechanical side hair ornament with circular cable", "small teal ribbon accent"],
        "viewer_relationship": "calm composed presence with a natural front, three-quarter, or side gaze; keep the eyes behind the glasses, pink hair silhouette, and mechanical side ornament readable.",
        "thumbnail_strategy": "soft pink hair, violet-pink eyes, thin dark glasses, black mechanical side ornament, circular cable, and a restrained teal accent must stay clear; uniform and weapon are not fixed identity.",
        "interaction_rule": "composed standing, walking, seated posture, or lightly folded arms are fine; keep hands simple, and treat any slim blade-shaped silhouette as an optional distant accent rather than a held prop.",
        "color_anchor": "soft pink, black, teal, violet",
    },
    "青衣": {
        "official_core": "long dark-green twin tails, blunt bangs with two short front braids, turquoise-green eyes, jade leaf-shaped hair ornaments, small white ribbon accents, and a restrained ancient-inspired android quality.",
        "identity_tokens": ["long dark-green twin tails", "blunt bangs with two short front braids", "turquoise-green eyes", "jade leaf-shaped hair ornaments", "small white ribbon accents"],
        "viewer_relationship": "calm leisurely presence with a natural front, three-quarter, or side gaze; keep the eyes, twin-tail silhouette, front braids, and jade ornaments readable.",
        "thumbnail_strategy": "dark-green twin tails, turquoise-green eyes, blunt bangs, two front braids, and jade leaf ornaments must stay clear; mechanical details are optional supporting accents.",
        "interaction_rule": "relaxed listening or hands resting naturally near the sides or lap are fine; keep hands object-free and let any android or staff-like detail remain subtle in the background.",
        "color_anchor": "dark green, teal, jade, black, muted gold",
    },
    "伊芙琳": {
        "official_core": "shoulder-length blonde hair gathered into a braided low bun, long side bangs, lavender-purple eyes, and geometric gold earrings.",
        "identity_tokens": ["shoulder-length blonde hair with braided low bun", "long side bangs", "lavender-purple eyes", "geometric gold earrings"],
        "viewer_relationship": "calm professional presence with a natural front, three-quarter, or side gaze; keep the eyes, blonde silhouette, braided bun, and earrings readable.",
        "thumbnail_strategy": "blonde hair, lavender-purple eyes, braided low bun, and geometric gold earrings must stay clear; coat, necktie, and tactical styling may vary with the selected outfit.",
        "interaction_rule": "adjusting a collar, holding a coat edge with one simple hand, walking, or standing with composed body language are fine; concealed equipment must remain subtle and optional.",
        "color_anchor": "blonde, black, crimson, gold, lavender",
    },
    "朱鸢": {
        "official_core": "high black ponytail with vivid red streaks, short layered bangs, amber-orange eyes, and a silver mechanical headband.",
        "identity_tokens": ["high black ponytail with vivid red streaks", "short layered bangs", "amber-orange eyes", "silver mechanical headband"],
        "viewer_relationship": "serious composed presence with a natural front, three-quarter, or side gaze; keep the eyes, ponytail silhouette, red streaks, and headband readable.",
        "thumbnail_strategy": "black high ponytail, vivid red streaks, amber-orange eyes, and silver mechanical headband must stay clear; police uniform and tactical equipment are not fixed identity.",
        "interaction_rule": "disciplined standing or walking with hands relaxed near the sides is fine; avoid forcing police equipment, firearms, or tactical action.",
        "color_anchor": "black, vivid red, blue, silver, amber",
    },
    "卢西娅": {
        "official_core": "short light-blue hair with a braided ponytail, small black horns, long pointed elf ears, golden-green eyes, and a dark-blue tassel braid tip with small gold ornaments.",
        "identity_tokens": ["short light-blue hair with braided ponytail", "small black horns", "long pointed elf ears", "golden-green eyes", "dark-blue tassel braid tip with small gold ornaments"],
        "viewer_relationship": "gentle mysterious presence with a natural front, three-quarter, or side gaze; keep the eyes, blue hair silhouette, horns, elf ears, and braided tassel readable.",
        "thumbnail_strategy": "light-blue hair, small black horns, golden-green eyes, pointed elf ears, and dark-blue tassel braid tip must stay clear; cape panels and magical tools are optional.",
        "interaction_rule": "a quiet contemplative pose or relaxed standing with hands naturally lowered is fine; staff-like forms and magical accessories may appear only as unobtrusive background elements.",
        "color_anchor": "light blue, teal, dark blue, black, muted gold",
    },
    "维琳娜": {
        "official_core": "very long pale silver-lavender hair, heavy side-swept bangs covering one eye, pointed elf ears, violet visible eye, and oversized white-blue bow ornaments.",
        "identity_tokens": ["very long pale silver-lavender hair", "heavy side-swept bangs covering one eye", "pointed elf ears", "violet visible eye", "oversized white-blue bow ornaments"],
        "viewer_relationship": "composed teasing presence with a natural front or front three-quarter gaze; keep the visible eye, one-eye bangs shape, elf ears, bow ornaments, and flowing hair silhouette clear.",
        "thumbnail_strategy": "one-eye side-swept fringe, pale silver-lavender long hair, pointed elf ears, violet eye, and large white-blue bow ornaments are the core read; outfit may vary with the selected fashion theme.",
        "interaction_rule": "elegant relaxed hands, a small sleeve or ribbon adjustment, or a refined quiet pose are preferred; a tiny fan-shaped accessory may appear only as a subtle background or clothing detail, not as a complex hand-held prop.",
        "color_anchor": "pale silver-lavender, deep blue, white, gold",
    },
    "铃": {
        "official_core": "short deep blue-violet bob hair with a large side-swept bang covering part of one eye, teal-blue eyes, an orange N-shaped hair clip, small teal earrings, and a bright music-loving academy-girl impression.",
        "identity_tokens": ["short deep blue-violet bob hair", "large side-swept bang covering part of one eye", "teal-blue eyes", "orange N-shaped hair clip", "small teal earrings"],
        "viewer_relationship": "cheerful, curious, quick-witted, and friendly; expressions can be a wink, bright smile, or playful focused gaze, but the face stays clean and readable.",
        "thumbnail_strategy": "deep blue-violet short hair, side-swept bang, teal eyes, orange N hair clip, and small teal earrings must remain readable; do not turn her into a long-haired mature model or generic blue-haired girl.",
        "interaction_rule": "music-shop gestures, holding a record case, listening pose, small finger-to-lips wink, or light academy pose are compatible; the portable CD player, student cap, academy uniform, and Yunki-style outfit are reference outfits or props only, not mandatory identity anchors for every photoset.",
        "color_anchor": "deep blue violet, teal blue, orange, black, warm gold",
    },
    "扳机": {
        "official_core": "creamy-blonde hair in one high ponytail with short layered face locks, an opaque glossy black visor fully covering both eyes, paired red triangular mechanical clips with round gray centers, angular black rear hair fixtures, and one thin yellow cable accent.",
        "identity_tokens": ["creamy-blonde high ponytail", "short layered blonde face locks", "opaque glossy black visor covering both eyes", "paired red triangular mechanical clips with round gray centers", "angular black rear hair fixtures", "thin yellow cable accent"],
        "viewer_relationship": "quiet, exact, and self-possessed; communicate emotion through head angle and mouth shape while the visor remains opaque.",
        "thumbnail_strategy": "the blonde ponytail, fully opaque visor, paired red clips, black rear fixtures, and yellow cable must remain readable at small size.",
        "interaction_rule": "Never expose eyes through the visor and never turn it into transparent glasses or a fabric blindfold. Reference weapons, tactical clothing, and combat poses are not identity traits and must not transfer into photoset outfits.",
        "color_anchor": "creamy blonde, glossy black, signal red, industrial gray, yellow",
    },
    "诺姆": {
        "official_core": "compact youthful proportions, golden-blonde hair with straight blunt bangs and two very long low braids, violet-blue eyes, and an oversized silver-gray cylindrical mechanical helmet with two dark antennae and circular A-mark side plates.",
        "identity_tokens": ["compact youthful proportions", "golden-blonde blunt bangs", "two very long low blonde braids", "violet-blue eyes", "oversized silver-gray cylindrical mechanical helmet", "two dark mechanical antennae", "circular A-mark side plates"],
        "viewer_relationship": "bright, curious, and earnest, with a small youthful silhouette and clear open eyes.",
        "thumbnail_strategy": "the helmet cylinder, twin antennae, side plates, blonde fringe and braids, violet-blue eyes, and compact proportions must remain immediately recognizable.",
        "interaction_rule": "The tall shapes are mechanical antennae, never biological ears. Keep the helmet coherent and wearable; reference machinery, companion creatures, gauntlets, and clothing are optional and must not transfer by default.",
        "color_anchor": "golden blonde, silver gray, charcoal black, violet blue, warm yellow",
    },
    "今汐": {
        "official_core": "pearl-silver hair with straight brow-length bangs, rounded jaw-length side locks, and exactly two extremely long low side tails fading to pale aqua feather-like tips, each anchored by a dark bronze openwork ornament and translucent aqua bow; pale gray-rose eyes.",
        "identity_tokens": ["pearl-silver hair", "straight brow-length bangs", "rounded jaw-length side locks", "exactly two extremely long low side tails", "pale aqua feather-like hair tips", "paired bronze openwork anchors", "paired translucent aqua bows", "pale gray-rose eyes"],
        "viewer_relationship": "serene, dignified, and gently attentive.",
        "thumbnail_strategy": "the short rounded front hair, paired bronze anchors, aqua bows, two long low tails, and rose-gray eyes must remain clear.",
        "interaction_rule": "Keep exactly two low side tails; never convert them into loose hair, one ponytail, or short twin tails. Dragons, weapons, ceremonial clothing, and scene effects visible in references are optional only.",
        "color_anchor": "pearl silver, pale aqua, muted bronze, soft rose gray",
    },
    "千咲": {
        "official_core": "slim human proportions; very long straight black hair; dense brow-length blunt bangs; short tapered cheek-framing locks; vivid red eyes; one narrow red bow at the side-back hair; black star-like vertical mark on the right upper arm when visible.",
        "identity_tokens": ["slim human proportions", "very long straight black hair", "dense brow-length blunt bangs", "short tapered cheek-framing locks", "vivid red eyes", "one narrow red bow at the side-back hair", "black star-like vertical mark on the right upper arm when visible"],
        "viewer_relationship": "Quiet, observant and composed, with a restrained direct or sideways gaze.",
        "thumbnail_strategy": "Preserve the blunt fringe, long straight dark hair, red eyes and narrow side bow without a generic long-hair redesign.",
        "interaction_rule": "Keep the long loose rear hair separate from the short cheek locks; do not turn it into twin ponytails. Preserve the right-upper-arm mark whenever uncovered; template sleeves may cover it normally. Use the first two character images for the canonical red hair bow. The summer bonnet, floral decorations, swimwear, drink and pool are alternate styling only. The giant red-black blade and school uniform are not identity locks.",
        "color_anchor": "black, red, pale neutral skin",
    },
    "卡提希娅": {
        "official_core": "very long golden-blonde hair, long pointed elf ears, clear blue eyes, a blue-silver branching crown ornament, and blue teardrop earrings.",
        "identity_tokens": ["very long golden-blonde hair", "long pointed elf ears", "clear blue eyes", "blue-silver branching crown ornament", "blue teardrop earrings"],
        "viewer_relationship": "graceful, bright, and composed.",
        "thumbnail_strategy": "blonde hair, pointed ears, clear blue eyes, the branching crown ornament, and teardrop earrings must remain readable.",
        "interaction_rule": "Never round off or hide the pointed ears. Reference weapons, ceremonial garments, and magical water effects are scene styling, not permanent identity.",
        "color_anchor": "golden blonde, sky blue, silver, soft white",
    },
    "坎特蕾拉": {
        "official_core": "very long flowing lavender-violet hair with a heavy curved side fringe and curled cheek locks, violet-pink eyes with cool cyan highlights, a narrow white ruffled headband, and one layered blue-violet flower ornament at the side of the head.",
        "identity_tokens": ["very long lavender-violet hair", "heavy curved side fringe", "curled cheek-length locks", "violet-pink eyes with cyan highlights", "narrow white ruffled headband", "layered blue-violet side flower ornament"],
        "viewer_relationship": "elegant, mysterious, and knowingly calm.",
        "thumbnail_strategy": "the lavender hair mass, curved fringe, cool multitone eyes, white headband, and side flower must remain clear.",
        "interaction_rule": "The parasol in the references is a removable prop, never a hat or identity trait. Do not add it unless the selected template requires an umbrella; reference dress and underwater effects are optional.",
        "color_anchor": "lavender violet, icy cyan, pearl white, deep blue",
    },
    "守岸人": {
        "official_core": "short softly waved pale aqua-blue hair, clear blue eyes, and a large white headpiece with luminous blue butterfly-wing or feather-like ornaments.",
        "identity_tokens": ["short softly waved pale aqua-blue hair", "clear blue eyes", "large white headpiece", "luminous blue butterfly-wing or feather-like ornaments"],
        "viewer_relationship": "gentle, tranquil, and quietly otherworldly.",
        "thumbnail_strategy": "the short aqua hair, blue eyes, white headpiece, and luminous blue wing-like ornaments must stay distinct.",
        "interaction_rule": "Keep the luminous head ornament separate from the hair. Cosmic effects and the exact white-blue costume in references are optional and must not replace the template outfit.",
        "color_anchor": "pale aqua, luminous blue, clean white, midnight blue",
    },
    "尤诺": {
        "official_core": "deep navy hair arranged into two large high ponytails that fade to pale blue, short face-framing layers, iridescent blue-gold eyes, and paired gold laurel-like head ornaments.",
        "identity_tokens": ["deep navy high twin ponytails", "pale blue gradient hair ends", "short face-framing layers", "iridescent blue-gold eyes", "paired gold laurel-like ornaments"],
        "viewer_relationship": "confident, poised, and observant.",
        "thumbnail_strategy": "the large navy twin-tail silhouette, pale blue tips, luminous eyes, and gold ornaments must remain clear.",
        "interaction_rule": "Keep exactly two high ponytails and do not flatten them into loose long hair. The circular device, weapons, and exact clothing are optional reference elements.",
        "color_anchor": "deep navy, pale blue, luminous gold, black",
    },
    "洛瑟菈": {
        "official_core": "extremely long indigo-violet hair fading to pale lavender, a heavy sweeping fringe covering one eye, one visible violet eye, a broad dark star-map disc hat, and large double-hoop earrings.",
        "identity_tokens": ["extremely long indigo-violet hair", "pale lavender ends", "heavy one-eye fringe", "one visible violet eye", "broad dark star-map disc hat", "large double-hoop earrings"],
        "viewer_relationship": "fashionable, enigmatic, and self-possessed.",
        "thumbnail_strategy": "the one-eye fringe, violet gradient hair, broad disc hat, visible violet eye, and hoop earrings must remain readable.",
        "interaction_rule": "Keep the disc hat broad and separate from the hair. Reference bags, gloves, laboratory props, and fashion garments are optional only.",
        "color_anchor": "indigo, violet, pale lavender, charcoal black",
    },
    "爱弥斯": {
        "official_core": "extremely long vivid pink hair in one high ponytail, luminous cyan feather-like hair ornaments and cyan accent strands, and amber-gold eyes.",
        "identity_tokens": ["extremely long vivid pink high ponytail", "luminous cyan feather-like hair ornaments", "cyan accent strands", "amber-gold eyes"],
        "viewer_relationship": "energetic, direct, and warmly confident.",
        "thumbnail_strategy": "the long pink ponytail, cyan luminous accents, and amber eyes must remain clear.",
        "interaction_rule": "Keep one high ponytail and coherent cyan ornaments. Mechanical companions, weapons, energy effects, and the exact reference outfit are optional only.",
        "color_anchor": "bright pink, luminous cyan, amber gold, clean black",
    },
    "琳奈": {
        "official_core": "slim lively human silhouette; long sandy-blonde hair with mint-turquoise accent lengths; long diagonal fringe partly crossing one eye; small close side braids; looped side-back hair sections above long loose lengths; violet-blue eyes with bright cyan and pink iris facets; small white skull-shaped hair clip; turquoise elongated four-point star earrings; small dark ear piercings.",
        "identity_tokens": ["slim lively human silhouette", "long sandy-blonde hair with mint-turquoise accent lengths", "long diagonal fringe partly crossing one eye", "small close side braids", "looped side-back hair sections above long loose lengths", "violet-blue eyes with bright cyan and pink iris facets", "small white skull-shaped hair clip", "turquoise elongated four-point star earrings", "small dark ear piercings"],
        "viewer_relationship": "Casual and confident, with a relaxed playful gaze rather than a fixed broad grin.",
        "thumbnail_strategy": "The diagonal fringe, close side braids, looped long hairstyle, multitone eyes, skull clip and turquoise star earrings must remain clear.",
        "interaction_rule": "Use the clear anniversary portrait for the skull clip, ear jewelry and sandy-blonde base color. Keep turquoise accents without recoloring all hair to match the strong blue-green summer illumination. Preserve the looped sections and their ties as shown; do not simplify to a plain bob or a single ponytail. Black rear ribbons remain distinct from hair; summer flowers, sunglasses, headphones, necktie, swimwear and motorcycle are optional styling, not fixed accessories.",
        "color_anchor": "sandy blonde, mint turquoise, violet blue, pink accents, black",
    },
    "秧秧": {
        "official_core": "long layered midnight-blue hair with a short rounded crown, separated bangs, broad feather-shaped side and rear locks transitioning through white and pale cyan to deep cobalt tips, clear cyan-blue eyes, a slim pale-blue vertical forehead mark, small gold bird ornaments, and one restrained red tassel.",
        "identity_tokens": ["long layered midnight-blue hair", "short rounded crown and separated bangs", "broad white-to-cyan feather-shaped hair locks", "deep cobalt tips", "clear cyan-blue eyes", "slim pale-blue vertical forehead mark", "small gold bird ornaments", "restrained red tassel"],
        "viewer_relationship": "calm, considerate, and quietly resolute.",
        "thumbnail_strategy": "the dark crown, white-cyan feather-shaped locks, blue eyes, slim forehead mark, gold ornament, and red tassel must stay clear.",
        "interaction_rule": "The pale feather shapes are grouped hair structures, not detached wings. Bird companions, loose feathers, weapons, and reference clothing are optional only.",
        "color_anchor": "deep navy, pale cyan, cobalt, soft gold, restrained red",
    },
    "绯雪": {
        "official_core": "slender elongated human proportions; very long loose silver-white rear hair; one large high rounded folded topknot; thick straight brow-length bangs with a narrow central separation; two long inward-curved face locks; vivid red eyes; paired dark-red ribbons beside the topknot; white blossom ornament beside the topknot; small dark mark below the right collarbone when visible.",
        "identity_tokens": ["slender elongated human proportions", "very long loose silver-white rear hair", "one large high rounded folded topknot", "thick straight brow-length bangs with a narrow central separation", "two long inward-curved face locks", "vivid red eyes", "paired dark-red ribbons beside the topknot", "white blossom ornament beside the topknot", "small dark mark below the right collarbone when visible"],
        "viewer_relationship": "Reserved and focused, with a soft controlled mouth and steady gaze.",
        "thumbnail_strategy": "Keep the folded white topknot, flowing loose rear hair, red eyes, red ribbons and side blossom distinct.",
        "interaction_rule": "Keep one high rounded topknot above loose rear hair, never a single high ponytail. Preserve the small right-collarbone mark where visible; do not expose it through clothing. The first isolated full-body image defines the target. Other faces and figures in the second blue collage are separate depictions or companions, not features to merge into her. Sword, white-red drapery, hair-like garment streamers and jewelry attached to clothing are not identity locks.",
        "color_anchor": "silver white, red, cool gray, restrained dark accents",
    },
    "莫宁": {
        "official_core": "pale silver-blue hair with a heavy fringe covering one eye and extremely long rear lengths, one visible red eye, two small triangular clips, long triangular earrings, a separate floating dark crystal halo, and two human-shaped but non-flesh translucent silver-white crystalline synthetic legs with internal cyan-blue diamond facets and tiny star-like specks.",
        "identity_tokens": ["pale silver-blue hair", "heavy one-eye fringe", "extremely long rear hair", "one visible red eye", "two triangular hair clips", "long triangular earrings", "separate floating dark crystal halo", "two non-flesh translucent silver-white crystalline synthetic legs", "internal cyan-blue diamond facets and tiny star-like specks"],
        "viewer_relationship": "cool, analytical, and quietly uncanny.",
        "thumbnail_strategy": "the one-eye fringe, red eye, long silver-blue hair, triangular details, and floating halo must remain clear; in full-body or leg-visible framing, both crystalline non-flesh legs and their cyan facets must also remain readable.",
        "interaction_rule": "The dark halo floats separately above the head and must never become a hat or solid headband. Both legs are permanent crystalline synthetic anatomy: whenever any leg area is visible, show translucent silver-white non-flesh material with cyan-blue facets and star-like specks, never ordinary skin or flesh legs. Template trousers, skirts, hosiery, and footwear may cover them normally, but clothing must not rewrite any exposed leg area as human skin. Holograms, tools, and laboratory clothing are optional.",
        "color_anchor": "silver blue, dark crystal black, red, restrained cyan",
    },
    "菲比": {
        "official_core": "very long wavy blonde hair with blunt bangs and side curls, violet eyes, a small blue cross-shaped hair clip, and an oversized white wide-brim hat with a blue feather ornament.",
        "identity_tokens": ["very long wavy blonde hair", "blunt bangs and side curls", "violet eyes", "small blue cross hair clip", "oversized white wide-brim hat", "blue feather ornament"],
        "viewer_relationship": "soft, courteous, and quietly luminous.",
        "thumbnail_strategy": "the blonde waves, violet eyes, blue cross clip, broad white hat, and blue feather must remain readable.",
        "interaction_rule": "Preserve the hat when compatible with the composition; if the crop excludes it, never replace it with unrelated headwear. Staff and exact clothing are optional.",
        "color_anchor": "warm blonde, white, clear blue, violet, soft gold",
    },
    "西格莉卡": {
        "official_core": "extremely voluminous vivid-orange hair divided into several coherent segmented bubble-braid tails, bright green eyes, and a white hood-like headpiece with angular ornaments.",
        "identity_tokens": ["extremely voluminous vivid-orange hair", "several segmented bubble-braid tails", "bright green eyes", "white hood-like headpiece", "angular head ornaments"],
        "viewer_relationship": "sunny, adventurous, and full of momentum.",
        "thumbnail_strategy": "the orange multi-tail bubble-braid silhouette, green eyes, and white headpiece must remain unmistakable.",
        "interaction_rule": "Keep the segmented tails coherent and separate; never simplify them into one ponytail. Forest companions, oversized props, and exact clothing are optional.",
        "color_anchor": "vivid orange, leaf green, clean white, dark brown",
    },
    "达妮娅": {
        "official_core": "very long pastel-pink hair fading to pale blue-lavender with curled ribbon-like ends, a side braid and curled side knot, pale blue-violet eyes, a blue gem with a white wing-like ornament, and black lace-like head trim.",
        "identity_tokens": ["very long pastel-pink hair", "pale blue-lavender gradient ends", "curled ribbon-like hair ends", "side braid and curled side knot", "pale blue-violet eyes", "blue gem with white wing ornament", "black lace-like head trim"],
        "viewer_relationship": "gentle, theatrical, and warmly expressive.",
        "thumbnail_strategy": "the pink-blue gradient hair, curled silhouette, side knot, blue gem, and black trim must remain clear.",
        "interaction_rule": "Preserve the elaborate hair as one coherent structure. Teddy pendants, weapons, stage props, and exact clothing are optional reference styling.",
        "color_anchor": "pastel pink, pale blue, lavender, black, pearl white",
    },
    "长离": {
        "official_core": "a layered coral-pink short crown and sweeping fringe over one extremely long pearl-white rear ponytail, two slim white braided face locks, warm amber-gold eyes, and dark bronze flower-shaped hair ornaments linked by fine loops.",
        "identity_tokens": ["layered coral-pink short crown hair", "sweeping coral-pink fringe", "one extremely long pearl-white rear ponytail", "two slim white braided face locks", "warm amber-gold eyes", "dark bronze flower ornaments with fine loops"],
        "viewer_relationship": "composed, intelligent, and subtly formidable.",
        "thumbnail_strategy": "the coral short crown, long white rear ponytail, paired white braids, amber eyes, and bronze flowers must remain readable.",
        "interaction_rule": "Preserve the two-tone construction and exactly one long white rear ponytail. Flame effects, weapons, and the black-red reference costume are optional.",
        "color_anchor": "pearl white, coral pink, charcoal black, warm gold",
    },
    "诀": {
        "official_core": "silver-white hair with pale mint-cyan underlayers, a rounded jaw-length bob and heavy curved fringe, several extremely long high-back streaming locks, two tall black crown feather tufts with white inner blades, separate broad horizontal white-gray side feather crests, vivid violet-cyan eyes, fine red outer-eye markings, and one vertical red forehead mark.",
        "identity_tokens": ["silver-white hair with pale mint-cyan underlayers", "rounded jaw-length bob and heavy curved fringe", "extremely long high-back streaming locks", "two tall black crown feather tufts with white inner blades", "separate broad horizontal white-gray side feather crests", "vivid violet-cyan eyes", "fine red outer-eye markings", "vertical red forehead mark"],
        "viewer_relationship": "focused and self-possessed, with a direct controlled gaze.",
        "thumbnail_strategy": "the short silver-mint bob, distinct vertical crown feathers, separate horizontal side crests, multitone eyes, and red forehead mark must remain unmistakable.",
        "interaction_rule": "Keep the crown tufts and horizontal side crests as two separate fixed feather structures, never mammal ears, horns, or a hat. Tactical gear, bow, and reference clothing are optional.",
        "color_anchor": "silver white, pale mint cyan, black, violet blue, restrained red",
    },
    "洛茜": {
        "official_core": "thick warm golden-blonde hair with layered bangs and large curled side locks, bright amber-gold eyes, two tall blonde fox ears with pale inner fur, and exactly one enormous fluffy golden fox tail.",
        "identity_tokens": ["thick warm golden-blonde hair", "layered bangs and large curled side locks", "bright amber-gold eyes", "two tall blonde fox ears", "exactly one enormous fluffy golden fox tail"],
        "viewer_relationship": "bright, curious, and energetic, with an alert friendly gaze.",
        "thumbnail_strategy": "the blonde curls, tall fox ears, amber eyes, and single huge tail must stay clear.",
        "interaction_rule": "Keep a human anime face and limbs, exactly two fox ears, and one tail. The red hood, weapons, drawing props, and exact clothing are optional.",
        "color_anchor": "golden blonde, amber, warm cream, restrained red",
    },
    "庄方宜": {
        "official_core": "extremely long deep black-green hair with a straight blunt fringe, vivid teal inner strands and broad red face-framing underlayers, luminous yellow-green eyes with red eyeliner, long pointed ears, paired silver square temple clips, two very large high angular black-crimson branching horns, and one thick dark-teal scaled tail with red fin tips.",
        "identity_tokens": ["extremely long deep black-green hair", "straight blunt fringe", "teal inner strands and broad red face layers", "yellow-green eyes with red eyeliner", "long pointed ears", "paired silver square temple clips", "two very large black-crimson branching horns", "one dark-teal scaled tail with red fin tips"],
        "viewer_relationship": "calm, warm, and quietly confident.",
        "thumbnail_strategy": "the black-green hair, red-teal face layers, huge horns, yellow-green eyes, pointed ears, and single scaled tail must remain distinct.",
        "interaction_rule": "Never shrink the horns into clips or replace them with mammal ears. Preserve exactly one continuous tail. Uniform, mechanical sleeves, weapons, and effects are optional.",
        "color_anchor": "forest green, deep teal, crimson red, green gold, soft white",
    },
    "艾尔黛拉": {
        "official_core": "a warm chestnut short layered crown bob with curled cheek locks and one enormous high rear-side ponytail built from a thick loop, a slim braid, and a long wavy length; vivid rose-magenta eyes, two medium gray ridged goat horns curving outward, dark pointed ears, and paired red-blue triangular temple clips.",
        "identity_tokens": ["warm chestnut short layered crown bob", "curled cheek locks", "one enormous high rear-side ponytail with thick loop, slim braid, and long wavy length", "vivid rose-magenta eyes", "two gray ridged outward-curving goat horns", "dark pointed ears", "paired red-blue temple clips"],
        "viewer_relationship": "gentle, upbeat, and approachable, with a soft lively smile.",
        "thumbnail_strategy": "the short crown bob, huge looped side ponytail, rose eyes, gray horns, dark ears, and red-blue clips must remain readable.",
        "interaction_rule": "Keep compact youthful proportions and keep horns, ears, and ponytail as separate structures. Medical styling, white coat, and companion creatures are optional.",
        "color_anchor": "warm chestnut, rose magenta, soft gray, small red and blue accents",
    },
    "佩丽卡": {
        "official_core": "silver-white hair in one enormous very-high fountain ponytail with black-gray outer strands, fine black ahoge arcs, thick separated bangs, and long curled face locks; clear ice-blue eyes and two large sharp horizontal gray-white feather crests with dark outer tips.",
        "identity_tokens": ["enormous very-high silver-white fountain ponytail", "black-gray outer strands and fine black ahoge arcs", "thick separated bangs", "long curled face locks", "clear ice-blue eyes", "two large horizontal gray-white feather crests with dark tips"],
        "viewer_relationship": "intelligent, attentive, and quietly friendly.",
        "thumbnail_strategy": "the towering ponytail, ice-blue eyes, curled side locks, and large dark-tipped horizontal feather crests must stay stable.",
        "interaction_rule": "The side crests are fixed feather structures, never small clips, cat ears, or loose hair. Technical clothing, gloves, tools, and machinery are optional.",
        "color_anchor": "silver white, ice blue, soft gray, small yellow accents",
    },
    "陈千语": {
        "official_core": "short tousled black crown hair with two very long high-back twin tails, warm red-orange eyes, two narrow black dragon horns edged in red and teal, and exactly one long dark dragon tail ending in a red-teal fin tip.",
        "identity_tokens": ["short tousled black crown hair", "two very long high-back black twin tails", "warm red-orange eyes", "two narrow black dragon horns edged red and teal", "exactly one long dark dragon tail with red-teal fin tip"],
        "viewer_relationship": "open, cheerful, and energetic, with a bright confident smile.",
        "thumbnail_strategy": "the short black crown, long twin tails, colored horns, red-orange eyes, and single tail must remain visible.",
        "interaction_rule": "Keep compact youthful proportions, exactly two horns, and one continuous tail. Uniform, sword, pistol, and combat equipment are optional.",
        "color_anchor": "black, deep blue, red orange, teal, clean white",
    },
    "弭弗": {
        "official_core": "long voluminous pale pink-white wavy hair with curled ends and a heavy side fringe covering one eye, luminous cyan-to-rose multicolored eyes, long pointed ears, and two huge dark navy branching horns with bright cyan edges attached at the temples.",
        "identity_tokens": ["long voluminous pale pink-white wavy hair", "heavy one-eye side fringe", "luminous cyan-to-rose eyes", "long pointed ears", "two huge dark navy branching horns with cyan edges"],
        "viewer_relationship": "bold, amused, and self-assured, with a relaxed direct presence.",
        "thumbnail_strategy": "the pale pink hair mass, one-eye fringe, pointed ears, multitone eyes, and huge cyan-edged horns must dominate the silhouette.",
        "interaction_rule": "Keep both horns attached at the temples and both pointed ears visible; never reduce the horns into clips or detach them as a crown. Combat outfit, gauntlets, cans, and effects are optional.",
        "color_anchor": "pale pink white, dark navy, electric cyan, magenta, small gold accents",
    },
    "茜特菈莉": {
        "official_core": "very long voluminous pastel pink hair fading through pale lavender into cool violet at the lower lengths, thick layered separated bangs, paired slim front braids, clear blue eyes with pink-violet lower iris accents, and two large black circular ring ornaments mounted high at the left and right sides of the head with luminous cyan centers, small gold fittings, and purple-pink ribbon tassels.",
        "identity_tokens": ["very long pastel pink hair", "pale lavender-to-cool-violet lower hair gradient", "thick layered separated bangs", "paired slim front braids", "clear blue eyes with pink-violet lower iris accents", "two large black circular side-ring head ornaments", "luminous cyan ornament centers with gold fittings", "purple-pink ribbon tassels"],
        "viewer_relationship": "youthful, composed, and slightly reserved, with a small thoughtful or faintly pouty expression rather than an exaggerated grin.",
        "thumbnail_strategy": "the pastel pink-to-violet hair mass, paired front braids, blue multitone eyes, and two black cyan-centered ring ornaments must remain immediately readable.",
        "interaction_rule": "Keep compact youthful proportions and preserve the two ring ornaments as symmetrical mechanical head accessories, never animal ears, horns, hair buns, or headphones. Ignore reference-only companions, props, effects, poses, and clothing; the selected photoset alone defines those elements.",
        "color_anchor": "pastel pink, pale lavender, cool violet, luminous cyan, black, small gold accents",
    },
    "桑多涅": {
        "official_core": "soft ash-taupe hair built from a rounded jaw-to-nape curled bob with layered inward-turning cheek locks plus several very long thin trailing curled strands behind it, vivid sapphire-blue eyes, and one large ornate white-and-gold mechanical ruffled headpiece around the crown and rear-right side with a black bow, small crimson details, and long red ribbon streamers.",
        "identity_tokens": ["soft ash-taupe hair", "rounded jaw-to-nape curled bob", "layered inward-turning cheek locks", "very long thin trailing curled rear strands", "vivid sapphire-blue eyes", "large white-and-gold mechanical ruffled headpiece", "black bow and small crimson headpiece details", "long red ribbon streamers"],
        "viewer_relationship": "quietly elegant, observant, and controlled, with a restrained expression and calm direct or slightly averted gaze.",
        "thumbnail_strategy": "the ash-taupe curled bob, sapphire eyes, white-gold mechanical ruffles, black bow, and red streamers must remain distinct from one another.",
        "interaction_rule": "Preserve the short rounded bob and separate trailing curled strands rather than turning all hair into one long hairstyle. The headpiece is mechanical and ruffled, never animal ears or an ordinary soft fabric cap. Ignore reference-only companions, props, effects, poses, and clothing; the selected photoset alone defines those elements.",
        "color_anchor": "ash taupe, sapphire blue, pearl white, antique gold, black, restrained crimson",
    },
    "哥伦比娅": {
        "official_core": "extremely long black hair transitioning into deep violet and muted magenta at the lower lengths, a smooth dark crown with thick straight blunt bangs, one fixed pearl-white translucent geometric blindfold fitted directly across both eyes, and one separate white feathered wing-like halo ornament rising and spreading behind the crown. The blindfold is a slim symmetrical eye-covering seal rather than a cloth band: layered right-angle key-pattern lines and stepped rectangular contours cross both eye sockets, meet over the bridge of the nose, and taper into narrow pointed ends at both temples; the upper edge is partly overlapped by the blunt fringe while both eyes remain fully concealed.",
        "identity_tokens": ["extremely long black hair", "deep violet-to-muted-magenta lower hair gradient", "smooth dark crown", "thick straight blunt bangs", "fixed pearl-white translucent geometric blindfold covering both eyes", "symmetrical stepped right-angle key-pattern linework across the blindfold", "blindfold contours meeting over the nose bridge and tapering at both temples", "white feathered wing-like halo ornament behind the crown"],
        "viewer_relationship": "serene, distant, and dreamlike; because both eyes stay concealed, express her quiet presence through a gentle head angle, relaxed mouth, and restrained facial tension rather than an exposed gaze, theatrical sadness, or a broad smile.",
        "thumbnail_strategy": "the pearl-white geometric blindfold fully covering both eyes, black-to-violet long hair, blunt fringe, and separate white feathered crown halo must remain the dominant recognition points.",
        "interaction_rule": "The blindfold is a fixed canonical identity feature and must remain on the face in every outfit and scene. Keep it centered across both eyes, close-fitting and pearl-white with translucent stepped geometric linework; never remove or lift it, expose either eye, reduce it to a single-eye patch, or replace it with a plain fabric strip, sleep mask, glasses, sunglasses, visor, lace veil, painted eyelids, or opaque rectangular bar. Keep the feather structure separate and attached behind the crown as a wing-like halo ornament, not part of the blindfold and not mammal ears, horns, a conventional hat, or wings growing from the back. Ignore reference-only props, effects, pose, and clothing; the selected photoset alone defines those elements.",
        "color_anchor": "black, deep violet, muted magenta, pearl white, translucent frost white",
    },
    "丝柯克": {
        "official_core": "very long silver-white hair with cool ice-blue shadows, layered separated bangs and face-framing locks, one large high rear ponytail that sweeps outward into a broad flowing mass, vivid crimson-red eyes, one angular black-and-cyan crystalline butterfly-fin ornament at the side of the crown, and one continuous dark indigo crystalline right arm with translucent blue-violet facets from the upper arm through the hand.",
        "identity_tokens": ["very long silver-white hair with cool ice-blue shadows", "layered separated bangs and face-framing locks", "one large high flowing rear ponytail", "vivid crimson-red eyes", "angular black-and-cyan crystalline butterfly-fin head ornament", "one continuous dark indigo crystalline right arm", "translucent blue-violet facets through the right hand"],
        "viewer_relationship": "mature, focused, and self-possessed, with an athletic poised presence and a controlled direct or side gaze.",
        "thumbnail_strategy": "the silver high-ponytail silhouette, crimson eyes, cyan-edged black head crystal, and asymmetrical indigo right arm must remain clearly readable whenever included by the crop.",
        "interaction_rule": "Keep exactly one high rear ponytail and exactly one crystalline right arm; the left arm remains ordinary. The right-arm crystal anatomy is continuous and body-fitted, never a second arm, loose sleeve, oversized weapon, or duplicated gauntlet. Swords, floating shards, combat effects, and the white-blue reference battle dress are optional and must not replace the selected photoset outfit or scene.",
        "color_anchor": "silver white, ice blue, dark indigo, electric cyan, vivid crimson",
    },
    "希希芙": {
        "official_core": "golden-blonde hair with warm peach-brown lower lengths; one long high side-back ponytail; thick curved bangs with a long central point; outward-curled cheek locks and a curved crown ahoge; a narrow temple braid; red eyes with pale cyan iris accents; small pointed fangs; dark loop-shaped forehead hair clip; white pompom and dark ribbon at the ponytail base; small silver ear ornaments; balanced feminine human proportions.",
        "identity_tokens": ["golden-blonde hair with warm peach-brown lower lengths", "one long high side-back ponytail", "thick curved bangs with a long central point", "outward-curled cheek locks and a curved crown ahoge", "a narrow temple braid", "red eyes with pale cyan iris accents", "small pointed fangs", "dark loop-shaped forehead hair clip", "white pompom and dark ribbon at the ponytail base", "small silver ear ornaments", "balanced feminine human proportions"],
        "viewer_relationship": "Playful and alert, with a restrained mischievous smile rather than a permanently open mouth.",
        "thumbnail_strategy": "Keep the blonde curved fringe, long ponytail, loop clip, pompom, red-cyan eyes and small fangs readable.",
        "interaction_rule": "Keep a human face, human ears and human limbs. The white snake with its own head and green bow is a separate companion, not her tail, hair, neck anatomy or mandatory accessory. The larger white police-marked curved equipment is not a biological tail. Do not add snake limbs, scales or a tail to her body. The spear, police clothing, cuffs, collar and pose are reference-only styling.",
        "color_anchor": "golden blonde, peach brown, red, pale cyan, dark navy, white",
    },
    "德蕾琪娜·挽昼": {
        "official_core": "compact human proportions and a soft rounded face; silver-white jaw-length rounded bob with cool blue shadows; heavy sweeping fringe covering her left eye; visible right eye in amber gold with a lime-green lower iris; two short low outward-fanning hair tufts secured by gold rings; small split crown ahoge; paired dark faceted triangular hair ornaments with black-and-gold hanging tabs; small dark-blue rear hair accents.",
        "identity_tokens": ["compact human proportions and a soft rounded face", "silver-white jaw-length rounded bob with cool blue shadows", "heavy sweeping fringe covering her left eye", "visible right eye in amber gold with a lime-green lower iris", "two short low outward-fanning hair tufts secured by gold rings", "small split crown ahoge", "paired dark faceted triangular hair ornaments with black-and-gold hanging tabs", "small dark-blue rear hair accents"],
        "viewer_relationship": "Quiet and gently attentive; convey expression through the visible eye and a small relaxed mouth.",
        "thumbnail_strategy": "The one-eye fringe, gold-green visible eye, short ring-bound tufts and faceted dark clips define the silhouette.",
        "interaction_rule": "Keep the left eye concealed by hair rather than an eyepatch. The pointed dark pieces are attached head ornaments, not animal ears or horns. Keep both low tufts short; never lengthen them into braids or long twin tails. The blue flower dress, metal chest plate and arm gear are clothing, not permanent anatomy. The four-panel reference shows the same person repeatedly; generate one person and one scene.",
        "color_anchor": "silver white, cool blue, amber gold, lime green, charcoal, dark blue",
    },
    "奥古斯塔": {
        "official_core": "tall mature feminine proportions with long limbs; very long voluminous orange-red hair with golden-orange inner locks; layered sweeping bangs and curled face-framing strands; red-orange eyes; large gold sunburst crown with radiating pointed rays; paired gold sun-shaped drop earrings.",
        "identity_tokens": ["tall mature feminine proportions with long limbs", "very long voluminous orange-red hair with golden-orange inner locks", "layered sweeping bangs and curled face-framing strands", "red-orange eyes", "large gold sunburst crown with radiating pointed rays", "paired gold sun-shaped drop earrings"],
        "viewer_relationship": "Dignified, resolute and composed, with a steady gaze.",
        "thumbnail_strategy": "The radiant crown, orange-red flowing hair and sun earrings should remain distinct from background effects.",
        "interaction_rule": "Keep the crown worn on the head, not a giant background halo. Maintain human ears and limbs; the enormous winged creature behind her belongs to the background and must not become her wings, horns or tail. Sword, gold armor, white drapery and orange cape are removable reference styling.",
        "color_anchor": "orange red, golden orange, warm gold",
    },
    "清宵": {
        "official_core": "slender elongated human silhouette; very long flowing light-blue hair with brighter icy-cyan lower locks; layered swept bangs and outward-curved cheek locks; blue eyes with pale warm inner iris accents; paired pale-cyan upward-curving flame-shaped crown structures with spiral linework; long jade-turquoise drop earrings.",
        "identity_tokens": ["slender elongated human silhouette", "very long flowing light-blue hair with brighter icy-cyan lower locks", "layered swept bangs and outward-curved cheek locks", "blue eyes with pale warm inner iris accents", "paired pale-cyan upward-curving flame-shaped crown structures with spiral linework", "long jade-turquoise drop earrings"],
        "viewer_relationship": "Calm, focused and composed, with relaxed lips and a precise gaze.",
        "thumbnail_strategy": "Keep the paired spiral crown shapes, airy blue hair layers and jade earrings clearly separated.",
        "interaction_rule": "Preserve the exact paired pale-cyan crown shapes shown in the references without substituting generic antlers, furry ears or a conventional hat. Their biological origin is not established by these images; do not invent extra nonhuman anatomy. Long flowing hair remains distinct from the mint energy ribbon, sword and white-blue garment streamers. The faded side portrait is another depiction of the same character, not a second subject.",
        "color_anchor": "light blue, icy cyan, jade turquoise, pale gold",
    },
    "折枝": {
        "official_core": "slim softly rounded human silhouette; dark brown-black rounded crown hair with separated curved bangs; two long high side ponytails with flowing dark teal lower strands and pink tips; paired white hair bows; thin round metal-frame glasses; turquoise eyes with pink iris accents; turquoise angular dangling earrings.",
        "identity_tokens": ["slim softly rounded human silhouette", "dark brown-black rounded crown hair with separated curved bangs", "two long high side ponytails with flowing dark teal lower strands and pink tips", "paired white hair bows", "thin round metal-frame glasses", "turquoise eyes with pink iris accents", "turquoise angular dangling earrings"],
        "viewer_relationship": "Reserved and gently attentive, with a small hesitant smile and a soft gaze.",
        "thumbnail_strategy": "Round glasses, short rounded front hair, paired white bows and long teal-pink tails must remain readable.",
        "interaction_rule": "Keep the glasses on the face with clear lenses. Keep exactly two hair ponytails; the huge white brush tuft and painted crane are props or scene elements, never an animal tail or body wings. The flowering branch, paintbrush, scrolls, embroidered dress and hosiery do not define permanent anatomy.",
        "color_anchor": "dark brown black, dark teal, soft pink, turquoise, white",
    },
    "漂泊者": {
        "official_core": "female human silhouette with balanced athletic proportions; black jaw-to-nape crown layers with pointed cheek locks; separated slanting bangs and a small forked crown ahoge; amber-gold eyes; slim gold side hair clips; small gold triangular earrings; a narrow tied dark rear hair section below the short crown.",
        "identity_tokens": ["female human silhouette with balanced athletic proportions", "black jaw-to-nape crown layers with pointed cheek locks", "separated slanting bangs and a small forked crown ahoge", "amber-gold eyes", "slim gold side hair clips", "small gold triangular earrings", "a narrow tied dark rear hair section below the short crown"],
        "viewer_relationship": "Alert, calm and quietly confident, with a natural small smile when appropriate.",
        "thumbnail_strategy": "The short dark face-framing layers, amber eyes and gold hair/ear details carry recognition across reference outfits.",
        "interaction_rule": "Use the isolated black-outfit full-body character reference for the long narrow rear hair section and complete silhouette; the anniversary portraits clarify the face and short crown layers. Keep one coherent haircut rather than merging multiple hair lengths or creating extra ponytails. Preserve the female character shown in all three images. The star-shaped clip embellishment, jacket, white dress, black combat outfit, sword and long costume ribbons are reference styling; do not copy clothing or mistake ribbons for extra hair tails.",
        "color_anchor": "black, amber gold, muted silver gray",
    },
    "弗洛洛": {
        "official_core": "slender mature human proportions; pale gray-green hair with pale pink accent strands; dense angled fringe crossing part of one eye; short inward-curved cheek locks; two long low segmented bubble tails secured by small metallic bands; pale rose-red eyes.",
        "identity_tokens": ["slender mature human proportions", "pale gray-green hair with pale pink accent strands", "dense angled fringe crossing part of one eye", "short inward-curved cheek locks", "two long low segmented bubble tails secured by small metallic bands", "pale rose-red eyes"],
        "viewer_relationship": "Cool and self-possessed, with a restrained knowing expression.",
        "thumbnail_strategy": "The sage-gray fringe, rose eyes and two large softly segmented hair tails must remain distinct.",
        "interaction_rule": "The rounded segments are bound hair, not ordinary plaited braids, ribbons or extra limbs. Keep exactly two low tails with separate banded sections and tapered loose ends. The red spider-lily flower is hand-held, not a fixed hair ornament. Red gloves, neck ruff, belts, dress, organ pipes and shattered mirrors are removable styling or scenery. The enlarged background face depicts the same person; do not add a second person.",
        "color_anchor": "pale gray green, pale pink, rose red",
    },
    "林德薇恩": {
        "official_core": "long silver-white hair flowing loosely behind the shoulders; layered sweeping bangs and curved cheek locks; one looped crown ahoge; heterochromia: her right eye amber gold and her left eye sapphire blue; paired tall black segmented horn-shaped head structures with red diamond insets; soft mature feminine face and balanced human torso proportions.",
        "identity_tokens": ["long silver-white hair flowing loosely behind the shoulders", "layered sweeping bangs and curved cheek locks", "one looped crown ahoge", "heterochromia: her right eye amber gold and her left eye sapphire blue", "paired tall black segmented horn-shaped head structures with red diamond insets", "soft mature feminine face and balanced human torso proportions"],
        "viewer_relationship": "Warmly composed, with a subtle confident smile and relaxed eyes.",
        "thumbnail_strategy": "Retain the gold-right/blue-left eyes, pale loose hair and two red-inset black crown structures.",
        "interaction_rule": "In a frontal view the gold eye is on the viewer left and the blue eye on the viewer right; never swap or equalize their colors. Preserve the two black angular structures exactly as shown, separate from hair; do not add another pair of horns or animal ears. Their ornament-versus-biological origin is not established by these references. Neither image shows the complete lower body, so do not invent a tail or special leg anatomy. Purple armor, dark collar and red flower brooches are clothing details rather than mandatory body features.",
        "color_anchor": "silver white, amber gold, sapphire blue, black, ruby red",
    },
    "穗穗": {
        "official_core": "slender mature human proportions; pale cream-blonde hair with golden-yellow lower accents; rounded brow-length bangs with a narrow central split; two curled cheek-length face locks; one very long high rear ponytail with broad curling ends; golden eyes with rose-red accents; blue-and-gold feather-shaped ornament at the ponytail base; fine red cords and pearl-like beads on the hair ornament; small turquoise drop earrings.",
        "identity_tokens": ["slender mature human proportions", "pale cream-blonde hair with golden-yellow lower accents", "rounded brow-length bangs with a narrow central split", "two curled cheek-length face locks", "one very long high rear ponytail with broad curling ends", "golden eyes with rose-red accents", "blue-and-gold feather-shaped ornament at the ponytail base", "fine red cords and pearl-like beads on the hair ornament", "small turquoise drop earrings"],
        "viewer_relationship": "Bright and graceful, with a poised open gaze and a light natural smile.",
        "thumbnail_strategy": "Preserve the blonde curled front locks, single long high ponytail, gold-rose eyes and blue-gold hair ornament.",
        "interaction_rule": "Keep one ponytail rooted high behind the head, separate from the curled front locks. Blue and gold decorative streamers belong to the headpiece or clothing, not additional ponytails or body feathers. The small bird, surrounding giant phoenix imagery, folding fan and dress are optional scene or costume elements; never attach bird wings or a feather tail to her body.",
        "color_anchor": "cream blonde, golden yellow, rose gold, turquoise, blue",
    },
    "Saber": {
        "official_core": "golden-blonde hair gathered into a braided rear bun; layered parted bangs and long cheek-framing locks; one tall curved ahoge; deep blue bow behind the bun; clear green eyes; slender athletic human proportions with a compact face.",
        "identity_tokens": ["golden-blonde hair gathered into a braided rear bun", "layered parted bangs and long cheek-framing locks", "one tall curved ahoge", "deep blue bow behind the bun", "clear green eyes", "slender athletic human proportions with a compact face"],
        "viewer_relationship": "Steady green-eyed attention with a restrained confident expression.",
        "thumbnail_strategy": "Keep golden-blonde hair gathered into a braided rear bun, layered parted bangs and long cheek-framing locks, one tall curved ahoge legible at thumbnail scale.",
        "interaction_rule": "Keep the braided bun and single ahoge; the sword, armor and blue dress are changeable equipment and clothing, not identity anatomy.",
        "color_anchor": "golden blonde, green eyes, deep blue hair bow",
    },
    "阿格莱雅": {
        "official_core": "short golden-blonde wavy bob with large curled cheek locks; softly parted layered bangs; turquoise eyes with yellow-gold inner facets; gold laurel-leaf hair ornaments with small white flowers; elegant oval face and tall slender human proportions.",
        "identity_tokens": ["short golden-blonde wavy bob with large curled cheek locks", "softly parted layered bangs", "turquoise eyes with yellow-gold inner facets", "gold laurel-leaf hair ornaments with small white flowers", "elegant oval face and tall slender human proportions"],
        "viewer_relationship": "Calm measured gaze and a composed mouth.",
        "thumbnail_strategy": "Keep short golden-blonde wavy bob with large curled cheek locks, softly parted layered bangs, turquoise eyes with yellow-gold inner facets legible at thumbnail scale.",
        "interaction_rule": "Keep the short waved bob and laurel ornaments. The headless golden mannequins and their many hands are separate constructs; never give her extra arms or a mannequin body.",
        "color_anchor": "warm blonde, turquoise irises, small gold and white hair ornaments",
    },
    "火花": {
        "official_core": "pale silver-lavender hair in two extremely long high twin tails; narrow braided strands woven alongside the twin tails; straight bangs with short curved face locks; small red accent strands among the pale hair; bright pink-red eyes; small red heart beneath each eye; black-and-white rabbit-shaped hair ornaments; compact human proportions.",
        "identity_tokens": ["pale silver-lavender hair in two extremely long high twin tails", "narrow braided strands woven alongside the twin tails", "straight bangs with short curved face locks", "small red accent strands among the pale hair", "bright pink-red eyes", "small red heart beneath each eye", "black-and-white rabbit-shaped hair ornaments", "compact human proportions"],
        "viewer_relationship": "Lively playful gaze with an alert small smile.",
        "thumbnail_strategy": "Keep pale silver-lavender hair in two extremely long high twin tails, narrow braided strands woven alongside the twin tails, straight bangs with short curved face locks legible at thumbnail scale.",
        "interaction_rule": "Preserve the pale twin tails, braids and cheek hearts. The rabbit shapes are head accessories and screen graphics, not biological ears. Do not substitute the dark-haired fox-mask design of Sparkle.",
        "color_anchor": "silver lavender, pink-red eyes, red cheek hearts",
    },
    "花火": {
        "official_core": "dark brown-black hair in two long high twin tails with red inner lengths; blunt straight bangs and short side locks; pink-magenta eyes with floral inner highlights; one small red dot below each eye; red pointed ribbon ties; red-and-white fox mask tilted at the side of the head; small red floral upper-chest mark when that area is visible; compact human proportions.",
        "identity_tokens": ["dark brown-black hair in two long high twin tails with red inner lengths", "blunt straight bangs and short side locks", "pink-magenta eyes with floral inner highlights", "one small red dot below each eye", "red pointed ribbon ties", "red-and-white fox mask tilted at the side of the head", "small red floral upper-chest mark when that area is visible", "compact human proportions"],
        "viewer_relationship": "Mischievous eyes and a light knowing smile.",
        "thumbnail_strategy": "Keep dark brown-black hair in two long high twin tails with red inner lengths, blunt straight bangs and short side locks, pink-magenta eyes with floral inner highlights legible at thumbnail scale.",
        "interaction_rule": "Keep the tilted fox mask as a fixed head accessory without covering the face. Do not turn it into real fox ears or borrow white hair and rabbit ornaments from the separate pale-haired form.",
        "color_anchor": "black and red hair, magenta eyes, red-white mask",
    },
    "青雀": {
        "official_core": "light ash-brown hair with short layered crown and swept pointed bangs; two low tied rear tails with teal bows and pale fluffy ornaments; small teal double-loop temple clip; bright lime-green eyes; small soft face and short compact human proportions.",
        "identity_tokens": ["light ash-brown hair with short layered crown and swept pointed bangs", "two low tied rear tails with teal bows and pale fluffy ornaments", "small teal double-loop temple clip", "bright lime-green eyes", "small soft face and short compact human proportions"],
        "viewer_relationship": "Relaxed amused green-eyed attention.",
        "thumbnail_strategy": "Keep light ash-brown hair with short layered crown and swept pointed bangs, two low tied rear tails with teal bows and pale fluffy ornaments, small teal double-loop temple clip legible at thumbnail scale.",
        "interaction_rule": "Keep the low tied hair and teal loop clip. Game tiles, scrolls and the sleeping duplicate vignette are props or background, not additional subjects.",
        "color_anchor": "ash brown, lime eyes, teal hair ties",
    },
    "昔涟": {
        "official_core": "very long flowing rose-pink hair with cyan-blue lowest tips; rounded layered fringe and outward-curving cheek locks; iridescent violet-pink-blue eyes with flower-like highlights; pale blue-white rose hair ornament; tall iridescent ribbon-like pointed head ornaments; gold loop-and-drop earrings with violet centers; soft oval face and slender graceful proportions.",
        "identity_tokens": ["very long flowing rose-pink hair with cyan-blue lowest tips", "rounded layered fringe and outward-curving cheek locks", "iridescent violet-pink-blue eyes with flower-like highlights", "pale blue-white rose hair ornament", "tall iridescent ribbon-like pointed head ornaments", "gold loop-and-drop earrings with violet centers", "soft oval face and slender graceful proportions"],
        "viewer_relationship": "Warm open gaze with a gentle cheerful expression.",
        "thumbnail_strategy": "Keep very long flowing rose-pink hair with cyan-blue lowest tips, rounded layered fringe and outward-curving cheek locks, iridescent violet-pink-blue eyes with flower-like highlights legible at thumbnail scale.",
        "interaction_rule": "Keep the rose, iridescent head ornaments and pink-to-blue hair lengths. Large luminous petals, shoulder ribbons and surrounding wing-shaped effects must not become extra body wings or tails.",
        "color_anchor": "rose pink, cool blue tips, iridescent violet eyes",
    },
    "大丽花": {
        "official_core": "very long dark brown-black hair with fine gold highlights and blue inner lengths; heavy angled fringe partially veiling one eye; violet eyes and a small violet beauty mark below her left eye; paired black-and-gold curled temple ornaments; large white wide-brim hat with dark flowers and blue plume accents; mature narrow oval face and tall slender human proportions.",
        "identity_tokens": ["very long dark brown-black hair with fine gold highlights and blue inner lengths", "heavy angled fringe partially veiling one eye", "violet eyes and a small violet beauty mark below her left eye", "paired black-and-gold curled temple ornaments", "large white wide-brim hat with dark flowers and blue plume accents", "mature narrow oval face and tall slender human proportions"],
        "viewer_relationship": "Cool half-lidded violet gaze and a subtle composed smile.",
        "thumbnail_strategy": "Keep very long dark brown-black hair with fine gold highlights and blue inner lengths, heavy angled fringe partially veiling one eye, violet eyes and a small violet beauty mark below her left eye legible at thumbnail scale.",
        "interaction_rule": "Retain her character-specific white hat and curled temple fittings. The gold claw glove, whip, blue flames and ravens are removable equipment or effects, not fingers, horns, wings or a tail.",
        "color_anchor": "dark hair with blue accents, violet eyes, white character hat",
    },
    "大黑塔": {
        "official_core": "extremely long ash-taupe hair fading to lavender at the ends; layered side bangs and curled cheek locks; violet eyes; oversized dark-purple pointed witch hat with a broad brim and violet flower; mature slender human body with long limbs and ordinary human joints.",
        "identity_tokens": ["extremely long ash-taupe hair fading to lavender at the ends", "layered side bangs and curled cheek locks", "violet eyes", "oversized dark-purple pointed witch hat with a broad brim and violet flower", "mature slender human body with long limbs and ordinary human joints"],
        "viewer_relationship": "Self-assured thoughtful gaze with slightly narrowed eyes.",
        "thumbnail_strategy": "Keep extremely long ash-taupe hair fading to lavender at the ends, layered side bangs and curled cheek locks, violet eyes legible at thumbnail scale.",
        "interaction_rule": "Preserve the pointed broad-brim witch hat as her fixed character accessory. Do not replace this adult human form with a jointed doll; books, staff, cat figure and portal hands are separate props.",
        "color_anchor": "ash taupe and lavender hair, violet eyes, dark purple hat",
    },
    "知更鸟·晴歌": {
        "official_core": "very long periwinkle-lavender hair with one thick low side braid over her right shoulder; large purple bow securing the side braid; sweeping bangs and soft curled face locks; aqua-green eyes; white star-shaped temple clip; tilted separate gold halo with star ornaments; small white feathered wings behind the ears; slender balanced feminine proportions.",
        "identity_tokens": ["very long periwinkle-lavender hair with one thick low side braid over her right shoulder", "large purple bow securing the side braid", "sweeping bangs and soft curled face locks", "aqua-green eyes", "white star-shaped temple clip", "tilted separate gold halo with star ornaments", "small white feathered wings behind the ears", "slender balanced feminine proportions"],
        "viewer_relationship": "Bright engaging gaze and an easy singing smile.",
        "thumbnail_strategy": "Keep very long periwinkle-lavender hair with one thick low side braid over her right shoulder, large purple bow securing the side braid, sweeping bangs and soft curled face locks legible at thumbnail scale.",
        "interaction_rule": "Use the sunny side-braid form only. Keep the small ear wings at the sides of the head and the separate star halo, never large back wings. Guitar, microphone, sunflower and bird float are props.",
        "color_anchor": "periwinkle braid, aqua eyes, gold star halo",
    },
    "知更鸟": {
        "official_core": "long loose periwinkle-lavender hair with sweeping fringe and curled front locks; aqua-green iridescent eyes; small colored dot accents beneath the outer left eye; tilted separate thin golden halo with pale hanging flower-like ornaments; small white-lavender feathered wings behind the ears; delicate star-shaped drop earrings; slender graceful human-shaped body.",
        "identity_tokens": ["long loose periwinkle-lavender hair with sweeping fringe and curled front locks", "aqua-green iridescent eyes", "small colored dot accents beneath the outer left eye", "tilted separate thin golden halo with pale hanging flower-like ornaments", "small white-lavender feathered wings behind the ears", "delicate star-shaped drop earrings", "slender graceful human-shaped body"],
        "viewer_relationship": "Gentle attentive eyes and a soft poised smile.",
        "thumbnail_strategy": "Keep long loose periwinkle-lavender hair with sweeping fringe and curled front locks, aqua-green iridescent eyes, small colored dot accents beneath the outer left eye legible at thumbnail scale.",
        "interaction_rule": "Preserve the loose-hair form and small ear wings, without importing the sunny version's thick side braid or star clip. The makeup artists' hands, gramophone, cage and birds are separate scene elements.",
        "color_anchor": "periwinkle, aqua green, small gold halo",
    },
    "停云": {
        "official_core": "chestnut-brown hair with swept bangs and gathered rear lengths; green-gold eyes; exactly two tall brown fox ears with pale inner fur; one large fluffy brown fox tail rooted behind the hips; gold hair fittings with red accents; slender feminine torso and ordinary human arms and legs.",
        "identity_tokens": ["chestnut-brown hair with swept bangs and gathered rear lengths", "green-gold eyes", "exactly two tall brown fox ears with pale inner fur", "one large fluffy brown fox tail rooted behind the hips", "gold hair fittings with red accents", "slender feminine torso and ordinary human arms and legs"],
        "viewer_relationship": "Warm composed gaze with a knowing small smile.",
        "thumbnail_strategy": "Keep chestnut-brown hair with swept bangs and gathered rear lengths, green-gold eyes, exactly two tall brown fox ears with pale inner fur legible at thumbnail scale.",
        "interaction_rule": "Use the single brown-tail form. The two small white foxes are separate companions, never additional tails. Do not import the many pale tails of Fugue.",
        "color_anchor": "chestnut brown, green gold, red and gold hair accents",
    },
    "忘归人": {
        "official_core": "very long dark chestnut hair with reddish lower lengths; layered swept bangs and long face-framing locks; green-gold eyes; two tall fox ears with pale interiors; gold floral hair ornaments and red tassels; a fan of multiple large pale pink-white fluffy fox tails rooted behind the hips; slender feminine human-shaped torso and limbs.",
        "identity_tokens": ["very long dark chestnut hair with reddish lower lengths", "layered swept bangs and long face-framing locks", "green-gold eyes", "two tall fox ears with pale interiors", "gold floral hair ornaments and red tassels", "a fan of multiple large pale pink-white fluffy fox tails rooted behind the hips", "slender feminine human-shaped torso and limbs"],
        "viewer_relationship": "Quiet focused gaze and a restrained expression.",
        "thumbnail_strategy": "Keep very long dark chestnut hair with reddish lower lengths, layered swept bangs and long face-framing locks, green-gold eyes legible at thumbnail scale.",
        "interaction_rule": "Use the pale multi-tail form, keeping the tail fan separate from her long brown hair. The background portrait is not another person to generate. Do not reduce the tails to the original single brown tail.",
        "color_anchor": "dark chestnut hair, green-gold eyes, pale pink-white tails",
    },
    "符玄": {
        "official_core": "pink hair with a short layered crown and two very long low tails; outward-pointing short side tufts; ornate pink-and-gold crown with looped raised sections and side tassels; central violet forehead gem; golden-pink eyes with fine concentric iris detail; round gold earrings with pale purple-white pendants; short compact stature and a soft small face.",
        "identity_tokens": ["pink hair with a short layered crown and two very long low tails", "outward-pointing short side tufts", "ornate pink-and-gold crown with looped raised sections and side tassels", "central violet forehead gem", "golden-pink eyes with fine concentric iris detail", "round gold earrings with pale purple-white pendants", "short compact stature and a soft small face"],
        "viewer_relationship": "Direct slightly stern gaze with a composed mouth.",
        "thumbnail_strategy": "Keep pink hair with a short layered crown and two very long low tails, outward-pointing short side tufts, ornate pink-and-gold crown with looped raised sections and side tassels legible at thumbnail scale.",
        "interaction_rule": "Keep the two low tails, ornamental crown and single forehead jewel. The jewel is not an extra eyeball; cosmic spheres, scrolls and floating disks are external objects.",
        "color_anchor": "pink hair, violet forehead jewel, warm gold eyes",
    },
    "流萤": {
        "official_core": "long loose silvery-ash hair with pale aqua lower tips; layered bangs crossing the center and curved cheek locks; iridescent eyes graduating from deep blue above to pink below; dark headband with angular gold-edged pale-green detailing; pale green leaf-shaped side hair ornament with a black bow; slim balanced human proportions.",
        "identity_tokens": ["long loose silvery-ash hair with pale aqua lower tips", "layered bangs crossing the center and curved cheek locks", "iridescent eyes graduating from deep blue above to pink below", "dark headband with angular gold-edged pale-green detailing", "pale green leaf-shaped side hair ornament with a black bow", "slim balanced human proportions"],
        "viewer_relationship": "Soft attentive eyes and a small sincere smile.",
        "thumbnail_strategy": "Keep long loose silvery-ash hair with pale aqua lower tips, layered bangs crossing the center and curved cheek locks, iridescent eyes graduating from deep blue above to pink below legible at thumbnail scale.",
        "interaction_rule": "Keep the human girl with loose silver-to-aqua hair. The large armored figure behind her is a separate suit depiction; do not turn her exposed limbs into machinery or add energy wings as anatomy.",
        "color_anchor": "silvery ash, pale aqua, blue-pink eyes",
    },
    "爻光": {
        "official_core": "long silver-blue hair with swept layered bangs and outward-curving temple locks; fine side braid with a small gold bead; iridescent violet-pink eyes with cyan and gold facets; blue-teal peacock-feather head ornament; slender human body with long legs.",
        "identity_tokens": ["long silver-blue hair with swept layered bangs and outward-curving temple locks", "fine side braid with a small gold bead", "iridescent violet-pink eyes with cyan and gold facets", "blue-teal peacock-feather head ornament", "slender human body with long legs"],
        "viewer_relationship": "Confident relaxed eyes and a small welcoming smile.",
        "thumbnail_strategy": "Keep long silver-blue hair with swept layered bangs and outward-curving temple locks, fine side braid with a small gold bead, iridescent violet-pink eyes with cyan and gold facets legible at thumbnail scale.",
        "interaction_rule": "Preserve the feather ornament on the head and silver hair geometry. Peacock-shaped background arcs, garment feather panels, dark shoulder trim and fire are not biological wings, hair or a tail.",
        "color_anchor": "silver blue hair, iridescent violet eyes, blue-teal head plume",
    },
    "遐蝶": {
        "official_core": "silver-lavender hair with deeper purple lower lengths; long sweeping bangs and outward-curving cheek locks; two long low tied sections with braided portions and small bows; bright violet-pink eyes; pointed ears; dark thorn-like crown adorned with small pale pink and violet flowers; small dark diamond ornaments along the front hairline; delicate slender proportions.",
        "identity_tokens": ["silver-lavender hair with deeper purple lower lengths", "long sweeping bangs and outward-curving cheek locks", "two long low tied sections with braided portions and small bows", "bright violet-pink eyes", "pointed ears", "dark thorn-like crown adorned with small pale pink and violet flowers", "small dark diamond ornaments along the front hairline", "delicate slender proportions"],
        "viewer_relationship": "Quiet contemplative gaze with gently parted lips.",
        "thumbnail_strategy": "Keep silver-lavender hair with deeper purple lower lengths, long sweeping bangs and outward-curving cheek locks, two long low tied sections with braided portions and small bows legible at thumbnail scale.",
        "interaction_rule": "Keep the pointed ears, flowered thorn crown and tied purple-gradient hair. Crown spikes are ornaments, not horns; the enormous dragon and butterflies are separate creatures, not her wings or tail.",
        "color_anchor": "silver lavender, deep purple ends, luminous pink-violet eyes",
    },
    "阮·梅": {
        "official_core": "long dark ash-brown hair with softly waved loose lengths and partially gathered rear sections; layered parted bangs and inward-curving cheek locks; fine teal accents among the dark rear hair; teal-green eyes with yellow inner facets; gold-edged white plum-blossom hair ornament with a pearl center; slender oval face and mature balanced human proportions.",
        "identity_tokens": ["long dark ash-brown hair with softly waved loose lengths and partially gathered rear sections", "layered parted bangs and inward-curving cheek locks", "fine teal accents among the dark rear hair", "teal-green eyes with yellow inner facets", "gold-edged white plum-blossom hair ornament with a pearl center", "slender oval face and mature balanced human proportions"],
        "viewer_relationship": "Calm thoughtful gaze with a subtle gentle smile.",
        "thumbnail_strategy": "Keep long dark ash-brown hair with softly waved loose lengths and partially gathered rear sections, layered parted bangs and inward-curving cheek locks, fine teal accents among the dark rear hair legible at thumbnail scale.",
        "interaction_rule": "Keep the dark waved hair and white plum-blossom hair ornament. Mirror reflections are not a second subject, and the string instrument, pastry, branches and costume pearls need not follow her into a photoset.",
        "color_anchor": "dark ash brown, teal-green eyes, white and gold blossom",
    },
    "卡芙卡": {
        "official_core": "wine-magenta hair with thick separated bangs and two long curved front locks; rear hair gathered into a loose low ponytail with looped side sections; pale pink-lavender eyes; round dark tinted sunglasses resting above the forehead; small pearl drop earrings; mature oval face and tall balanced human proportions.",
        "identity_tokens": ["wine-magenta hair with thick separated bangs and two long curved front locks", "rear hair gathered into a loose low ponytail with looped side sections", "pale pink-lavender eyes", "round dark tinted sunglasses resting above the forehead", "small pearl drop earrings", "mature oval face and tall balanced human proportions"],
        "viewer_relationship": "Relaxed half-lidded gaze and a knowing faint smile.",
        "thumbnail_strategy": "Keep wine-magenta hair with thick separated bangs and two long curved front locks, rear hair gathered into a loose low ponytail with looped side sections, pale pink-lavender eyes legible at thumbnail scale.",
        "interaction_rule": "Preserve the wine-colored low ponytail, front locks and forehead sunglasses without hiding her eyes. Guns, strings, umbrellas, cat and background people are separate props or subjects.",
        "color_anchor": "wine magenta, pale lavender eyes, dark round sunglasses",
    },
    "姬子": {
        "official_core": "very long copper-red hair with broad flowing waves; layered side-parted bangs and curled cheek locks; warm amber-gold eyes; mature oval face and tall long-legged human proportions.",
        "identity_tokens": ["very long copper-red hair with broad flowing waves", "layered side-parted bangs and curled cheek locks", "warm amber-gold eyes", "mature oval face and tall long-legged human proportions"],
        "viewer_relationship": "Warm assured gaze and an open confident smile.",
        "thumbnail_strategy": "Keep very long copper-red hair with broad flowing waves, layered side-parted bangs and curled cheek locks, warm amber-gold eyes legible at thumbnail scale.",
        "interaction_rule": "Keep the red waves and amber eyes across the two depicted outfits; small side hair jewelry follows the chosen character reference. Spears, orbital machinery, mechanical dragon and star trails are equipment or scenery, not anatomical appendages.",
        "color_anchor": "copper red, amber gold, small gold jewelry accents",
    },
    "灵砂": {
        "official_core": "very long dark brown hair with warm brown front layers; straight blunt bangs and long curved side locks; orange-red eyes; small pointed ears; gold hair fittings with red tassels and a small green inset; red coloration on the hands fading along the forearms; slender mature human-shaped body.",
        "identity_tokens": ["very long dark brown hair with warm brown front layers", "straight blunt bangs and long curved side locks", "orange-red eyes", "small pointed ears", "gold hair fittings with red tassels and a small green inset", "red coloration on the hands fading along the forearms", "slender mature human-shaped body"],
        "viewer_relationship": "Composed softly narrowed eyes and a gentle knowing smile.",
        "thumbnail_strategy": "Keep very long dark brown hair with warm brown front layers, straight blunt bangs and long curved side locks, orange-red eyes legible at thumbnail scale.",
        "interaction_rule": "Preserve the pointed ears and visible red hand-to-forearm coloration rather than replacing it with ordinary skin. The incense rabbits, smoke, lantern and staff are separate objects; they do not give her rabbit ears or a tail.",
        "color_anchor": "dark brown hair, orange-red eyes, red hand accents",
    },
    "绯英": {
        "official_core": "pale pink short layered hair flaring outward at the sides; long narrow pink face-framing strands; swept overlapping bangs and a small lifted crown tuft; violet-pink eyes; two long pale pink rabbit-like ear structures above the crown with gold tip ornaments; large red bow behind the crown and a small pale blossom hair clip; compact human-shaped torso and limbs.",
        "identity_tokens": ["pale pink short layered hair flaring outward at the sides", "long narrow pink face-framing strands", "swept overlapping bangs and a small lifted crown tuft", "violet-pink eyes", "two long pale pink rabbit-like ear structures above the crown with gold tip ornaments", "large red bow behind the crown and a small pale blossom hair clip", "compact human-shaped torso and limbs"],
        "viewer_relationship": "Alert amused gaze with a light smile.",
        "thumbnail_strategy": "Keep pale pink short layered hair flaring outward at the sides, long narrow pink face-framing strands, swept overlapping bangs and a small lifted crown tuft legible at thumbnail scale.",
        "interaction_rule": "Preserve exactly the two long reference head structures and their gold tips; do not add another pair of ears on the crown. The huge pink long-eared creature, its tail and the small plush companion are separate from her body.",
        "color_anchor": "pale pink hair, violet-pink eyes, red crown bow",
    },
    "银狼": {
        "official_core": "silver-gray hair with layered sweeping bangs; one high ponytail with loosely curled pale blue-tinted ends; blue-violet tinted goggles resting on the crown; dark pointed ribbon ponytail tie with blue dot pattern; gray-violet eyes; short compact human proportions.",
        "identity_tokens": ["silver-gray hair with layered sweeping bangs", "one high ponytail with loosely curled pale blue-tinted ends", "blue-violet tinted goggles resting on the crown", "dark pointed ribbon ponytail tie with blue dot pattern", "gray-violet eyes", "short compact human proportions"],
        "viewer_relationship": "Cool concentrated eyes with a faint competitive smile.",
        "thumbnail_strategy": "Keep silver-gray hair with layered sweeping bangs, one high ponytail with loosely curled pale blue-tinted ends, blue-violet tinted goggles resting on the crown legible at thumbnail scale.",
        "interaction_rule": "Use the original ponytail and dotted ribbon form. Ribbon tips are not animal ears; chibi game avatars are separate graphic figures. Do not borrow the upgraded form's triple-pronged hair fitting or armored glove as anatomy.",
        "color_anchor": "silver gray, blue-violet goggles, cool pale-blue hair ends",
    },
    "银狼LV.999": {
        "official_core": "very long silver-gray high ponytail with large curled blue-tinted ends; layered swept bangs and short cheek locks; gray-violet eyes; wide connected blue-purple visor goggles; dark circular ponytail fitting with three long cyan-violet prongs; compact athletic human proportions.",
        "identity_tokens": ["very long silver-gray high ponytail with large curled blue-tinted ends", "layered swept bangs and short cheek locks", "gray-violet eyes", "wide connected blue-purple visor goggles", "dark circular ponytail fitting with three long cyan-violet prongs", "compact athletic human proportions"],
        "viewer_relationship": "Sharp engaged gaze and a confident playful grin.",
        "thumbnail_strategy": "Keep very long silver-gray high ponytail with large curled blue-tinted ends, layered swept bangs and short cheek locks, gray-violet eyes legible at thumbnail scale.",
        "interaction_rule": "Use the upgraded long-ponytail form with three-pronged fitting, keeping goggles on the crown when clear eye contact is required. The armored hand device and floating blades are equipment, not permanent synthetic fingers or extra limbs.",
        "color_anchor": "silver gray, cyan-violet fitting, iridescent blue-purple goggles",
    },
    "风堇": {
        "official_core": "pastel pink hair in two voluminous curled side tails with pale blue ends; large spiral forelock and rounded curled cheek locks; bright aqua-green eyes; small burgundy cap with white wing-shaped decoration and gold arched trim; small lilac flower ornaments beside the cap; short compact stature and soft rounded face.",
        "identity_tokens": ["pastel pink hair in two voluminous curled side tails with pale blue ends", "large spiral forelock and rounded curled cheek locks", "bright aqua-green eyes", "small burgundy cap with white wing-shaped decoration and gold arched trim", "small lilac flower ornaments beside the cap", "short compact stature and soft rounded face"],
        "viewer_relationship": "Bright friendly gaze and an animated cheerful smile.",
        "thumbnail_strategy": "Keep pastel pink hair in two voluminous curled side tails with pale blue ends, large spiral forelock and rounded curled cheek locks, bright aqua-green eyes legible at thumbnail scale.",
        "interaction_rule": "Retain the burgundy character cap and curled pink-blue hair. White wing shapes on the cap are ornaments; the enormous winged staff, floating little creature and rainbow are props or companions, not her body wings.",
        "color_anchor": "pastel pink, pale blue curls, aqua eyes, burgundy cap",
    },
}


CHARACTER_PROFILE_VARIANTS = {
    "哥伦比娅": {
        "unmasked": {
            "official_core": "extremely long black hair transitioning into deep violet and muted magenta at the lower lengths, a smooth dark crown with thick straight blunt bangs, fully visible pale lavender-violet half-lidded eyes, and one fixed white feathered wing-like halo ornament rising and spreading behind the crown with small white side fittings near the temples. Her face is unobstructed: both eyes, both upper lash lines, the nose bridge, and the area between the bangs and cheekbones remain visible.",
            "identity_tokens": ["extremely long black hair", "deep violet-to-muted-magenta lower hair gradient", "smooth dark crown", "thick straight blunt bangs", "fully visible pale lavender-violet half-lidded eyes", "unobstructed eye area and nose bridge", "white feathered wing-like halo ornament behind the crown", "small white temple fittings"],
            "viewer_relationship": "serene, distant, and dreamlike, with relaxed half-lidded eyes and a subtle neutral expression rather than theatrical sadness or a broad smile.",
            "thumbnail_strategy": "the fully visible pale lavender eyes, black-to-violet long hair, blunt fringe, and separate white feathered crown halo must remain the dominant recognition points.",
            "interaction_rule": "This is the unmasked version. Keep both pale lavender-violet eyes fully visible and unobstructed in every outfit and scene. Never add the geometric blindfold, an eye patch, cloth band, sleep mask, glasses, sunglasses, visor, lace veil, opaque bar, face seal, or painted markings across the eyes. Keep the feather structure separate and attached behind the crown as a wing-like halo ornament, not mammal ears, horns, a conventional hat, or wings growing from the back. Ignore reference-only companions, props, effects, poses, and clothing; the selected photoset alone defines those elements.",
            "color_anchor": "black, deep violet, muted magenta, pale lavender, feather white",
        },
    },
}

_ACTIVE_CHARACTER_PROFILE_VARIANTS: dict[str, str] = {}


def set_character_profile_variant(character_name: str, variant: str | None) -> None:
    if variant is None:
        _ACTIVE_CHARACTER_PROFILE_VARIANTS.pop(character_name, None)
        return
    available = CHARACTER_PROFILE_VARIANTS.get(character_name, {})
    if variant not in available:
        raise ValueError(f"Unknown profile variant for {character_name}: {variant}")
    _ACTIVE_CHARACTER_PROFILE_VARIANTS[character_name] = variant


def active_character_profile_variant(character_name: str) -> str | None:
    return _ACTIVE_CHARACTER_PROFILE_VARIANTS.get(character_name)


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
        "weight": 0.55,
    },
    {
        "name": "knee_up_medium",
        "description": "knee-up or thigh-up framing, character is the only person and remains clearly readable; face, hair, outfit silhouette, and hands are visible",
        "weight": 1.4,
    },
    {
        "name": "waist_up_half_body",
        "description": "waist-up or half-body framing, face and upper body become the main read while the scene still frames the character",
        "weight": 3.2,
    },
    {
        "name": "bust_close",
        "description": "upper-torso portrait, face, eyes, hair silhouette, shoulders, and main accessories are prominent; keep enough background to preserve the selected scene",
        "weight": 2.3,
    },
    {
        "name": "close_upper_body",
        "description": "close upper-body framing, face and identity details dominate; background appears as layered atmosphere rather than empty space",
        "weight": 1.8,
    },
]


ART_DIRECTION_PLANS = [
    {
        "name": "trend_mirror_studio",
        "graphic_concept": "bright practice-room or mirror-studio key visual; the character feels freshly finished with training, caught by the camera during a natural pause",
        "spatial_structure": "large mirror, pale floor, window light, and a few circular lamp dots; keep the background spacious and uncluttered",
        "visual_device": "mirror reflection and window light make the hair silhouette, face, and main accessory read clearly at thumbnail size",
        "body_silhouette": "close knee-up or seated pose, character relatively large in frame, hands relaxed near the jacket edge, sides, or lap",
        "outfit_direction": "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit",
        "material_language": "soft sweatshirt fabric, small skirt embellishments, polished floor reflection, mirror glass, soft hair shine",
        "color_strategy": "the scene may stay bright and clean, but the outfit should usually carry a distinct non-white mid-tone, dark, earthy, or muted-chromatic main value",
        "lighting_behavior": "bright window light with crisp but soft highlights on skin and hair; no oily or harsh rendering",
        "tags": ["trend_lifestyle", "mirror", "studio", "close_character"],
    },
    {
        "name": "capsule_toy_corner",
        "graphic_concept": "collectible capsule-toy corner; transparent toy balls, pale walls, and small mascot shapes make the character feel like a premium character good",
        "spatial_structure": "transparent capsule balls, light circular wall shapes, and a few tiny toys; the scene stays cute but not crowded",
        "visual_device": "repeating circles echo the eyes and create a strong thumbnail memory point",
        "body_silhouette": "half-body to knee-up framing; a small toy may sit nearby, but hands should not dominate the camera",
        "outfit_direction": "sleeveless top, denim overalls, youthful clean casual style",
        "material_language": "glossy capsule shells, denim overall texture, cotton sleeveless top, tiny charms, candy accents, controlled reflections",
        "color_strategy": "pale background plus small toy accents; keep the outfit visibly separated from the pale setting with a non-white main value",
        "lighting_behavior": "soft high-key light; eyes and hair edges stay sharp",
        "tags": ["trend_lifestyle", "toy", "pastel", "close_character"],
    },
    {
        "name": "graphic_poster_studio",
        "graphic_concept": "clean graphic poster shoot; character colors, simple symbols, and large unreadable letter blocks create an advertising-poster feeling",
        "spatial_structure": "light background, bold color blocks, simple geometry, and a few decorative non-readable letters",
        "visual_device": "large color fields turn the character palette into a clear visual logo",
        "body_silhouette": "seated or kneeling pose, knee-up to full-body range, face and main accessory remain the first read",
        "outfit_direction": "waist-shaped mini dress, lace panels, bell sleeves, boots, idol stagewear",
        "material_language": "clean waist seam, lace panels, bell sleeves, boots, small charms, matte graphic panels",
        "color_strategy": "white or pale graphic base; use a clearly colored or deeper-value outfit so the clothing does not merge into the poster background",
        "lighting_behavior": "clean studio light with minimal shadow",
        "tags": ["trend_lifestyle", "poster", "graphic", "close_character"],
    },
    {
        "name": "balcony_breeze_half_out_frame",
        "graphic_concept": "home balcony breeze scene; curtain, sky, railing, and white interior wall carry the first read, with the character as an emotional note near the edge",
        "spatial_structure": "interior looking toward balcony or balcony looking inward; character half out of frame or placed low to one side; doorframe and curtain create foreground layers",
        "visual_device": "wind-blown curtain, small plant pot, sandals, folded cloth, and reflected floor light create domestic narrative",
        "body_silhouette": "front three-quarter or relaxed side angle near the balcony breeze; hair and accessories move lightly in wind while face stays readable",
        "outfit_direction": "tank top, oversized cropped hoodie, loose jeans, relaxed casual style",
        "material_language": "thin curtain, glass door, metal railing, ceramic pot, polished floor reflection, hoodie cotton and denim",
        "color_strategy": "large bright sky and interior fields; the outfit should usually use a distinct non-white main value for separation",
        "lighting_behavior": "bright exterior light, interior in pale shade, thin rim light on hair and shoulder",
        "tags": ["balcony", "large_space", "half_out_frame", "foreground_occlusion", "breeze", "daily", "novel_cg"],
    },
    {
        "name": "greenhouse_terrace_reflection",
        "graphic_concept": "flower greenhouse terrace with glass reflections; plants, window grids, and pale green light define the image more than the pose",
        "spatial_structure": "layered glasshouse perspective; character behind plants or faintly reflected in glass; foreground leaves partially cover edges without hiding identity essentials",
        "visual_device": "flower bouquet, watering can, small sweets tray, folded ribbon, and sun patches on tile floor build a small daily scene",
        "body_silhouette": "three-quarter front or quiet side glance, medium readable figure inside deep space, not centered",
        "outfit_direction": "lace dress, ribbon waist, airy garden fairy style",
        "material_language": "glass, leaf translucency, ceramic tile, lace, ribbon waist, soft moisture shine",
        "color_strategy": "large pale greenhouse blocks with controlled flower accents; the outfit should retain a visible non-white color presence",
        "lighting_behavior": "diffused greenhouse light with clear window-grid shadows and soft reflective highlights",
        "tags": ["greenhouse", "terrace", "reflection", "foreground_occlusion", "flower", "large_space", "novel_cg"],
    },
    {
        "name": "flower_sea_afternoon",
        "graphic_concept": "afternoon flower field; dreamy but not cluttered, with the character still acting as the main visual subject",
        "spatial_structure": "broad flower field as soft color blocks; only a few blurred foreground flowers",
        "visual_device": "flower color fields frame the character hair color and eyes as the memory point",
        "body_silhouette": "standing, seated, or gentle side-angle facing the flower field; hand may lightly touch a flower branch without covering the face",
        "outfit_direction": "waist-shaped dress, off-shoulder cut, uneven skirt, romantic cottagecore style",
        "material_language": "petals, softly structured fabric, light gauze, uneven skirt hem, hair ornament, moderate detail density",
        "color_strategy": "flower colors support the character palette; avoid filling the image with one high-saturation color",
        "lighting_behavior": "soft afternoon light, clear face, lightly blurred background",
        "tags": ["flower_field", "afternoon", "dream", "nature"],
    },
    {
        "name": "flower_bridal_garden",
        "graphic_concept": "romantic bridal garden illustration; clean, bright, and focused on the character face, hairstyle, and silhouette",
        "spatial_structure": "pale flower arch, veil fabric, bouquet, and grass; background is light and not crowded",
        "visual_device": "veil, bouquet, and flower arch create a soft frame around the character",
        "body_silhouette": "standing or seated three-quarter pose, hands naturally near bouquet or skirt",
        "outfit_direction": "lace bridal gown, high-neck bodice, ruffle sleeves, princess skirt, clean wedding style",
        "material_language": "thin veil, flower bouquet, high-neck lace bodice, layered ruffle sleeves, voluminous skirt",
        "color_strategy": "light bridal-garden colors support the character; non-bridal outfits should not default to white or pale neutrals",
        "lighting_behavior": "soft garden daylight, clear face, clean high-key atmosphere",
        "tags": ["bridal", "garden", "flower", "soft_light"],
    },
    {
        "name": "rooftop_laundry_sunset",
        "graphic_concept": "quiet city rooftop laundry moment; hanging cloth, low railing, distant apartment blocks, and evening wind create a lived-in daily anime CG",
        "spatial_structure": "rooftop floor, laundry line, railing, water tank edge, and distant building silhouettes create layered depth; character placed near one side, not centered",
        "visual_device": "fluttering cloth, clothespins, small basket, railing line, and long rooftop shadow guide attention back to face and hair",
        "body_silhouette": "standing, walking past the laundry line, or lightly turning in the wind; hands simple near basket, sleeve, or railing",
        "outfit_direction": "oversized sweater, loose sleeves, cozy homewear, soft casual style",
        "material_language": "soft knit or pullover fabric, hanging cloth, clothespins, rooftop concrete, railing metal, wind-blown hair",
        "color_strategy": "sunset sky and muted city blocks support the character palette; clothing palette is chosen by the model to harmonize with identity",
        "lighting_behavior": "late sunset side light with long shadows, soft rim light on hair and shoulders, face still readable",
        "tags": ["rooftop", "laundry", "sunset", "breeze", "daily", "large_space", "novel_cg"],
    },
    {
        "name": "beach_wind_open_sand",
        "graphic_concept": "open beach wind scene; shoreline, parasol edge, wave line, and small beach items create a clean summer image without swimsuit focus",
        "spatial_structure": "wide sand plane, wave edge, parasol or towel in foreground, and open horizon; character readable at medium distance with plenty of air",
        "visual_device": "wave foam, sandal marks, small bag, towel edge, and wind on hair form a light summer rhythm",
        "body_silhouette": "walking along wet sand, pausing near a parasol, or turning in sea breeze; hands simple, posture natural",
        "outfit_direction": "striped swim top under loose cover shirt, clean beach resort style",
        "material_language": "loose cover shirt, subtle striped swim top, sand, wave foam, parasol fabric, small beach bag",
        "color_strategy": "sea and sky support the character palette; outfit colorway is chosen freely to fit the character",
        "lighting_behavior": "bright beach daylight with soft reflected fill from sand, clear eyes, no harsh glamour lighting",
        "tags": ["beach", "summer", "breeze", "large_space", "natural_light", "daily", "novel_cg"],
    },
    {
        "name": "record_shop_listening_corner",
        "graphic_concept": "record shop listening corner; shelves, headphones, poster color blocks without readable text, and a small listening booth create a stylish music mood",
        "spatial_structure": "record shelves, listening booth counter, headphone hook, and poster wall create dense but ordered vertical layers",
        "visual_device": "record circles, headphone cable curve, shelf rows, and sticker-like shapes create strong rhythm around the character",
        "body_silhouette": "standing beside record shelves, lightly holding headphones, or listening with relaxed posture; avoid complex hand poses",
        "outfit_direction": "cropped sweatshirt, embellished mini skirt, clean idol-stage outfit",
        "material_language": "record sleeves, headphone plastic, shelf wood, soft sweatshirt fabric, skirt embellishments, small sticker details",
        "color_strategy": "record-shop graphic accents can vary; outfit colorway should harmonize with character identity",
        "lighting_behavior": "soft shop light with small glossy highlights on records and headphones, eyes remain the sharpest read",
        "tags": ["record_shop", "music", "poster", "shelf_layers", "trend_lifestyle", "reflection", "novel_cg"],
    },
    {
        "name": "planetarium_star_dome",
        "graphic_concept": "planetarium star-dome scene; curved seats, projected star map, and low ambient glow create a dreamy non-fantasy night atmosphere",
        "spatial_structure": "dome ceiling, curved seating rows, aisle light, and projection arc create a circular composition around the character",
        "visual_device": "star-map dots, seat arcs, small ticket, and soft projection glow create a quiet memory point",
        "body_silhouette": "seated, standing near the aisle, or looking upward naturally; face and eyes readable in low light",
        "outfit_direction": "chiffon fairy gown, off-shoulder ruffles, bouquet, elegant evening style",
        "material_language": "soft ruffles, light fabric, curved seats, ticket paper, projected star light, subtle floor reflection",
        "color_strategy": "projection glow and character palette guide the outfit colorway; avoid forcing a fixed costume color",
        "lighting_behavior": "low dome light with star projection highlights, gentle rim on hair, face softly readable",
        "tags": ["planetarium", "star_dome", "night", "dream", "circular_composition", "soft_light", "novel_cg"],
    },
    {
        "name": "transparent_acrylic_display_wall",
        "graphic_concept": "transparent acrylic display wall key visual; clear panels, soft reflections, and display blocks slice the composition without hiding identity",
        "spatial_structure": "layered acrylic panels stand between camera and character; transparent plinths and clean floor reflections create foreground-midground-background depth",
        "visual_device": "panel edges, reflected highlights, and partial occlusion split the silhouette while keeping face, hair, and core accessories readable",
        "body_silhouette": "standing, seated on a low display block, or pausing behind a panel; hands simple near panel edge, sleeve, or lap",
        "outfit_direction": "clean minimal studio outfit, simple silhouette, palette selected to support character identity",
        "material_language": "clear acrylic, polished floor, soft cloth, transparent plinths, crisp reflected highlights",
        "color_strategy": "clear materials and pale display planes stay secondary; the outfit should usually use a distinct non-white main value",
        "lighting_behavior": "large soft studio light creates thin bright edges on acrylic and a clean readable face",
        "tags": ["acrylic", "transparent", "display", "reflection", "foreground_occlusion", "mechanism_scene", "novel_cg"],
    },
    {
        "name": "frosted_glass_partition_scene",
        "graphic_concept": "frosted glass partition scene; blurred color blocks and clear face-side detail create a quiet graphic reveal",
        "spatial_structure": "frosted panels partially cover the body while one side opening keeps face and hair silhouette sharp; background shapes stay abstract and unreadable",
        "visual_device": "soft glass blur, sharp edge cuts, and partial transparency create visual tension without becoming a hidden-face image",
        "body_silhouette": "front three-quarter or gentle side pose near a glass edge; one hand may rest naturally on the partition",
        "outfit_direction": "soft date outfit: cardigan, camisole or blouse, A-line skirt, small shoulder bag, clean and youthful",
        "material_language": "frosted glass, soft knit or blouse fabric, diffused highlights, matte floor, faint reflected color fields",
        "color_strategy": "glass blur may echo character colors softly; no fixed outfit color requirement",
        "lighting_behavior": "backlit diffused glow through glass with clean eye highlights and readable facial planes",
        "tags": ["frosted_glass", "partition", "occlusion", "soft_blur", "reflection", "mechanism_scene", "novel_cg"],
    },
    {
        "name": "mirror_fragment_corner",
        "graphic_concept": "mirror-fragment corner key visual; broken-up reflections and angled mirror slabs create graphic rhythm around one real character",
        "spatial_structure": "angled mirror panels, floor reflection, and clean corner planes surround the character; reflections may fragment details but must not create duplicate people",
        "visual_device": "mirror shards repeat hair color, eye glow, and outfit edges as abstract fragments while only one true body exists",
        "body_silhouette": "standing or seated near angled mirrors, face readable in the real body; hands simple and not pressed dramatically on glass",
        "outfit_direction": "short one-piece dress, youthful clean date styling",
        "material_language": "mirror glass, polished floor, crisp cloth silhouette, thin metal panel edges, reflected light",
        "color_strategy": "reflections carry small accents from character palette; outfit colorway is chosen freely",
        "lighting_behavior": "clean directional studio light creates mirror glints but avoids overexposed face or duplicate silhouettes",
        "tags": ["mirror", "fragment", "reflection", "single_character_only", "graphic", "mechanism_scene", "novel_cg"],
    },
    {
        "name": "monochrome_color_block_studio",
        "graphic_concept": "monochrome color-block studio; huge flat graphic shapes and clean poster spacing create a fashion editorial anime KV",
        "spatial_structure": "large panels, floor blocks, circular or rectangular cutouts, and negative space place the character inside a graphic layout",
        "visual_device": "flat shapes, hard edges, and asymmetrical spacing make the whole image read like a designed poster instead of a plain studio shot",
        "body_silhouette": "seated on a block, leaning lightly near a panel, or standing offset inside the color shapes; hands simple",
        "outfit_direction": "academy pinafore dress, shirt, ribbon tie, round glasses, preppy school style",
        "material_language": "matte color panels, smooth floor, crisp fabric edges, small accessory shine, clean shadows",
        "color_strategy": "one dominant graphic color family is chosen by the model to flatter the character, with identity colors kept readable",
        "lighting_behavior": "clean studio light, controlled hard-edged shadows, and no noisy background texture",
        "tags": ["color_block", "studio", "poster", "graphic", "negative_space", "mechanism_scene", "novel_cg"],
    },
    {
        "name": "hanging_fabric_light_tunnel",
        "graphic_concept": "hanging fabric light tunnel; sheets of fabric form a soft corridor of light with a slight domestic-surreal feeling",
        "spatial_structure": "layered hanging cloth panels create a tunnel from foreground to background; character appears between fabric openings",
        "visual_device": "fabric gaps, translucent edges, and light bands create depth and reveal the character in stages",
        "body_silhouette": "walking through fabric, pausing between panels, or gently turning as cloth frames the face and shoulders",
        "outfit_direction": "satin lounge slip dress, lace panel, halter neck, side tie ribbon, relaxed resort-home mood",
        "material_language": "thin cloth, soft satin, lace edge, diffused window light, floor shadow bands",
        "color_strategy": "fabric stays airy, while the outfit keeps a distinct non-white or deeper-value color presence",
        "lighting_behavior": "backlit translucent fabric with soft glow, clear face fill, and gentle rim light on hair",
        "tags": ["hanging_fabric", "light_tunnel", "translucent", "foreground_occlusion", "soft_light", "mechanism_scene", "novel_cg"],
    },
    {
        "name": "white_room_floor_window",
        "graphic_concept": "quiet interior white room with floor-to-ceiling window; white wall, pale floor reflection, curtain shadow, and one character-color accent build the composition",
        "spatial_structure": "strictly indoors: a white room, window glass, pale floor, curtain, sofa edge, or low table; character stays off-center but medium-large with intentional blank white space",
        "visual_device": "thin curtain, small jewelry tray, flower stem in a vase, folded cloth, and soft indoor floor reflection create minimal narrative detail",
        "body_silhouette": "standing, leaning, or neatly seated beside the window or low table, front three-quarter or relaxed side angle, calm and cinematic",
        "outfit_direction": "simple camisole, lightweight opaque chiffon off-shoulder sleeves, high-waisted denim shorts, clean summer date style",
        "material_language": "camisole fabric, lightweight opaque chiffon sleeves, denim, glass, polished floor, thin curtain, small metal accessory",
        "color_strategy": "the room remains white and pale gray, but the outfit should usually be distinctly non-white and clearly separated from the background",
        "lighting_behavior": "large soft window light plus one hard curtain-shadow cut across the floor",
        "extra_prompt_guardrail": "keep the location as an indoor white room only; avoid exterior walls, stone stairs, balcony courtyard, garden path, mansion facade, or outdoor street.",
        "tags": ["white_room", "floor_window", "negative_space", "large_space", "soft_light", "minimal", "novel_cg"],
    },
    {
        "name": "pure_white_character_focus",
        "graphic_concept": "pure-white photographer-led character key visual; bright white negative space, clean crop choice, and crisp identity readability become the main design",
        "spatial_structure": "mostly white or high-key background with intentional blank margin; it may support close-up, half-body, knee-up, or full-body framing without turning into a real location",
        "visual_device": "photographer composition decides the crop: face and eyes stay sharp, hair silhouette and outfit line remain readable, and any small flower, hair strand, or white edge stays minimal",
        "body_silhouette": "close-up, bust-up, waist-up, knee-up, or full-body portrait; standing, light lean, or gentle walking balance is preferred, with clean hands and clean feet when visible",
        "outfit_direction": "strap maxi dress, fitted waist, flowing full skirt, elegant lightweight summer style",
        "material_language": "white negative space, soft skin-like light, clean flowing cloth, small flower or petal accent, soft hair, tiny accessories",
        "color_strategy": "white dominates the background layout only; the outfit should usually be distinctly non-white, cohesive, and clearly separated from the white field",
        "lighting_behavior": "bright natural high-key daylight, clear catchlights, soft overexposed white margins, face and eyes stay crisp",
        "tags": ["pure_white", "studio", "minimal", "portrait", "white_negative_space", "photographer_frame"],
    },
    {
        "name": "zero_gravity_fairy_room",
        "graphic_concept": "zero-gravity fairy-tale room; the character floats inside a soft dream space with petals, ribbons, and small toys drifting around",
        "spatial_structure": "pale fairy-tale room or cloud space, pillows, petals, ribbons, paper stars, and small toys floating lightly",
        "visual_device": "floating objects form a circular rhythm that returns the eye to face and eyes",
        "body_silhouette": "character lightly floating, body naturally curled or side-lying in the air, hands simple",
        "outfit_direction": "light fairy-tale floating outfit, airy fabric, ribbons, soft fantasy feeling",
        "material_language": "light gauze, ribbon, cloud shapes, petals, soft toys, tiny glow particles",
        "color_strategy": "pale dream background stays airy; the outfit should retain a distinct non-white color presence without becoming oversaturated",
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
        "material_language": "opaque airy gauze, petals, transparent bubbles, ribbons, soft hair",
        "color_strategy": "flower colors are accents only; character palette must remain the memory point",
        "lighting_behavior": "bright natural soft light with a slight glowing edge in the air",
        "tags": ["zero_gravity", "fairy_tale", "flower", "floating"],
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
        "graphic_concept": "low foreground-edge anime screenshot composition; table, stair, chair, or garden-path height creates depth while the character stays readable without upward body distortion",
        "spatial_structure": "camera near floor, tabletop, stair, chair, or garden path level, looking upward through a foreground edge; midground character remains medium-readable and off-center; background rises behind the character",
        "visual_device": "low foreground object, middle character, and rising window, door, wall, tree, or ceiling line form a readable upward three-depth stack",
        "body_silhouette": "medium readable figure seen from a low upward perspective, front three-quarter or clean side angle preferred, simple hands",
        "outfit_direction": "clean light-novel casual outfit, character palette stays recognizable",
        "material_language": "large blurred foreground edge, polished floor or stone path, glass, curtain, plant leaves, fabric",
        "color_strategy": "foreground shadow mass plus bright background plane; character color sits between them as the second read",
        "lighting_behavior": "low camera catches floor reflection and rim light; strong light direction clarifies depth",
        "tags": ["low_camera", "foreground_depth", "deep_perspective", "foreground_occlusion", "novel_cg"],
    },
    {
        "name": "far_shot_readable_room",
        "graphic_concept": "wide light-novel CG; environment carries emotion while the character remains the readable subject inside a room or terrace",
        "spatial_structure": "longer camera distance with wide room, balcony, exhibit aisle, archive-like shelving, or clean interior floor visible; character occupies a medium-readable area near a third or corner",
        "visual_device": "large empty wall, floor, or window area and repeated perspective lines create scale; readable character placement creates quiet warmth or loneliness",
        "body_silhouette": "readable full-body, knee-up, or three-quarter figure; identity kept by face, hair shape, color, and accessory silhouette",
        "outfit_direction": "tank top, oversized cropped hoodie, loose jeans, relaxed casual style",
        "material_language": "wall, floor, window, shelf, railing, curtain, table plane, hoodie cotton, loose denim, soft reflection",
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
        "outfit_direction": "soft casual outfit with warm simple styling",
        "material_language": "glass reflection, curtain layers, shelf edges, leaves, ceramic, paper, soft cloth",
        "color_strategy": "stacked muted color planes; one sharper character-color accent controls the focal point",
        "lighting_behavior": "compressed light bands, reflected highlights, and soft shadow layers separate foreground, character, and background",
        "tags": ["telephoto", "layered_space", "foreground_occlusion", "reflection", "deep_perspective", "novel_cg"],
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
        "name": "adjusting_sleeve_cuff",
        "body_silhouette": "one hand lightly adjusting a sleeve cuff below shoulder level, the other hand relaxed downward, complete readable fingers",
        "tags": ["micro_action", "simple_hand"],
    },
    {
        "name": "relaxed_visible_hands",
        "body_silhouette": "hands relaxed and visible near sides, sleeve cuff, bag strap, or lap; keep fingers clear and never frame the chest, neckline, waistband, or clothing openings",
        "tags": ["hands_visible", "simple_hand"],
    },
    {
        "name": "nearby_small_scene_prop",
        "body_silhouette": "a small dessert, bouquet, note card, or toy may sit nearby as scene detail; beverage containers are rare and, if present, stay on a distant surface away from the hands",
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
        "body_silhouette": "character caught after an action: turning from the window, adjusting a sleeve, or pausing beside a table; hands remain empty, relaxed, and clearly readable; emotion is quiet and cinematic",
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
        "body_silhouette": "low foreground-edge framing from table, stair, chair, or garden-path height; camera stays near eye-level enough to avoid body distortion while the character remains medium-readable",
        "tags": ["low_camera", "foreground_depth", "story_pose"],
    },
    {
        "name": "clean_lowered_pose",
        "body_silhouette": "stable lowered pose such as sitting on a step, leaning near a low shelf, or pausing beside floor-level props; hands stay visible and outside clothing",
        "tags": ["seated", "stable_hands", "story_pose"],
    },
]


ACTION_STYLES.append(
    {
        "name": "post_workout_stretch",
        "body_silhouette": "gentle body stretch, seated or one-knee pose, modest body angle, shoulders relaxed, hands naturally near knee, shoe, or floor; avoid athletic-room assumptions and suggestive framing",
        "tags": ["stretch", "stable_hands"],
    }
)

ACTION_STYLES.extend([
    {
        "name": "small_camera_v_sign",
        "body_silhouette": "small one-hand V-sign toward the camera, held beside the shoulder with clear space from the face; the other arm stays relaxed and the body remains still",
        "tags": ["small_gesture", "v_sign", "simple_hand", "eye_contact"],
    },
    {
        "name": "small_camera_ok_sign",
        "body_silhouette": "small one-hand OK-sign toward the camera, held around shoulder level without covering the face; the other arm stays relaxed and the body remains still",
        "tags": ["small_gesture", "ok_sign", "simple_hand", "eye_contact"],
    },
    {
        "name": "small_camera_wave",
        "body_silhouette": "small restrained one-hand wave toward the camera with the palm below face level; the other arm stays relaxed and the body remains still",
        "tags": ["small_gesture", "small_wave", "simple_hand", "eye_contact"],
    },
])


CAMERA_COMPOSITION_ACTION_NAMES = {
    "camera_from_low_foreground",
    "camera_looking_down",
    "half_hidden_by_foreground",
    "readable_figure_in_depth",
    "three_quarter_observed_from_distance",
}


COMPOSITION_PLANS = [
    {
        "name": "clean_three_quarter_character_frame",
        "composition": "clean three-quarter character framing with readable face, outfit silhouette, hands, and a simple scene rhythm",
        "camera": "waist-up to knee-up, natural eye-level or slight side angle",
        "pose": "use the selected action naturally without adding extra props or contradictory body direction",
        "foreground": "minimal foreground depth only when the scene already provides it",
        "lighting": "balanced soft light that supports the selected plan",
        "guardrail": "do not add new scene objects, flowers, curtains, hats, bouquets, or bed/floor requirements",
        "tags": ["generic_composition", "readable_subject", "medium_shot"],
    },
    {
        "name": "readable_environment_medium_shot",
        "composition": "medium shot where character remains the focus while the selected environment stays clearly readable",
        "camera": "medium distance, straight or gentle three-quarter angle, no extreme lens effect",
        "pose": "follow the selected action with relaxed hands and a stable body line",
        "foreground": "scene edges may frame the image lightly without covering the face",
        "lighting": "use the plan lighting as the main atmosphere",
        "guardrail": "avoid forcing close-up, flower foreground, curtain fabric, bouquet, or large dress shape",
        "tags": ["generic_composition", "environment_readable", "medium_shot"],
    },
    {
        "name": "foreground_edge_depth_frame",
        "composition": "simple foreground edge or object plane creates depth while keeping face and outfit fully visible",
        "camera": "medium-close to medium-wide, foreground edge near camera, character in readable midground",
        "pose": "selected action remains unchanged, body direction stays coherent with the plan",
        "foreground": "use only objects already natural to the scene as a soft edge frame",
        "lighting": "foreground is slightly softer than the character, no heavy obstruction",
        "guardrail": "avoid adding flowers, curtains, bouquet, hat, bed, or unrelated props unless already specified by the plan",
        "tags": ["generic_composition", "foreground_depth", "readable_subject"],
    },
    {
        "name": "clean_full_body_silhouette_frame",
        "composition": "readable full-body or near full-body framing with a clean outfit silhouette and stable negative space",
        "camera": "medium-wide, natural perspective, character large enough for identity details",
        "pose": "selected action remains clear from head to feet",
        "foreground": "no required foreground object",
        "lighting": "plan lighting stays primary and does not hide hands or face",
        "guardrail": "avoid adding special props, flowers, curtains, hats, bouquet, or bed/floor requirements",
        "tags": ["generic_composition", "full_body", "readable_subject"],
    },
    {
        "name": "slight_side_medium_close_frame",
        "composition": "medium-close three-quarter side framing with face, shoulders, hairstyle, and upper outfit readable",
        "camera": "waist-up, slight side angle, natural portrait distance",
        "pose": "selected action is simplified into a calm readable body line",
        "foreground": "no forced foreground obstruction",
        "lighting": "soft face light with clean eye highlights",
        "guardrail": "avoid new props, extra hand gestures, or close-up cropping that contradicts the selected action",
        "tags": ["generic_composition", "medium_shot", "side_glance"],
    },
    {
        "name": "layered_scene_corner_frame",
        "composition": "character placed near one side of the frame with existing scene architecture or furniture creating depth",
        "camera": "medium shot, slight diagonal angle, background remains readable",
        "pose": "selected action stays coherent with the scene direction",
        "foreground": "only natural scene edges may appear as soft framing",
        "lighting": "depth layers separated by the plan lighting",
        "guardrail": "avoid adding unrelated flowers, curtains, bouquet, hat, or oversized dress volume",
        "tags": ["generic_composition", "foreground_depth", "environment_readable"],
    },
    {
        "name": "vertical_poster_readable_pose",
        "composition": "vertical poster-like frame with character centered or slightly off-center, identity and outfit shape readable",
        "camera": "knee-up to full-body, straight perspective",
        "pose": "selected action is kept simple and balanced",
        "foreground": "clean frame edges without heavy occlusion",
        "lighting": "clear face light, controlled background contrast",
        "guardrail": "avoid turning the scene into a graphic poster unless the plan already asks for it",
        "tags": ["generic_composition", "readable_subject", "poster_balance"],
    },
    {
        "name": "calm_motion_midground_frame",
        "composition": "midground character caught in a quiet motion beat with the selected environment still visible",
        "camera": "medium distance, natural lens, body direction follows the selected action",
        "pose": "walking, turning, pausing, or adjusting motion stays modest and readable",
        "foreground": "no mandatory foreground prop",
        "lighting": "plan lighting supports motion without blur or anatomy confusion",
        "guardrail": "avoid adding a second action, bouquet, curtain, hat, or floor pose requirement",
        "tags": ["generic_composition", "story_pose", "environment_readable"],
    },
    {
        "name": "quiet_close_upper_body_frame",
        "composition": "clean upper-body portrait with enough outfit context and no extra required prop",
        "camera": "bust-up to waist-up, eye-level, shallow but not extreme depth of field",
        "pose": "selected action is reduced to a natural expression and relaxed hands if visible",
        "foreground": "hair or scene edge may frame lightly without covering eyes",
        "lighting": "soft readable face light",
        "guardrail": "avoid hand-on-cheek, hat shadow, flowers, curtains, or lingerie-like cropping unless selected elsewhere",
        "tags": ["generic_composition", "close_character", "eye_contact"],
    },
    {
        "name": "pure_white_social_close_portrait",
        "composition": "high-key close portrait with large clean white margin around the image; face, eyes, hairstyle, and shoulder line dominate the read",
        "camera": "close-up to bust-up, natural eye-level or slight high angle, shallow depth of field but crisp eyes",
        "pose": "quiet direct gaze, soft smile, or side glance; hands remain naturally below shoulder level or outside the close crop",
        "foreground": "optional tiny flower, petal, hair strand, or soft white edge near camera, never covering both eyes",
        "lighting": "bright natural daylight, white overexposed margins, clean catchlights, soft facial shadow",
        "guardrail": "avoid busy room, distant figure, seated floor pose, big props, UI text, or cleavage crop",
        "tags": ["pure_white_special", "close_character", "white_negative_space", "portrait", "soft_light"],
    },
    {
        "name": "pure_white_half_body_social_photo",
        "composition": "vertical social-photo half-body portrait with clean white space above or below, character cropped from head to waist or upper torso",
        "camera": "half-body to upper-torso, slight high angle or front three-quarter, face remains the sharpest detail",
        "pose": "natural standing or light lean; hands rest near the sides or may lightly touch a sleeve cuff, frame edge, or small flower",
        "foreground": "white margin, soft flower edge, or hair crossing one side can add depth without becoming a separate scene",
        "lighting": "sunny high-key fill, clean white background, gentle skin and hair highlights",
        "guardrail": "avoid full-length fashion pose, distant figure, cluttered background, bed/floor pose, or large handheld objects",
        "tags": ["pure_white_special", "close_character", "half_body", "white_negative_space", "soft_light"],
    },
    {
        "name": "pure_white_three_quarter_editorial_frame",
        "composition": "high-key white-space three-quarter portrait; character is cropped from head to thigh or knee with deliberate white margin, clean outfit silhouette, and no separate scene narrative",
        "camera": "thigh-up or knee-up, eye-level or slightly high portrait angle, natural front three-quarter or gentle side angle, face remains crisp",
        "pose": "standing, light lean, or slow walking balance; arms and hands stay simple and outside clothing, with no forced prop action",
        "foreground": "optional white edge, hair strand, tiny flower, or soft shoulder-level blur may frame one side without hiding identity details",
        "lighting": "bright high-key daylight with controlled overexposed white space, soft skin shadow, and clear hair-edge separation",
        "guardrail": "avoid garden, flower field, product set, installation props, bed/floor pose, low-angle distortion, or distant full-scene framing",
        "tags": ["pure_white_special", "three_quarter", "white_negative_space", "photographer_frame", "soft_light"],
    },
    {
        "name": "pure_white_full_body_editorial_frame",
        "composition": "full-body high-key fashion portrait on a clean white field; the whole silhouette is readable head-to-toe while generous white margin creates a photographer's negative-space layout",
        "camera": "full-body to near full-body, stable eye-level or gentle high angle, character large enough that face, hair silhouette, outfit shape, hands, and visible feet stay readable",
        "pose": "natural standing, small step, or relaxed weight shift; feet are clear when included and arms do not cross awkwardly into clothing",
        "foreground": "none or a very soft white edge only; keep the body contour and outfit line unobstructed",
        "lighting": "clean white studio daylight, subtle floor contact shadow if needed, bright but not washed out on face or clothes",
        "guardrail": "avoid tiny subject, extreme wide shot, low-angle legs-first framing, floor sitting, bed pose, clutter, flowers as a location, or unrelated props",
        "tags": ["pure_white_special", "full_body", "white_negative_space", "photographer_frame", "soft_light"],
    },
    {
        "name": "wide_readable_scene_balance",
        "composition": "wider scene-balanced frame where the character remains readable and the environment explains the plan",
        "camera": "medium-wide, character not tiny, stable horizon or room geometry",
        "pose": "selected action stays clear from silhouette alone",
        "foreground": "optional natural scene edge only",
        "lighting": "environment light frames the character without overexposure",
        "guardrail": "avoid empty landscape, forced flower field, curtain, bouquet, hat, or bed/floor pose",
        "tags": ["generic_composition", "wide_shot", "environment_readable"],
    },
    {
        "name": "foreground_flower_occlusion_closeup",
        "composition": "close-up or bust-up with large blurred flowers covering 20-50 percent of the foreground while eyes, face shape, and hair silhouette remain readable",
        "camera": "close distance, shallow depth of field, eye-level or gentle side angle",
        "pose": "looking up at flowers, gentle side glance, or quiet direct gaze through gaps",
        "foreground": "large soft flower branches create airy obstruction, never a dense flower wall",
        "lighting": "soft sunlight, clear eye highlights, clean pastel air",
        "guardrail": "flowers must not fully cover the face; avoid flat centered ID-photo composition",
        "tags": ["foreground_occlusion", "flower", "close_character", "soft_light"],
    },
    {
        "name": "low_angle_under_flower_canopy",
        "composition": "low-angle portrait below flower branches, flower canopy above the head with bright open background behind",
        "camera": "low foreground height, close-up to half-body, slight upward perspective without facial distortion",
        "pose": "chin slightly raised, eyes looking upper-left or upper-right, hair lightly moved by wind",
        "foreground": "flower canopy crosses the upper frame as a soft ceiling",
        "lighting": "sunlight touches eyes and cheek, sky negative space stays clean",
        "guardrail": "avoid extreme nostril angle, distorted face, tiny character, or stiff front pose",
        "tags": ["low_camera", "flower", "breeze", "negative_space"],
    },
    {
        "name": "flower_frame_clear_face",
        "composition": "face framed by flowers or soft foreground objects around image edges, facial features remain the clean focal point",
        "camera": "bust-up to waist-up, medium-close distance, shallow depth of field",
        "pose": "soft direct gaze or slight smile, hands hidden or naturally near flowers",
        "foreground": "petals cross edges but leave eyes and face open",
        "lighting": "bright spring-like color and clean facial focus",
        "guardrail": "avoid symmetrical wreath feeling, idol-poster overload, or petals blocking the face",
        "tags": ["foreground_occlusion", "flower", "eye_contact", "close_character"],
    },
    {
        "name": "cinematic_wide_flower_side_view",
        "composition": "cinematic horizontal crop, character off-center, large flower foreground and sky negative space, side or three-quarter side body",
        "camera": "medium to long landscape framing, character readable but not tiny",
        "pose": "looking upward or sideways, hair flowing backward, calm spring moment",
        "foreground": "wide soft flower blur crosses lower or side frame",
        "lighting": "clean sky light and airy color separation",
        "guardrail": "avoid empty landscape where the character becomes unreadable",
        "tags": ["wide_shot", "flower", "negative_space", "side_glance"],
    },
    {
        "name": "diagonal_window_light_haze",
        "composition": "seated character near window, strong sunlight beam cuts diagonally through visible mist or dust",
        "camera": "knee-up or three-quarter body, slight side angle beside the light beam",
        "pose": "quiet seated pose, side glance, hands resting naturally",
        "foreground": "haze and window-shadow shapes create layered depth",
        "lighting": "diagonal beam, soft face highlight, carved window shadow",
        "guardrail": "avoid horror smoke, dirty abandoned room, face lost in darkness, or fog covering body",
        "tags": ["window_frame", "light_cut", "haze", "seated"],
    },
    {
        "name": "over_shoulder_bouquet_turn",
        "composition": "shoulder-away posture with head turned back in profile or three-quarter view, flowers crossing the back line",
        "camera": "waist-up to thigh-up, close enough to read face and hair ornaments",
        "pose": "gentle over-shoulder glance, arms naturally behind or holding a simple flower shape",
        "foreground": "bouquet or floral edge stays behind the body line",
        "lighting": "elegant shoulder line with clear face light",
        "guardrail": "avoid full back with no face, forced seductive pose, broken arms, or bouquet blocking body shape",
        "tags": ["back_view", "looking_back", "flower", "story_pose"],
    },
    {
        "name": "floor_diagonal_negative_space",
        "composition": "character seated diagonally on floor, body forms a long slanted line across lower frame with designed empty area around",
        "camera": "medium-wide shot, slightly high or eye-level, full body or near full body",
        "pose": "one hand supporting body on floor, legs extended or folded naturally, head turned toward light",
        "foreground": "floor reflection or shadow becomes a graphic field",
        "lighting": "strong light patch or shadow shape organizes empty space",
        "guardrail": "avoid twisted torso, unclear floor hand, or random empty area without design",
        "tags": ["negative_space", "floor", "seated", "full_body"],
    },
    {
        "name": "gray_studio_large_dress_shape",
        "composition": "minimal studio with large dress fabric spreading across lower frame as the main graphic mass",
        "camera": "full-body or three-quarter body, clean fashion portrait with negative space",
        "pose": "standing, sitting on a low block, or gently holding the outer skirt fabric so the dress shape stays readable",
        "foreground": "fabric volume forms a sculptural lower-frame shape",
        "lighting": "clean studio light with crisp dress volume and soft face highlight",
        "guardrail": "avoid wedding ceremony mood, bouquet overload, noisy background, or dress swallowing anatomy",
        "tags": ["studio", "dress_volume", "negative_space", "fashion"],
    },
    {
        "name": "hat_brim_shadow_closeup",
        "composition": "tight close-up with wide hat brim or veil shadow crossing upper face while eyes remain visible",
        "camera": "tight bust-up, frontal or slight side angle, shallow depth",
        "pose": "quiet direct gaze with relaxed shoulders; hands remain naturally lowered or outside the close crop",
        "foreground": "hat brim shadow and hair strands create layered close framing",
        "lighting": "soft skin light and darker eye shadow contrast without losing readability",
        "guardrail": "avoid hand covering mouth, face too dark, or oversexual finger pose",
        "tags": ["close_character", "shadow", "fashion", "eye_contact"],
    },
    {
        "name": "high_angle_bed_or_floor_frame",
        "composition": "camera looks down from above, character lying or leaning on bed or floor, surrounding objects form a soft frame",
        "camera": "high angle, medium-wide shot, face looking up toward camera",
        "pose": "lying on stomach, elbows on pillow, or leaning on bedding with relaxed hands",
        "foreground": "bedding shapes, magazines, or small props frame without clutter",
        "lighting": "cozy soft room light with clear face and eyes",
        "guardrail": "avoid erotic bedroom framing, top-down map view, tiny character, or messy prop overload",
        "tags": ["high_camera", "bed_floor", "soft_light", "story_props"],
    },
    {
        "name": "lace_curtain_backlight_occlusion",
        "composition": "character partly behind lace curtain or lightweight foreground curtain fabric, translucent scene layer over body while face remains readable",
        "camera": "medium shot to close-up, side or three-quarter angle",
        "pose": "standing beside curtain, holding fabric lightly, looking down or toward window",
        "foreground": "glowing lace texture and lightweight curtain fabric create soft scene obstruction",
        "lighting": "warm backlight through lace, soft silhouette, clear facial features",
        "guardrail": "avoid blown-out face, explicit lingerie framing, excessive exposure, or unreadable features",
        "tags": ["lace", "curtain", "backlight", "foreground_occlusion"],
    },
    {
        "name": "soft_relaxed_close_face",
        "composition": "intimate close-up where face fills most of frame and the shoulder line remains natural",
        "camera": "close-up, shallow depth of field, warm soft light",
        "pose": "direct quiet gaze or slightly lowered eyelids; hands remain outside the close crop",
        "foreground": "loose hair strands cross face lightly without hiding eyes",
        "lighting": "warm soft light, glossy eyes, delicate skin texture",
        "guardrail": "avoid plastic doll face, oversexual expression, wet-shirt look, or cleavage crop",
        "tags": ["close_character", "relaxed_pose", "soft_light", "eye_contact"],
    },
]


VISUAL_MOTIF_SYSTEMS = [
    {
        "name": "moonlit_toy_window_kv",
        "motifs": "quiet moonlit shapes selected only when already natural to the scene",
        "layering": "foreground and background remain scene-native; midground character stays the only subject",
        "shape_rhythm": "large calm arcs, clean hair flow, soft repeated light dots",
        "light_bloom": "cool moonlight cut by restrained warm highlights, soft rim light on hair edges",
        "poetic_line": "quiet moonlit atmosphere with no extra objects beyond the selected scene",
    },
    {
        "name": "pastel_lace_decorative_kv",
        "motifs": "soft graphic accents selected only from the active scene",
        "layering": "simple foreground, readable character, and clean background spacing without unrelated props",
        "shape_rhythm": "rounded graphic blocks, outfit silhouette curves, and clear negative space",
        "light_bloom": "milky pastel bloom with restrained warm highlights and clean color separation",
        "poetic_line": "soft commercial anime atmosphere without adding a second scene",
    },
    {
        "name": "fairy_tale_anniversary_kv",
        "motifs": "fairy-tale light accents selected only when the plan already includes them",
        "layering": "scene-native foreground and background support the character without a new stage",
        "shape_rhythm": "arched composition lines, hair flow, and small repeated light marks",
        "light_bloom": "golden fairy light against cool blue or pale green air with controlled edge glow",
        "poetic_line": "fairy-tale atmosphere tied to the selected location only",
    },
    {
        "name": "candy_air_parlor_kv",
        "motifs": "small scene-native accents with no unrelated dessert or toy layer",
        "layering": "foreground detail, character, and background all belong to the selected location",
        "shape_rhythm": "small circular highlights, clean curves, and readable hair silhouette",
        "light_bloom": "cold cyan shadows crossed with peach-pink highlights and airy haze",
        "poetic_line": "soft color atmosphere that stays secondary to identity and the selected scene",
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
    if "pure_white" in plan_tags:
        bonuses = {
            "full_body_readable": 0.45,
            "knee_up_medium": 0.85,
            "waist_up_half_body": 0.95,
            "bust_close": 0.65,
            "close_upper_body": 0.45,
        }
    elif plan_tags & {"close_character", "studio", "white_room"}:
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
    "柏妮思",
    "妮可",
    "简",
    "月城柳",
    "青衣",
    "伊芙琳",
    "朱鸢",
    "卢西娅",
    "维琳娜",
    "铃",
    "扳机",
    "诺姆",
    "希希芙",
    "德蕾琪娜·挽昼",
    "今汐",
    "千咲",
    "卡提希娅",
    "坎特蕾拉",
    "守岸人",
    "尤诺",
    "洛瑟菈",
    "爱弥斯",
    "琳奈",
    "秧秧",
    "绯雪",
    "莫宁",
    "菲比",
    "西格莉卡",
    "达妮娅",
    "长离",
    "奥古斯塔",
    "清宵",
    "折枝",
    "漂泊者",
    "弗洛洛",
    "林德薇恩",
    "穗穗",
    "诀",
    "洛茜",
    "庄方宜",
    "艾尔黛拉",
    "佩丽卡",
    "陈千语",
    "弭弗",
    "茜特菈莉",
    "桑多涅",
    "哥伦比娅",
    "丝柯克",
    "Saber",
    "阿格莱雅",
    "火花",
    "花火",
    "青雀",
    "昔涟",
    "大丽花",
    "大黑塔",
    "知更鸟·晴歌",
    "知更鸟",
    "停云",
    "忘归人",
    "符玄",
    "流萤",
    "爻光",
    "遐蝶",
    "阮·梅",
    "卡芙卡",
    "姬子",
    "灵砂",
    "绯英",
    "银狼",
    "银狼LV.999",
    "风堇",
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
    "balcony_breeze_half_out_frame": 3.0,
    "greenhouse_terrace_reflection": 2.8,
    "white_room_floor_window": 2.8,
    "rooftop_laundry_sunset": 2.7,
    "beach_wind_open_sand": 2.4,
    "record_shop_listening_corner": 2.1,
    "planetarium_star_dome": 1.8,
    "transparent_acrylic_display_wall": 0.9,
    "frosted_glass_partition_scene": 0.55,
    "mirror_fragment_corner": 1.0,
    "monochrome_color_block_studio": 2.3,
    "hanging_fabric_light_tunnel": 2.3,
    "trend_mirror_studio": 0.7,
    "capsule_toy_corner": 0.8,
    "graphic_poster_studio": 0.55,
    "pure_white_character_focus": 0.75,
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
    "seated_quiet_pose": 0.45,
    "nearby_small_scene_prop": 0.9,
    "walking_forward": 2.0,
    "steady_eye_contact": 2.2,
    "relaxed_visible_hands": 1.25,
    "adjusting_hair": 1.6,
    "post_workout_stretch": 0.2,
    "clean_lowered_pose": 0.3,
}


def _apply_weight_overrides(default_weights, character_weights, overrides):
    for item_name, weight in overrides.items():
        default_weights[item_name] = weight
        for weights in character_weights.values():
            weights[item_name] = weight


def _require_unique_names(items, label):
    names = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"].strip():
            raise ValueError(f"{label} contains an item without a valid name")
        names.append(item["name"])
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"{label} contains duplicate names: {duplicates}")


def _validate_runtime_plans(plans, outfit_directions, plan_weight_overrides):
    if not isinstance(outfit_directions, list) or not all(isinstance(item, str) and item.strip() for item in outfit_directions):
        raise ValueError("outfit_directions must be a non-empty list of strings")
    if not isinstance(plans, list) or not plans:
        raise ValueError("art_direction_plans must be a non-empty list")
    required_fields = {
        "name",
        "graphic_concept",
        "spatial_structure",
        "visual_device",
        "body_silhouette",
        "outfit_direction",
        "material_language",
        "color_strategy",
        "lighting_behavior",
        "tags",
    }
    for plan in plans:
        missing = sorted(required_fields - set(plan))
        if missing:
            raise ValueError(f"plan {plan.get('name', '<unknown>')} missing fields: {missing}")
        if plan["outfit_direction"] not in outfit_directions:
            raise ValueError(f"plan {plan['name']} outfit_direction is not in outfit_directions")
        if not isinstance(plan.get("tags"), list):
            raise ValueError(f"plan {plan['name']} tags must be a list")
    _require_unique_names(plans, "art_direction_plans")
    plan_names = {plan["name"] for plan in plans}
    unknown_weights = sorted(set(plan_weight_overrides) - plan_names)
    if unknown_weights:
        raise ValueError(f"plan_weight_overrides references unknown plans: {unknown_weights}")
    for name, weight in plan_weight_overrides.items():
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError(f"plan_weight_overrides[{name!r}] must be a positive number")


def _validate_runtime_composition_plans(composition_plans):
    if not isinstance(composition_plans, list) or not composition_plans:
        raise ValueError("composition_plans must be a non-empty list")
    required_fields = {"name", "composition", "camera", "pose", "foreground", "lighting", "guardrail", "tags"}
    for plan in composition_plans:
        missing = sorted(required_fields - set(plan))
        if missing:
            raise ValueError(f"composition plan {plan.get('name', '<unknown>')} missing fields: {missing}")
        if not isinstance(plan.get("tags"), list):
            raise ValueError(f"composition plan {plan['name']} tags must be a list")
    _require_unique_names(composition_plans, "composition_plans")


def _rebuild_art_direction_runtime_state(plan_weight_overrides=None):
    PLAN_TAGS.clear()
    PLAN_TAGS.update({
        plan["name"]: list(plan.get("tags", []))
        for plan in ART_DIRECTION_PLANS
    })
    DEFAULT_PLAN_WEIGHTS.clear()
    DEFAULT_PLAN_WEIGHTS.update({
        plan["name"]: 1.0
        for plan in ART_DIRECTION_PLANS
    })
    CHARACTER_PLAN_WEIGHTS.clear()
    CHARACTER_PLAN_WEIGHTS.update({
        character_name: dict(DEFAULT_PLAN_WEIGHTS)
        for character_name in KNOWN_CHARACTER_NAMES
    })
    _apply_weight_overrides(
        DEFAULT_PLAN_WEIGHTS,
        CHARACTER_PLAN_WEIGHTS,
        plan_weight_overrides or NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES,
    )
    _apply_weight_overrides(DEFAULT_ACTION_WEIGHTS, CHARACTER_ACTION_WEIGHTS, NARRATIVE_SPACE_ACTION_WEIGHT_OVERRIDES)


def apply_runtime_art_direction_config(config_data):
    global RUNTIME_CONFIG_REVISION
    if not isinstance(config_data, dict):
        raise ValueError("runtime config must be a JSON object")
    outfit_directions = config_data.get("outfit_directions", OUTFIT_DIRECTIONS)
    plans = config_data.get("art_direction_plans", ART_DIRECTION_PLANS)
    composition_plans = config_data.get("composition_plans", COMPOSITION_PLANS)
    plan_weight_overrides = config_data.get("plan_weight_overrides", NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES)
    if not isinstance(plan_weight_overrides, dict):
        raise ValueError("plan_weight_overrides must be an object")
    plan_weight_overrides = {
        str(name): float(weight)
        for name, weight in plan_weight_overrides.items()
    }
    _validate_runtime_plans(plans, outfit_directions, plan_weight_overrides)
    _validate_runtime_composition_plans(composition_plans)
    OUTFIT_DIRECTIONS[:] = list(outfit_directions)
    ART_DIRECTION_PLANS[:] = [dict(plan) for plan in plans]
    COMPOSITION_PLANS[:] = [dict(plan) for plan in composition_plans]
    NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES.clear()
    NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES.update(plan_weight_overrides)
    _rebuild_art_direction_runtime_state(plan_weight_overrides)
    RUNTIME_CONFIG_REVISION = str(config_data.get("revision") or "json-local")
    return RUNTIME_CONFIG_REVISION


def load_runtime_art_direction_config(path=RUNTIME_CONFIG_PATH):
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return apply_runtime_art_direction_config(data)


_rebuild_art_direction_runtime_state(NARRATIVE_SPACE_PLAN_WEIGHT_OVERRIDES)


PLAN_ACTION_COMPATIBILITY = [
    ({"white_room", "pure_white", "minimal"}, {"stable_hands", "simple_hand", "eye_contact", "stable_pose", "hair_touch", "hands_visible", "seated", "walking"}),
    ({"high_camera"}, {"high_camera", "deep_perspective", "far_shot", "readable_subject", "eye_contact", "stable_pose", "seated"}),
    ({"low_camera", "foreground_depth"}, {"low_camera", "foreground_depth", "eye_contact", "stable_pose", "seated", "walking"}),
    ({"far_shot", "readable_subject"}, {"far_shot", "readable_subject", "deep_perspective", "eye_contact", "stable_pose", "walking", "seated"}),
    ({"telephoto", "layered_space"}, {"foreground_occlusion", "edge_framing", "simple_hand", "eye_contact", "stable_pose", "hair_touch", "hands_visible", "seated"}),
]


def _profile_for(character_name):
    active_variant = _ACTIVE_CHARACTER_PROFILE_VARIANTS.get(character_name)
    if active_variant is not None:
        return CHARACTER_PROFILE_VARIANTS[character_name][active_variant]
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
        and action["name"] not in CAMERA_COMPOSITION_ACTION_NAMES
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
        and action["name"] not in CAMERA_COMPOSITION_ACTION_NAMES
    ]
    plan_name = (plan or {}).get("name", "")
    stretch_allowed_plans = set()
    if plan_name not in stretch_allowed_plans:
        action_pool = [
            action for action in action_pool
            if action["name"] != "post_workout_stretch"
        ]
    close_character_plans = {
        "trend_mirror_studio",
        "capsule_toy_corner",
        "graphic_poster_studio",
        "pure_white_character_focus",
    }
    if plan_name in close_character_plans:
        action_pool = [
            action for action in action_pool
            if action["name"] not in {"readable_figure_in_depth", "three_quarter_observed_from_distance"}
        ]
    return dict(_weighted_choice(action_pool, recent_tags=recent_tags, weights=weights))


def choose_plan_and_action(character_name, recent_tags=None):
    plan = choose_art_plan(character_name, recent_tags)
    action = choose_compatible_action_style(character_name, recent_tags, plan)
    return plan, action


FLOWER_COMPOSITION_NAMES = {
    "foreground_flower_occlusion_closeup",
    "low_angle_under_flower_canopy",
    "flower_frame_clear_face",
    "cinematic_wide_flower_side_view",
    "over_shoulder_bouquet_turn",
}

FLOWER_COMPOSITION_TAGS = {
    "flower",
    "garden",
    "greenhouse",
    "bridal",
    "fairy_tale",
    "zero_gravity",
}

FLOWER_COMPOSITION_PLANS = {
    "flower_sea_afternoon",
    "flower_bridal_garden",
    "greenhouse_terrace_reflection",
    "zero_gravity_fairy_room",
    "zero_gravity_fairy_garden",
}

INTERIOR_COMPOSITION_NAMES = {
    "diagonal_window_light_haze",
    "floor_diagonal_negative_space",
    "high_angle_bed_or_floor_frame",
    "lace_curtain_backlight_occlusion",
}

INTERIOR_COMPOSITION_TAGS = {
    "white_room",
    "pure_white",
    "window_frame",
    "indoor",
    "interior",
    "room",
    "studio",
    "fashion",
    "tea_room",
    "foreground_occlusion",
    "layered_space",
    "deep_perspective",
    "large_space",
}

INTERIOR_COMPOSITION_PLANS = {
    "white_room_floor_window",
    "pure_white_character_focus",
    "transparent_acrylic_display_wall",
    "frosted_glass_partition_scene",
    "mirror_fragment_corner",
    "monochrome_color_block_studio",
    "clean_archive_storage_room",
    "giant_cushion_showroom",
    "paper_sculpture_room",
    "hanging_fabric_light_tunnel",
    "table_edge_magazine_occlusion",
    "telephoto_layered_interior",
    "far_shot_readable_room",
    "low_angle_foreground_depth",
    "overhead_deep_perspective_space",
}

COMPOSITION_BASE_WEIGHTS = {
    "clean_three_quarter_character_frame": 0.85,
    "readable_environment_medium_shot": 0.45,
    "foreground_edge_depth_frame": 0.8,
    "clean_full_body_silhouette_frame": 0.18,
    "slight_side_medium_close_frame": 0.8,
    "layered_scene_corner_frame": 0.8,
    "vertical_poster_readable_pose": 0.6,
    "calm_motion_midground_frame": 0.8,
    "quiet_close_upper_body_frame": 1.15,
    "pure_white_social_close_portrait": 1.8,
    "pure_white_half_body_social_photo": 1.55,
    "pure_white_three_quarter_editorial_frame": 1.3,
    "pure_white_full_body_editorial_frame": 0.9,
    "wide_readable_scene_balance": 0.75,
    "floor_diagonal_negative_space": 0.12,
    "high_angle_bed_or_floor_frame": 0.08,
    "diagonal_window_light_haze": 0.25,
    "foreground_flower_occlusion_closeup": 0.45,
    "low_angle_under_flower_canopy": 0.4,
    "flower_frame_clear_face": 0.45,
    "cinematic_wide_flower_side_view": 0.35,
    "over_shoulder_bouquet_turn": 0.35,
    "lace_curtain_backlight_occlusion": 0.18,
    "gray_studio_large_dress_shape": 0.25,
    "hat_brim_shadow_closeup": 0.55,
    "soft_relaxed_close_face": 0.7,
}

GENERIC_COMPOSITION_NAMES = {
    "clean_three_quarter_character_frame",
    "readable_environment_medium_shot",
    "foreground_edge_depth_frame",
    "clean_full_body_silhouette_frame",
    "slight_side_medium_close_frame",
    "layered_scene_corner_frame",
    "vertical_poster_readable_pose",
    "calm_motion_midground_frame",
    "quiet_close_upper_body_frame",
    "wide_readable_scene_balance",
}

COMPOSITION_ALLOWED_ACTIONS = {
    "floor_diagonal_negative_space": {
        "seated_quiet_pose",
        "clean_lowered_pose",
        "camera_looking_down",
    },
    "high_angle_bed_or_floor_frame": {
        "seated_quiet_pose",
        "unaware_candid_moment",
        "camera_looking_down",
    },
    "over_shoulder_bouquet_turn": {
        "looking_back_from_edge",
        "gentle_side_glance",
        "quiet_prop_after_moment",
    },
    "soft_relaxed_close_face": {
        "steady_eye_contact",
        "gentle_side_glance",
    },
    "hat_brim_shadow_closeup": {
        "steady_eye_contact",
        "gentle_side_glance",
    },
    "gray_studio_large_dress_shape": {
        "seated_quiet_pose",
        "steady_eye_contact",
        "adjusting_hair",
        "clean_lowered_pose",
    },
}

COMPOSITION_FORBIDDEN_ACTIONS = {
    "low_angle_under_flower_canopy": {
        "camera_looking_down",
    },
    "high_angle_bed_or_floor_frame": {
        "camera_from_low_foreground",
    },
    "clean_full_body_silhouette_frame": {
        "half_hidden_by_foreground",
    },
    "quiet_close_upper_body_frame": {
        "clean_lowered_pose",
        "readable_figure_in_depth",
        "three_quarter_observed_from_distance",
    },
    "slight_side_medium_close_frame": {
        "clean_lowered_pose",
        "readable_figure_in_depth",
        "three_quarter_observed_from_distance",
    },
}

COMPOSITION_REQUIRED_PLAN_NAMES = {
    "pure_white_social_close_portrait": {
        "pure_white_character_focus",
    },
    "pure_white_half_body_social_photo": {
        "pure_white_character_focus",
    },
    "pure_white_three_quarter_editorial_frame": {
        "pure_white_character_focus",
    },
    "pure_white_full_body_editorial_frame": {
        "pure_white_character_focus",
    },
    "diagonal_window_light_haze": {
        "white_room_floor_window",
        "balcony_breeze_half_out_frame",
        "telephoto_layered_interior",
        "far_shot_readable_room",
    },
    "lace_curtain_backlight_occlusion": {
        "white_room_floor_window",
        "hanging_fabric_light_tunnel",
    },
}

COMPOSITION_ALLOWED_OUTFIT_KEYWORDS = {
    "gray_studio_large_dress_shape": [
        "gown",
        "bridal",
        "princess skirt",
        "voluminous",
        "ruffle",
        "chiffon",
        "layered skirt",
    ],
    "hat_brim_shadow_closeup": [
        "hat",
        "veil",
        "sundress",
        "bridal",
        "resort",
        "beach",
    ],
    "over_shoulder_bouquet_turn": [
        "bouquet",
        "bridal",
        "gown",
        "dress",
        "flower",
        "lace",
        "fairy",
    ],
}

COMPOSITION_FORBIDDEN_PLAN_TAGS = {
    "foreground_flower_occlusion_closeup": {"pure_white", "poster", "industrial", "aquarium", "beach", "product", "ribbon"},
    "low_angle_under_flower_canopy": {"pure_white", "poster", "industrial", "aquarium", "beach", "product", "ribbon"},
    "flower_frame_clear_face": {"pure_white", "poster", "industrial", "aquarium", "beach", "product", "ribbon"},
    "cinematic_wide_flower_side_view": {"pure_white", "poster", "industrial", "aquarium", "beach", "product", "ribbon"},
    "lace_curtain_backlight_occlusion": {"outdoor", "rooftop", "beach", "aquarium", "pure_white", "mirror", "acrylic", "glass", "ribbon"},
    "diagonal_window_light_haze": {"aquarium", "beach", "mirror", "acrylic", "glass", "ribbon", "product"},
    "soft_relaxed_close_face": {"far_shot", "deep_perspective", "large_space"},
    "high_angle_bed_or_floor_frame": {"low_camera"},
}

FAR_SPACE_COMPOSITION_FORBIDDEN_NAMES = {
    "clean_three_quarter_character_frame",
    "slight_side_medium_close_frame",
    "quiet_close_upper_body_frame",
    "soft_relaxed_close_face",
    "hat_brim_shadow_closeup",
}

SCENE_COMPOSITION_ALLOWLIST = {
    "beach_wind_open_sand": {
        *GENERIC_COMPOSITION_NAMES,
        "floor_diagonal_negative_space",
        "hat_brim_shadow_closeup",
        "soft_relaxed_close_face",
    },
    "record_shop_listening_corner": {
        *GENERIC_COMPOSITION_NAMES,
        "hat_brim_shadow_closeup",
        "soft_relaxed_close_face",
    },
    "planetarium_star_dome": {
        *GENERIC_COMPOSITION_NAMES,
        "hat_brim_shadow_closeup",
        "soft_relaxed_close_face",
        "floor_diagonal_negative_space",
    },
    "pure_white_character_focus": {
        "pure_white_social_close_portrait",
        "pure_white_half_body_social_photo",
        "pure_white_three_quarter_editorial_frame",
        "pure_white_full_body_editorial_frame",
    },
}


def _composition_plan_compatible(composition_plan, plan, action=None, outfit_direction=None):
    plan = plan or {}
    plan_name = plan.get("name", "")
    composition_name = composition_plan.get("name", "")
    plan_tags = _tags_of(plan)
    action_name = (action or {}).get("name", "")
    outfit_text = (outfit_direction or plan.get("outfit_direction", "")).lower()

    if plan_tags & COMPOSITION_FORBIDDEN_PLAN_TAGS.get(composition_name, set()):
        return False

    if composition_name in COMPOSITION_REQUIRED_PLAN_NAMES:
        if plan_name not in COMPOSITION_REQUIRED_PLAN_NAMES[composition_name]:
            return False

    forbidden_actions = COMPOSITION_FORBIDDEN_ACTIONS.get(composition_name, set())
    if action_name and action_name in forbidden_actions:
        return False

    allowed_actions = COMPOSITION_ALLOWED_ACTIONS.get(composition_name)
    if allowed_actions and action_name and action_name not in allowed_actions:
        return False

    if composition_name == "gray_studio_large_dress_shape":
        if "studio" not in plan_tags:
            return False

    if plan_tags & {"far_shot", "deep_perspective", "large_space"}:
        if composition_name in FAR_SPACE_COMPOSITION_FORBIDDEN_NAMES:
            return False

    allowed_outfit_keywords = COMPOSITION_ALLOWED_OUTFIT_KEYWORDS.get(composition_name)
    if allowed_outfit_keywords and outfit_text:
        if not any(keyword in outfit_text for keyword in allowed_outfit_keywords):
            return False

    if plan_name in SCENE_COMPOSITION_ALLOWLIST:
        return composition_name in SCENE_COMPOSITION_ALLOWLIST[plan_name]

    if composition_name in FLOWER_COMPOSITION_NAMES:
        return (
            plan_name in FLOWER_COMPOSITION_PLANS
            or bool(plan_tags & FLOWER_COMPOSITION_TAGS)
        )

    if composition_name in INTERIOR_COMPOSITION_NAMES:
        return (
            plan_name in INTERIOR_COMPOSITION_PLANS
            or bool(plan_tags & INTERIOR_COMPOSITION_TAGS)
        )

    return True


def choose_composition_plan(recent_tags=None, plan=None, action=None, outfit_direction=None):
    recent = _recent_set(recent_tags)
    plan_tags = _tags_of(plan or {})
    composition_pool = [
        composition_plan for composition_plan in COMPOSITION_PLANS
        if _composition_plan_compatible(composition_plan, plan, action, outfit_direction)
    ]
    if not composition_pool:
        composition_pool = [
            composition_plan for composition_plan in COMPOSITION_PLANS
            if composition_plan.get("name") in GENERIC_COMPOSITION_NAMES
        ] or COMPOSITION_PLANS
    scored = []
    for composition_plan in composition_pool:
        tags = _tags_of(composition_plan)
        score = COMPOSITION_BASE_WEIGHTS.get(composition_plan.get("name", ""), 0.4)
        tag_bonus = 0.08 if composition_plan.get("name") in GENERIC_COMPOSITION_NAMES else 0.25
        score += len(tags & plan_tags) * tag_bonus
        score -= len(tags & recent) * 0.35
        scored.append((max(score, 0.15), composition_plan))
    total = sum(score for score, _ in scored)
    pick = random.random() * total
    cursor = 0.0
    for score, composition_plan in scored:
        cursor += score
        if pick <= cursor:
            return dict(composition_plan)
    return dict(scored[-1][1])


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
    return "keep the character medium-readable; face, hair silhouette, eyes, outfit shape, and main accessories stay clear"


OUTFIT_COLOR_RELATIONSHIPS = [
    "choose a cohesive chromatic outfit colorway independent from the main hair color, using identity colors only as tiny accessory accents",
    "choose a medium-value fashion colorway with clear separation from both the hair and the background",
    "choose a dark or deep muted outfit colorway that complements the character without copying the hair color",
    "choose an earthy or softly saturated outfit colorway with one model-chosen dominant family",
    "choose a balanced editorial colorway where clothing has its own visible color presence instead of defaulting to white",
]

OUTFIT_COLOR_HARMONY_RULE = (
    "keep the outfit palette cohesive and wearable; white, ivory, cream, and pale gray are occasional supporting values, "
    "not the default main outfit color; avoid random clashing colors, rainbow mixing, harsh neon contrast, "
    "or too many unrelated accent colors"
)


def outfit_variation_for(character_name, outfit_direction=None):
    profile = _profile_for(character_name)
    base = outfit_direction if outfit_direction else random.choice(OUTFIT_DIRECTIONS)
    color_relationship = random.choice(OUTFIT_COLOR_RELATIONSHIPS)
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
    if outfit_has_fixed_colorway(base):
        return (
            f"{base}{sanrio_detail}{eyewear_detail}; clothing must be opaque fabric, never clear plastic, vinyl, PVC, or see-through outerwear; "
            "preserve the explicitly stated garment color relationship as the outfit's main colorway; keep the palette cohesive and do not add unrelated accent colors; "
            f"character palette remains identity-only ({profile['color_anchor']}); keep hairstyle, hair color, eye color, and core accessories"
        )
    return (
        f"{base}{sanrio_detail}{eyewear_detail}; clothing must be opaque fabric, never clear plastic, vinyl, PVC, or see-through outerwear; outfit colors are not specified; "
        f"{color_relationship}; {OUTFIT_COLOR_HARMONY_RULE}; character palette is identity-only ({profile['color_anchor']}) and should not become a full outfit color lock; "
        "keep hairstyle, hair color, eye color, and core accessories"
    )


def outfit_has_fixed_colorway(outfit_direction):
    text = str(outfit_direction or "")
    return any(text.startswith(theme) for theme in FIXED_COLOR_OUTFIT_DIRECTIONS)


def outfit_prop_rule_for(outfit_direction):
    text = str(outfit_direction or "").lower()
    rules = []
    if "glasses" in text or "eyewear" in text:
        rules.append("glasses may remain worn naturally but must not hide the eyes")
    if "hat" in text or "cap" in text:
        rules.append("headwear may remain worn naturally but must not hide the face or signature hair silhouette")
    if "bouquet" in text:
        rules.append("a small bouquet may appear beside the body without covering the face or outfit silhouette")
    if "bag" in text:
        rules.append("a small bag may hang naturally from the shoulder or rest beside the body")
    return "; ".join(rules)


def outfit_material_rule_for(outfit_direction):
    text = str(outfit_direction or "").lower()
    rules = []
    soft_materials = ("satin", "lace", "chiffon", "silk", "knit", "cotton", "sweatshirt", "jersey", "tulle", "mesh")
    if "leather" in text and any(keyword in text for keyword in soft_materials):
        rules.append(
            "leather texture and leather shine apply only to the explicitly leather garment; all other garments remain "
            "soft flexible textiles; never spread leather, latex, vinyl, PVC, plastic, or wet-look shine onto them"
        )
    if "velvet" in text and any(keyword in text for keyword in ("chiffon", "blazer", "tailored", "shirt", "lace", "satin")):
        rules.append(
            "velvet remains a dense soft-pile fabric with restrained plush highlights only on the velvet garment; "
            "chiffon stays lightweight and airy, while tailored fabric stays matte and structured"
        )
    if "satin" in text and "lace" in text:
        rules.append(
            "satin keeps a soft flexible low-gloss drape, while lace remains delicate matte textile lace rather than "
            "shiny leather, latex, vinyl, PVC, or molded plastic"
        )
    if "lace" in text and "denim" in text:
        rules.append(
            "lace remains delicate matte textile with opaque lining, while denim remains sturdy woven twill; "
            "do not merge their textures"
        )
    if ("knit" in text or "sweater" in text) and any(keyword in text for keyword in ("denim", "corduroy", "shirt", "blouse")):
        rules.append(
            "knitwear remains soft looped yarn, clearly separate from woven denim, corduroy, shirt, or blouse fabric"
        )
    return "; ".join(rules)
