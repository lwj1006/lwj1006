import json
import random
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import art_direction_options as options
from art_direction_templates import prompt_for_art_direction


PROJECT_DIR = Path(__file__).resolve().parent
RESULT_MD = PROJECT_DIR / "PRODUCTION_LIKE_PROMPT_1000_SAMPLE_AUDIT.md"
RESULT_JSONL = PROJECT_DIR / "PRODUCTION_LIKE_PROMPT_1000_SAMPLE_AUDIT.jsonl"

SAMPLE_COUNT = 1000
RANDOM_SEED = 20260602
MAX_PROMPT_LENGTH = 3000
CHARACTERS_PER_BATCH = 3


def choose_character_batch(used_characters):
    available = [
        name for name in options.KNOWN_CHARACTER_NAMES
        if name not in used_characters
    ]
    if not available:
        used_characters.clear()
        available = options.KNOWN_CHARACTER_NAMES[:]
    return random.sample(available, k=min(CHARACTERS_PER_BATCH, len(available)))


def choose_production_like_plan_and_action(
    character_name,
    recent_tags,
    used_themes_by_character,
    used_plans_by_character,
    batch_used_themes,
    batch_used_plans,
):
    used_themes = used_themes_by_character.setdefault(character_name, [])
    used_themes[:] = [
        theme for theme in used_themes
        if theme in options.OUTFIT_DIRECTIONS
    ]
    used_theme_set = set(used_themes)

    valid_plan_names = {plan["name"] for plan in options.ART_DIRECTION_PLANS}
    used_plans = used_plans_by_character.setdefault(character_name, [])
    used_plans[:] = [
        plan_name for plan_name in used_plans
        if plan_name in valid_plan_names
    ]
    used_plan_set = set(used_plans)

    if len(used_theme_set) >= len(options.OUTFIT_DIRECTIONS):
        used_themes.clear()
        used_theme_set = set()

    if len(used_plan_set) >= len(options.ART_DIRECTION_PLANS):
        used_plans.clear()
        used_plan_set = set()

    best_unused_plan = None
    best_unused_theme = None
    fallback = None
    for _ in range(180):
        plan, action = options.choose_plan_and_action(character_name, recent_tags)
        fallback = fallback or (plan, action)
        plan_unused = plan["name"] not in used_plan_set and plan["name"] not in batch_used_plans
        theme_unused = plan["outfit_direction"] not in used_theme_set and plan["outfit_direction"] not in batch_used_themes
        if plan_unused and theme_unused:
            return plan, action, "fresh_plan_and_theme"
        if plan_unused and best_unused_plan is None:
            best_unused_plan = (plan, action)
        if theme_unused and best_unused_theme is None:
            best_unused_theme = (plan, action)

    unused_plans = [
        plan for plan in options.ART_DIRECTION_PLANS
        if plan["name"] not in used_plan_set and plan["name"] not in batch_used_plans
    ]
    if unused_plans:
        unused_themes = {
            theme for theme in options.OUTFIT_DIRECTIONS
            if theme not in used_theme_set and theme not in batch_used_themes
        }
        matching = [
            plan for plan in unused_plans
            if plan["outfit_direction"] in unused_themes
        ]
        plan = random.choice(matching or unused_plans)
        action = options.choose_compatible_action_style(character_name, recent_tags, plan)
        return dict(plan), action, "explicit_unused_plan_pool"

    if best_unused_plan is not None:
        plan, action = best_unused_plan
        return plan, action, "unused_plan_only"
    if best_unused_theme is not None:
        plan, action = best_unused_theme
        return plan, action, "unused_theme_only"
    plan, action = fallback or options.choose_plan_and_action(character_name, recent_tags)
    return plan, action, "fallback"


def check_sample(row):
    issues = []
    prompt = row["prompt"]
    prompt_positive = prompt.split("Avoid:", 1)[0]
    prompt_lower = prompt_positive.lower()

    if row["prompt_length"] > MAX_PROMPT_LENGTH:
        issues.append(f"length>{MAX_PROMPT_LENGTH}:{row['prompt_length']}")

    for token in options.required_identity_tokens_for(row["character"]):
        if str(token).lower() not in prompt_lower:
            issues.append("identity_missing:" + str(token))
            break

    forbidden = [
        "rainy",
        "factory",
        "neon",
        "nude",
        "explicit",
        "industrial hammer weapon",
        "white blouse and black stockings",
        "holding_small_cute_prop",
    ]
    hits = [term for term in forbidden if term in prompt_lower]
    if hits:
        issues.append("forbidden_terms:" + "|".join(hits))

    compatible_actions = {
        action["name"] for action in options._compatible_actions_for_plan(row["plan"])
    }
    if row["action_name"] not in compatible_actions:
        issues.append("action_plan_incompatible")

    compatible_visuals = {
        visual["name"] for visual in options._visuals_for_plan(row["plan"])
    }
    if row["visual_name"] not in compatible_visuals:
        issues.append("visual_plan_incompatible")

    return issues


