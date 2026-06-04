import json
import random
from pathlib import Path

import chatgpt_batch_pyautogui as batch
import art_direction_options as options


PROJECT_DIR = Path(__file__).resolve().parent
REPORT_PATH = PROJECT_DIR / "feedback" / "plan_clothing_inventory.md"
SAMPLE_PATH = PROJECT_DIR / "feedback" / "random_100_plan_clothing_results.jsonl"
SAMPLE_MD_PATH = PROJECT_DIR / "feedback" / "random_100_plan_clothing_results.md"


def label_for(theme: str) -> str:
    return batch.CLOTHING_DISPLAY_LABELS.get(theme, theme)


def compatible_for_plan(plan_name: str) -> list[str]:
    configured = [
        theme for theme in batch.PLAN_COMPATIBLE_CLOTHING_THEMES.get(plan_name, [])
        if theme in batch.CLOTHING_THEMES
    ]
    if configured:
        return configured
    return batch.SAFE_DAILY_CLOTHING_POOL[:]


def format_theme(theme: str) -> str:
    label = label_for(theme)
    return f"{label} | `{theme}`"


def main() -> None:
    random.seed(20260604)
    batch.maybe_refresh_runtime_config(force=True, enable_git_pull=False)
    plans = options.ART_DIRECTION_PLANS
    plan_names = [plan["name"] for plan in plans]
    strong_themes = [
        theme for theme in batch.STRONG_SCENE_ONLY_CLOTHING_THEMES
        if theme in batch.CLOTHING_THEMES
    ]
    regular_themes = [
        theme for theme in batch.REGULAR_CLOTHING_THEMES
        if theme in batch.CLOTHING_THEMES
    ]
    configured_plan_names = {
        name for name in batch.PLAN_COMPATIBLE_CLOTHING_THEMES
        if name in plan_names
    }
    unconfigured_plan_names = [
        name for name in plan_names
        if name not in configured_plan_names
    ]
    limited_theme_plans: dict[str, list[str]] = {}
    for theme in batch.CLOTHING_THEMES:
        supported = [
            plan["name"] for plan in plans
            if theme in compatible_for_plan(plan["name"])
        ]
        if len(supported) < len(plans):
            limited_theme_plans[theme] = supported

    lines: list[str] = []
    lines.append("# Plan / Clothing Inventory")
    lines.append("")
    lines.append(f"- Active plans: {len(plans)}")
    lines.append(f"- Clothing themes: {len(batch.CLOTHING_THEMES)}")
    lines.append(f"- Regular cycle clothing themes: {len(regular_themes)}")
    lines.append(f"- Strong scene-only clothing themes: {len(strong_themes)}")
    lines.append("")

    lines.append("## All Clothing Themes")
    lines.append("")
    for index, theme in enumerate(batch.CLOTHING_THEMES, start=1):
        kind = "scene-only" if theme in strong_themes else "regular"
        lines.append(f"{index}. {format_theme(theme)} ({kind})")
    lines.append("")

    lines.append("## Scene-Only / Limited Clothing")
    lines.append("")
    if strong_themes:
        lines.append("These are intentionally excluded from the regular per-character clothing cycle.")
        lines.append("")
        for theme in strong_themes:
            supported = limited_theme_plans.get(theme, [])
            supported_text = ", ".join(supported) if supported else "no configured compatible plan"
            lines.append(f"- {format_theme(theme)}")
            lines.append(f"  Compatible plans: {supported_text}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Plan Defaults And Compatible Clothing")
    lines.append("")
    for index, plan in enumerate(plans, start=1):
        compatible = compatible_for_plan(plan["name"])
        lines.append(f"### {index}. {plan['name']}")
        lines.append(f"- Default outfit direction: {format_theme(plan['outfit_direction'])}")
        lines.append(f"- Tags: {', '.join(plan.get('tags', []))}")
        lines.append(f"- Compatible clothing count: {len(compatible)}")
        for theme in compatible:
            lines.append(f"  - {format_theme(theme)}")
        lines.append("")

    lines.append("## Plans Using Default Safe Pool")
    lines.append("")
    if unconfigured_plan_names:
        for name in unconfigured_plan_names:
            lines.append(f"- {name}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Clothing Restricted To Some Plans")
    lines.append("")
    for theme, supported in limited_theme_plans.items():
        lines.append(f"- {format_theme(theme)}")
        lines.append(f"  Plans ({len(supported)}): {', '.join(supported)}")
    lines.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8-sig")

    used_by_character: dict[str, list[str]] = {}
    used_plans_by_character: dict[str, list[str]] = {}
    recent_visual_tags: list[str] = []
    results = []
    for run_number in range(1, 101):
        if (run_number - 1) % batch.CHARACTERS_PER_BATCH == 0:
            batch_used_themes: set[str] = set()
            batch_used_plans: set[str] = set()
        character_name = random.choice(batch.CHARACTER_SEQUENCE)
        art_plan, action_style = batch.choose_character_plan_and_action(
            character_name,
            recent_visual_tags,
            used_by_character,
            used_plans_by_character,
            batch_used_themes,
            batch_used_plans,
            None,
        )
        theme = batch.choose_compatible_clothing_theme(
            character_name,
            art_plan,
            used_by_character,
            batch_used_themes,
        )
        batch_used_themes.add(theme)
        batch_used_plans.add(art_plan["name"])
        recent_visual_tags.extend(options.collect_cooldown_tags(art_plan, action_style))
        recent_visual_tags = recent_visual_tags[-12:]
        results.append(
            {
                "run": run_number,
                "character": character_name,
                "plan": art_plan["name"],
                "action": action_style["name"],
                "clothing_label": label_for(theme),
                "clothing_theme": theme,
                "plan_default_outfit": art_plan["outfit_direction"],
                "scene_only_clothing": theme in strong_themes,
            }
        )

    with SAMPLE_PATH.open("w", encoding="utf-8-sig") as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    sample_lines = [
        "# Random 100 Plan / Clothing Results",
        "",
        "| # | Character | Plan | Action | Clothing | Scene-only |",
        "|---:|---|---|---|---|---|",
    ]
    for item in results:
        sample_lines.append(
            "| {run} | {character} | `{plan}` | `{action}` | {clothing_label} | {scene_only} |".format(
                run=item["run"],
                character=item["character"],
                plan=item["plan"],
                action=item["action"],
                clothing_label=item["clothing_label"],
                scene_only="yes" if item["scene_only_clothing"] else "no",
            )
        )
    SAMPLE_MD_PATH.write_text("\n".join(sample_lines), encoding="utf-8-sig")

    print(f"report: {REPORT_PATH}")
    print(f"samples: {SAMPLE_PATH}")
    print(f"samples_md: {SAMPLE_MD_PATH}")
    print(f"plans: {len(plans)}")
    print(f"clothing themes: {len(batch.CLOTHING_THEMES)}")
    print(f"sample results: {len(results)}")


if __name__ == "__main__":
    main()
