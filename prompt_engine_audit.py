import ast
import sys
from pathlib import Path

import art_direction_options as options
import chatgpt_batch_pyautogui as batch
from art_direction_templates import prompt_for_art_direction


PROJECT_DIR = Path(__file__).resolve().parent
KNOWN_CHARACTERS = [
    "南宫",
    "爱芮",
    "千夏",
    "丹",
    "星见雅",
    "仪玄",
    "叶瞬光",
    "席德",
    "橘福福",
]
SAMPLE_CHARACTERS = KNOWN_CHARACTERS + ["新角色测试"]
BAD_SCENE_WORDS = [
    "工厂",
    "雨天",
    "霓虹",
    "城市夜景",
    "factory",
    "rainy",
    "neon",
]
PROMPT_MIN_LENGTH = 800
PROMPT_MAX_LENGTH = 3000


def count_top_level_assignments(path: Path, name: str) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    count = 0
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    count += 1
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == name:
                count += 1
    return count


def fail(message: str, failures: list[str]) -> None:
    print(f"FAIL: {message}")
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    options_path = Path(options.__file__).resolve()
    print(f"options file: {options_path}")
    print(f"project dir: {PROJECT_DIR}")
    runtime_config_path = PROJECT_DIR / "config" / "runtime_art_direction.json"
    if runtime_config_path.exists():
        batch.load_runtime_batch_config(runtime_config_path)
        print(f"runtime config: {runtime_config_path} revision={options.RUNTIME_CONFIG_REVISION}")

    if options_path.parent != PROJECT_DIR:
        fail("art_direction_options.py is imported from the wrong directory", failures)

    plan_assign_count = count_top_level_assignments(options_path, "ART_DIRECTION_PLANS")
    if plan_assign_count != 1:
        fail(f"ART_DIRECTION_PLANS should be assigned once, got {plan_assign_count}", failures)

    plan_names = [plan["name"] for plan in options.ART_DIRECTION_PLANS]
    action_names = [action["name"] for action in options.ACTION_STYLES]
    outfit_directions = set(options.OUTFIT_DIRECTIONS)
    plan_tags = getattr(options, "PLAN_TAGS", {})
    action_tags = getattr(options, "ACTION_TAGS", {})
    plan_weights = getattr(options, "CHARACTER_PLAN_WEIGHTS", {})
    action_weights = getattr(options, "CHARACTER_ACTION_WEIGHTS", {})

    print(f"active plans: {len(plan_names)}")
    print(f"active actions: {len(action_names)}")
    print(f"PLAN_TAGS coverage: {len(plan_tags)}/{len(plan_names)}")
    print(f"ACTION_TAGS coverage: {len(action_tags)}/{len(action_names)}")

    missing_tags = [name for name in plan_names if name not in plan_tags]
    if missing_tags:
        fail(f"missing PLAN_TAGS: {missing_tags}", failures)

    missing_outfit_directions = [
        plan["outfit_direction"] for plan in options.ART_DIRECTION_PLANS
        if plan.get("outfit_direction") not in outfit_directions
    ]
    if missing_outfit_directions:
        fail(f"plan outfit_direction not in OUTFIT_DIRECTIONS: {missing_outfit_directions}", failures)

    missing_action_tags = [name for name in action_names if name not in action_tags]
    if missing_action_tags:
        fail(f"missing ACTION_TAGS: {missing_action_tags}", failures)

    for character_name in KNOWN_CHARACTERS:
        missing_plan_weights = [
            name for name in plan_names
            if name not in plan_weights.get(character_name, {})
        ]
        missing_action_weights = [
            name for name in action_names
            if name not in action_weights.get(character_name, {})
        ]
        if missing_plan_weights:
            fail(f"{character_name} missing plan weights: {missing_plan_weights}", failures)
        if missing_action_weights:
            fail(f"{character_name} missing action weights: {missing_action_weights}", failures)

    for character_name in SAMPLE_CHARACTERS:
        plan, action = options.choose_plan_and_action(character_name, [])
        prompt = prompt_for_art_direction(character_name, plan, action)
        length = len(prompt)
        print(f"prompt length {character_name}: {length}")
        if not (PROMPT_MIN_LENGTH <= length <= PROMPT_MAX_LENGTH):
            fail(f"{character_name} prompt length out of range: {length}", failures)
        bad_hits = [word for word in BAD_SCENE_WORDS if word in prompt]
        if bad_hits:
            fail(f"{character_name} prompt contains unwanted scene words: {bad_hits}", failures)
        if plan["outfit_direction"] not in prompt:
            fail(f"{character_name} prompt did not use selected outfit_direction: {plan['outfit_direction']}", failures)

    if failures:
        print(f"audit result: NOT READY ({len(failures)} issue(s))")
        return 1

    print("audit result: READY for longer run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
