import sys

import chatgpt_batch_pyautogui as batch


PHOTOGRAPHER_CATEGORY_ARGUMENTS = {
    "1": "studio_editorial",
    "A": "studio_editorial",
    "STUDIO": "studio_editorial",
    "STUDIO_EDITORIAL": "studio_editorial",
    "2": "indoor_novel_cg",
    "I": "indoor_novel_cg",
    "INDOOR": "indoor_novel_cg",
    "INDOOR_NOVEL_CG": "indoor_novel_cg",
    "3": "bright_daily_scene",
    "D": "bright_daily_scene",
    "DAILY": "bright_daily_scene",
    "BRIGHT_DAILY_SCENE": "bright_daily_scene",
    "0": None,
    "ALL": None,
    "RANDOM": None,
}


def choose_prompt_mode() -> str:
    for argument in sys.argv[1:]:
        normalized = argument.strip().upper()
        if normalized in {"A", "--MODE=A", "--PROMPT-MODE=A"}:
            return "A"
        if normalized in {"B", "--MODE=B", "--PROMPT-MODE=B"}:
            return "B"

    while True:
        print("")
        print("Choose prompt mode:")
        print("  A = original stable compact style")
        print("  B = photographer four-block style")
        choice = input("Prompt mode [A/B, default A]: ").strip().upper() or "A"
        if choice in {"A", "B"}:
            return choice
        print("Please enter A or B.")


def choose_photographer_category():
    import photographer_prompt_plans as photographer_plans

    for argument in sys.argv[1:]:
        normalized = argument.strip().upper()
        if normalized.startswith("--PHOTOGRAPHER-CATEGORY="):
            normalized = normalized.split("=", 1)[1].strip().upper()
        elif normalized.startswith("--SCENE-CATEGORY="):
            normalized = normalized.split("=", 1)[1].strip().upper()
        elif normalized not in PHOTOGRAPHER_CATEGORY_ARGUMENTS:
            continue
        if normalized in PHOTOGRAPHER_CATEGORY_ARGUMENTS:
            return PHOTOGRAPHER_CATEGORY_ARGUMENTS[normalized]
        raise ValueError(f"Unknown photographer scene category: {argument}")

    while True:
        print("")
        print("Choose photographer scene category:")
        print("  1 = 棚拍 / 杂志 / 摄影棚")
        print("  2 = 室内 / 小说CG / 空间感")
        print("  3 = 明亮日常 / 店铺 / 街区")
        print("  0 = 全随机摄影师场景")
        choice = input("Photographer scene [1/2/3/0, default 0]: ").strip().upper() or "0"
        if choice in PHOTOGRAPHER_CATEGORY_ARGUMENTS:
            category = PHOTOGRAPHER_CATEGORY_ARGUMENTS[choice]
            print(
                f"Photographer scene category: {photographer_plans.photographer_scene_category_label(category)}",
                flush=True,
            )
            return category
        print("Please enter 1, 2, 3, or 0.")


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
        available_plans = photographer_plans.photographer_scene_plans_for_category()
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


def activate_prompt_mode(mode: str) -> None:
    if mode == "A":
        print("Prompt mode A active: original stable compact style.", flush=True)
        return

    import photographer_prompt_templates as photographer
    import photographer_prompt_plans as photographer_plans

    category = choose_photographer_category()
    photographer_plans.set_active_photographer_scene_category(category)
    _activate_photographer_runtime_hooks(photographer, photographer_plans)
    print(
        "Prompt mode B active: photographer dedicated-plan style. "
        f"Scene category: {photographer_plans.photographer_scene_category_label(category)}.",
        flush=True,
    )


if __name__ == "__main__":
    activate_prompt_mode(choose_prompt_mode())
    batch.main()
