import sys
import re

import chatgpt_batch_pyautogui as batch


LAUNCHER_VERSION = "C-world-cup-20260612"


def choose_prompt_mode() -> str:
    for argument in sys.argv[1:]:
        normalized = argument.strip().upper()
        if normalized in {"A", "--MODE=A", "--PROMPT-MODE=A"}:
            return "A"
        if normalized in {"B", "--MODE=B", "--PROMPT-MODE=B"}:
            return "B"
        if normalized in {"C", "--MODE=C", "--PROMPT-MODE=C", "--WORLD-CUP"}:
            return "C"

    while True:
        print("")
        print("Choose prompt mode:")
        print("  A = original stable compact style")
        print("  B = photographer four-block style")
        print("  C = World Cup roadside supporter special")
        choice = input("Prompt mode [A/B/C, default A]: ").strip().upper() or "A"
        if choice in {"A", "B", "C"}:
            return choice
        print("Please enter A, B, or C.")


def _parse_photographer_scene_selection(raw_choice, plan_count):
    normalized = raw_choice.strip().upper()
    if normalized in {"", "0", "ALL", "RANDOM"}:
        return None

    indexes = []
    for token in re.split(r"[\s,，]+", normalized):
        if not token:
            continue
        if "-" in token:
            parts = token.split("-", 1)
            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                raise ValueError(f"Invalid range: {token}")
            start, end = (int(part) for part in parts)
            if start > end:
                start, end = end, start
            indexes.extend(range(start, end + 1))
        elif token.isdigit():
            indexes.append(int(token))
        else:
            raise ValueError(f"Invalid selection token: {token}")

    invalid = [index for index in indexes if index < 1 or index > plan_count]
    if invalid:
        raise ValueError(f"Scene indexes out of range: {invalid}")
    return list(dict.fromkeys(indexes))


def choose_photographer_scene_plans():
    import photographer_prompt_plans as photographer_plans

    plans = photographer_plans.PHOTOGRAPHER_SCENE_PLANS
    for argument in sys.argv[1:]:
        normalized = argument.strip().upper()
        if normalized.startswith("--PHOTOGRAPHER-SCENE="):
            normalized = normalized.split("=", 1)[1].strip().upper()
        elif normalized.startswith("--SCENE-PLAN="):
            normalized = normalized.split("=", 1)[1].strip().upper()
        elif normalized in {"A", "B", "C", "--MODE=A", "--MODE=B", "--MODE=C", "--PROMPT-MODE=A", "--PROMPT-MODE=B", "--PROMPT-MODE=C", "--WORLD-CUP"}:
            continue
        elif re.fullmatch(r"[\d\s,，-]+|ALL|RANDOM", normalized):
            pass
        else:
            continue
        selected_indexes = _parse_photographer_scene_selection(normalized, len(plans))
        return None if selected_indexes is None else [plans[index - 1]["name"] for index in selected_indexes]

    while True:
        print("")
        print("Choose photographer background:")
        for index, plan in enumerate(plans, start=1):
            print(f"  {index} = {plan.get('label', plan['name'])}")
        print("  0 = 全随机摄影师背景")
        print("  支持多选和区间，例如: 1 2 3 / 1-3 / 1-3 7 10-12")
        choice = input(f"Photographer backgrounds [0-{len(plans)}, default 0]: ").strip().upper() or "0"
        try:
            selected_indexes = _parse_photographer_scene_selection(choice, len(plans))
        except ValueError as exc:
            print(f"{exc}. Please enter valid indexes from 1-{len(plans)}, or 0.")
            continue
        selected_plans = None if selected_indexes is None else [plans[index - 1]["name"] for index in selected_indexes]
        print(
            f"Photographer backgrounds: {photographer_plans.photographer_scene_plan_label(selected_plans)}",
            flush=True,
        )
        return selected_plans


