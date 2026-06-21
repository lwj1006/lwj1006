from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from fenjue.modes.original.plans import propagation_profile_for, required_identity_tokens_for


PROJECT_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_ROOT = PROJECT_DIR / "templatesE"
IMAGE_EXTENSIONS = (".jpeg", ".jpg", ".png", ".webp")


CHARACTER_PHOTOSET_ADAPTATIONS = {
    "千夏": (
        "Chinatsu adaptation: compact youthful anime proportions, cute approachable face, soft cheerful expression, "
        "petite-to-average height impression, not a tall mature fashion-model silhouette. Keep her mint gray-green short layered hair, "
        "large mint bow, soft asymmetrical bangs, and pink-gold eyes. Scale the template pose and furniture relationship to her body; "
        "do not lengthen legs, enlarge bust/hips, sharpen the face into a mature model, or give her template-reference hair."
    ),
}


GENERAL_CHARACTER_ADAPTATION = (
    "Adapt the photoset to the selected character's original age impression, height impression, body proportions, facial softness, "
    "and personality. The template pose is a geometry guide, not a body-shape guide. Do not stretch a short or youthful character into "
    "a tall mature model, and do not borrow the reference person's body type."
)


A3_HAND_DRAWN_STYLE = (
    "Mode 3 style: keep the original photoset prompt and composition, but render it as unmistakable hand-drawn Japanese 2D anime art. "
    "Visible clean black lineart must outline the face, hair silhouette, eyes, hands, clothing edges, fabric folds, props, and key furniture. "
    "Use cel-shaded anime forms with soft painted gradients, simplified smooth anime skin, stylized large eyes, graphic hair strand groups, "
    "and illustration-like color separation. The room can keep photographic composition and lighting, but the final surface must look drawn, "
    "not photographed. Prefer a polished anime key visual / light-novel cover finish over semi-realistic digital painting."
)


