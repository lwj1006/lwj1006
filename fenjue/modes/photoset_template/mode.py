
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

from .library import PhotosetShot, PhotosetTemplate, list_template_ids, load_template, prompt_for_shot
from .descriptions import template_description


LABEL = "photoset template mode"
PROJECT_DIR = Path(__file__).resolve().parents[3]
COMPLETED_TEMPLATE_FILE = PROJECT_DIR / "config" / "used_character_photoset_templates.json"

_active_templates: tuple[PhotosetTemplate, ...] = ()
_active_characters: tuple[str, ...] = ()
_active_character_schedule: tuple[str, ...] = ()
_active_shot_schedule: tuple[tuple[PhotosetTemplate, PhotosetShot], ...] = ()
_current_shot_index = 0
_last_reference_files_for_shot: list[str] | None = None
_completed_templates_by_character: dict[str, list[str]] = {}


def _option_value(argv: list[str], *names: str) -> str | None:
    upper_names = tuple(name.upper() for name in names)
    for index, argument in enumerate(argv):
        stripped = argument.strip()
        upper = stripped.upper()
        for name in upper_names:
            if upper == name and index + 1 < len(argv):
                return argv[index + 1].strip()
            if upper.startswith(name + "="):
                return stripped.split("=", 1)[1].strip()
    return None


def _display_template_id(template_id: str) -> str:
    if template_id.upper().endswith("_A_3"):
        return template_id[:-4]
    if template_id.endswith("_adapted"):
        return template_id.removesuffix("_adapted") + "_ADD"
    return template_id


def _template_from_menu_token(token: str, available: list[str]) -> str:
    item = token.strip()
    if not item:
        raise ValueError("Empty photoset template selection.")

    # Short menu input: 1 -> first displayed template, 2 -> second displayed template.
    if item.isdigit() and not item.startswith("0"):
        index = int(item)
        if 1 <= index <= len(available):
            return available[index - 1]

    normalized = item
    upper = item.upper()
    if upper.endswith("_ADD"):
        normalized = item[:-4] + "_A_3"
    elif upper.endswith("_ADAPTED"):
        normalized = item[:-8] + "_A_3"
    elif upper.endswith("_A3"):
        normalized = item[:-3] + "_A_3"
    elif upper.endswith("_A_3"):
        normalized = item

    if normalized.isdigit():
        normalized = f"{int(normalized):03d}_A_3"
    elif normalized.upper() not in {template_id.upper() for template_id in available}:
        candidate = f"{normalized}_A_3"
        if candidate.upper() in {template_id.upper() for template_id in available}:
            normalized = candidate
    return normalized


def _split_template_selection(raw: str, available: list[str]) -> list[str]:
    text = raw.strip()
    if not text:
        return []
    lowered = text.lower()
    if lowered in {"all", "*"}:
        return available[:]
    if lowered in {"all_a3", "a3", "all_a_3", "a_3", "mode3", "mode_3"}:
        return available[:]
    if lowered in {"random", "rondom", "shuffle", "all_random", "random_all"}:
        shuffled = available[:]
        random.shuffle(shuffled)
        return shuffled

    selected: list[str] = []
    for part in text.replace("，", ",").replace(" ", ",").split(","):
        item = part.strip()
        if not item:
            continue
        if "-" in item and all(piece.strip().isdigit() for piece in item.split("-", 1)):
            start_text, end_text = item.split("-", 1)
            start, end = int(start_text), int(end_text)
            step = 1 if start <= end else -1
            for number in range(start, end + step, step):
                selected.append(_template_from_menu_token(str(number), available))
            continue
        selected.append(_template_from_menu_token(item, available))
    return selected


def _choose_templates(argv: list[str], batch) -> tuple[PhotosetTemplate, ...]:
    raw = _option_value(argv, "--TEMPLATES", "--TEMPLATE", "--PHOTOSETS", "--PHOTOSET", "--E-TEMPLATES", "--E-TEMPLATE")
    available = list_template_ids()
    if raw:
        selections = _split_template_selection(raw, available)
        return tuple(load_template(template_id) for template_id in selections)

    if batch.noninteractive_selection_enabled():
        return (load_template(available[0]),)

    while True:
        print("")
        print("Choose photoset template(s):")
        for index, template_id in enumerate(available, start=1):
            description = template_description(template_id)
            print(f"  {index}: {description} [{_display_template_id(template_id)}]")
        print("Enter one number, comma-separated numbers, a range like 1-4, exact ids like 001, all, or random.")
        choice = input(f"Photoset template(s) [default {available[0]}]: ").strip() or available[0]
        try:
            selections = _split_template_selection(choice, available)
            if not selections:
                raise ValueError("No photoset templates selected.")
            return tuple(load_template(template_id) for template_id in selections)
        except (FileNotFoundError, ValueError) as exc:
            print(exc)


