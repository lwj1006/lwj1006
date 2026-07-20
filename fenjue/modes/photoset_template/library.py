from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from fenjue.modes.original.plans import propagation_profile_for, required_identity_tokens_for

from .extended_templates import (
    EXTENDED_IMAGE_INDICES,
    EXTENDED_SHOT_TITLES,
    SHOT_OUTFIT_OVERRIDES,
    STANDARD_NEGATIVE_PROMPT,
)


PROJECT_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_ROOT = PROJECT_DIR / "templatesE"
IMAGE_EXTENSIONS = (".jpeg", ".jpg", ".png", ".webp")


CHARACTER_PHOTOSET_ADAPTATIONS = {
    "千夏": (
        "Chinatsu adaptation: keep compact youthful proportions, a cute soft face, and a petite-to-average height impression. "
        "Keep the jaw-to-nape short-bob foundation, thick asymmetrical clipped fringe, and only one mid-high half-up side ponytail. "
        "The ponytail ornament is a large faceted teal four-point star shape, never a bow; do not expand the half-up ponytail into a full high ponytail or long hair. "
        "Scale the pose and furniture to her body; do not create a tall mature silhouette, elongated legs, enlarged proportions, "
        "a sharp mature face, or the photoset model's hair."
    ),
    "铃": (
        "Belle adaptation: keep a lively youthful academy-girl impression, short deep blue-violet bob hair, a large side-swept bang, "
        "teal-blue eyes, the orange N-shaped hair clip, and small teal earrings clear in every shot. Adapt the photoset pose to her "
        "compact bright silhouette; do not copy the photoset model's long hair, mature body type, heavy glamour face, or unrelated hair accessories. "
        "Music-shop props, a portable CD player, student cap, or academy uniform are optional reference motifs only, not mandatory outfit locks."
    ),
    "扳机": (
        "Trigger adaptation: preserve her creamy-blonde high ponytail, opaque glossy black eye visor, paired red triangular mechanical hair clips, "
        "black rear hair fixtures, and thin yellow cable. The visor must stay opaque and cover both eyes in every camera angle. "
        "Do not copy the photoset model's eyes, eyewear, hairstyle, weapons, or mature glamour identity."
    ),
    "诺姆": (
        "Nome adaptation: preserve compact youthful proportions, golden-blonde blunt bangs, long low braided tails, violet-blue eyes, and the oversized "
        "silver-gray cylindrical mechanical helmet with two dark antennae and circular side plates. The antennae are machine parts, not animal ears. "
        "Scale furniture and poses to the small silhouette; never copy a mature model body, remove the helmet, or add the reference companion."
    ),
    "今汐": (
        "Jinhsi adaptation: preserve exactly two extremely long low side tails of pearl-white hair with pale aqua feather-like ends, bronze openwork side anchors, "
        "translucent aqua bows, clear aqua eyes, and a small red forehead mark. Never convert the hairstyle into loose hair, one ponytail, or short twin tails. "
        "Dragons, weapons, and ceremonial clothing in the references are optional scene elements, not identity requirements."
    ),
    "坎特蕾拉": (
        "Cantarella adaptation: preserve the long wavy violet hair with indigo ends, violet-pink eyes with cyan inner highlights, narrow white ruffled headband, "
        "and blue-violet side flower ornament. The parasol visible in the references is a removable handheld prop, never a hat or part of her silhouette. "
        "Do not include an umbrella or parasol unless the selected photoset explicitly requires one."
    ),
    "秧秧": (
        "Yangyang adaptation: preserve the short dark crown hair, broad white-to-cyan feather-shaped side and rear locks, blue-gray eyes, slim vertical forehead mark, "
        "and small gold bird ornaments with a red tassel. Do not flatten the feather-shaped hair layers into ordinary long blue hair. "
        "The bird companion, loose feathers, weapons, and reference clothing are optional and must not be copied by default."
    ),
    "绯雪": (
        "Feixue adaptation: preserve one high rounded white topknot above very long loose silver-white rear hair, red eyes, the small black-red forehead ornament, "
        "and compact youthful proportions. The long rear hair remains loose and must never become a high ponytail."
    ),
    "长离": (
        "Changli adaptation: preserve the short coral-pink crown and side fringe over one extremely long pearl-white rear ponytail, two slim white braided face locks, "
        "amber-gold eyes, and bronze flower-shaped side ornaments. Keep the two-tone hair structure distinct; never make all of the hair uniformly white or red."
    ),
    "卡提希娅": (
        "Cartethyia adaptation: keep her very long golden-blonde hair, clear blue eyes, long pointed elf ears, blue-silver branching crown ornament, "
        "and blue teardrop earrings visible. Never hide or round off the elf ears, and do not copy the photoset model's hairstyle."
    ),
    "莫宁": (
        "Morning adaptation: keep her pale silver-blue one-eye fringe, visible red eye, extremely long rear hair, triangular clips and earrings, "
        "and the floating dark crystal halo. The halo must remain a separate hovering structure, never a hat or solid headband."
    ),
    "菲比": (
        "Phoebe adaptation: preserve her very long wavy blonde hair, violet eyes, blue cross hair clip, and oversized white wide-brim hat with its blue feather. "
        "Do not replace the broad hat or blonde side curls with the photoset model's headwear or hairstyle."
    ),
    "西格莉卡": (
        "Sigrika adaptation: preserve the extremely voluminous vivid-orange hair divided into multiple coherent segmented bubble-braid tails, bright green eyes, "
        "and white hood-like headpiece. Do not simplify the hair into one ponytail or copy the photoset model's hair volume."
    ),
    "诀": (
        "Jue adaptation: preserve the short silver-white and pale-mint face-framing bob plus very long high-back locks, violet-cyan eyes, red outer-eye markings, "
        "and the vertical red forehead mark. Keep two distinct feather structures: tall upright black crown tufts with white inner blades and broad horizontal "
        "white-gray side crests. Never merge them into one headdress or reinterpret them as mammal ears or a hat."
    ),
    "洛茜": (
        "Rossi adaptation: preserve the warm blonde curls, amber-gold eyes, two tall fox ears, and one enormous fluffy golden fox tail. "
        "Keep a human face and limbs; never omit the tail, add extra tails, or force the red hood and combat outfit."
    ),
    "庄方宜": (
        "Zhuang Fangyi adaptation: preserve the very long dark green hair with red and teal face-framing layers, green-gold eyes, paired silver temple clips, "
        "two very large high angular black-crimson branching horns, pointed ears, and one long scaled teal tail. Never shrink the horns into hair ornaments, "
        "replace them with mammal ears, omit the tail, or copy the reference uniform and weapons."
    ),
    "艾尔黛拉": (
        "Ardelia adaptation: keep compact youthful proportions, a short chestnut crown bob, and one enormous high rear-side ponytail formed by a thick loop, "
        "a slim braid, and a long hanging length. Preserve the rose-magenta eyes, medium gray ridged outward-curving horns, dark pointed Caprinae ears, "
        "and red-blue hair clips. Never shrink the horns, copy the pink companion, or force medical clothing."
    ),
    "佩丽卡": (
        "Perlica adaptation: preserve the enormous high fountain ponytail of silver-white hair, ice-blue eyes, softly separated bangs, and the large sharp "
        "horizontal gray-white Liberi side crests with darker tips. The side crests are feathers, not small clips or cat ears; never reduce their scale or "
        "replace them with the photoset model's hairstyle."
    ),
    "陈千语": (
        "Chen Qianyu adaptation: keep compact youthful proportions, short tousled black crown hair with two very long rear twin tails, red-orange eyes, "
        "two narrow red-teal-edged dragon horns, and one continuous dark dragon tail with a colored fin tip. Never omit or duplicate the tail."
    ),
    "弭弗": (
        "Mi Fu adaptation: preserve the voluminous pale pink-white wavy hair, heavy one-eye fringe, multicolored cyan-rose eyes, long pointed ears, "
        "and two huge dark navy branching horns with cyan edges. Keep both horns attached at the temples; never shrink them into hair clips or copy the photoset hair."
    ),
}


