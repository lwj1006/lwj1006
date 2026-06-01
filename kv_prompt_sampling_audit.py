import json
import random
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import art_direction_options as options
from art_direction_templates import prompt_for_art_direction


PROJECT_DIR = Path(__file__).resolve().parent
RESULT_MD = PROJECT_DIR / "KV_PROMPT_1000_SAMPLE_AUDIT.md"
RESULT_JSONL = PROJECT_DIR / "KV_PROMPT_1000_SAMPLE_AUDIT.jsonl"

SAMPLE_COUNT = 1000
RANDOM_SEED = 20260601
MAX_PROMPT_LENGTH = 3000

FORBIDDEN_GENERAL_TERMS = [
    "rainy",
    "factory",
    "neon",
    "hand reaching toward camera",
    "adult",
    "nude",
    "explicit",
]

FORBIDDEN_CHINESE_TERMS = [
    "雨天",
    "工厂",
    "霓虹",
    "色情",
    "成人",
    "裸体",
    "伸向镜头",
]

CAMERA_GROUPS = {
    "high": ["high angle", "seen from a high angle", "looks down", "overhead"],
    "low": ["low-angle", "low foreground", "seen from low", "camera near floor"],
    "far": ["far-shot", "small figure", "long distance"],
    "telephoto": ["telephoto", "compressed"],
}

PROBLEMATIC_TRUNCATION_PATTERNS = [
    "no came...",
    "storyboo...",
    "butterfl...",
    "character's...",
    "instead of.",
    "across the.",
    "feel.",
    "were a.",
    "in a soft.",
    "through the.",
]


def contains_any(text, terms):
    text_lower = text.lower()
    return [term for term in terms if term.lower() in text_lower]


def camera_modes_in(text):
    text_lower = text.lower()
    modes = []
    for mode, terms in CAMERA_GROUPS.items():
        if any(term in text_lower for term in terms):
            modes.append(mode)
    return modes


def profile_for(character_name):
    return options.propagation_profile_for(character_name)


def identity_missing(character_name, prompt):
    if character_name == "新角色测试":
        return []
    missing = []
    prompt_lower = prompt.lower()
    for token in options.required_identity_tokens_for(character_name):
        if str(token).lower() not in prompt_lower:
            missing.append(token)
    return missing


def check_sample(row):
    issues = []
    prompt = row["prompt"]
    prompt_positive = prompt.split("Avoid:", 1)[0]
    prompt_lower = prompt_positive.lower()

    if len(prompt) > MAX_PROMPT_LENGTH:
        issues.append(f"length>{MAX_PROMPT_LENGTH}:{len(prompt)}")

    missing = identity_missing(row["character"], prompt)
    if missing:
        issues.append("identity_missing:" + "|".join(missing[:3]))

    bad_general = contains_any(prompt_positive, FORBIDDEN_GENERAL_TERMS)
    bad_chinese = contains_any(prompt_positive, FORBIDDEN_CHINESE_TERMS)
    if bad_general:
        issues.append("forbidden_general:" + "|".join(bad_general))
    if bad_chinese:
        issues.append("forbidden_chinese:" + "|".join(bad_chinese))

    for pattern in PROBLEMATIC_TRUNCATION_PATTERNS:
        if pattern in prompt:
            issues.append("bad_truncation:" + pattern)

    modes = camera_modes_in(prompt_positive)
    plan_tags = set(row["plan_tags"])
    action_tags = set(row["action_tags"])
    compatible = options.choose_compatible_action_style(row["character"], [], row["plan"])
    compatible_names = {action["name"] for action in options._compatible_actions_for_plan(row["plan"])}

    if row["action_name"] not in compatible_names:
        issues.append("action_plan_incompatible")

    compatible_visuals = {
        visual["name"] for visual in options._visuals_for_plan(row["plan"])
    }
    if row["visual_name"] not in compatible_visuals:
        issues.append("visual_plan_incompatible")

    if "high_camera" in plan_tags and "low" in modes:
        issues.append("camera_conflict:high_plan_low_prompt")
    if "low_camera" in plan_tags and "high" in modes:
        issues.append("camera_conflict:low_plan_high_prompt")
    if "far_shot" in plan_tags and "close-up" in prompt_lower:
        issues.append("camera_conflict:far_closeup")

    if "centered portrait" in prompt_lower and "not a normal portrait" not in prompt_lower:
        issues.append("portrait_misleading")

    return issues