def _parse_character_selection(raw: str, batch) -> list[str]:
    selected = batch._parse_character_selection(raw)
    if selected is None:
        return batch.CHARACTER_SEQUENCE[:]
    return selected


def _choose_characters(argv: list[str], batch) -> tuple[str, ...]:
    raw = _option_value(argv, "--CHARACTERS", "--CHARACTER", "--E-CHARACTERS", "--E-CHARACTER")
    if raw:
        return tuple(_parse_character_selection(raw, batch))

    if batch.noninteractive_selection_enabled():
        return (batch.CHARACTER_SEQUENCE[0],)

    while True:
        print("")
        print("Choose character(s) for photoset mode:")
        for index, character_name in enumerate(batch.CHARACTER_SEQUENCE, start=1):
            print(f"  {index} = {character_name}")
        print("Input examples: 1 = one character; 1 2 = rotate two characters; 1-3 = rotate a range; names are also OK.")
        choice = input(f"Character(s) [default 1]: ").strip() or "1"
        try:
            selected = _parse_character_selection(choice, batch)
        except ValueError as exc:
            print(f"{exc}. Please try again.")
            continue
        if not selected:
            print("No characters selected. Please try again.")
            continue
        return tuple(selected)


def _load_completed_templates(available: list[str]) -> dict[str, list[str]]:
    if not COMPLETED_TEMPLATE_FILE.exists():
        return {}
    try:
        data = json.loads(COMPLETED_TEMPLATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"Photoset history is invalid; starting fresh: {exc}", flush=True)
        return {}
    if not isinstance(data, dict):
        return {}

    valid_ids = set(available)
    cleaned: dict[str, list[str]] = {}
    for character_name, template_ids in data.items():
        if not isinstance(character_name, str) or not isinstance(template_ids, list):
            continue
        cleaned[character_name] = list(dict.fromkeys(
            template_id for template_id in template_ids
            if isinstance(template_id, str) and template_id in valid_ids
        ))
    return cleaned


def _save_completed_templates(history: dict[str, list[str]]) -> None:
    COMPLETED_TEMPLATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = COMPLETED_TEMPLATE_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(COMPLETED_TEMPLATE_FILE)


def _mark_template_completed(
    character_name: str,
    template: PhotosetTemplate,
    completed: dict[str, list[str]],
    available_count: int,
) -> bool:
    completed_ids = completed.setdefault(character_name, [])
    if template.template_id in completed_ids:
        return False
    completed_ids.append(template.template_id)
    _save_completed_templates(completed)
    print(
        f"Photoset history: {character_name} completed {_display_template_id(template.template_id)}; "
        f"progress {len(completed_ids)}/{available_count} -> {COMPLETED_TEMPLATE_FILE}",
        flush=True,
    )
    return True


def _resolve_template_assignments(
    requested_templates: tuple[PhotosetTemplate, ...],
    characters: tuple[str, ...],
    completed: dict[str, list[str]],
    available_ids: list[str],
) -> tuple[tuple[str, PhotosetTemplate], ...]:
    assignments: list[tuple[str, PhotosetTemplate]] = []
    scheduled_by_character = {character_name: set() for character_name in characters}
    history_changed = False

    for slot_index, requested_template in enumerate(requested_templates):
        character_name = characters[slot_index % len(characters)]
        used_list = completed.setdefault(character_name, [])
        used = set(used_list)
        if len(used) >= len(available_ids):
            used_list.clear()
            used.clear()
            history_changed = True
            print(
                f"Photoset cycle complete for {character_name}: starting a new {len(available_ids)}-template cycle.",
                flush=True,
            )

        scheduled = scheduled_by_character[character_name]
        selected_id = requested_template.template_id
        if selected_id in used or selected_id in scheduled:
            candidates = [
                template_id for template_id in available_ids
                if template_id not in used and template_id not in scheduled
            ]
            if not candidates:
                print(
                    f"Photoset history: {character_name} has no unfinished templates left for this run; "
                    f"skipping requested {_display_template_id(selected_id)}.",
                    flush=True,
                )
                continue
            replacement_id = random.choice(candidates)
            reason = "already completed" if selected_id in used else "already scheduled"
            print(
                f"Photoset history: {character_name} {_display_template_id(selected_id)} is {reason}; "
                f"replaced with {_display_template_id(replacement_id)}.",
                flush=True,
            )
            selected_id = replacement_id

        scheduled.add(selected_id)
        template = requested_template if selected_id == requested_template.template_id else load_template(selected_id)
        assignments.append((character_name, template))

    if history_changed:
        _save_completed_templates(completed)
    return tuple(assignments)


