from art_direction_options import (
    choose_action_style,
    choose_art_plan,
    outfit_variation_for,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
)


STYLE_BASELINE = (
    "clean high-quality anime illustration, crisp lineart, stable cel shading, "
    "soft clean lighting, sharp face and eyes, clear color separation, fresh trendy lifestyle illustration"
)


NEGATIVE_GUARDRAILS = (
    "Avoid: extra people, duplicate character, identity drift, broken hands, broken feet, extra fingers, "
    "missing arms, phone, hand reaching toward camera, forced weapon holding, text, watermark, 3D render, clutter."
)


def prompt_template_name(template_index=0):
    return "fenjue_v4_stable_compact"


def _join_list(values):
    return "; ".join(str(v).strip() for v in values if str(v).strip())


def _compact_lines(lines):
    return "\n".join(line.strip() for line in lines if line and line.strip())


def prompt_for_art_direction(character_name, art_plan=None, action_style=None, recent_tags=None):
    if art_plan is None:
        art_plan = choose_art_plan(character_name, recent_tags)
    if action_style is None:
        action_style = choose_action_style(character_name, recent_tags)

    profile = propagation_profile_for(character_name)
    identity_tokens = required_identity_tokens_for(character_name)
    outfit = outfit_variation_for(character_name, art_plan.get("outfit_direction"))

    lines = [
        "Independent image task. Ignore previous context. Uploaded references are identity reference only. One single character.",
        "Character identity, scene, outfit, action, and composition are separate layers; apply this scene to the current character without changing identity.",
        "",
        f"Character: {character_name}.",
        f"Identity: {profile['official_core']}",
        f"Must keep visible: {_join_list(identity_tokens)}.",
        f"Feeling: {profile['viewer_relationship']} {profile['thumbnail_strategy']}",
        "",
        f"Pose and framing: {action_style.get('body_silhouette', '')} {viewer_distance_for(character_name)}.",
        "Hands: relaxed, simple, naturally drawn, no exaggerated foreground hands. Feet only need to be clear when visible.",
        "",
        f"Scene: {art_plan.get('graphic_concept', '')} {art_plan.get('spatial_structure', '')}",
        f"Visual focus: {art_plan.get('visual_device', '')}",
        "Scene rule: the setting supports the character; it must not redefine the character's species, hairstyle, personality, or fixed lore.",
        "",
        f"Outfit: {outfit}.",
        f"Color and light: {profile['color_anchor']} as character anchor; {art_plan.get('color_strategy', '')} {art_plan.get('lighting_behavior', '')}",
        "",
        f"Style: {STYLE_BASELINE}.",
        "Composition: face, hair silhouette, eyes, and core accessories are more important than environment detail.",
        NEGATIVE_GUARDRAILS,
    ]
    return _compact_lines(lines)
