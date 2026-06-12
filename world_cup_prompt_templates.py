from art_direction_options import propagation_profile_for, required_identity_tokens_for, viewer_distance_for
from world_cup_prompt_plans import (
    choose_world_cup_action_style,
    choose_world_cup_composition_plan,
    choose_world_cup_shot_scale,
    world_cup_outfit_for,
    world_cup_plan_for,
    world_cup_spec_for,
)


STYLE_BASELINE = "high-quality Japanese commercial anime lifestyle key visual, crisp lineart, clean color separation, premium World Cup street-viewing campaign finish"


def prompt_template_name(template_index=0):
    return "fenjue_world_cup_2026_character_team_special_v1"


def _join_list(values):
    return "; ".join(str(value).strip() for value in values if str(value).strip())


def _compact_lines(lines):
    return "\n".join(line.strip() for line in lines if line and line.strip())


def prompt_for_art_direction(
    character_name,
    art_plan=None,
    action_style=None,
    recent_tags=None,
    visual_design=None,
    outfit_direction=None,
    shot_scale=None,
    composition_plan=None,
):
    art_plan = art_plan or world_cup_plan_for(character_name)
    action_style = action_style or choose_world_cup_action_style(character_name, recent_tags, art_plan)
    shot_scale = shot_scale or choose_world_cup_shot_scale(recent_tags, art_plan)
    composition_plan = composition_plan or choose_world_cup_composition_plan(recent_tags, art_plan, action_style, outfit_direction)
    profile = propagation_profile_for(character_name)
    identity_tokens = required_identity_tokens_for(character_name)
    spec = world_cup_spec_for(character_name)
    outfit = outfit_direction or art_plan.get("outfit_direction") or world_cup_outfit_for(character_name)

    lines = [
        "Independent image task. Uploaded references define character identity only. Create exactly one clearly featured character in one polished World Cup roadside-viewing key visual.",
        "",
        "[CHARACTER-TEAM MATCH]",
        f"Character: {character_name}. Assigned team inspiration: {spec['team']}.",
        f"Why this pairing works visually: {spec['fit_reason']}.",
        f"Identity: {profile['official_core']}",
        f"Must keep visible: {_join_list(identity_tokens)}.",
        f"Identity readability: {viewer_distance_for(character_name)}.",
        "The World Cup supporter theme changes clothing, expression, and environment only. Never change species, hairstyle, eye color, fixed accessories, face, or personality.",
        "",
        "[NATIONAL-TEAM KIT]",
        f"Garment design: {outfit}.",
        "Make the country association readable through classic jersey color blocking, not through copied official branding.",
        "The supporter outfit must fit the character naturally and must not hide signature hair accessories, ears, tail, mechanical parts, or other identity anchors.",
        "All fabric is opaque. Execute the selected T-shirt length, hem treatment, and bottom silhouette clearly; do not replace them with a professional player uniform.",
        "A selected front knot must be one small neat clothing knot only. A selected loose longline T-shirt must remain fully untied with its hem down.",
        "A selected cheek mark must stay tiny, simple, unofficial, and readable as team-color fan decoration rather than an official crest.",
        "Style the outfit as comfortable, tasteful roadside supporter fashion with natural proportions.",
        "",
        "[SPECTATOR MOMENT]",
        f"Natural viewing reaction: {action_style['body_silhouette']}.",
        f"Shot scale: {shot_scale['description']}.",
        f"Composition: {composition_plan['composition']}.",
        f"Camera: {composition_plan['camera']}.",
        f"Foreground and depth: {composition_plan['foreground']}.",
        f"Lighting: {composition_plan['lighting']}.",
        f"Composition guardrail: {composition_plan['guardrail']}.",
        "The character is watching the match as a roadside spectator, not playing football, training, posing as an athlete, or standing on the pitch.",
        "Hands stay simple and anatomically readable. Preserve natural original proportions and a neutral slim anime build. Optional scarf or small team-color accessory must not hide the face or identity.",
        "",
        "[MATCHDAY WORLD]",
        f"Scene: {art_plan['graphic_concept']}. {art_plan['spatial_structure']}.",
        f"World Cup viewing atmosphere: {art_plan['visual_device']}.",
        f"Color direction: {art_plan['color_strategy']}.",
        f"Scene guardrail: {art_plan['extra_prompt_guardrail']}.",
        f"Finish: {STYLE_BASELINE}.",
        "Avoid: football-playing action, kicking, dribbling, shooting, ball at feet, player tunnel, pitch-side athlete pose, extra featured people, duplicate character, broken hands, missing limbs, identity drift, photorealism, 3D render, sexualized pose, fetish framing, trophy, official FIFA marks, official team crest, sponsor logo, watermark, readable words, readable player name, readable jersey number, readable score, readable signage.",
    ]
    prompt = _compact_lines(lines)
    for heading in ("[CHARACTER-TEAM MATCH]", "[NATIONAL-TEAM KIT]", "[SPECTATOR MOMENT]", "[MATCHDAY WORLD]"):
        if prompt.count(heading) != 1:
            raise ValueError(f"final prompt must contain exactly one {heading} block")
    return prompt