def _build_photoset_schedule(
    templates: tuple[PhotosetTemplate, ...],
    characters: tuple[str, ...],
) -> tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...]:
    schedule: list[tuple[str, PhotosetTemplate, PhotosetShot]] = []
    for template_index, template in enumerate(templates):
        character_name = characters[template_index % len(characters)]
        for shot in template.shots:
            schedule.append((character_name, template, shot))
    return tuple(schedule)


def _build_assigned_photoset_schedule(
    assignments: tuple[tuple[str, PhotosetTemplate], ...],
) -> tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...]:
    return tuple(
        (character_name, template, shot)
        for character_name, template in assignments
        for shot in template.shots
    )


def _active_template_and_shot() -> tuple[PhotosetTemplate, PhotosetShot]:
    if not _active_shot_schedule:
        raise RuntimeError("Photoset mode has no active shot schedule.")
    if _current_shot_index < len(_active_shot_schedule):
        return _active_shot_schedule[_current_shot_index]
    return _active_shot_schedule[-1]


def _active_character_for_shot() -> str:
    if not _active_character_schedule:
        raise RuntimeError("Photoset mode has no active character schedule.")
    if _current_shot_index < len(_active_character_schedule):
        return _active_character_schedule[_current_shot_index]
    return _active_character_schedule[-1]


def _active_template() -> PhotosetTemplate:
    template, _ = _active_template_and_shot()
    return template


def _active_shot() -> PhotosetShot:
    _, shot = _active_template_and_shot()
    return shot


def _total_shots() -> int:
    return len(_active_shot_schedule)