def _activate_photographer_runtime_hooks(photographer, photographer_plans):
    def skip_original_scene_selection():
        print(
            "Original scene category menu skipped: photographer mode uses its own scene category.",
            flush=True,
        )
        return None

    def choose_photographer_plan_and_action(
        character_name,
        recent_visual_tags,
        used_themes_by_character,
        used_plans_by_character,
        batch_used_themes=None,
        batch_used_plans=None,
        allowed_plan_names=None,
    ):
        batch_used_plans = batch_used_plans or set()
        available_plans = photographer_plans.photographer_scene_plans_for_selection()
        if allowed_plan_names:
            allowed = set(allowed_plan_names)
            filtered = [plan for plan in available_plans if plan["name"] in allowed]
            available_plans = filtered or available_plans

        selected_plan = None
        for _ in range(40):
            candidate = photographer_plans.choose_photographer_scene_plan(character_name, recent_visual_tags)
            if candidate["name"] not in batch_used_plans:
                selected_plan = candidate
                break
        if selected_plan is None:
            fresh = [plan for plan in available_plans if plan["name"] not in batch_used_plans]
            selected_plan = fresh[0] if fresh else photographer_plans.choose_photographer_scene_plan(character_name, recent_visual_tags)

        action_style = photographer_plans.choose_photographer_action_style(
            character_name,
            recent_visual_tags,
            selected_plan,
        )
        return dict(selected_plan), action_style

    batch.choose_character_plan_and_action = choose_photographer_plan_and_action
    batch.choose_shot_scale = photographer_plans.choose_photographer_shot_scale
    batch.choose_composition_plan = photographer_plans.choose_photographer_composition_plan
    batch.startup_scene_selection = skip_original_scene_selection
    batch.prompt_for_art_direction = photographer.prompt_for_art_direction
    batch.prompt_template_name = photographer.prompt_template_name


def _activate_world_cup_runtime_hooks(world_cup_templates, world_cup_plans):
    def skip_original_scene_selection():
        print("Original scene category menu skipped: World Cup mode uses dedicated roadside viewing scenes.", flush=True)
        return None

    def skip_original_clothing_selection():
        print("Original clothing menu skipped: every character uses their assigned national-team supporter outfit.", flush=True)
        return None

    def choose_world_cup_plan_and_action(
        character_name,
        recent_visual_tags,
        used_themes_by_character,
        used_plans_by_character,
        batch_used_themes=None,
        batch_used_plans=None,
        allowed_plan_names=None,
    ):
        plan = world_cup_plans.world_cup_plan_for(character_name)
        action = world_cup_plans.choose_world_cup_action_style(character_name, recent_visual_tags, plan)
        return plan, action

    def choose_world_cup_clothing(character_name, art_plan, used_by_character, batch_used_themes=None):
        return world_cup_plans.world_cup_outfit_for(character_name)

    def keep_world_cup_outfit(character_name, theme, art_plan):
        return theme, False

    batch.choose_character_plan_and_action = choose_world_cup_plan_and_action
    batch.choose_compatible_clothing_theme = choose_world_cup_clothing
    batch.outfit_with_optional_black_hosiery = keep_world_cup_outfit
    batch.choose_shot_scale = world_cup_plans.choose_world_cup_shot_scale
    batch.choose_composition_plan = world_cup_plans.choose_world_cup_composition_plan
    batch.startup_scene_selection = skip_original_scene_selection
    batch.startup_clothing_selection = skip_original_clothing_selection
    batch.prompt_for_art_direction = world_cup_templates.prompt_for_art_direction
    batch.prompt_template_name = world_cup_templates.prompt_template_name


def activate_prompt_mode(mode: str) -> None:
    print(f"Fenjue prompt launcher version: {LAUNCHER_VERSION}", flush=True)
    if mode == "A":
        print("Prompt mode A active: original stable compact style.", flush=True)
        return

    if mode == "C":
        import world_cup_prompt_plans as world_cup_plans
        import world_cup_prompt_templates as world_cup_templates

        _activate_world_cup_runtime_hooks(world_cup_templates, world_cup_plans)
        print(
            "Prompt mode C active: World Cup roadside supporter special. "
            f"Stable assignments: {len(world_cup_plans.CHARACTER_TEAM_SPECS)} characters.",
            flush=True,
        )
        return

    import photographer_prompt_templates as photographer
    import photographer_prompt_plans as photographer_plans

    selected_plans = choose_photographer_scene_plans()
    photographer_plans.set_active_photographer_scene_plans(selected_plans)
    _activate_photographer_runtime_hooks(photographer, photographer_plans)
    print(
        "Prompt mode B active: photographer dedicated-plan style. "
        f"Backgrounds: {photographer_plans.photographer_scene_plan_label(selected_plans)}.",
        flush=True,
    )


if __name__ == "__main__":
    activate_prompt_mode(choose_prompt_mode())
    batch.main()
