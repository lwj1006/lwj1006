from art_direction_options import propagation_profile_for, required_identity_tokens_for, viewer_distance_for
from world_cup_prompt_plans import (
    choose_world_cup_action_style,
    choose_world_cup_composition_plan,
    choose_world_cup_shot_scale,
    world_cup_outfit_for,
    world_cup_plan_for,
    world_cup_spec_for,
)


STYLE_BASELINE = "high-quality Japanese commercial anime supporter campaign poster, crisp lineart, clean color separation, bold national-color graphic design, premium series-ready World Cup advertising finish"


def prompt_template_name(template_index=0):
    return "fenjue_world_cup_2026_supporter_campaign_poster_v2"


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
    spec = {
        "team": art_plan.get("team"),
        "slug": str(art_plan.get("name", "")).removeprefix("world_cup_"),
        "kit": "",
        "fit_reason": art_plan.get("fit_reason", "modern supporter-poster styling"),
    }
    if not spec["team"]:
        spec = world_cup_spec_for(character_name)
    outfit = outfit_direction or art_plan.get("outfit_direction") or world_cup_outfit_for(character_name)

    lines = [
        "Independent image task. Uploaded references define character identity only. Create exactly one clearly featured character in one official campaign-style World Cup supporter poster, not a scene of someone actually watching a match.",
        "Poster hierarchy: first read is the designed World Cup supporter campaign poster; second read is the national-team-inspired fashion; third read is the recognizable character portrait.",
        "",
        "[CHARACTER-TEAM MATCH]",
        f"Character: {character_name}. Randomly selected team inspiration for this poster: {spec['team']}.",
        f"Selected supporter-poster mood: {spec['fit_reason']}.",
        f"Identity: {profile['official_core']}",
        f"Must keep visible: {_join_list(identity_tokens)}.",
        f"Identity readability: {viewer_distance_for(character_name)}.",
        "The World Cup supporter theme changes clothing, expression, and environment only. Never change species, hairstyle, eye color, fixed accessories, face, or personality.",
        "",
        "[NATIONAL-TEAM KIT]",
        f"Garment design: {outfit}.",
        "Make the country association readable through classic jersey color blocking, not through copied official branding.",
        "Jersey design fidelity: preserve the selected modern tonal pattern, collar shape, sleeve-cuff structure, shoulder treatment, and side-panel geometry. Do not fall back to a plain-color national-team shirt.",
        "The supporter outfit must fit the character naturally and must not hide signature hair accessories, ears, tail, mechanical parts, or other identity anchors.",
        "All fabric is opaque. Execute the selected T-shirt length, hem treatment, and bottom silhouette clearly; do not replace them with a professional player uniform.",
        "A selected front knot must be one small neat clothing knot only. A selected loose longline T-shirt must remain fully untied with its hem down.",
        "A selected cheek mark must stay tiny, simple, unofficial, and readable as team-color fan decoration rather than an official crest.",
        "Style the outfit as comfortable, tasteful national-team supporter poster fashion with natural proportions.",
        "",
        "[FRONT-FACING SUPPORTER POSTER]",
        f"Iconic supporter pose: {action_style['body_silhouette']}.",
        f"Shot scale: {shot_scale['description']}.",
        f"Composition: {composition_plan['composition']}.",
        f"Camera: {composition_plan['camera']}.",
        f"Foreground and depth: {composition_plan['foreground']}.",
        f"Lighting: {composition_plan['lighting']}.",
        f"Composition guardrail: {composition_plan['guardrail']}.",
        "The character is posing for a national-team supporter campaign poster, not actually watching a match, playing football, training, or posing as an athlete.",
        "Pose and expression discipline: execute the selected football-supporter pose clearly, but keep the face natural, attractive, restrained, and faithful to the character's established personality. Expression intensity stays low to moderate; use relaxed eyes and a closed-mouth or only slightly open natural smile when appropriate. Do not force dramatic acting.",
        "Supporter-prop rule: a selected scarf stays text-free and crest-free. A selected large or small national flag may be held in front, beside the body, diagonally across the foreground, waved from a pole, or spread behind the shoulders, but must never be worn, wrapped around the body, or draped like a cape. Front flags stay below the upper torso and must not hide the face, hair identity, hands, or main jersey design.",
        "Hands stay simple and anatomically readable. Preserve natural original proportions and a neutral slim anime build.",
        "",
        "[MATCHDAY POSTER WORLD]",
        f"Scene: {art_plan['graphic_concept']}. {art_plan['spatial_structure']}.",
        f"World Cup viewing atmosphere: {art_plan['visual_device']}.",
        f"Color direction: {art_plan['color_strategy']}.",
        f"Scene guardrail: {art_plan['extra_prompt_guardrail']}.",
        "Poster layout rule: use a vertical poster composition, a clean top or side title-space negative area, bold national-color framing, structured graphic layers, and deliberate breathing room around the full hair silhouette.",
        "Background rule: use a bright open daytime football stadium with fresh green pitch, pale seating tiers, blue sky, soft white clouds, and simplified shallow stadium geometry. Keep it clean, airy, and subordinate to the character.",
        "Title-space rule: reserve an intentionally empty clean area for later typography, but generate no actual letters, words, numbers, slogan, logo, or UI text.",
        f"Finish: {STYLE_BASELINE}.",
        "Avoid: exaggerated facial acting, unnaturally wide smile, forced open mouth, shouting mouth, tongue visible, overly wide eyes, sparkling manic eyes, strained eyebrows, crying face, distorted expression, blank expression, emotionless face, mechanical raised open hand, polite clapping pose, hands hovering as if clapping, attendance-roll gesture, stiff idle pose, flag worn as clothing, flag wrapped around the body, flag cape, watching an off-frame screen, off-frame viewing gaze, night scene, darkness, black background, street, cafe, shopfront, bar, public screen, dramatic night bokeh, realistic deep environment, scenery-dominant composition, cramped crop, missing title-space margin, football-playing action, kicking, dribbling, shooting, ball at feet, player tunnel, pitch-side athlete pose, extra featured people, duplicate character, broken hands, missing limbs, identity drift, photorealism, 3D render, sexualized pose, fetish framing, trophy, official FIFA marks, official team crest, sponsor logo, watermark, readable words, readable player name, readable jersey number, readable score, readable signage.",
    ]
    prompt = _compact_lines(lines)
    for heading in ("[CHARACTER-TEAM MATCH]", "[NATIONAL-TEAM KIT]", "[FRONT-FACING SUPPORTER POSTER]", "[MATCHDAY POSTER WORLD]"):
        if prompt.count(heading) != 1:
            raise ValueError(f"final prompt must contain exactly one {heading} block")
    return prompt
