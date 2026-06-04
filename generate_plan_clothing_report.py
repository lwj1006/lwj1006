import json
import random
from pathlib import Path

import chatgpt_batch_pyautogui as batch
import art_direction_options as options


PROJECT_DIR = Path(__file__).resolve().parent
REPORT_PATH = PROJECT_DIR / "feedback" / "plan_clothing_inventory.md"
SAMPLE_PATH = PROJECT_DIR / "feedback" / "random_100_plan_clothing_results.jsonl"
SAMPLE_MD_PATH = PROJECT_DIR / "feedback" / "random_100_plan_clothing_results.md"
SAMPLE_1000_PATH = PROJECT_DIR / "feedback" / "random_1000_runtime_results.jsonl"
SAMPLE_1000_MD_PATH = PROJECT_DIR / "feedback" / "random_1000_runtime_results.md"
SAMPLE_1000_SUMMARY_PATH = PROJECT_DIR / "feedback" / "random_1000_runtime_summary.md"


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


def simulate_runtime_results(total_runs: int) -> list[dict]:
    used_by_character: dict[str, list[str]] = {}
    used_plans_by_character: dict[str, list[str]] = {}
    recent_visual_tags: list[str] = []
    results = []
    category_lookup = {
        plan_name: category["label"]
        for category in batch.SCENE_CATEGORY_OPTIONS
        for plan_name in category["plan_names"]
    }
    strong_themes = set(batch.STRONG_SCENE_ONLY_CLOTHING_THEMES)
    for run_number in range(1, total_runs + 1):
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
        outfit_prompt, black_hosiery_applied = batch.outfit_with_optional_black_hosiery(
            character_name,
            theme,
            art_plan,
        )
        composition_plan = options.choose_composition_plan(
            recent_visual_tags,
            art_plan,
            action_style,
            outfit_prompt,
        )
        batch_used_themes.add(theme)
        batch_used_plans.add(art_plan["name"])
        recent_visual_tags.extend(options.collect_cooldown_tags(art_plan, action_style))
        recent_visual_tags = recent_visual_tags[-12:]
        results.append(
            {
                "run": run_number,
                "character": character_name,
                "category": category_lookup.get(art_plan["name"], ""),
                "plan": art_plan["name"],
                "action": action_style["name"],
                "composition": composition_plan["name"],
                "clothing_label": label_for(theme),
                "clothing_theme": theme,
                "plan_default_outfit": art_plan["outfit_direction"],
                "black_hosiery_applied": black_hosiery_applied,
                "scene_only_clothing": theme in strong_themes,
                "outfit_prompt": outfit_prompt,
            }
        )
    return results


