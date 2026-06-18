from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_ROOT = PROJECT_DIR / "templatesE"
IMAGE_EXTENSIONS = (".jpeg", ".jpg", ".png", ".webp")


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


def list_template_ids(root: Path = TEMPLATE_ROOT) -> list[str]:
    if not root.exists():
        return []
    return sorted(path.name for path in root.iterdir() if path.is_dir() and (path / f"{path.name}.md").exists())


def _heading_pattern() -> re.Pattern[str]:
    return re.compile(r"^#\s+Image\s+(\d+)\b\s*(?:\W+\s*(.*?))?\s*$", re.MULTILINE)


def _section_between(text: str, start_pattern: str, stop_pattern: str = r"^#{1,3}\s+") -> str:
    match = re.search(start_pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    stop = re.search(stop_pattern, text[start:], flags=re.MULTILINE)
    end = start + stop.start() if stop else len(text)
    return text[start:end].strip()


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
    folder = root / normalized
    markdown_path = folder / f"{normalized}.md"
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


def prompt_for_shot(character_name: str, template: PhotosetTemplate, shot: PhotosetShot) -> str:
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