GENERAL_CHARACTER_ADAPTATION = (
    "Adapt the photoset to the selected character's original age impression, height impression, body proportions, facial softness, "
    "and personality. The template pose is a geometry guide, not a body-shape guide. Do not stretch a short or youthful character into "
    "a tall mature model, and do not borrow the reference person's body type."
)


A3_HAND_DRAWN_STYLE = (
    "Render the original composition as a premium hand-drawn Japanese anime key visual. Keep clean black lineart visible around the face, eyes, "
    "hair masses, hands, garment edges, folds, and important props, with elegant line-weight variation rather than thick uniform outlines. "
    "Use refined layered cel shading, restrained soft transitions, detailed irises, carefully grouped hair locks, nuanced fabric texture, and luminous "
    "illustrated light. Preserve a clearly drawn 2D surface while achieving polished light-novel-cover finish; avoid both photographic realism and cheap flat coloring."
)


A3_NEGATIVE = (
    "photorealistic, live-action, cosplay, semi-realistic face, 3D render, game CG, painterly rendering, "
    "realistic skin texture, pores, glossy realistic lips, modeled nostrils, airbrushed face, invisible lineart, "
    "photographic depth of field, lens bokeh, individual realistic hair strands, crude flat coloring, low-detail face, "
    "generic anime avatar, thick uniform outlines, rough sketch, muddy colors"
)


ANIME_FACE_DETAIL = (
    "Preserve the selected character's canonical anime face design from the character references. "
    "Match the current photoset reference's emotional intent through precise gaze direction, upper- and lower-eyelid opening, "
    "eyebrow angle, cheek tension, head tilt, and mouth shape, but never copy the reference model's facial identity. "
    "Draw crisp upper lash lines, readable lower lashes, layered iris color, centered pupils, and two controlled catchlights. "
    "Use only a tiny graphic anime nose mark and a small simplified anime mouth line, never modeled nostrils or volumetric glossy lips. "
    "Use restrained illustrated blush with a controlled soft transition. Keep both eyes aligned and equally finished. "
    "Avoid a blank stare, generic smile, frozen doll face, asymmetrical eyes, muddy pupils, photographic lips, or an unfinished face."
)


@dataclass(frozen=True)
class PhotosetShot:
    index: int
    title: str
    reference_image: Path | None
    section_text: str
    ready_prompt: str
    negative_prompt: str


@dataclass(frozen=True)
class PhotosetTemplate:
    template_id: str
    folder: Path
    markdown_path: Path
    global_identity: str
    shots: tuple[PhotosetShot, ...]


def normalize_template_id(value: str | int) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError("Template id cannot be empty.")
    if text.isdigit():
        return f"{int(text):03d}"
    return text


def _variant_for(template_id: str) -> str:
    upper = template_id.upper()
    if upper.endswith("_A_3"):
        return "a3"
    if template_id.lower().endswith("_adapted"):
        return "adapted"
    return "original"


def _base_template_id(template_id: str) -> str:
    if template_id.upper().endswith("_A_3"):
        return template_id[:-4]
    if template_id.lower().endswith("_adapted"):
        return template_id[:-8]
    return template_id


def _variant_template_id(base_id: str, variant: str) -> str:
    if variant == "adapted":
        return f"{base_id}_adapted"
    if variant == "a3":
        return f"{base_id}_A_3"
    return base_id


def _template_sort_key(template_id: str) -> tuple[int, int, str]:
    base_id = _base_template_id(template_id)
    match = re.match(r"^(\d+)", base_id)
    number = int(match.group(1)) if match else 999999
    variant_order = {"original": 0, "adapted": 1, "a3": 2}[_variant_for(template_id)]
    return number, variant_order, template_id


def list_base_template_ids(root: Path = TEMPLATE_ROOT) -> list[str]:
    if not root.exists():
        return []
    ids = [
        path.name
        for path in root.iterdir()
        if path.is_dir() and any(path.glob("*.md"))
    ]
    return sorted(ids, key=lambda value: _template_sort_key(value))


def list_template_ids(root: Path = TEMPLATE_ROOT) -> list[str]:
    ids: list[str] = []
    for base_id in list_base_template_ids(root):
        ids.append(_variant_template_id(base_id, "a3"))
    return sorted(ids, key=_template_sort_key)


def _heading_pattern() -> re.Pattern[str]:
    return re.compile(
        r"^#{1,3}\s+(?:(?:\d+|[A-Za-z]+)\.\s*)?Image\s+0*(?P<index>\d+)\b\s*(?:[-—:]+\s*(?P<title>.*?))?\s*$",
        re.IGNORECASE | re.MULTILINE,
    )


