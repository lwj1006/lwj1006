
from __future__ import annotations

import sys

from .library import PhotosetShot, PhotosetTemplate, list_template_ids, load_template, prompt_for_shot


LABEL = "photoset template mode"

_active_template: PhotosetTemplate | None = None
_active_character: str | None = None
_current_shot_index = 0
_last_reference_files_for_shot: list[str] | None = None


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


def _choose_template(argv: list[str], batch) -> PhotosetTemplate:
    raw = _option_value(argv, "--TEMPLATE", "--PHOTOSET", "--E-TEMPLATE")
    if raw:
        return load_template(raw)

    available = list_template_ids()
    if batch.noninteractive_selection_enabled():
        return load_template(available[0])

    while True:
        print("")
        print("Choose photoset template:")
        for template_id in available:
            print(f"  {template_id}")
        choice = input(f"Photoset template [default {available[0]}]: ").strip() or available[0]
        try:
            return load_template(choice)
        except (FileNotFoundError, ValueError) as exc:
            print(exc)


def _choose_character(argv: list[str], batch) -> str:
    raw = _option_value(argv, "--CHARACTER", "--E-CHARACTER")
    if raw:
        return raw

    if batch.noninteractive_selection_enabled():
        return batch.CHARACTER_SEQUENCE[0]

    while True:
        print("")
        print("Choose one character for photoset mode:")
        for index, character_name in enumerate(batch.CHARACTER_SEQUENCE, start=1):
            print(f"  {index} = {character_name}")
        choice = input(f"Character [1-{len(batch.CHARACTER_SEQUENCE)}, default 1]: ").strip() or "1"
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(batch.CHARACTER_SEQUENCE):
                return batch.CHARACTER_SEQUENCE[index - 1]
        for character_name in batch.CHARACTER_SEQUENCE:
            if choice.lower() == character_name.lower():
                return character_name
        print("Unknown character. Please enter a listed number or exact character name.")


def _active_shot() -> PhotosetShot:
    assert _active_template is not None
    index = min(_current_shot_index, len(_active_template.shots) - 1)
    return _active_template.shots[index]


def activate(batch, args=None) -> None:
    global _active_template, _active_character, _current_shot_index
    argv = list(args or [])
    _active_template = _choose_template(argv, batch)
    _active_character = _choose_character(argv, batch)
    _current_shot_index = 0

    original_reference_files_for_character = batch.reference_files_for_character

    def fixed_character_selection():
        assert _active_character is not None
        print(f"Photoset mode character: {_active_character}", flush=True)
        return [_active_character]

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
            "name": f"photoset_{_active_template.template_id}_shot_{shot.index:02d}",
            "graphic_concept": shot.title,
            "spatial_structure": shot.title,
            "visual_device": f"photoset reference image {shot.index}",
            "lighting_behavior": "use the selected photoset shot lighting from the markdown and reference image",
            "color_strategy": "use the selected photoset color grade and continuity system",
            "material_language": "use the selected photoset outfit and fabric language",
            "body_silhouette": shot.title,
            "outfit_direction": f"photoset {_active_template.template_id} outfit system",
            "tags": {"photoset_template", f"photoset_{_active_template.template_id}", f"shot_{shot.index:02d}"},
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
        assert _active_template is not None
        prompt = prompt_for_shot(character_name, _active_template, shot)
        _current_shot_index += 1
        return prompt

    def collect_photoset_tags(art_plan, action_style):
        return ["photoset_template", art_plan.get("name", "photoset_unknown")]

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
    batch.prompt_template_name = lambda template_index=0: f"photoset_template_{_active_template.template_id}"
    batch.CHARACTERS_PER_BATCH = 1
    batch.TOTAL_RUNS = len(_active_template.shots)

    while "--runs" in sys.argv:
        option_index = sys.argv.index("--runs")
        del sys.argv[option_index:option_index + 2]

    print(
        "Prompt mode E active: photoset template mode. "
        f"Template: {_active_template.template_id}. "
        f"Character: {_active_character}. "
        f"Shots: {len(_active_template.shots)}.",
        flush=True,
    )
