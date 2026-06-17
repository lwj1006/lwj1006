from __future__ import annotations

from . import plans, templates

LABEL = "master artist composition"
_combo_cache: dict[str, dict] = {}
_last_combo: dict | None = None

def _cache_key(character_name: str, plan_name: str | None = None) -> str:
    return f"{character_name}::{plan_name or ''}"

def _remember_combo(character_name: str, combo: dict) -> None:
    global _last_combo
    plan_name = combo["art_plan"]["name"]
    _combo_cache[_cache_key(character_name, plan_name)] = combo
    _combo_cache[_cache_key(character_name)] = combo
    _last_combo = combo

def _combo_for(character_name: str, art_plan: dict | None = None, recent_tags=None) -> dict:
    plan_name = art_plan.get("name") if art_plan else None
    if not character_name and _last_combo:
        return _last_combo
    cached = _combo_cache.get(_cache_key(character_name, plan_name)) or _combo_cache.get(_cache_key(character_name))
    if cached:
        return cached
    combo = plans.choose_develop_combo(character_name, recent_tags)
    _remember_combo(character_name, combo)
    return combo

def activate(batch, args=None) -> None:
    def skip_original_scene_selection():
        print("Original scene category menu skipped: mode C uses the master artist composition plan system.", flush=True)
        return None
    def skip_original_clothing_selection():
        print("Original clothing menu skipped: mode C uses each artist composition plan's outfit direction.", flush=True)
        return None
    def choose_artist_plan_and_action(character_name, recent_visual_tags, used_themes_by_character, used_plans_by_character, batch_used_themes=None, batch_used_plans=None, allowed_plan_names=None):
        batch_used_plans = batch_used_plans or set()
        allowed = set(allowed_plan_names or [])
        fallback = None
        for _ in range(120):
            combo = plans.choose_develop_combo(character_name, recent_visual_tags)
            art_plan = combo["art_plan"]
            if allowed and art_plan["name"] not in allowed:
                continue
            if fallback is None:
                fallback = combo
            if art_plan["name"] not in batch_used_plans:
                _remember_combo(character_name, combo)
                return art_plan, combo["action_style"]
        combo = fallback or plans.choose_develop_combo(character_name, recent_visual_tags)
        _remember_combo(character_name, combo)
        return combo["art_plan"], combo["action_style"]
    def choose_artist_clothing(character_name, art_plan, used_by_character, batch_used_themes=None):
        return art_plan["outfit_direction"]
    def keep_artist_outfit(character_name, theme, art_plan):
        return theme, False
    def choose_artist_shot_scale(recent_tags=None, plan=None):
        combo = _combo_for("", plan, recent_tags)
        lens = combo["camera_lens"]
        return {"name": lens["name"], "description": lens["prompt_concept"], "tags": lens.get("tags", set())}
    def choose_artist_composition_plan(recent_tags=None, plan=None, action=None, outfit_direction=None):
        combo = _combo_for("", plan, recent_tags)
        information_balance = combo["information_balance"]
        return {"name": information_balance["name"], "composition": information_balance["prompt_concept"], "tags": information_balance.get("tags", set())}
    def prompt_for_artist_composition(character_name, art_plan=None, action_style=None, recent_tags=None, visual_design=None, outfit_direction=None, shot_scale=None, composition_plan=None):
        combo = _combo_for(character_name, art_plan, recent_tags)
        return templates.prompt_for_art_direction(character_name, combo["art_plan"], combo["director_class"], combo["energy_profile"], combo["energy_state"], combo["action_style"], combo["weather_atmosphere"], combo["camera_lens"], combo["lighting_strategy"], combo["information_balance"], combo["complexity_budget"])
    def collect_artist_cooldown_tags(art_plan, action_style):
        combo = _combo_for("", art_plan)
        return plans.collect_develop_cooldown_tags(combo["art_plan"], combo["action_style"], combo["weather_atmosphere"], combo["camera_lens"], combo["lighting_strategy"], combo["information_balance"], combo["director_class"], combo["complexity_budget"], combo["energy_profile"], combo["energy_state"])
    batch.choose_character_plan_and_action = choose_artist_plan_and_action
    batch.choose_compatible_clothing_theme = choose_artist_clothing
    batch.outfit_with_optional_black_hosiery = keep_artist_outfit
    batch.choose_shot_scale = choose_artist_shot_scale
    batch.choose_composition_plan = choose_artist_composition_plan
    batch.collect_cooldown_tags = collect_artist_cooldown_tags
    batch.startup_scene_selection = skip_original_scene_selection
    batch.startup_clothing_selection = skip_original_clothing_selection
    batch.prompt_for_art_direction = prompt_for_artist_composition
    batch.prompt_template_name = templates.prompt_template_name
    print("Prompt mode C active: master artist composition pipeline. " f"Visual plans: {len(plans.ART_DIRECTION_PLANS)}.", flush=True)