def _section_between(text: str, start_pattern: str, stop_pattern: str = r"^#{1,3}\s+") -> str:
    match = re.search(start_pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    stop = re.search(stop_pattern, text[start:], flags=re.MULTILINE)
    end = start + stop.start() if stop else len(text)
    return text[start:end].strip()


def _first_code_or_inline_prompt(text: str) -> str:
    fenced = re.search(r"```(?:text|prompt)?\s*\n(.*?)\n```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    inline = re.search(r"`([^`]{80,})`", text, flags=re.DOTALL)
    if inline:
        return inline.group(1).strip()
    return text.strip()


def _named_prompt_block(section: str) -> str:
    labels = r"(?:Ready-to-Use Prompt|Reusable Prompt|Prompt Block|Prompt Notes|可复用提示词)"
    block = _section_between(section, rf"^#{{2,4}}\s+(?:\d+(?:\.\d+)?\.?\s+)?{labels}\s*$")
    return _first_code_or_inline_prompt(block) if block else ""


IDENTITY_SENSITIVE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r",?\s*(?:and\s+)?long\s+dark\s+twin[- ]tail\s+hair", re.IGNORECASE), ""),
    (re.compile(r",?\s*(?:and\s+)?dark\s+twin[- ]tail\s+hair", re.IGNORECASE), ""),
    (re.compile(r",?\s*(?:and\s+)?long\s+dark\s+hair(?:\s+falling\s+to\s+the\s+side)?", re.IGNORECASE), ""),
    (re.compile(r"^-\s*long\s+dark\s+hair.*$", re.IGNORECASE | re.MULTILINE), ""),
    (re.compile(r"^-\s*dark\s+twin[- ]tail\s+hair\.?\s*$", re.IGNORECASE | re.MULTILINE), ""),
    (re.compile(r"^-\s*long\s+dark\s+hair\s+styled\s+into\s+twin\s+tails\s+or\s+side-tied\s+sections\.?\s*$", re.IGNORECASE | re.MULTILINE), ""),
    (re.compile(r"\bwith\s+long\s+dark\s+twin[- ]tail\s+hair\b", re.IGNORECASE), ""),
    (re.compile(r"\byoung\s+adult\s+woman\b", re.IGNORECASE), "the selected character"),
    (re.compile(r"\ba\s+young\s+adult\s+woman\b", re.IGNORECASE), "the selected character"),
)

PLATFORM_SENSITIVE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bbare\s+upper\s+back\b", re.IGNORECASE), "elegant back-facing pose with airy fabric coverage"),
    (re.compile(r"\bdelicate\s+bare\s+back\b", re.IGNORECASE), "delicate back-facing pose with fabric coverage"),
    (re.compile(r"\bbare\s+back\b", re.IGNORECASE), "back-facing pose with fabric coverage"),
    (re.compile(r"\bexposed\s+shoulders?\b", re.IGNORECASE), "soft shoulder-line styling with secure fabric coverage"),
    (re.compile(r"\bshoulders?\s+exposed\b", re.IGNORECASE), "shoulder line softly framed by fabric"),
    (re.compile(r"\bexposed\s+leg\b", re.IGNORECASE), "leg line shaped by the gown movement"),
    (re.compile(r"\brevealing\s+skin\s+and\s+collarbone\b", re.IGNORECASE), "soft collar area with secure fabric coverage"),
    (re.compile(r"\brevealing\s+(?:a\s+)?(?:thin\s+)?(?:white\s+)?camisole\s+strap(?:\s+and\s+pale\s+white\s+underlayer)?\b", re.IGNORECASE), "with a secure inner layer visible"),
    (re.compile(r"\brevealing\s+the\s+airy\s+quality\s+of\s+the\s+fabric\b", re.IGNORECASE), "showing the soft movement of the fabric"),
    (re.compile(r"\brevealing\s+delicate\s+white\s+inner\s+structure\b", re.IGNORECASE), "showing delicate layered white structure"),
    (re.compile(r"\bno\s+revealing\s+emphasis\b", re.IGNORECASE), "no body-emphasis framing"),
    (re.compile(r"\brevealing\b", re.IGNORECASE), "securely styled"),
    (re.compile(r"\bslipped\s+off\s+one\s+shoulder\b", re.IGNORECASE), "softly draped with secure shoulder coverage"),
    (re.compile(r"\boff\s+one\s+shoulder\b", re.IGNORECASE), "softly draped with secure shoulder coverage"),
    (re.compile(r"\boff[- ]shoulder\b", re.IGNORECASE), "soft draped neckline"),
    (re.compile(r"\bstrapless\b", re.IGNORECASE), "structured evening neckline"),
    (re.compile(r"\bthin\s+straps?\b", re.IGNORECASE), "delicate shoulder straps"),
    (re.compile(r"\bfloral\s+organza\s+dress\b", re.IGNORECASE), "floral chiffon dress with opaque lining"),
    (re.compile(r"\bpale\s+floral\s+organza\s+fabric\b", re.IGNORECASE), "pale floral chiffon fabric with opaque lining"),
    (re.compile(r"\borganza\b", re.IGNORECASE), "matte chiffon"),
    (re.compile(r"\bairy\s+layered\s+fabric\b", re.IGNORECASE), "soft layered fabric with opaque lining"),
    (re.compile(r"\blayered\s+airy\s+skirt\b", re.IGNORECASE), "layered skirt with a clear sewn silhouette"),
    (re.compile(r"\blayered\s+airy\b", re.IGNORECASE), "layered with a clear sewn silhouette"),
    (re.compile(r"\bairy\s+layered\b", re.IGNORECASE), "soft layered cloth"),
    (re.compile(r"\blingerie[- ](?:inspired|like)\b", re.IGNORECASE), "delicate fashion"),
    (re.compile(r"\blingerie\b", re.IGNORECASE), "delicate fashionwear"),
    (re.compile(r"\bsemi[- ]transparent\b", re.IGNORECASE), "soft opaque layered fabric"),
    (re.compile(r"\btransparent\b", re.IGNORECASE), "glasslike"),
    (re.compile(r"\btranslucent\b", re.IGNORECASE), "soft opaque layered fabric"),
    (re.compile(r"\bsheer\b", re.IGNORECASE), "soft opaque layered"),
    (re.compile(r"\bsee[- ]through\b", re.IGNORECASE), "soft opaque layered"),
    (re.compile(r"\bwet[- ]skin\s+detail\b", re.IGNORECASE), "dewy skin highlights"),
    (re.compile(r"\bwet\s+skin\s+droplets\b", re.IGNORECASE), "dewy highlight details"),
    (re.compile(r"\bcleavage\b", re.IGNORECASE), "neckline detail"),
    (re.compile(r"\bunderboob\b|\bsideboob\b", re.IGNORECASE), "unsafe crop"),
    (re.compile(r"\bbikini\b", re.IGNORECASE), "sporty blue poolwear with secure coverage"),
    (re.compile(r"\bnude\b", re.IGNORECASE), "neutral"),
)


ANIME_POSITIVE_REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bphotorealistic\b|\bhyperrealistic\b", re.IGNORECASE), "high-detail hand-drawn anime illustration"),
    (re.compile(r"\brealistic skin texture\b|\brealistic skin\b", re.IGNORECASE), "smooth cel-shaded anime skin"),
    (re.compile(r"\bhigh[- ]end editorial photography\b|\beditorial photography\b", re.IGNORECASE), "polished anime editorial illustration"),
    (re.compile(r"\bfashion photography\b", re.IGNORECASE), "anime fashion illustration"),
    (re.compile(r"\bportrait photography\b", re.IGNORECASE), "anime portrait illustration"),
    (re.compile(r"\bprofessional photography\b", re.IGNORECASE), "professional anime illustration"),
    (re.compile(r"\bfilm photography\b", re.IGNORECASE), "anime film-inspired color treatment"),
    (re.compile(r"\bfilm still\b", re.IGNORECASE), "anime cinematic keyframe"),
    (re.compile(r"\bDSLR photo\b|\blive-action photo\b|\braw photo\b", re.IGNORECASE), "hand-drawn anime image"),
    (re.compile(r"\bno anime skin texture\b", re.IGNORECASE), "no photographic skin texture"),
    (re.compile(r"\brealistic anime\b", re.IGNORECASE), "polished hand-drawn anime"),
    (re.compile(r"\bpainterly realism\b", re.IGNORECASE), "hand-drawn cel-shaded anime illustration"),
    (re.compile(r"\bJapanese photobook aesthetic\b", re.IGNORECASE), "Japanese light-novel illustration aesthetic"),
    (re.compile(r"\bphotobook\b", re.IGNORECASE), "illustration series"),
    (re.compile(r"\bphotoshoot\b|\bphoto shoot\b", re.IGNORECASE), "illustration set"),
    (re.compile(r"\b\d{2,3}\s*mm(?:\s+portrait)?\s+lens\b", re.IGNORECASE), "reference-matched portrait framing"),
    (re.compile(r"\bportrait lens\b", re.IGNORECASE), "portrait framing"),
    (re.compile(r"\bshallow depth of field\b", re.IGNORECASE), "layered anime depth with a simplified background"),
    (re.compile(r"\bsoft focus\b", re.IGNORECASE), "soft-edged illustrated background"),
    (re.compile(r"\bbokeh\b", re.IGNORECASE), "simplified painted light shapes"),
    (re.compile(r"\brealistic fabric texture\b", re.IGNORECASE), "clearly drawn fabric folds and texture"),
    (re.compile(r"\b(?:fair|luminous|clear|dewy) skin\b", re.IGNORECASE), "clean flat cel-shaded anime complexion"),
    (re.compile(r"\bnatural skin tone\b", re.IGNORECASE), "flat anime skin palette"),
    (re.compile(r"\bcinematic lighting\b", re.IGNORECASE), "graphic anime lighting"),
    (re.compile(r"\bpainted illumination\b", re.IGNORECASE), "luminous illustrated anime lighting"),
    (re.compile(r"\bpainted light\b", re.IGNORECASE), "luminous illustrated anime light"),
    (re.compile(r"\bsmooth stylized anime skin\b", re.IGNORECASE), "refined cel-shaded anime skin"),
    (re.compile(r"\bsoft painted gradients\b", re.IGNORECASE), "restrained soft transitions within layered cel shading"),
    (re.compile(r"\ba (?:clearly drawn|clear) lip line\b", re.IGNORECASE), "a small simplified anime mouth line"),
)


TEMPLATE_PERSON_TRAIT_CLAUSE = re.compile(
    r"\b(?:adult(?:-presenting)?|young adult|woman|model|hair|hairstyle|bangs|"
    r"hairpins?|hair ornaments?|hair accessories|braids?|braided|buns?|ponytails?|"
    r"pigtails?|twin[- ]tails?|updo|makeup|eyeliner|eyeshadow|lipstick|lips|skin|"
    r"eyes?|lashes|eyelashes|cheeks|blush|complexion|facial features|nose|mouth|gaze|"
    r"expression|smile|face stickers?|beauty mark|tiara|flower crown|headpiece|"
    r"glitter under (?:her|the) eyes|body type|slender body|curvy body)\b",
    re.IGNORECASE,
)

PROTECTED_INSTRUCTION_LINE = re.compile(
    r"^(?:\[|#|---|`|Reference-matched|Create a hand-drawn\b|Never\b|Character references\b|"
    r"The uploaded character references\b|The current photoset reference\b|"
    r"Preserve the exact garment\b|Render as\b)",
    re.IGNORECASE,
)


