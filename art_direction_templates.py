from art_direction_options import (
    choose_compatible_action_style,
    choose_art_plan,
    choose_visual_design,
    choose_shot_scale,
    outfit_variation_for,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
)


STYLE_BASELINE = (
    "high-quality Japanese commercial anime KV, crisp lineart, clean color separation"
)


NEGATIVE_GUARDRAILS = (
    "Avoid: extra people, identity drift, broken hands/fingers, missing arms, phone, centered portrait, generic AI portrait, text, watermark, 3D render, empty plain background, sexualized pose, fetish framing, forced weapon, forced vehicle."
)


SCENE_FIRST_RULES = (
    "Identity first; then pose/composition, selected scene, and compatible decorative KV motifs."
)


READING_ORDER_RULES = (
    "Read order: big shape, layered atmosphere, identity, small motifs."
)


COMPOSITION_RULES = (
    "Composition: layered foreground/midground/background, occlusion, frames/reflection, clear light cuts."
)


CAMERA_PERSPECTIVE_RULES = (
    "Camera: cinematic composition with clear depth; natural front three-quarter, front-facing, or gentle side angles are all valid."
)


CANDID_GAZE_RULES = (
    "Gaze/body direction: vary naturally; prefer front-facing, front three-quarter attention, or gentle side angles; direct eye contact and eyes-away moments are both allowed."
)


def prompt_template_name(template_index=0):
    return "fenjue_v4_stable_compact"


def _join_list(values):
    return "; ".join(str(v).strip() for v in values if str(v).strip())


def _compact_lines(lines):
    return "\n".join(line.strip() for line in lines if line and line.strip())


def _clip_text(value, limit):
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    clipped = text[:limit].rstrip()
    for marker in (". ", "。", "; ", "；"):
        cut = clipped.rfind(marker)
        if cut >= int(limit * 0.45):
            return clipped[: cut + len(marker)].strip().rstrip(";,，；。.") + "."
    for marker in (", ", "，", " "):
        cut = clipped.rfind(marker)
        if cut >= int(limit * 0.72):
            return clipped[:cut].strip().rstrip(";,，；。.") + "."
    return clipped.strip().rstrip(";,，；。.") + "."


def prompt_for_art_direction(
    character_name,
    art_plan=None,
    action_style=None,
    recent_tags=None,
    visual_design=None,
    outfit_direction=None,
    shot_scale=None,
):
    if art_plan is None:
        art_plan = choose_art_plan(character_name, recent_tags)
    if action_style is None:
        action_style = choose_compatible_action_style(character_name, recent_tags, art_plan)
    if visual_design is None:
        visual_design = choose_visual_design(recent_tags, art_plan)
    if shot_scale is None:
        shot_scale = choose_shot_scale(recent_tags, art_plan)

    profile = propagation_profile_for(character_name)
    identity_tokens = required_identity_tokens_for(character_name)
    outfit = outfit_variation_for(character_name, outfit_direction or art_plan.get("outfit_direction"))

    lines = [
        "Independent image task. References are identity only. One single character.",
        "Apply scene/outfit/action/composition without changing identity.",
        "",
        f"Character: {character_name}.",
        f"Identity: {_clip_text(profile['official_core'], 90)}",
        f"Must keep visible: {_join_list(identity_tokens)}.",
        f"Character rule: {_clip_text(profile['interaction_rule'], 160)}",
        "",
        f"Shot scale: {_clip_text(shot_scale.get('description', ''), 150)}.",
        f"Pose/framing: {_clip_text(action_style.get('body_silhouette', ''), 105).rstrip('.')}. {viewer_distance_for(character_name)}.",
        "Hands simple and natural; feet clear only when visible.",
        "",
        SCENE_FIRST_RULES,
        f"Scene: {_clip_text(art_plan.get('graphic_concept', ''), 90)} {_clip_text(art_plan.get('spatial_structure', ''), 95)}",
        f"Visual focus: {_clip_text(art_plan.get('visual_device', ''), 80)}",
        f"Motif/layers: {_clip_text(visual_design.get('motifs', ''), 65)} {_clip_text(visual_design.get('layering', ''), 75)}",
        f"Shape rhythm: {_clip_text(visual_design.get('shape_rhythm', ''), 70)}",
        READING_ORDER_RULES,
        COMPOSITION_RULES,
        CAMERA_PERSPECTIVE_RULES,
        CANDID_GAZE_RULES,
        "Scene must not redefine species, hairstyle, personality, or fixed lore.",
        "",
        f"Outfit: {_clip_text(outfit, 105)}",
        f"Color/light: {_clip_text(profile['color_anchor'], 60)} anchor; {_clip_text(art_plan.get('color_strategy', ''), 65)} {_clip_text(visual_design.get('light_bloom', ''), 80)}",
        f"Poetic direction: {_clip_text(visual_design.get('poetic_line', ''), 120)}",
        "",
        f"Style: {STYLE_BASELINE}.",
        "Keep hair silhouette, eyes, and core accessories recognizable; make it feel like a decorative anime key visual, not a normal portrait.",
        NEGATIVE_GUARDRAILS,
    ]
    return _compact_lines(lines)