def main():
    random.seed(RANDOM_SEED)
    recent_tags = []
    used_character_cycle = []
    used_themes_by_character = {}
    used_plans_by_character = {}
    rows = []
    issue_counter = Counter()
    character_counter = Counter()
    plan_counter = Counter()
    outfit_counter = Counter()
    action_counter = Counter()
    visual_counter = Counter()
    selection_counter = Counter()
    length_by_character = defaultdict(list)

    run_number = 1
    while run_number <= SAMPLE_COUNT:
        selected_characters = choose_character_batch(used_character_cycle)
        batch_used_themes = set()
        batch_used_plans = set()

        for character in selected_characters:
            if run_number > SAMPLE_COUNT:
                break
            plan, action, selection_mode = choose_production_like_plan_and_action(
                character,
                recent_tags,
                used_themes_by_character,
                used_plans_by_character,
                batch_used_themes,
                batch_used_plans,
            )
            visual = options.choose_visual_design(recent_tags, plan)
            prompt = prompt_for_art_direction(character, plan, action, recent_tags, visual)
            row = {
                "index": run_number,
                "character": character,
                "plan_name": plan["name"],
                "outfit_direction": plan["outfit_direction"],
                "action_name": action["name"],
                "visual_name": visual["name"],
                "selection_mode": selection_mode,
                "plan_tags": plan.get("tags", []),
                "action_tags": action.get("tags", []),
                "prompt_length": len(prompt),
                "prompt": prompt,
                "plan": plan,
            }
            row["issues"] = check_sample(row)
            rows.append(row)

            if plan["name"] not in used_plans_by_character.setdefault(character, []):
                used_plans_by_character[character].append(plan["name"])
            if plan["outfit_direction"] not in used_themes_by_character.setdefault(character, []):
                used_themes_by_character[character].append(plan["outfit_direction"])
            batch_used_plans.add(plan["name"])
            batch_used_themes.add(plan["outfit_direction"])
            if character not in used_character_cycle:
                used_character_cycle.append(character)
            recent_tags.extend(options.collect_cooldown_tags(plan, action))
            recent_tags = recent_tags[-12:]

            character_counter[character] += 1
            plan_counter[plan["name"]] += 1
            outfit_counter[plan["outfit_direction"]] += 1
            action_counter[action["name"]] += 1
            visual_counter[visual["name"]] += 1
            selection_counter[selection_mode] += 1
            length_by_character[character].append(len(prompt))
            for issue in row["issues"]:
                issue_counter[issue.split(":", 1)[0]] += 1
            run_number += 1

    with RESULT_JSONL.open("w", encoding="utf-8") as f:
        for row in rows:
            output = dict(row)
            output.pop("plan", None)
            f.write(json.dumps(output, ensure_ascii=False) + "\n")

    issue_rows = [row for row in rows if row["issues"]]
    max_len_row = max(rows, key=lambda item: item["prompt_length"])
    min_len_row = min(rows, key=lambda item: item["prompt_length"])

    lines = [
        "# Production-Like Prompt 1000 Sample Audit",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- random_seed: {RANDOM_SEED}",
        f"- sample_count: {SAMPLE_COUNT}",
        f"- active_plan_count: {len(options.ART_DIRECTION_PLANS)}",
        f"- active_outfit_count: {len(options.OUTFIT_DIRECTIONS)}",
        f"- issue_samples: {len(issue_rows)}",
        f"- max_prompt_length: {max_len_row['prompt_length']} ({max_len_row['character']} / {max_len_row['plan_name']} / {max_len_row['action_name']} / {max_len_row['visual_name']})",
        f"- min_prompt_length: {min_len_row['prompt_length']} ({min_len_row['character']} / {min_len_row['plan_name']} / {min_len_row['action_name']} / {min_len_row['visual_name']})",
        "",
        "## Issue Summary",
        "",
    ]
    if issue_counter:
        for issue, count in issue_counter.most_common():
            lines.append(f"- {issue}: {count}")
    else:
        lines.append("- none")

    lines.extend(["", "## Selection Mode Distribution", ""])
    for name, count in selection_counter.most_common():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Character Distribution", ""])
    for name, count in character_counter.most_common():
        lengths = length_by_character[name]
        avg_len = sum(lengths) / len(lengths)
        lines.append(f"- {name}: {count}, avg_len={avg_len:.1f}, max_len={max(lengths)}")

    lines.extend(["", "## Plan Distribution", ""])
    for name, count in plan_counter.most_common():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Outfit Distribution", ""])
    for name, count in outfit_counter.most_common():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Action Distribution", ""])
    for name, count in action_counter.most_common():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Visual Motif Distribution", ""])
    for name, count in visual_counter.most_common():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Issue Samples", ""])
    if issue_rows:
        for row in issue_rows[:80]:
            lines.append(
                f"- #{row['index']} {row['character']} / {row['plan_name']} / {row['action_name']} / {row['visual_name']}: "
                + "; ".join(row["issues"])
            )
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Full Samples",
        "",
        f"Full 1000 prompts are stored in `{RESULT_JSONL.name}`.",
    ])

    RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {RESULT_MD}")
    print(f"wrote {RESULT_JSONL}")
    print(f"issue_samples={len(issue_rows)}")
    if issue_counter:
        print(f"issues={dict(issue_counter)}")


if __name__ == "__main__":
    main()
