from __future__ import annotations

import re

from fenjue.modes.selection import normalize_mode_argument, parse_index_selection
from . import plans, templates

LABEL = "photographer mode"

def choose_scene_plans(batch, argv: list[str]):
    available_plans = plans.PHOTOGRAPHER_SCENE_PLANS
    for argument in argv:
        normalized = argument.strip().upper()
        if normalized.startswith("--PHOTOGRAPHER-SCENE="):
            normalized = normalized.split("=", 1)[1].strip().upper()
        elif normalized.startswith("--SCENE-PLAN="):
            normalized = normalized.split("=", 1)[1].strip().upper()
        elif normalize_mode_argument(normalized):
            continue
        elif re.fullmatch("[\\d\\s,\\u3001\\uff0c+\\-]+|ALL|RANDOM", normalized):
            pass
        else:
            continue
        selected_indexes = parse_index_selection(normalized, len(available_plans))
        return None if selected_indexes is None else [available_plans[index - 1]["name"] for index in selected_indexes]
    if batch.noninteractive_selection_enabled():
        return None
    while True:
        print("")
        print("Choose photographer background:")
        for index, plan in enumerate(available_plans, start=1):
            print(f"  {index} = {plan.get('label', plan['name'])}")
        print("  0 = all photographer backgrounds")
        print("  Multi-select supported: 1 2 3 / 1-3 / 1-3 7 10-12")
        choice = input(f"Photographer backgrounds [0-{len(available_plans)}, default 0]: ").strip().upper() or "0"
        try:
            selected_indexes = parse_index_selection(choice, len(available_plans))
        except ValueError as exc:
            print(f"{exc}. Please enter valid indexes from 1-{len(available_plans)}, or 0.")
            continue
        selected_plans = None if selected_indexes is None else [available_plans[index - 1]["name"] for index in selected_indexes]
        print(f"Photographer backgrounds: {plans.photographer_scene_plan_label(selected_plans)}", flush=True)
        return selected_plans

def activate(batch, args=None) -> None:
    argv = list(args or [])
    selected_plans = choose_scene_plans(batch, argv)
    plans.set_active_photographer_scene_plans(selected_plans)
    def skip_original_scene_selection():
        print("Original scene category menu skipped: photographer mode uses its own scene category.", flush=True)
        return None
    def choose_photographer_plan_and_action(character_name, recent_visual_tags, used_themes_by_character, used_plans_by_character, batch_used_themes=None, batch_used_plans=None, allowed_plan_names=None):
        batch_used_plans = batch_used_plans or set()
        available_plans = plans.photographer_scene_plans_for_selection()
        if allowed_plan_names:
            allowed = set(allowed_plan_names)
            filtered = [plan for plan in available_plans if plan["name"] in allowed]
            available_plans = filtered or available_plans
        selected_plan = None
        for _ in range(40):
            candidate = plans.choose_photographer_scene_plan(character_name, recent_visual_tags)
            if candidate["name"] not in batch_used_plans:
                selected_plan = candidate
                break
        if selected_plan is None:
            fresh = [plan for plan in available_plans if plan["name"] not in batch_used_plans]
            selected_plan = fresh[0] if fresh else plans.choose_photographer_scene_plan(character_name, recent_visual_tags)
        action_style = plans.choose_photographer_action_style(character_name, recent_visual_tags, selected_plan)
        return dict(selected_plan), action_style
    batch.choose_character_plan_and_action = choose_photographer_plan_and_action
    batch.choose_shot_scale = plans.choose_photographer_shot_scale
    batch.choose_composition_plan = plans.choose_photographer_composition_plan
    batch.startup_scene_selection = skip_original_scene_selection
    batch.prompt_for_art_direction = templates.prompt_for_art_direction
    batch.prompt_template_name = templates.prompt_template_name
    print("Prompt mode B active: photographer dedicated-plan style. " f"Backgrounds: {plans.photographer_scene_plan_label(selected_plans)}.", flush=True)