def write_runtime_sample_reports(results: list[dict]) -> None:
    from collections import Counter

    with SAMPLE_1000_PATH.open("w", encoding="utf-8-sig") as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    sample_lines = [
        "# Random 1000 Runtime Results",
        "",
        f"- Runtime config revision: {options.RUNTIME_CONFIG_REVISION}",
        f"- Active plans: {len(options.ART_DIRECTION_PLANS)}",
        f"- Clothing themes: {len(batch.CLOTHING_THEMES)}",
        f"- Results: {len(results)}",
        "",
        "| # | Character | Category | Plan | Action | Composition | Clothing | Black hosiery | Scene-only |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]
    for item in results:
        sample_lines.append(
            "| {run} | {character} | {category} | `{plan}` | `{action}` | `{composition}` | {clothing_label} | {hosiery} | {scene_only} |".format(
                run=item["run"],
                character=item["character"],
                category=item["category"],
                plan=item["plan"],
                action=item["action"],
                composition=item["composition"],
                clothing_label=item["clothing_label"],
                hosiery="yes" if item["black_hosiery_applied"] else "no",
                scene_only="yes" if item["scene_only_clothing"] else "no",
            )
        )
    SAMPLE_1000_MD_PATH.write_text("\n".join(sample_lines), encoding="utf-8-sig")

    def table(counter: Counter, total: int, limit: int) -> list[str]:
        lines = ["| Item | Count | Rate |", "|---|---:|---:|"]
        for name, count in counter.most_common(limit):
            lines.append(f"| {name} | {count} | {count / max(total, 1):.1%} |")
        return lines

    plan_counts = Counter(item["plan"] for item in results)
    composition_counts = Counter(item["composition"] for item in results)
    clothing_counts = Counter(item["clothing_label"] for item in results)
    character_counts = Counter(item["character"] for item in results)
    hosiery_counts = Counter()
    scene_only_counts = Counter()
    for item in results:
        if item["black_hosiery_applied"]:
            hosiery_counts[item["character"]] += 1
        if item["scene_only_clothing"]:
            scene_only_counts[item["clothing_label"]] += 1

    summary_lines = [
        "# Random 1000 Runtime Summary",
        "",
        f"- Runtime config revision: `{options.RUNTIME_CONFIG_REVISION}`",
        f"- Active plans: {len(options.ART_DIRECTION_PLANS)}",
        f"- Clothing themes: {len(batch.CLOTHING_THEMES)}",
        f"- Scene categories: {len(batch.SCENE_CATEGORY_OPTIONS)}",
        f"- Results: {len(results)}",
        "",
        "## Plan Distribution",
        "",
        *table(plan_counts, len(results), 50),
        "",
        "## Clothing Distribution",
        "",
        *table(clothing_counts, len(results), 60),
        "",
        "## Composition Distribution",
        "",
        *table(composition_counts, len(results), 30),
        "",
        "## Character Distribution",
        "",
        *table(character_counts, len(results), 30),
        "",
        "## Black Hosiery By Character",
        "",
        "| Character | Count | Hosiery Count | Rate |",
        "|---|---:|---:|---:|",
    ]
    for character_name in batch.CHARACTER_SEQUENCE:
        total = character_counts[character_name]
        hosiery = hosiery_counts[character_name]
        rate = hosiery / total if total else 0
        summary_lines.append(f"| {character_name} | {total} | {hosiery} | {rate:.1%} |")
    summary_lines += ["", "## Scene-Only Clothing", ""]
    summary_lines += table(scene_only_counts, len(results), 20) if scene_only_counts else ["- None"]
    SAMPLE_1000_SUMMARY_PATH.write_text("\n".join(summary_lines), encoding="utf-8-sig")


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

    results = simulate_runtime_results(100)

    with SAMPLE_PATH.open("w", encoding="utf-8-sig") as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    sample_lines = [
        "# Random 100 Plan / Clothing Results",
        "",
        "| # | Character | Plan | Action | Composition | Clothing | Scene-only |",
        "|---:|---|---|---|---|---|---|",
    ]
    for item in results:
        sample_lines.append(
            "| {run} | {character} | `{plan}` | `{action}` | `{composition}` | {clothing_label} | {scene_only} |".format(
                run=item["run"],
                character=item["character"],
                plan=item["plan"],
                action=item["action"],
                composition=item["composition"],
                clothing_label=item["clothing_label"],
                scene_only="yes" if item["scene_only_clothing"] else "no",
            )
        )
    SAMPLE_MD_PATH.write_text("\n".join(sample_lines), encoding="utf-8-sig")
    runtime_1000_results = simulate_runtime_results(1000)
    write_runtime_sample_reports(runtime_1000_results)

    print(f"report: {REPORT_PATH}")
    print(f"samples: {SAMPLE_PATH}")
    print(f"samples_md: {SAMPLE_MD_PATH}")
    print(f"runtime_1000_summary: {SAMPLE_1000_SUMMARY_PATH}")
    print(f"plans: {len(plans)}")
    print(f"clothing themes: {len(batch.CLOTHING_THEMES)}")
    print(f"sample results: {len(results)}")


if __name__ == "__main__":
    main()