A3_NEGATIVE = (
    "photorealistic, hyperrealistic, live-action photo, cosplay photo, DSLR photo, realistic skin pores, photographic skin texture, "
    "semi-realistic face, 3D render, doll, plastic figure, waxy skin, no lineart, invisible outlines, overly soft airbrushed edges, "
    "oil painting realism, realistic human portrait, raw photo, film still"
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
    ids = [path.name for path in root.iterdir() if path.is_dir() and (path / f"{path.name}.md").exists()]
    return sorted(ids, key=lambda value: _template_sort_key(value))


def list_template_ids(root: Path = TEMPLATE_ROOT) -> list[str]:
    ids: list[str] = []
    for base_id in list_base_template_ids(root):
        ids.append(_variant_template_id(base_id, "a3"))
    return sorted(ids, key=_template_sort_key)


def _heading_pattern() -> re.Pattern[str]:
    return re.compile(r"^#{1,3}\s+Image\s+(\d+)\b\s*(?:\W+\s*(.*?))?\s*$", re.MULTILINE)


def _section_between(text: str, start_pattern: str, stop_pattern: str = r"^#{1,3}\s+") -> str:
    match = re.search(start_pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    stop = re.search(stop_pattern, text[start:], flags=re.MULTILINE)
    end = start + stop.start() if stop else len(text)
    return text[start:end].strip()


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
    (re.compile(r"\boff[- ]shoulder\b", re.IGNORECASE), "soft draped neckline"),
    (re.compile(r"\bstrapless\b", re.IGNORECASE), "structured evening neckline"),
    (re.compile(r"\bthin\s+straps?\b", re.IGNORECASE), "delicate shoulder straps"),
    (re.compile(r"\blingerie[- ](?:inspired|like)\b", re.IGNORECASE), "delicate fashion"),
    (re.compile(r"\blingerie\b", re.IGNORECASE), "delicate fashionwear"),
    (re.compile(r"\bsemi[- ]transparent\b", re.IGNORECASE), "airy layered"),
    (re.compile(r"\btransparent\b", re.IGNORECASE), "airy layered"),
    (re.compile(r"\btranslucent\b", re.IGNORECASE), "airy layered"),
    (re.compile(r"\bsheer\b", re.IGNORECASE), "light layered"),
    (re.compile(r"\bsee[- ]through\b", re.IGNORECASE), "light layered"),
    (re.compile(r"\bwet[- ]skin\s+detail\b", re.IGNORECASE), "dewy skin highlights"),
    (re.compile(r"\bwet\s+skin\s+droplets\b", re.IGNORECASE), "dewy highlight details"),
    (re.compile(r"\bcleavage\b", re.IGNORECASE), "neckline detail"),
    (re.compile(r"\bunderboob\b|\bsideboob\b", re.IGNORECASE), "unsafe crop"),
    (re.compile(r"\bnude\b", re.IGNORECASE), "neutral"),
)


def _compact(text: str, limit: int) -> str:
    squashed = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(squashed) <= limit:
        return squashed
    return squashed[:limit].rsplit(" ", 1)[0].strip()


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
    return cleaned.strip(" ,\n")


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
    cleaned = _remove_template_identity_traits(text)
    cleaned = _soften_platform_sensitive_terms(cleaned)
    cleaned = re.sub(r"\bthe selected character\b", character_name, cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bHer\b", f"{character_name}'s", cleaned)
    cleaned = re.sub(r"\bher\b", f"{character_name}'s", cleaned)
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


def _parse_shots(folder: Path, markdown: str) -> tuple[PhotosetShot, ...]:
    matches = list(_heading_pattern().finditer(markdown))
    shots: list[PhotosetShot] = []
    for position, match in enumerate(matches):
        index = int(match.group(1))
        title = (match.group(2) or f"Image {index}").strip()
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(markdown)
        section = markdown[start:end].strip()
        ready = _section_between(section, r"^##\s+\d+\.\s+Ready-to-Use Prompt\s*$")
        negative = _section_between(section, r"^##\s+\d+\.\s+Negative Prompt\s*$")
        shots.append(
            PhotosetShot(
                index=index,
                title=title,
                reference_image=_image_path(folder, index),
                section_text=section[:7000].strip(),
                ready_prompt=ready[:3500].strip(),
                negative_prompt=negative[:1800].strip(),
            )
        )
    return tuple(shots)


def load_template(template_id: str | int, root: Path = TEMPLATE_ROOT) -> PhotosetTemplate:
    normalized = normalize_template_id(template_id)
    base_id = _base_template_id(normalized)
    folder = root / base_id
    markdown_path = folder / f"{base_id}.md"
    if not markdown_path.exists():
        available = ", ".join(list_template_ids(root)) or "none"
        raise FileNotFoundError(f"Photoset template {normalized} was not found. Available templates: {available}")
    markdown = markdown_path.read_text(encoding="utf-8")
    shots = _parse_shots(folder, markdown)
    if not shots:
        raise ValueError(f"Photoset template {normalized} has no '# Image N' sections.")
    missing_images = [shot.index for shot in shots if shot.reference_image is None]
    if missing_images:
        raise ValueError(f"Photoset template {normalized} is missing reference images for shots: {missing_images}")
    return PhotosetTemplate(
        template_id=normalized,
        folder=folder,
        markdown_path=markdown_path,
        global_identity=_global_identity(markdown),
        shots=shots,
    )


def _is_adapted_template(template: PhotosetTemplate) -> bool:
    return template.template_id.lower().endswith("_adapted")


def _is_a3_template(template: PhotosetTemplate) -> bool:
    return template.template_id.upper().endswith("_A_3")


def _prompt_for_original_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    ready_block = shot.ready_prompt or shot.section_text
    negative_block = shot.negative_prompt or (
        "Avoid identity drift, extra people, duplicated body parts, broken hands, unreadable face, "
        "text, watermark, logo, oversexualized framing, and copying the reference person's face."
    )
    return f"""
Independent image task. Create exactly one finished anime-style photoset image.

Uploaded character reference images define the identity of {character_name}. The photoset reference image defines only this shot's design: outfit language, pose, camera, lighting, environment, composition, and mood. Replace the reference person's identity with {character_name}; do not copy the reference person's face.

[PHOTOSET]
Template: {template.template_id}
Shot: {shot.index} / {len(template.shots)}
Shot title: {shot.title}

[GLOBAL PHOTOSET IDENTITY]
{template.global_identity}

[SHOT-SPECIFIC PROMPT]
{ready_block}

[CHARACTER IDENTITY OVERRIDE]
The final subject is {character_name}. Preserve {character_name}'s uploaded-reference identity, face design, hairstyle, eye color, fixed accessories, species traits, and personality signals. The photoset styling may adapt clothing, pose, lighting, and setting only.

[CONTINUITY RULE]
This image belongs to one coherent photoset. Keep the same outfit system, hair styling logic, color grade, environment family, and photographic language described above, while executing this shot's unique pose and camera.

[NEGATIVE]
{negative_block}
""".strip()


def _prompt_for_adapted_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    ready_block = _adapt_shot_prompt(character_name, shot.ready_prompt or shot.section_text)
    global_style = _compact(_soften_platform_sensitive_terms(_remove_template_identity_traits(template.global_identity)), 1800)
    negative_block = shot.negative_prompt or (
        "Avoid identity drift, extra people, duplicated body parts, broken hands, unreadable face, "
        "text, watermark, logo, oversexualized framing, and copying the reference person's face."
    )
    negative_block = _soften_platform_sensitive_terms(_remove_template_identity_traits(negative_block))
    return f"""
Independent image task. Create exactly one finished anime-style photoset image.

[HIGHEST PRIORITY: CHARACTER LOCK]
The final subject is {character_name}. Character reference images override every person-related detail in the photoset template and photoset reference image.
{_profile_identity_block(character_name)}
{_character_adaptation(character_name)}

[REFERENCE PRIORITY]
1. Character reference images define identity: face, eyes, hair color, exact hairstyle, bangs, body proportions, fixed accessories, species traits, age impression, and personality.
2. Photoset reference image defines only picture design: camera distance, crop, pose geometry, hand/leg placement, subject size in frame, furniture/window/prop placement, light direction, shadow pattern, color grade, and room atmosphere.
3. Template markdown defines outfit category, scene objects, camera language, and lighting plan only after the character lock is satisfied.
Never copy the photoset reference person's face, hair color, hairstyle, bangs, height, mature body type, or personal identity.

[PHOTOSET]
Template: {template.template_id}
Shot: {shot.index} / {len(template.shots)}
Shot title: {shot.title}

[COLOR AND LIGHT MATCH]
Match the photoset reference color logic closely: bright window-side daylight, cream wall values, golden afternoon highlights, soft nostalgic low-contrast air, readable black clothing, and visible window-shadow geometry. Avoid turning the room into a dark brown antique interior, heavy sepia grade, muddy shadows, over-dramatic oil-paint lighting, or a generic fantasy study. Preserve the left-window brightness and airy editorial lifestyle feeling.

[COMPACT PHOTOSET STYLE]
{global_style}

[SHOT DESIGN PROMPT - IDENTITY WORDS ALREADY FILTERED]
{ready_block}

[ADAPTATION RULE]
Use the pose as a pose, not as a body transplant. Adjust stool height, leg length impression, camera crop, and facial maturity so the same composition fits {character_name}. If any template wording conflicts with {character_name}'s profile or references, delete the template wording mentally and keep {character_name}.

[CONTINUITY RULE]
This image belongs to one coherent photoset. Keep the outfit system, room family, lighting direction, color grade, props, and photographic language consistent across the set. Do not use template hair styling or template body type as continuity; character continuity comes only from {character_name}'s references.

[NEGATIVE]
{negative_block}
Keep the styling elegant and editorial, but avoid platform-sensitive revealing framing, clothing slipping, overly revealing light-layered clothing, or body-part emphasis.
Identity drift, wrong hairstyle, wrong hair color, copied reference-person face, copied reference-person hair silhouette, changed bangs, changed body proportions, tall mature model body when the character is youthful, overlong legs, enlarged bust, mature sharp face, dark brown/sepia color cast, muddy shadows, low-key fantasy room.
""".strip()


def _prompt_for_a3_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    base_prompt = _prompt_for_adapted_shot(character_name, template, shot)
    return f"""
{base_prompt}

[MODE 3 HAND-DRAWN ANIME STYLE ADDENDUM]
{A3_HAND_DRAWN_STYLE}

[MODE 3 EXTRA NEGATIVE]
{A3_NEGATIVE}
""".strip()


def prompt_for_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
    if _is_a3_template(template):
        return _prompt_for_a3_shot(character_name, template, shot)
    if _is_adapted_template(template):
        return _prompt_for_adapted_shot(character_name, template, shot)
    return _prompt_for_original_shot(character_name, template, shot)
