from art_direction_options import (
    choose_compatible_action_style,
    choose_art_plan,
    choose_visual_design,
    outfit_variation_for,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
)


STYLE_BASELINE = (
    "high-quality Japanese commercial anime KV, decorative fantasy illustration, crisp lineart, clean color separation"
)


NEGATIVE_GUARDRAILS = (
    "Avoid: extra people, identity drift, broken hands/fingers, missing arms, phone, centered portrait, generic AI portrait, text, watermark, 3D render, empty plain background."
)


SCENE_FIRST_RULES = (
    "KV design first: visual design > world atmosphere > shape rhythm > character."
)


READING_ORDER_RULES = (
    "Read order: big shape, layered atmosphere, identity, small motifs."
)


COMPOSITION_RULES = (
    "Composition: foreground/midground/background layers, occlusion, frames/reflection, arcs, S-curves, repeated circles/ribbons, strong light cuts."
)


CAMERA_PERSPECTIVE_RULES = (
    "Camera: keep one clear perspective; let floor/window/table/path lines prove depth."
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
    for marker in ("; ", ", ", "，", "。", " "):
        cut = clipped.rfind(marker)
        if cut >= int(limit * 0.62):
            clipped = clipped[: cut + len(marker)].rstrip()
            break
    return clipped.rstrip(";,，。") + "..."


def prompt_for_art_direction(character_name, art_plan=None, action_style=None, recent_tags=None):
    if art_plan is None:
        art_plan = choose_art_plan(character_name, recent_tags)
    if action_style is None:
        action_style = choose_compatible_action_style(character_name, recent_tags, art_plan)
    visual_design = choose_visual_design(recent_tags)

    profile = propagation_profile_for(character_name)
    identity_tokens = required_identity_tokens_for(character_name)
    outfit = outfit_variation_for(character_name, art_plan.get("outfit_direction"))

    lines = [
        "Independent image task. References are identity only. One single character.",
        "Apply scene/outfit/action/composition without changing identity.",
        "",
        f"Character: {character_name}.",
        f"Identity: {_clip_text(profile['official_core'], 120)}",
        f"Must keep visible: {_join_list(identity_tokens)}.",
        "",
        f"Pose/framing: {_clip_text(action_style.get('body_silhouette', ''), 135)} {viewer_distance_for(character_name)}.",
        "Hands simple and natural; feet clear only when visible.",
        "",
        SCENE_FIRST_RULES,
        f"Scene: {_clip_text(art_plan.get('graphic_concept', ''), 135)} {_clip_text(art_plan.get('spatial_structure', ''), 150)}",
        f"Visual focus: {_clip_text(art_plan.get('visual_device', ''), 120)}",
        f"Motif/layers: {_clip_text(visual_design.get('motifs', ''), 95)}; {_clip_text(visual_design.get('layering', ''), 115)}.",
        f"Shape rhythm: {_clip_text(visual_design.get('shape_rhythm', ''), 105)}.",
        READING_ORDER_RULES,
        COMPOSITION_RULES,
        CAMERA_PERSPECTIVE_RULES,
        "Scene must not redefine species, hairstyle, personality, or fixed lore.",
        "",
        f"Outfit: {_clip_text(outfit, 170)}.",
        f"Color/light: {_clip_text(profile['color_anchor'], 75)} anchor; {_clip_text(art_plan.get('color_strategy', ''), 95)} {_clip_text(visual_design.get('light_bloom', ''), 120)}",
        f"Poetic direction: {_clip_text(visual_design.get('poetic_line', ''), 155)}.",
        "",
        f"Style: {STYLE_BASELINE}.",
        "Keep hair silhouette, eyes, and core accessories recognizable; make it feel like a product package / VTuber anniversary key visual, not a normal portrait.",
        NEGATIVE_GUARDRAILS,
    ]
    return _compact_lines(lines)
