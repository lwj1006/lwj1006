import collections
import random

from fenjue.runtime import batch
from fenjue.modes.original.templates import prompt_for_art_direction


SAMPLE_COUNT = 50
RANDOM_SEED = 5600

FORBIDDEN_TERMS = [
    "classroom",
    "blackboard",
    "chalkboard",
    "after-school",
    "school-inspired",
    "track jacket",
    "warm-up jacket",
    "tennis skirt",
    "badminton warm-up",
]


def is_brand_theme(theme: str) -> bool:
    return "Adidas-inspired" in theme or "Yonex-inspired" in theme


def run_audit(sample_count: int = SAMPLE_COUNT) -> dict:
    random.seed(RANDOM_SEED)
    used_themes_by_character: dict[str, list[str]] = {}
    used_plans_by_character: dict[str, list[str]] = {}
    recent_visual_tags: list[str] = []
    characters = batch.CHARACTER_SEQUENCE

    plan_counts = collections.Counter()
    theme_counts = collections.Counter()
    character_theme_counts = collections.defaultdict(collections.Counter)
    plan_theme_counts = collections.Counter()
    forbidden_hits = []

    for index in range(sample_count):
        if index % batch.CHARACTERS_PER_BATCH == 0:
            batch_used_themes: set[str] = set()
            batch_used_plans: set[str] = set()

        character_name = characters[index % len(characters)]
        art_plan, action_style = batch.choose_character_plan_and_action(
            character_name,
            recent_visual_tags,
            used_themes_by_character,
            used_plans_by_character,
            batch_used_themes,
            batch_used_plans,
        )
        theme = batch.choose_character_clothing_theme(
            character_name,
            used_themes_by_character,
            batch_used_themes,
        )
        prompt = prompt_for_art_direction(
            character_name,
            art_plan,
            action_style,
            outfit_direction=theme,
        )

        plan_name = art_plan["name"]
        plan_counts[plan_name] += 1
        theme_counts[theme] += 1
        character_theme_counts[character_name][theme] += 1
        plan_theme_counts[(plan_name, theme)] += 1

        batch_used_themes.add(theme)
        batch_used_plans.add(plan_name)
        recent_visual_tags.extend(batch.collect_cooldown_tags(art_plan, action_style))
        recent_visual_tags = recent_visual_tags[-12:]

        lowered = prompt.lower()
        for term in FORBIDDEN_TERMS:
            if term in lowered:
                forbidden_hits.append(
                    {
                        "index": index,
                        "character": character_name,
                        "plan": plan_name,
                        "theme": theme,
                        "term": term,
                    }
                )

    brand_count = sum(count for theme, count in theme_counts.items() if is_brand_theme(theme))
    brand_pairs = [
        (plan, theme, count)
        for (plan, theme), count in plan_theme_counts.items()
        if is_brand_theme(theme)
    ]
    repeated_character_themes = {
        character: themes
        for character, themes in character_theme_counts.items()
        if any(
            count > 1
            for theme, count in themes.items()
            if not is_brand_theme(theme)
        )
    }

    return {
        "sample_count": sample_count,
        "forbidden_hits": forbidden_hits,
        "brand_count": brand_count,
        "yonex_count": sum(count for theme, count in theme_counts.items() if "Yonex-inspired" in theme),
        "adidas_count": sum(count for theme, count in theme_counts.items() if "Adidas-inspired" in theme),
        "top_plans": plan_counts.most_common(10),
        "top_themes": theme_counts.most_common(10),
        "brand_pairs": brand_pairs,
        "repeated_character_themes": repeated_character_themes,
    }


def main() -> None:
    result = run_audit()
    for key, value in result.items():
        print(f"{key}: {value}")

    if result["forbidden_hits"]:
        raise SystemExit("Forbidden terms appeared in final prompts")
    if result["brand_count"] > 8:
        raise SystemExit("Brand outfits exceeded low-frequency audit threshold")


if __name__ == "__main__":
    main()