def main():
    random.seed(RANDOM_SEED)
    characters = options.KNOWN_CHARACTER_NAMES + ["新角色测试"]
    rows = []
    issue_counter = Counter()
    plan_counter = Counter()
    action_counter = Counter()
    visual_counter = Counter()
    character_counter = Counter()
    length_by_character = defaultdict(list)

    for index in range(1, SAMPLE_COUNT + 1):
        character = random.choice(characters)
        recent_tags = []
        plan = options.choose_art_plan(character, recent_tags)
        action = options.choose_compatible_action_style(character, recent_tags, plan)
        visual = options.choose_visual_design(recent_tags, plan)
        prompt = prompt_for_art_direction(character, plan, action, recent_tags, visual)
        row = {
            "index": index,
            "character": character,
            "plan_name": plan["name"],
            "action_name": action["name"],
            "visual_name": visual["name"],
            "plan_tags": plan.get("tags", []),
            "action_tags": action.get("tags", []),
            "prompt_length": len(prompt),
            "prompt": prompt,
            "plan": plan,
        }
        issues = check_sample(row)
        row["issues"] = issues
        rows.append(row)

        character_counter[character] += 1
        plan_counter[plan["name"]] += 1
        action_counter[action["name"]] += 1
        visual_counter[visual["name"]] += 1
        length_by_character[character].append(len(prompt))
        for issue in issues:
            issue_counter[issue.split(":", 1)[0]] += 1

    with RESULT_JSONL.open("w", encoding="utf-8") as f:
        for row in rows:
            out = dict(row)
            out.pop("plan", None)
            f.write(json.dumps(out, ensure_ascii=False) + "\n")

    issue_rows = [row for row in rows if row["issues"]]
    max_len_row = max(rows, key=lambda item: item["prompt_length"])
    min_len_row = min(rows, key=lambda item: item["prompt_length"])

    lines = [
        "# KV Prompt 1000 Sample Audit",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- random_seed: {RANDOM_SEED}",
        f"- sample_count: {SAMPLE_COUNT}",
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

    lines.extend(["", "## Character Distribution", ""])
    for name, count in character_counter.most_common():
        lengths = length_by_character[name]
        avg_len = sum(lengths) / len(lengths)
        lines.append(f"- {name}: {count}, avg_len={avg_len:.1f}, max_len={max(lengths)}")

    lines.extend(["", "## Visual Motif Distribution", ""])
    for name, count in visual_counter.most_common():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Top Plan Distribution", ""])
    for name, count in plan_counter.most_common(20):
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Top Action Distribution", ""])
    for name, count in action_counter.most_common(20):
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## Issue Samples", ""])
    if issue_rows:
        for row in issue_rows[:30]:
            lines.append(
                f"- #{row['index']} {row['character']} / {row['plan_name']} / {row['action_name']} / {row['visual_name']}: {', '.join(row['issues'])}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Full Samples", ""])
    lines.append("Full 1000 prompts are stored in `KV_PROMPT_1000_SAMPLE_AUDIT.jsonl`.")
    lines.append("Each JSONL row contains character, plan, action, visual motif system, prompt length, issues, and full prompt.")

    RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {RESULT_MD}")
    print(f"wrote {RESULT_JSONL}")
    print(f"issue_samples={len(issue_rows)}")
    if issue_counter:
        print("issues:", dict(issue_counter))
    else:
        print("issues: none")


if __name__ == "__main__":
    main()
