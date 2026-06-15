from art_direction_options import (
    choose_visual_design,
    outfit_has_fixed_colorway,
    outfit_material_rule_for,
    outfit_variation_for,
    propagation_profile_for,
    required_identity_tokens_for,
    viewer_distance_for,
)
from photographer_prompt_plans import (
    choose_photographer_action_style,
    choose_photographer_composition_plan,
    choose_photographer_focus_style,
    choose_photographer_scene_plan,
    choose_photographer_shot_scale,
)


STYLE_BASELINE = "high-quality Japanese commercial anime KV, crisp lineart, clean color separation"

NEGATIVE_GUARDRAILS = (
    "Avoid: extra people, identity drift, broken hands/fingers, missing arms, hand-held cup, "
    "hand-held mug, hand-held drinking glass, hand-held bottle, phone, generic AI portrait, "
    "text, watermark, 3D render, empty plain background, sexualized pose, fetish framing, "
    "large foreground obstruction, scenery-dominant composition, tiny unclear subject, "
    "forced weapon, forced vehicle, transparent clothing, clear plastic/vinyl/PVC garments, "
    "see-through hoodies, see-through jackets, see-through coats."
)


def prompt_template_name(template_index=0):
    return "fenjue_v8_balanced_camera_photographer"


def _join_list(values):
    return "; ".join(str(value).strip() for value in values if str(value).strip())


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


def _scene_block(art_plan):
    lines = [
        f"Location and atmosphere: {_clip_text(art_plan.get('graphic_concept', ''), 135)}",
        f"Spatial structure: {_clip_text(art_plan.get('spatial_structure', ''), 165)}",
        f"Environmental visual rhythm: {_clip_text(art_plan.get('visual_device', ''), 125)}",
        f"Light and scene color: {_clip_text(art_plan.get('lighting_behavior', ''), 115)} {_clip_text(art_plan.get('color_strategy', ''), 115)}",
        f"Scene guardrail: {_clip_text(art_plan.get('extra_prompt_guardrail', ''), 135)}"
        if art_plan.get("extra_prompt_guardrail")
        else "",
        "Keep one coherent, restrained location. Background supports the character and must never compete with face or outfit.",
    ]
    scene_text = " ".join(str(art_plan.get(key, "")) for key in ("name", "graphic_concept", "spatial_structure", "visual_device", "tags")).lower()
    if any(word in scene_text for word in ("poster", "letter", "typography", "graphic")):
        lines.append("Typography-like shapes must stay abstract: no readable words, letters, logos, brand text, or UI text.")
    if any(word in scene_text for word in ("mirror", "reflection", "reflected", "acrylic", "glass")):
        lines.append("Reflections may show abstract fragments or partial echoes only, never a second character or duplicate person.")
    return lines


def _photographer_block(action_style, shot_scale, composition_plan, focus_style):
    return [
        "Photographic intent: create a stable photographer-composed anime image with face and outfit as the first visual focus.",
        f"Photographer position and framing: {_clip_text(composition_plan.get('composition', ''), 135)}",
        f"Lens and viewpoint: {_clip_text(composition_plan.get('camera', ''), 115)}",
        f"Exact timing and subject motion: {_clip_text(action_style.get('body_silhouette', ''), 175)}",
        f"Camera-specific pose handling: {_clip_text(composition_plan.get('pose', ''), 165)}",
        f"Perspective and foreground depth: {_clip_text(composition_plan.get('foreground', ''), 115)}",
        f"Exposure and separation: {_clip_text(composition_plan.get('lighting', ''), 100)}",
        f"Subject scale: {_clip_text(shot_scale.get('description', ''), 145)}",
        f"Optical focus treatment: {_clip_text(focus_style.get('description', ''), 155)}",
        f"Framing guardrail: {_clip_text(composition_plan.get('guardrail', ''), 130)}",
        (
            "Hard crop rule: never create a full-body, near-full-body, head-to-toe, or distant standing-character image. "
            "Do not show both feet completely. Even for standing, walking, seated, high-angle, or wide environmental shots, "
            "crop at upper calf or closer and keep the face plus outfit as the dominant read."
        ),
        (
            "The photographer position, subject movement, body direction, weight, gaze, foreground, "
            "and perspective must describe the same captured instant. Follow the selected camera angle, "
            "shot scale, and body direction exactly rather than replacing them with a generic default portrait. "
            "Keep the character readable and the background subordinate."
        ),
    ]


