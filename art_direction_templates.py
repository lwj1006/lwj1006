from art_direction_options import (
    choose_compatible_action_style,
    choose_art_plan,
    choose_visual_design,
    choose_shot_scale,
    choose_composition_plan,
    outfit_variation_for,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
)


STYLE_BASELINE = (
    "high-quality Japanese commercial anime KV, crisp lineart, clean color separation"
)


NEGATIVE_GUARDRAILS = (
    "Avoid: extra people, identity drift, broken hands/fingers, missing arms, hand-held cup, hand-held mug, hand-held drinking glass, hand-held bottle, phone, centered portrait, generic AI portrait, text, watermark, 3D render, empty plain background, sexualized pose, fetish framing, forced weapon, forced vehicle, transparent clothing, clear plastic/vinyl/PVC garments, see-through hoodies, see-through jackets, see-through coats."
)


SCENE_FIRST_RULES = (
    "Identity first; then one selected scene, one compatible outfit, one action, and one camera composition."
)


READING_ORDER_RULES = (
    "Read order: selected scene shape, character identity, outfit silhouette, then only small natural scene details."
)


COMPOSITION_RULES = (
    "Composition: keep one coherent location; foreground and background must come from the selected scene only."
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
    for marker in (". ", "; ", ": "):
        cut = clipped.rfind(marker)
        if cut >= int(limit * 0.45):
            return clipped[: cut + len(marker)].strip().rstrip(";,:.") + "."
    for marker in (", ", " "):
        cut = clipped.rfind(marker)
        if cut >= int(limit * 0.72):
            return clipped[:cut].strip().rstrip(";,:.") + "."
    return clipped.strip().rstrip(";,:.") + "."


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
    if art_plan is None:
        art_plan = choose_art_plan(character_name, recent_tags)
    if action_style is None:
        action_style = choose_compatible_action_style(character_name, recent_tags, art_plan)
    if visual_design is None:
        visual_design = choose_visual_design(recent_tags, art_plan)
    if shot_scale is None:
        shot_scale = choose_shot_scale(recent_tags, art_plan)
    if composition_plan is None:
        composition_plan = choose_composition_plan(
            recent_tags,
            art_plan,
            action_style,
            outfit_direction or art_plan.get("outfit_direction"),
        )

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
        "Body silhouette: preserve natural original proportions; do not enlarge bust, hips, or thighs. Use a neutral slim anime build with modest bust, no cleavage emphasis, no chest-forward pose, and no exaggerated hourglass silhouette.",
        "Hands simple and natural; hands stay empty and must not hold, lift, set down, or touch cups, mugs, drinking glasses, bottles, or beverage containers; any rare beverage prop stays on a distant surface away from the hands. Hands stay outside clothing and away from waistband, pants opening, shorts opening, and inner thigh; feet clear only when visible.",
        "",
        SCENE_FIRST_RULES,
        f"Scene: {_clip_text(art_plan.get('graphic_concept', ''), 90)} {_clip_text(art_plan.get('spatial_structure', ''), 95)}",
        f"Visual focus: {_clip_text(art_plan.get('visual_device', ''), 80)}",
        f"Scene guardrail: {_clip_text(art_plan.get('extra_prompt_guardrail', ''), 120)}" if art_plan.get("extra_prompt_guardrail") else "",
        f"Composition layer: {_clip_text(composition_plan.get('composition', ''), 90)} {_clip_text(composition_plan.get('camera', ''), 70)}",
        f"Foreground/light: {_clip_text(composition_plan.get('foreground', ''), 70)} {_clip_text(composition_plan.get('lighting', ''), 65)}",
        f"Composition guardrail: {_clip_text(composition_plan.get('guardrail', ''), 100)}",
        READING_ORDER_RULES,
        COMPOSITION_RULES,
        CAMERA_PERSPECTIVE_RULES,
        CANDID_GAZE_RULES,
        "Scene must not redefine species, hairstyle, personality, or fixed lore.",
        "",
        f"Outfit: {_clip_text(outfit, 105)}",
        "Outfit opacity rule: all clothing must be opaque woven/knit fabric; lightweight lace, chiffon, or gauze can feel airy but must not look like clear plastic or reveal the body underneath.",
        f"Color/light: identity colors stay in hair, eyes, and small accents ({_clip_text(profile['color_anchor'], 60)}); outfit colorway is model-chosen, cohesive, and wearable. Do not default to white, ivory, cream, pale gray, or an all-pale outfit; most outfits should have a clearly colored, mid-tone, dark, earthy, or muted-chromatic main value, while mostly white/light-neutral outfits appear only occasionally or when the garment concept explicitly requires them. A white or pale background must not make the clothing white. Avoid random clashing colors, rainbow mixing, and harsh neon contrast. {_clip_text(art_plan.get('color_strategy', ''), 70)}",
        "",
        f"Style: {STYLE_BASELINE}.",
        "Keep hair silhouette, eyes, and core accessories recognizable; make it feel like a decorative anime key visual, not a normal portrait.",
        NEGATIVE_GUARDRAILS,
    ]
    prompt = _compact_lines(lines)
    if prompt.count("Outfit:") != 1:
        raise ValueError("final prompt must contain exactly one outfit block")
    return prompt