def activate(batch, args=None) -> None:
    global _active_templates, _active_characters, _active_character_schedule, _active_shot_schedule
    global _current_shot_index, _completed_templates_by_character
    argv = list(args or [])
    requested_templates = _choose_templates(argv, batch)
    _active_characters = _choose_characters(argv, batch)
    available_ids = list_template_ids()
    _completed_templates_by_character = _load_completed_templates(available_ids)
    for character_name in _active_characters:
        completed_count = len(_completed_templates_by_character.get(character_name, []))
        print(
            f"Photoset history: {character_name} completed {completed_count}/{len(available_ids)}; "
            f"{len(available_ids) - completed_count} remaining in the current cycle.",
            flush=True,
        )
    assignments = _resolve_template_assignments(
        requested_templates,
        _active_characters,
        _completed_templates_by_character,
        available_ids,
    )
    if not assignments:
        raise RuntimeError("No unfinished photoset templates are available for the selected characters.")
    _active_templates = tuple(template for _, template in assignments)
    photoset_schedule = _build_assigned_photoset_schedule(assignments)
    _active_character_schedule = tuple(character_name for character_name, _, _ in photoset_schedule)
    _active_shot_schedule = tuple((template, shot) for _, template, shot in photoset_schedule)
    _current_shot_index = 0

    original_reference_files_for_character = batch.reference_files_for_character

    def fixed_character_selection():
        print(f"Photoset mode characters: {' / '.join(_active_characters)}", flush=True)
        return list(_active_characters)

    def resolve_photoset_run_character(character_name: str, run_number: int) -> str:
        global _current_shot_index
        _current_shot_index = max(0, min(run_number - 1, _total_shots() - 1))
        return _active_character_for_shot()

    def record_completed_photoset_run(character_name: str, run_number: int) -> None:
        schedule_index = run_number - 1
        if not 0 <= schedule_index < len(photoset_schedule):
            return
        scheduled_character, template, shot = photoset_schedule[schedule_index]
        if character_name != scheduled_character or shot is not template.shots[-1]:
            return

        _mark_template_completed(
            character_name,
            template,
            _completed_templates_by_character,
            len(available_ids),
        )

    def skip_scene_selection():
        print("Original scene menu skipped: photoset mode uses the selected template shots.", flush=True)
        return None

    def skip_clothing_selection():
        print("Original clothing menu skipped: photoset mode uses the selected template outfit system.", flush=True)
        return None

    def reference_files_for_photoset(character_name: str) -> list[str]:
        global _last_reference_files_for_shot
        shot = _active_shot()
        character_refs = original_reference_files_for_character(character_name)
        _last_reference_files_for_shot = [*character_refs, str(shot.reference_image)]
        return _last_reference_files_for_shot

    def choose_photoset_plan_and_action(
        character_name,
        recent_visual_tags,
        used_themes_by_character,
        used_plans_by_character,
        batch_used_themes=None,
        batch_used_plans=None,
        allowed_plan_names=None,
    ):
        shot = _active_shot()
        plan = {
            "name": f"photoset_{_active_template().template_id}_shot_{shot.index:02d}",
            "graphic_concept": shot.title,
            "spatial_structure": shot.title,
            "visual_device": f"photoset reference image {shot.index}",
            "lighting_behavior": "use the selected photoset shot lighting from the markdown and reference image",
            "color_strategy": "use the selected photoset color grade and continuity system",
            "material_language": "use the selected photoset outfit and fabric language",
            "body_silhouette": shot.title,
            "outfit_direction": f"photoset {_active_template().template_id} outfit system",
            "tags": {"photoset_template", f"photoset_{_active_template().template_id}", f"shot_{shot.index:02d}"},
        }
        action = {
            "name": f"photoset_shot_{shot.index:02d}",
            "body_silhouette": shot.title,
            "personality_logic": "follow the selected shot's facial expression and body language",
            "support_rule": "follow the selected shot's hands, props, pose, and environment supports",
            "avoid_rule": "avoid changing the photoset continuity or copying the reference person's identity",
            "tags": {"photoset_action", f"shot_{shot.index:02d}"},
        }
        return plan, action

    def choose_photoset_clothing(character_name, art_plan, used_by_character, batch_used_themes=None):
        return art_plan["outfit_direction"]

    def keep_photoset_outfit(character_name, theme, art_plan):
        return theme, False

    def choose_photoset_shot_scale(recent_tags=None, plan=None):
        shot = _active_shot()
        return {"name": f"photoset_shot_{shot.index:02d}_camera", "description": shot.title, "tags": {"photoset_camera"}}

    def choose_photoset_composition(recent_tags=None, plan=None, action=None, outfit_direction=None):
        shot = _active_shot()
        return {"name": f"photoset_shot_{shot.index:02d}_composition", "composition": shot.title, "tags": {"photoset_composition"}}

    def prompt_for_photoset(
        character_name,
        art_plan=None,
        action_style=None,
        recent_tags=None,
        visual_design=None,
        outfit_direction=None,
        shot_scale=None,
        composition_plan=None,
    ):
        global _current_shot_index
        shot = _active_shot()
        template = _active_template()
        prompt = prompt_for_shot(character_name, template, shot)
        _current_shot_index += 1
        return prompt

    def collect_photoset_tags(art_plan, action_style):
        return ["photoset_template", art_plan.get("name", "photoset_unknown")]

    batch.resolve_run_character = resolve_photoset_run_character
    batch.record_completed_run = record_completed_photoset_run
    batch.startup_character_selection = fixed_character_selection
    batch.startup_scene_selection = skip_scene_selection
    batch.startup_clothing_selection = skip_clothing_selection
    batch.reference_files_for_character = reference_files_for_photoset
    batch.choose_character_plan_and_action = choose_photoset_plan_and_action
    batch.choose_compatible_clothing_theme = choose_photoset_clothing
    batch.outfit_with_optional_black_hosiery = keep_photoset_outfit
    batch.choose_shot_scale = choose_photoset_shot_scale
    batch.choose_composition_plan = choose_photoset_composition
    batch.collect_cooldown_tags = collect_photoset_tags
    batch.prompt_for_art_direction = prompt_for_photoset
    batch.prompt_template_name = lambda template_index=0: f"photoset_template_{_active_template().template_id}"
    batch.CHARACTERS_PER_BATCH = max(1, len(_active_characters))
    batch.TOTAL_RUNS = _total_shots()

    while "--runs" in sys.argv:
        option_index = sys.argv.index("--runs")
        del sys.argv[option_index:option_index + 2]

    print(
        "Prompt mode E active: photoset template mode. "
        f"Templates: {', '.join(_display_template_id(template.template_id) for template in _active_templates)}. "
        f"Characters: {' / '.join(_active_characters)}. "
        "Rotation: one character completes one full template, then the next character takes the next template. "
        f"Total templates: {len(_active_templates)}. "
        f"Total shots: {_total_shots()}.",
        flush=True,
    )