def _character_block(character_name, profile, identity_tokens):
    return [
        f"Character: {character_name}.",
        f"Identity: {_clip_text(profile['official_core'], 125)}",
        f"Must keep visible: {_join_list(identity_tokens)}.",
        f"Natural behavior: {_clip_text(profile['interaction_rule'], 185)}",
        f"Identity readability: {viewer_distance_for(character_name)}.",
        (
            "Preserve natural original proportions. Use a neutral slim anime build with modest bust, "
            "no cleavage emphasis, no chest-forward pose, and no exaggerated hourglass silhouette."
        ),
        (
            "Hands stay simple, empty of objects, and anatomically readable. They must not hold, lift, set down, "
            "or touch cups, mugs, drinking glasses, bottles, or beverage containers. Hands stay outside "
            "clothing and away from clothing openings."
        ),
        (
            "Scene, camera, and action may change, but species, hairstyle, eye color, identity accessories, "
            "and fixed character traits must remain stable."
        ),
    ]


def _outfit_block(outfit, profile):
    outfit_material_rule = outfit_material_rule_for(outfit)
    if outfit_has_fixed_colorway(outfit):
        color_direction = (
            "Color direction: preserve the garment colors explicitly stated in the outfit. Keep character "
            f"identity colors stable ({_clip_text(profile['color_anchor'], 70)}) and do not add unrelated accent colors."
        )
    else:
        color_direction = (
            "Color direction: identity colors remain mainly in hair, eyes, and small accents "
            f"({_clip_text(profile['color_anchor'], 70)}). Do not default to white, ivory, cream, pale gray, "
            "or an all-pale outfit. Most outfits need a clearly colored, mid-tone, dark, earthy, or "
            "muted-chromatic main value. A white or pale background must not make the clothing white."
        )
    return [
        f"Garment design: {_clip_text(outfit, 190)}",
        f"Material separation: {outfit_material_rule}." if outfit_material_rule else "",
        (
            "Use opaque woven or knit fabric. Lightweight lace, chiffon, or gauze may feel airy but must "
            "never look like clear plastic or reveal the body underneath."
        ),
        color_direction,
        (
            f"Finish: {STYLE_BASELINE}. Keep clothing cohesive and wearable; avoid random clashing colors, "
            "rainbow mixing, and harsh neon contrast."
        ),
        NEGATIVE_GUARDRAILS,
    ]


def prompt_for_art_direction(
    character_name,
    art_plan=None,
    action_style=None,
    recent_tags=None,
    visual_design=None,
    outfit_direction=None,
    shot_scale=None,
    composition_plan=None,
    focus_style=None,
):
    if art_plan is None:
        art_plan = choose_photographer_scene_plan(character_name, recent_tags)
    if action_style is None:
        action_style = choose_photographer_action_style(character_name, recent_tags, art_plan)
    if visual_design is None:
        visual_design = choose_visual_design(recent_tags, art_plan)
    if composition_plan is None:
        composition_plan = choose_photographer_composition_plan(
            recent_tags,
            art_plan,
            action_style,
            outfit_direction or art_plan.get("outfit_direction"),
        )
    if shot_scale is None:
        shot_scale = choose_photographer_shot_scale(recent_tags, art_plan, composition_plan, action_style)
    if focus_style is None:
        focus_style = choose_photographer_focus_style(recent_tags, art_plan, composition_plan)

    profile = propagation_profile_for(character_name)
    identity_tokens = required_identity_tokens_for(character_name)
    outfit = outfit_variation_for(character_name, outfit_direction or art_plan.get("outfit_direction"))

    lines = [
        "Independent image task. References define character identity only. Create one coherent photographer-composed anime key visual with one character, not photorealistic.",
        "",
        "[SCENE]",
        *_scene_block(art_plan),
        "",
        "[PHOTOGRAPHER]",
        *_photographer_block(action_style, shot_scale, composition_plan, focus_style),
        "",
        "[CHARACTER]",
        *_character_block(character_name, profile, identity_tokens),
        "",
        "[OUTFIT]",
        *_outfit_block(outfit, profile),
    ]
    prompt = _compact_lines(lines)
    for heading in ("[SCENE]", "[PHOTOGRAPHER]", "[CHARACTER]", "[OUTFIT]"):
        if prompt.count(heading) != 1:
            raise ValueError(f"final prompt must contain exactly one {heading} block")
    return prompt