def _remove_template_person_clauses(text: str) -> str:
    """Discard the photoset model's appearance while retaining shot design evidence."""
    kept_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        protected_instruction = PROTECTED_INSTRUCTION_LINE.match(stripped)
        if protected_instruction:
            kept_lines.append(line)
            continue
        clauses = re.split(r"\s*[,;]\s*", line)
        kept = [clause.strip() for clause in clauses if clause.strip() and not TEMPLATE_PERSON_TRAIT_CLAUSE.search(clause)]
        if kept:
            kept_lines.append(", ".join(kept))
    return "\n".join(kept_lines).strip()


def _remove_character_trait_conflicts(character_name: str, text: str) -> str:
    identity = " ".join(required_identity_tokens_for(character_name)).lower()
    cleaned = text
    has_nonhuman_ears = (
        ("animal ears" in identity and "no animal ears" not in identity)
        or "tiger ears" in identity
        or "elf ears" in identity
    )
    has_horns = "horns" in identity
    has_tail = "tail" in identity
    if has_nonhuman_ears or has_horns:
        cleaned = re.sub(
            r"\b(?:human ears only|no real animal ears|real animal ears|no animal ears|"
            r"cat ears|bear ears growing from (?:the )?head)\b",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
    if has_tail:
        cleaned = re.sub(r"\b(?:no (?:animal )?tail|animal tail)\b", "", cleaned, flags=re.IGNORECASE)
    if has_nonhuman_ears:
        cleaned = re.sub(
            r"\s*(?:decorated with|with)\s+two\s+(?:soft\s+)?(?:plush\s+)?(?:caramel\s+)?"
            r"(?:teddy\s+)?bear\s+ears(?:\s+attached\s+to\s+the\s+hat|\s+on\s+the\s+hat\s+only)?",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
    cleaned = re.sub(r",\s*,+", ",", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip(" ,\n")


POSTURE_WORDS = re.compile(
    r"\b(?:stand(?:s|ing)?|standing|sit(?:s|ting)?|seated|lie|lies|lying|"
    r"recline[sd]?|reclining|kneel(?:s|ing)?|kneeling|walk(?:s|ing)?|walking|"
    r"crouch(?:es|ing)?|crouching|prone|supine)\b",
    re.IGNORECASE,
)
POSE_ACTION_WORDS = re.compile(
    r"\b(?:look(?:s|ing)?|gaze[sd]?|gazing|touch(?:es|ing)?|hold(?:s|ing)?|"
    r"reach(?:es|ing)?|raise[sd]?|raising|rest(?:s|ing)?|lean(?:s|ing)?|"
    r"turn(?:s|ing)?|smell(?:s|ing)?|hug(?:s|ging)?|present(?:s|ing)?)\b",
    re.IGNORECASE,
)
HAND_ACTION_WORDS = re.compile(
    r"\b(?:touch(?:es|ing)?|hold(?:s|ing)?|reach(?:es|ing)?|raise[sd]?|raising|"
    r"rest(?:s|ing)?|grasp(?:s|ing)?|grip(?:s|ping)?|carry|carries|carrying|"
    r"present(?:s|ing)?|adjust(?:s|ing)?|brush(?:es|ing)?)\b",
    re.IGNORECASE,
)
CHOICE_WORDS = re.compile(r"\b(?:or|either|alternatively)\b", re.IGNORECASE)
CAMERA_CHOICE_WORDS = re.compile(
    r"\b(?:\d{2,3}\s*mm|wide[- ]angle|telephoto|close[- ]up|tight portrait|"
    r"half[- ]body|waist[- ]up|knee[- ]up|full[- ]body|overhead|high[- ]angle|low[- ]angle)\b",
    re.IGNORECASE,
)
EXPRESSION_CHOICE_WORDS = re.compile(
    r"\b(?:look(?:s|ing)?|gaze[sd]?|gazing|eyes? closed|closing (?:the )?eyes?|"
    r"smile[sd]?|smiling|side profile|front profile|expression)\b",
    re.IGNORECASE,
)
MULTI_SHOT_TRANSITION_WORDS = re.compile(
    r"\b(?:two[- ]part|first half|front half|back half|second half|then|later|"
    r"adjacent shots?|depending on (?:the )?shot|across the set)\b",
    re.IGNORECASE,
)


def _remove_ambiguous_pose_and_camera_choices(text: str) -> str:
    """Remove set-wide alternatives that conflict with one current shot image."""
    text = re.sub(
        r"\b(?:\d{2,3}\s*mm\s*(?:to|[-–—])\s*\d{2,3}\s*mm|"
        r"\d{2,3}\s*(?:to|[-–—])\s*\d{2,3}\s*mm)\b",
        "reference-matched focal length",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\b\d{2,3}\s*mm\s*(?:or|/|to|[-–—])\s*\d{2,3}\s*mm(?:\s+portrait)?\s+lens\b",
        "reference-matched lens perspective",
        text,
        flags=re.IGNORECASE,
    )
    kept_lines: list[str] = []
    for line in text.splitlines():
        if PROTECTED_INSTRUCTION_LINE.match(line.strip()):
            kept_lines.append(line)
            continue
        kept_sentences: list[str] = []
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            sentence = sentence.strip()
            if not sentence:
                continue
            if re.search(r"\b(?:pose|camera|framing)\s+(?:options?|variations?|choices?)\s*:", sentence, re.IGNORECASE):
                continue
            postures = {match.lower() for match in POSTURE_WORDS.findall(sentence)}
            actions = {match.lower() for match in POSE_ACTION_WORDS.findall(sentence)}
            hand_actions = {match.lower() for match in HAND_ACTION_WORDS.findall(sentence)}
            expressions = {match.lower() for match in EXPRESSION_CHOICE_WORDS.findall(sentence)}
            has_choice = bool(CHOICE_WORDS.search(sentence))
            has_clause_breaks = "," in sentence or ";" in sentence
            if len(postures) >= 2 and not has_clause_breaks:
                continue
            if has_choice and not has_clause_breaks and len(sentence) < 500 and len(postures) + len(actions) >= 2:
                continue
            if has_choice and not has_clause_breaks and len(expressions) >= 2:
                continue

            kept_clauses: list[str] = []
            for clause in re.split(r"\s*[,;]\s*", sentence):
                clause = clause.strip()
                if not clause:
                    continue
                if MULTI_SHOT_TRANSITION_WORDS.search(clause):
                    continue
                clause_has_choice = bool(CHOICE_WORDS.search(clause))
                clause_actions = POSE_ACTION_WORDS.findall(clause)
                clause_hands = HAND_ACTION_WORDS.findall(clause)
                clause_cameras = CAMERA_CHOICE_WORDS.findall(clause)
                if clause_has_choice:
                    continue
                if len({item.lower() for item in clause_cameras}) >= 2 and re.search(r"\b(?:and|or|to)\b", clause, re.IGNORECASE):
                    kept_clauses.append("reference-matched camera framing and perspective")
                    continue
                kept_clauses.append(clause)
            if kept_clauses:
                kept_sentences.append(", ".join(kept_clauses))
        if kept_sentences:
            kept_lines.append(" ".join(kept_sentences))
    return "\n".join(kept_lines).strip()


def _has_cjk(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def _english_only_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if _has_cjk(line):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"```(?:text|prompt)?\s*\n\s*```", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def _english_title(text: str, fallback: str) -> str:
    cleaned = _english_only_text(text).strip(" -—:|/")
    if cleaned:
        cleaned = _soften_platform_sensitive_terms(cleaned)
    return cleaned or fallback


def _prompt_subject_name(character_name: str) -> str:
    return "the selected character"


def _compact(text: str, limit: int) -> str:
    squashed = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(squashed) <= limit:
        return squashed
    return squashed[:limit].rsplit(" ", 1)[0].strip()


def _dedupe_negative_terms(*blocks: str) -> str:
    terms: list[str] = []
    seen: set[str] = set()
    for block in blocks:
        for raw_term in re.split(r"[,\n]+", block):
            term = raw_term.strip(" `.-")
            key = term.casefold()
            if term and key not in seen:
                seen.add(key)
                terms.append(term)
    return ", ".join(terms)


def _remove_template_identity_traits(text: str) -> str:
    cleaned = text
    for pattern, replacement in IDENTITY_SENSITIVE_PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    cleaned = re.sub(r"\s+,", ",", cleaned)
    cleaned = re.sub(r",\s*,", ",", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = re.sub(r"\n\s*\n\s*\n+", "\n\n", cleaned)
    return cleaned.strip(" ,\n")


def _soften_platform_sensitive_terms(text: str) -> str:
    cleaned = text
    for pattern, replacement in PLATFORM_SENSITIVE_PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    cleaned = re.sub(r"\bsoft opaque layered fabric fabric\b", "soft opaque layered fabric", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bwith opaque lining with soft opaque layered fabric\b", "with opaque lining and soft layered fabric", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bsoft opaque layered pastel floral chiffon dress with opaque lining with soft opaque layered fabric\b", "soft opaque layered pastel floral chiffon dress with opaque lining and soft layered fabric", cleaned, flags=re.IGNORECASE)
    return cleaned.strip(" ,\n")


def _anime_only_positive_text(text: str) -> str:
    cleaned = text
    for pattern, replacement in ANIME_POSITIVE_REPLACEMENTS:
        cleaned = pattern.sub(replacement, cleaned)
    return cleaned.strip()


TRAILING_SET_WIDE_SECTION = re.compile(
    r"^#{1,4}\s+(?:Cross[- ]Image\b|Set[- ]Wide\b|Best Use Cases\b|"
    r"Prompt Construction Formula\b|Example Master Prompt\b|Negative Prompt Suggestions\b|"
    r"Final Practical Summary\b)",
    re.IGNORECASE | re.MULTILINE,
)


def _simplify_verbose_environment(text: str) -> str:
    if len(text) <= 3500:
        return text
    pattern = re.compile(
        r"(?P<head>^##\s+\d+\.\s+Environment(?:\s*&\s*Props)?[^\n]*\n)"
        r"(?P<body>.*?)(?=^##\s+\d+\.|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    def compact(match: re.Match[str]) -> str:
        lines = [line.strip() for line in match.group("body").splitlines() if line.strip()]
        intro = next(
            (line for line in lines if not line.startswith("-") and not line.endswith(":")),
            "Keep the main environment shown in the final reference.",
        )
        anchors = [line for line in lines if line.startswith("-")][:8]
        anchor_text = "\n".join(anchors)
        return f"{match.group('head')}{intro}\nMain background anchors:\n{anchor_text}\n"

    return pattern.sub(compact, text)


def _current_shot_only(text: str) -> str:
    """Drop set-wide advice accidentally stored after a single-shot prompt."""
    match = TRAILING_SET_WIDE_SECTION.search(text)
    current = text[: match.start()].rstrip(" -\n") if match else text
    current = re.sub(
        r"^##\s+\d+\.\s+Narrative(?:\s*/\s*Mood)?\b.*?(?=^##\s+\d+\.|\Z)",
        "",
        current,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    ).strip()
    return _simplify_verbose_environment(current)


def _character_adaptation(character_name: str) -> str:
    return CHARACTER_PHOTOSET_ADAPTATIONS.get(character_name, GENERAL_CHARACTER_ADAPTATION)


def _profile_identity_block(character_name: str) -> str:
    profile = propagation_profile_for(character_name)
    tokens = "; ".join(required_identity_tokens_for(character_name))
    return (
        f"Official identity: {profile['official_core']}\n"
        f"Must keep visible: {tokens}.\n"
        f"Character behavior: {profile['interaction_rule']}\n"
        f"Color identity anchor: {profile['color_anchor']}"
    )


def _adapt_shot_prompt(character_name: str, text: str) -> str:
    cleaned = _remove_template_person_clauses(_current_shot_only(text))
    cleaned = _remove_template_identity_traits(cleaned)
    cleaned = _remove_character_trait_conflicts(character_name, cleaned)
    cleaned = _soften_platform_sensitive_terms(cleaned)
    cleaned = _remove_ambiguous_pose_and_camera_choices(cleaned)
    subject_name = _prompt_subject_name(character_name)
    cleaned = _english_only_text(cleaned)
    cleaned = _anime_only_positive_text(cleaned)
    cleaned = re.sub(r"`{2,3}(?:text|prompt)?", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bthe selected character\b", subject_name, cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bthe model\b", subject_name, cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def _global_identity(markdown: str) -> str:
    match = _heading_pattern().search(markdown)
    preface = markdown[: match.start()].strip() if match else markdown.strip()
    return preface[:5000].strip()


def _image_path(folder: Path, index: int) -> Path | None:
    for suffix in IMAGE_EXTENSIONS:
        candidate = folder / f"{index}{suffix}"
        if candidate.exists():
            return candidate
    return None


def _markdown_path(folder: Path, base_id: str) -> Path | None:
    standard = folder / f"{base_id}.md"
    if standard.exists():
        return standard
    candidates = sorted(folder.glob("*.md"))
    return candidates[0] if candidates else None


def _english_full_prompt(markdown: str) -> str:
    match = re.search(
        r"^##\s+\d+\.\s+English Prompt[^\n]*\n(?P<body>.*?)(?=^##\s+\d+\.)",
        markdown,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    return match.group("body").strip() if match else ""


def _remove_reference_person_sentences(text: str) -> str:
    person_terms = re.compile(
        r"\b(?:young adult|woman|girl|hair|bangs|face|facial|skin|makeup|blush|lashes|"
        r"eyeliner|eyeshadow|eyes|lips|expression|body shape|body type)\b",
        flags=re.IGNORECASE,
    )
    sentences = re.split(r"(?<=[.!?])\s+", text)
    kept = [sentence for sentence in sentences if not person_terms.search(sentence)]
    return " ".join(kept).strip()


def _extended_shots(folder: Path, base_id: str, markdown: str) -> tuple[PhotosetShot, ...]:
    titles = EXTENDED_SHOT_TITLES.get(base_id)
    indices = EXTENDED_IMAGE_INDICES.get(base_id)
    if not titles or not indices:
        return ()

    source = _english_full_prompt(markdown)
    source = _remove_reference_person_sentences(source)
    source = _soften_platform_sensitive_terms(source)
    source = _compact(source, 2600)
    shots: list[PhotosetShot] = []
    for index, title in zip(indices, titles):
        outfit_override = SHOT_OUTFIT_OVERRIDES.get((base_id, index), "")
        outfit_line = f"Exact outfit for this shot: {outfit_override}\n" if outfit_override else ""
        prompt = f"""Reference-matched photoset shot: {title}.
The uploaded character references are the only authority for identity, hairstyle, hair ornaments, face, age impression, height, and body proportions. Never copy those person traits from the photoset reference.
The current photoset reference image is the authority for camera height, crop, body placement, pose geometry, hand contact, garment construction, props, room layout, light direction, and color grade. Reproduce this exact shot rather than an average of the set.
{outfit_line}{source}
Keep every garment visibly sewn and wearable: preserve its category, neckline, straps or sleeves, waist position, hem length, layering, fabric weight, trim, pattern, and opaque lining. Adapt the same outfit to the selected character's canonical proportions without changing the design.
Render as polished hand-drawn Japanese 2D anime art with visible clean black line art, controlled cel shading, painted light, and no photographic skin texture."""
        shots.append(
            PhotosetShot(
                index=index,
                title=title,
                reference_image=_image_path(folder, index),
                section_text=prompt.strip(),
                ready_prompt=prompt.strip(),
                negative_prompt=STANDARD_NEGATIVE_PROMPT,
            )
        )
    return tuple(shots)


def _parse_shots(folder: Path, markdown: str) -> tuple[PhotosetShot, ...]:
    matches = list(_heading_pattern().finditer(markdown))
    shots: list[PhotosetShot] = []
    for position, match in enumerate(matches):
        index = int(match.group("index"))
        title = _english_title(match.group("title") or "", f"Image {index}")
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(markdown)
        section = markdown[start:end].strip()
        ready = _section_between(section, r"^##\s+\d+\.\s+Ready-to-Use Prompt\s*$") or _named_prompt_block(section)
        negative = _section_between(section, r"^##\s+\d+\.\s+Negative Prompt\s*$")
        shots.append(
            PhotosetShot(
                index=index,
                title=title,
                reference_image=_image_path(folder, index),
                section_text=_compact(section, 7000),
                ready_prompt=_compact(ready, 3500),
                negative_prompt=_compact(negative, 1800),
            )
        )
    return tuple(shots)


def load_template(template_id: str | int, root: Path = TEMPLATE_ROOT) -> PhotosetTemplate:
    normalized = normalize_template_id(template_id)
    base_id = _base_template_id(normalized)
    folder = root / base_id
    markdown_path = _markdown_path(folder, base_id)
    if markdown_path is None:
        available = ", ".join(list_template_ids(root)) or "none"
        raise FileNotFoundError(f"Photoset template {normalized} was not found. Available templates: {available}")
    markdown = markdown_path.read_text(encoding="utf-8")
    shots = _parse_shots(folder, markdown)
    if not shots:
        shots = _extended_shots(folder, base_id, markdown)
    if not shots:
        raise ValueError(f"Photoset template {normalized} has no '# Image N' sections.")
    missing_images = [shot.index for shot in shots if shot.reference_image is None]
    if missing_images:
        raise ValueError(f"Photoset template {normalized} is missing reference images for shots: {missing_images}")
    return PhotosetTemplate(
        template_id=normalized,
        folder=folder,
        markdown_path=markdown_path,
        global_identity=(
            _remove_reference_person_sentences(
                _english_full_prompt(markdown) or _english_only_text(_global_identity(markdown))
            )
            if base_id in EXTENDED_SHOT_TITLES
            else _english_only_text(_global_identity(markdown))
        ),
        shots=shots,
    )


def _is_adapted_template(template: PhotosetTemplate) -> bool:
    return template.template_id.lower().endswith("_adapted")


def _is_a3_template(template: PhotosetTemplate) -> bool:
    return template.template_id.upper().endswith("_A_3")


def _prompt_for_original_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    subject_name = _prompt_subject_name(character_name)
    ready_block = _english_only_text(shot.ready_prompt or shot.section_text)
    negative_block = shot.negative_prompt or (
        "Avoid identity drift, extra people, duplicated body parts, broken hands, unreadable face, "
        "text, watermark, logo, oversexualized framing, and copying the reference person's face."
    )
    return f"""
Independent image task. Create exactly one finished anime-style photoset image.

Uploaded character reference images define the identity of {subject_name}. The photoset reference image defines only this shot's design: outfit language, pose, camera, lighting, environment, composition, and mood. Replace the reference person's identity with {subject_name}; do not copy the reference person's face.

[PHOTOSET]
Template: {template.template_id}
Shot: {shot.index} / {len(template.shots)}
Shot title: {shot.title}

[GLOBAL PHOTOSET IDENTITY]
{template.global_identity}

[SHOT-SPECIFIC PROMPT]
{ready_block}

[CHARACTER IDENTITY OVERRIDE]
The final subject is {subject_name}. Preserve the uploaded-reference identity, face design, hairstyle, eye color, fixed accessories, species traits, and personality signals. The photoset styling may adapt clothing, pose, lighting, and setting only.

[CONTINUITY RULE]
This image belongs to one coherent photoset. Keep the same outfit system, hair styling logic, color grade, environment family, and photographic language described above, while executing this shot's unique pose and camera.

[NEGATIVE]
{negative_block}
""".strip()


def _prompt_for_adapted_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    subject_name = _prompt_subject_name(character_name)
    ready_block = _adapt_shot_prompt(character_name, shot.ready_prompt or shot.section_text)
    global_style = _compact(
        _anime_only_positive_text(
            _english_only_text(
                _soften_platform_sensitive_terms(
                    _remove_character_trait_conflicts(
                        character_name,
                        _remove_template_person_clauses(
                            _remove_template_identity_traits(template.global_identity)
                        ),
                    )
                )
            )
        ),
        1800,
    )
    negative_block = shot.negative_prompt or (
        "Avoid identity drift, extra people, duplicated body parts, broken hands, unreadable face, "
        "text, watermark, logo, oversexualized framing, and copying the reference person's face."
    )
    negative_block = _soften_platform_sensitive_terms(_remove_template_identity_traits(negative_block))
    negative_block = _remove_character_trait_conflicts(character_name, negative_block)
    return f"""
Independent image task. Create exactly one finished anime-style photoset image.

[HIGHEST PRIORITY: CHARACTER LOCK]
The final subject is {subject_name}. Character reference images override every person-related detail in the photoset template and photoset reference image.
{_profile_identity_block(character_name)}
{_character_adaptation(character_name)}

[REFERENCE PRIORITY]
1. Character reference images define identity: face, eyes, hair color, exact hairstyle, bangs, body proportions, fixed accessories, species traits, age impression, and personality.
2. Photoset reference image defines only picture design: camera distance, crop, pose geometry, hand/leg placement, subject size in frame, furniture/window/prop placement, light direction, shadow pattern, color grade, and room atmosphere.
3. Template markdown defines outfit category, scene objects, camera language, and lighting plan only after the character lock is satisfied.
Never copy the photoset reference person's face, hair color, hairstyle, bangs, height, mature body type, or personal identity.

[UPLOADED IMAGE ROLE MAP]
All uploaded images except the final image are character-reference images. Read them together only for canonical face geometry, eye design, exact hair silhouette and bangs, fixed head accessories, fixed jewelry, species traits, age impression, and body proportions. Their clothing, costume colors, weapons, staffs, tools, hand poses, body poses, backgrounds, lighting, and scene props are not transferable and must not appear merely because they are visible in the character references.
If a character-reference image contains multiple people, identify the target as the person consistently repeated across the complete character-reference set. Every companion, crossover character, background person, partial face, and overlapping body belongs to someone else and must be ignored. Never merge another person's hair, face, eyes, ears, accessories, clothing, or body into the selected character.
The final uploaded image is the current photoset reference. It alone defines this shot's garment, pose, hand contacts, camera, crop, set, props, light direction, and color palette. It is never a rendering-style reference: do not copy its photographic skin, realistic face, individual hair strands, lens blur, bokeh, retouching, or surface realism. Its person identity, face, hairstyle, bangs, makeup, hair ornaments, body type, and age impression are not transferable.

[EXCLUSIVE OUTFIT SOURCE LOCK]
Build the outfit exclusively from the final photoset reference image. First match its base garment color, garment category, silhouette, neckline, shoulder construction, sleeves or straps, bodice structure, waist position, skirt or trouser construction, hem, layering, fabric weight, trim, pattern, appliques, and opaque lining. Do not reuse, recolor toward, hybridize with, or add any garment, armor, uniform, cape, sleeve, stocking, footwear, weapon harness, or costume ornament visible in the character-reference images. The selected character keeps only fixed identity accessories; every changeable clothing item comes from the final photoset image.

[SINGLE POSE, CAMERA, AND ANATOMY LOCK]
The current single photoset reference image is the sole authority for this shot's camera and body action. Execute only the one pose visibly shown in that image. Never combine alternate standing, sitting, reclining, leaning, looking, touching, or prop actions from set-wide prose. Match one camera distance, one crop, one viewing angle, and one perspective from the current image; never average lens or framing alternatives.
Preserve normal two-arm anatomy. Account for every visible shoulder, elbow, wrist, and hand as one continuous limb. Each visible hand performs exactly the contact shown in the current reference and interacts with at most one prop or body area. A hand or arm hidden by the crop, hair, flowers, furniture, or the torso stays hidden; do not invent a replacement hand. Keep the torso supported by the same chair, table, floor, bed, wall, or standing leg shown in the reference. Do not add decorative hands, duplicated fingers, extra arms, or impossible joints to fill negative space.

[PHOTOSET]
Template: {template.template_id}
Shot: {shot.index} / {len(template.shots)}
Shot title: {shot.title}

[COLOR AND LIGHT MATCH]
Use only the current photoset reference image as the palette and light-direction authority. Match its dominant background hue, white balance, exposure hierarchy, highlight color, shadow color, contrast, saturation, light direction, and broad shadow placement, then translate them into flat graphic anime color regions and hard-edged two-step cel shadows. Do not reproduce photographic skin response, realistic light falloff, lens bloom, bokeh, depth-of-field blur, or airbrushed atmosphere. Do not import cream walls, golden window light, sepia grading, or any palette from a different template.

[FACIAL EXPRESSION PRECISION]
{ANIME_FACE_DETAIL}

[COMPACT PHOTOSET STYLE]
{global_style}

[SHOT DESIGN PROMPT - IDENTITY WORDS ALREADY FILTERED]
{ready_block}

[OUTFIT STRUCTURE LOCK]
The outfit must read as a real finished garment, not decorative material placed on skin. Keep a clear bodice, clear skirt or shorts boundary, stable shoulder construction, secure back coverage, and visible opaque lining. Fabric may be soft, floral, layered, and fairy-like, but it must stay matte, cloth-like, continuous, and sewn together. Keep ruffles attached to the dress, keep flower patterns printed or embroidered on fabric, and translate delicate reference fabric into a coherent matte cloth dress with a finished silhouette.

[ADAPTATION RULE]
Use the pose as a pose, not as a body transplant. Adjust stool height, leg length impression, camera crop, and facial maturity so the same composition fits {subject_name}. If any template wording conflicts with the character profile or references, delete the template wording mentally and keep the uploaded character identity.

[CONTINUITY RULE]
This image belongs to one coherent photoset. Keep only details visibly shared by adjacent reference images. If this shot changes outfit, room, lighting, props, or palette, the current reference image wins. Do not use template hair styling or template body type as continuity; character continuity comes only from {character_name}'s references.

[NEGATIVE]
{negative_block}
Keep the styling elegant and editorial, with stable clothing, opaque lined fabric, a clear sewn garment silhouette, secure shoulder and back coverage, and no body-part emphasis.
Identity drift, wrong hairstyle, wrong hair color, copied reference-person face, copied reference-person hair silhouette, changed bangs, changed body proportions, tall mature model body when the character is youthful, overlong legs, enlarged bust, mature sharp face, dark brown/sepia color cast, muddy shadows, low-key fantasy room.
Third hand, more than two arms, duplicated hand, floating hand, hand emerging from hair or flowers, disconnected wrist, conflicting poses, mixed camera angles, combined lens alternatives, invented off-frame limb.
""".strip()


def _prompt_for_a3_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    subject_name = _prompt_subject_name(character_name)
    shot_prompt = _adapt_shot_prompt(character_name, shot.ready_prompt or shot.section_text)
    if not shot_prompt:
        shot_prompt = (
            f"Follow the visible final photoset reference exactly for this shot: {shot.title}. "
            "Preserve its outfit construction, pose, hand contacts, framing, main setting anchors, light direction, and palette."
        )
    source_negative = _compact(
        _english_only_text(
            _remove_character_trait_conflicts(
                character_name,
                _remove_template_identity_traits(shot.negative_prompt),
            )
        ),
        350,
    )
    negative = _dedupe_negative_terms(
        source_negative,
        A3_NEGATIVE,
        "wrong character, copied photoset-model identity, clothing copied from character references, extra person, "
        "extra arm, third hand, duplicated limb, fused hand, extra fingers, broken joint, impossible pose, "
        "conflicting camera, text, logo, watermark",
    )

    prompt = f"""
Independent image task. Create one finished image.

[STYLE]
Premium hand-drawn Japanese 2D anime key visual with clean visible black lineart and elegant line-weight variation. Use refined layered cel shading, restrained soft transitions, detailed expressive eyes, carefully grouped hair locks, nuanced fabric folds, and luminous illustrated lighting. Keep the main setting anchors and light pattern while simplifying only minor clutter and distant texture. Aim for polished light-novel-cover quality, never a generic flat avatar, rough sketch, photograph, semi-realistic painting, 3D render, cosplay, or live action.

[CHARACTER]
The subject is {subject_name}. Character references define canonical identity and proportions only, never clothing or scene design.
{_profile_identity_block(character_name)}
{_character_adaptation(character_name)}

[REFERENCE ROLES]
All images except the final one define only the target character's face, eyes, hair, fixed identity accessories, species traits, age, and proportions. Ignore companions, outfits, weapons, poses, and backgrounds.
The final image alone defines outfit, pose, hand contacts, camera, crop, set, props, light, and palette. Never copy its person's identity or body type. Visible final-image evidence overrides text.

[SHOT]
Template {template.template_id}, image {shot.index} of {len(template.shots)}: {shot.title}
{shot_prompt}

[FACE AND ANATOMY]
Keep the canonical anime face. Match the final reference's gaze, eyelids, brows, head tilt, and mouth expression. Use aligned detailed eyes, a tiny anime nose mark, and a small mouth line. Preserve exactly two continuous arms and reproduce only visible hand contacts; never invent hidden hands. Adapt the pose to canonical proportions without changing camera or outfit.

[NEGATIVE]
{negative}
""".strip()
    return _english_only_text(prompt)


def prompt_for_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    if _is_a3_template(template):
        return _prompt_for_a3_shot(character_name, template, shot)
    if _is_adapted_template(template):
        return _prompt_for_adapted_shot(character_name, template, shot)
    return _prompt_for_original_shot(character_name, template, shot)
