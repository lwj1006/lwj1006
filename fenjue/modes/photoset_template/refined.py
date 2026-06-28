from __future__ import annotations

import re

from .library import (
    A3_HAND_DRAWN_STYLE,
    A3_NEGATIVE,
    PhotosetShot,
    PhotosetTemplate,
    _adapt_shot_prompt,
    _character_adaptation,
    _compact,
    _english_only_text,
    _profile_identity_block,
    _remove_template_identity_traits,
    _soften_platform_sensitive_terms,
)


REFINED_SHOT_TITLES: dict[str, tuple[str, ...]] = {
    "035": (
        "Close portrait with both hands at the collarbone and grapes in the foreground",
        "Reclining three-quarter portrait on the wooden platform among hydrangeas and grapes",
        "Prone side pose with bent raised feet behind the body and grapes near the front edge",
        "Two-part close portrait variation holding a green grape cluster near the cheek",
        "Tight face portrait holding one grape beside the lips",
        "Seated full-body portrait on the platform with one leg lowered through mint tulle",
        "Overhead reclining portrait framed by fern leaves, grapes, and pale flowers",
        "Diagonal seated portrait lifting one grape into the window light",
        "Kneeling three-quarter portrait holding a full grape cluster against the torso",
        "Low prone close portrait with grapes and a green apple in the foreground",
    ),
    "036": (
        "Standing side-profile portrait against dark carved courtyard panels",
        "Horizontal tight side profile with pink orchids and dark wood behind",
        "Seated three-quarter portrait with one knee raised and one orchid in hand",
        "Front close portrait holding a single orchid below the chin",
        "Standing full portrait beneath a white paper parasol in the shaded courtyard",
    ),
    "037": (
        "Wide seated floor portrait beside oversized hydrangeas and black ceramic vase",
        "Knee-up tea-table portrait with one hand beside the celadon cup",
        "Tight face portrait raising a pale green cup near the lips",
        "Standing side portrait holding one white flower in warm rim light",
        "Extreme side-profile flower portrait with strong golden edge light",
        "Close three-quarter portrait smelling a white flower in golden light",
    ),
    "038": (
        "Low prone white-bed portrait extending a water glass toward the foreground",
        "Tight seated portrait with one hand raised above the crown",
        "Kneeling three-quarter portrait on white drapery with one hand near the crown",
        "Wide prone bed portrait holding a glass with the body stretched diagonally",
        "Compact seated portrait hugging both knees close to the torso",
        "Side-lean portrait resting both forearms across a black sofa back",
        "Extreme horizontal face close-up with a white feather above the lips",
        "Wide seated bed portrait with asymmetrical legs and white negative space",
        "Overhead black-sofa portrait with both arms lifted above the head",
    ),
    "039": (
        "Back-facing window portrait in white lace with head turned to profile",
        "High-angle full seated portrait on a white-covered sofa beside bottles and books",
        "Tight frontal portrait with one arm raised above the crown",
        "Reclining portrait with one arm extended overhead across white bedding",
        "Waist-up seated portrait crossed by a narrow warm window-light stripe",
        "Extreme face close-up with warm rim light crossing one side of the face",
        "Over-shoulder close portrait with bare-back dress geometry translated to secure coverage",
        "Standing rear three-quarter portrait with hands near the face and dark wood wall",
        "Wide prone sofa portrait holding a camera over white drapery",
        "Front seated portrait adjusting the upper edge of the white lace garment",
    ),
    "040": (
        "Close seated white-studio portrait with one knee dominating the lower foreground",
        "Full-body high-key stool portrait with one raised knee and white socks",
        "Rear three-quarter seated stool portrait looking back over the shoulder",
        "Tight face portrait with fingertips near the lips and white shirt draped around arms",
        "Centered seated stool portrait with one knee raised beneath the chin",
        "Knee-up seated portrait with both hands low between the knees",
        "Full seated figure with crossed folded legs and large white negative space",
        "Centered waist-up stool portrait with the white shirt framing the torso",
    ),
    "041": (
        "Front seated portrait holding a berry branch across an ivory robe",
        "Side-curled seated portrait on an antique table beside the large ceramic vase",
        "Rear seated floor portrait with a long ivory train and bare branches above",
        "Wide seated table portrait with one knee raised and robe draped to the floor",
        "Close portrait seen through blurred white berries and dark branches",
        "Waist-up side portrait with berry collar and vase branch silhouette",
        "Low side-profile portrait looking upward beside the oversized ceramic vase",
    ),
    "042": (
        "Front table portrait smiling over the clear strawberry water tank",
        "Tight face portrait with hands under the chin and blind shadows across the cheeks",
        "Three-quarter table portrait holding one strawberry above the water tank",
        "Repeat frontal tank portrait with denser plant framing and lower gaze",
        "High-angle standing portrait pouring water while holding a strawberry glass",
        "Side-seated bed portrait with mint cardigan and strawberry tank in foreground",
        "Backlit seated portrait presenting a plate of strawberries near the blinds",
        "Overhead reclining bed portrait surrounded by strawberries and blue flowers",
        "Reclining three-quarter portrait lifting a strawberry above the face",
        "Back-turn reading portrait on the bed with mint cardigan slipping around the arms",
    ),
    "043": (
        "Standing waist-deep pool portrait offering both hands toward the lens",
        "Seated pool-edge portrait with one knee raised and blue cover layer draped at the arms",
        "Steep high-angle close portrait leaning toward the pool edge",
        "Wide seated architectural portrait inside the rooftop pool enclosure",
        "Tight bust portrait with both arms arched above the head",
        "Full seated pool-edge portrait with crossed knees and urban windows behind",
        "Rear three-quarter standing water portrait looking back toward camera",
        "Close playful wink portrait with both arms forming a loose arch overhead",
        "Standing side-profile pool portrait against soft high-rise buildings",
    ),
    "044": (
        "Wide floor portrait lying beside a tall clear goldfish tank in warm window light",
        "Tight face portrait viewed through the waterline and swimming goldfish",
        "Warm close portrait resting the chin near the glass tank edge",
        "Seated floor portrait beside the fish tank and shoji-style wooden panels",
        "Overhead curled floor portrait with diagonal sunlight crossing the body and tank",
        "Front close portrait with both hands at the cheeks behind plant and glass layers",
        "Low reclining face portrait framed by green leaves and warm aquarium reflections",
    ),
    "045": (
        "Seated full portrait holding a paintbrush and oval palette in the mint flower studio",
        "Medium portrait presenting the paintbrush and pastel palette toward the viewer",
        "Seated straw-hat portrait with one hand resting beside the chair",
        "Playful seated portrait raising the paintbrush overhead under the straw hat",
        "Tight smiling straw-hat portrait with one hand on the brim",
        "Medium seated portrait laughing with one hand near the scarf",
        "Wide seated portrait surrounded by flower pots and mint fabric",
        "Waist-up portrait holding a small green vessel above the head",
    ),
    "046": (
        "Side-seated garden portrait surrounded by pink flowers beside the white bathtub",
        "Close portrait resting against the bathtub rim with one flower at the cheek",
        "Indoor sparkle portrait leaning back with one hand at the collarbone",
        "High-angle seated portrait among pink flowers with the tub behind",
        "Close flower portrait holding two pink blooms at different depths",
        "Wide reclining garden portrait with crossed ankles and the bathtub behind",
        "Front seated portrait with pearl bubbles floating near the face",
        "Tight front portrait holding one pink flower below the chin",
        "Three-quarter seated portrait smelling a flower with palms and tub framing the scene",
        "Vertical side portrait beside the tub with the floral skirt spread downward",
    ),
    "047": (
        "Front seated portrait in red floral dress against warm wood and tropical leaves",
        "Back-turn window portrait with sunlight outlining the red dress and shoulder",
        "Full seated floor portrait holding a red gerbera with the skirt spread around",
        "Tight face portrait holding a small red flower beside the lips",
        "Seated portrait behind the empty glass aquarium with red flowers in the room",
        "Window side-profile portrait holding the round goldfish bowl low",
        "Rear three-quarter portrait holding a gerbera near the shoulder",
        "Centered seated portrait framed by glass tank edges and tropical leaves",
        "Low seated portrait raising a red flower toward the face under palm leaves",
    ),
    "048": (
        "Side-seated mint studio portrait beneath hanging white flower branches",
        "Seated table portrait with one knee raised and one hand near the blossoms",
        "Close seated portrait studying a white flower beside the face",
        "Standing full portrait with one arm curved above the head near the flower tree",
        "Close three-quarter portrait partly screened by white blossoms",
        "Full seated table portrait with both legs hanging and flower pot at left",
        "Tight side portrait with mint fabric and soft white blossom foreground",
        "Full seated side portrait with one knee raised on the table",
        "Close portrait holding a small flower near the lips against mint backdrop",
    ),
    "049": (
        "Standing full fairy-stage portrait with one hand raised among crystal strands",
        "Medium seated portrait with hands near face and crystal wings behind",
        "Standing three-quarter portrait reaching toward hanging crystal ornaments",
        "Waist-up portrait holding one white rose at the jeweled necklace",
        "Centered full portrait with both palms open and crystal wings spread symmetrically",
        "Seated medium portrait with hands together at the chest and candles behind",
        "Vertical standing portrait holding the skirt edge with crystal curtain at left",
    ),
    "050": (
        "Close lavender-bed portrait holding a flower stem between both hands",
        "Side-seated portrait holding red grapes above a butterfly plate",
        "Tight reclining face portrait beside grapes and lavender bedding",
        "Wide prone bed portrait with both lower legs raised behind the body",
        "Wide seated bed portrait holding grapes amid lavender flowers",
        "Front prone portrait with chin resting on both hands and flowers in foreground",
        "Rear three-quarter standing portrait showing layered lavender sleeves and purple flowers",
        "Three-quarter seated portrait placing grapes onto a butterfly plate",
        "Reclining bed portrait with one hand at the collarbone and grape plate nearby",
    ),
}


REFERENCE_PERSON_SENTENCE = re.compile(
    r"\b(?:adult(?:-presenting)?\s+(?:woman|model)|young\s+(?:adult\s+)?woman|"
    r"hair|hairstyle|bangs|braid|braided|bun|ponytail|pigtail|twin[- ]tails?|updo|"
    r"body\s+type|mature\s+(?:body|face|model)|slender\s+body|curvy\s+body|"
    r"long[- ]legged|beauty\s+mark)\b",
    re.IGNORECASE,
)


def _strip_reference_person_traits(text: str) -> str:
    """Keep shot design evidence while removing the template model's identity."""
    kept: list[str] = []
    for line in text.splitlines():
        sentences = re.split(r"(?<=[.!?])\s+", line)
        clean_sentences: list[str] = []
        for sentence in sentences:
            clauses = re.split(r"\s*[,;]\s*", sentence)
            clean_clauses = [
                clause.strip()
                for clause in clauses
                if clause.strip() and not REFERENCE_PERSON_SENTENCE.search(clause)
            ]
            if clean_clauses:
                clean_sentences.append(", ".join(clean_clauses))
        if clean_sentences:
            kept.append(" ".join(clean_sentences))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()


def refined_shot_title(template: PhotosetTemplate, shot: PhotosetShot) -> str:
    base_id = template.template_id.split("_", 1)[0]
    titles = REFINED_SHOT_TITLES.get(base_id)
    if titles and 1 <= shot.index <= len(titles):
        return titles[shot.index - 1]
    return shot.title


def prompt_for_refined_shot(
    character_name: str,
    template: PhotosetTemplate,
    shot: PhotosetShot,
) -> str:
    subject_name = "the selected character"
    shot_evidence = _strip_reference_person_traits(
        _adapt_shot_prompt(character_name, shot.ready_prompt or shot.section_text)
    )
    global_evidence = _compact(
        _strip_reference_person_traits(_english_only_text(
            _soften_platform_sensitive_terms(
                _remove_template_identity_traits(template.global_identity)
            )
        )),
        2600,
    )
    title = refined_shot_title(template, shot)

    return _english_only_text(f"""
Independent image task. Create exactly one polished hand-drawn Japanese anime illustration.

[E2 REFERENCE AUTHORITY]
The uploaded character references and the single photoset reference image have different jobs.
Character references are the only authority for identity and anatomy. The photoset reference image is the only authority for this shot's pose geometry, framing, outfit design, set layout, lighting, and color treatment. The written notes are a precise aid; whenever wording and visible evidence differ, follow the visible current-shot reference.

[CHARACTER IDENTITY AND PROPORTION LOCK]
The final subject is {subject_name}.
{_profile_identity_block(character_name)}
{_character_adaptation(character_name)}
Read all uploaded character references together as one character sheet. Preserve the character's canonical apparent height, head-to-body ratio, head size, shoulder width, torso length, hip width, leg-to-torso ratio, limb thickness, facial age impression, and fixed nonhuman traits. Do not inherit the photoset model's tall stature, long legs, narrow adult face, bust or hip volume, skin realism, hairstyle, bangs, or body maturity. Adapt the pose to the character by moving furniture contact points and joint positions; never adapt the character by stretching limbs or shrinking the head.

[SHOT]
Template: {template.template_id}
Shot: {shot.index} / {len(template.shots)}
Exact shot read: {title}

[COMPOSITION GEOMETRY]
Reconstruct the reference image's camera distance, camera height, pitch, roll, crop boundaries, subject occupancy, head position, body direction, weight-bearing point, limb foreshortening, hand placement, leg placement, gaze direction, foreground overlap, and negative-space distribution. Keep the same visible body range. Do not automatically turn a close-up into a full-body image or center an off-center composition. Preserve which objects sit in front of, beside, and behind the subject.

[OUTFIT TRANSLATION]
Match this shot's visible garment category, silhouette, neckline shape, sleeve shape, waist position, hem length, layer count, color, pattern scale, trim placement, and fabric weight. Fit that design to {subject_name}'s canonical body. Render it as a coherent finished anime garment with connected panels, stable seams, and an opaque lining where needed. Preserve fashionable shape and delicacy; do not replace it with generic conservative clothing. Do not copy the reference model's hairstyle or use hair as part of the outfit.

[POSE AND HANDS]
Treat the pose as a joint-and-support diagram. State one clear support for the pelvis and torso, preserve the reference shoulder and hip rotation, and keep every visible hand anatomically readable. A hand touching hair, face, flower, glass, book, fruit, chair, floor, or clothing must make the same contact shown in the reference. Do not invent a second prop, extra fingers, extra limbs, crossed anatomy, or a new body direction.

[SCENE, LIGHT, AND COLOR]
Use the current photoset reference image, not any other template, for environmental geometry and color. Match its dominant background hue, white balance, exposure level, highlight color, shadow color, contrast, saturation, light-source direction, shadow hardness, rim-light strength, depth of field, and atmospheric density. Preserve the reference's key furniture, flowers, windows, plants, vessels, fabric, water, or architectural forms at approximately the same positions and scale. Do not add a generic warm vintage room, golden window light, cream walls, or sepia grading unless they are visibly present in this exact reference image.

[CONTINUITY WITHOUT FALSE UNIFORMITY]
Keep character identity constant across the set. Carry over outfit, set, and color details only when they are visibly shared by adjacent reference images. If this shot changes outfit, location, prop system, time of day, or palette, this shot's reference wins. Never force one room or one garment across a deliberately mixed-concept template.

[EXISTING IMAGE-SPECIFIC EVIDENCE]
{global_evidence}

{shot_evidence}

[HAND-DRAWN ANIME FINISH]
{A3_HAND_DRAWN_STYLE}
Use clean visible black lineart, controlled cel shading, drawn fabric folds, stylized anime facial planes, and illustration color separation. Preserve photographic composition without producing photographic skin or live-action rendering.

[NEGATIVE]
Identity drift, reference-model face, reference-model hairstyle, wrong bangs, wrong eye color, wrong fixed accessories, wrong species traits, copied adult model proportions, stretched torso, overlong legs, undersized head, enlarged bust or hips, mature sharp face, pose substitution, wrong crop, centered composition when the reference is offset, missing support surface, floating body, disconnected garment pieces, decorative material pasted onto skin, transparent unlined clothing, accidental exposure, body-part emphasis, extra fingers, fused hands, extra limbs, duplicated props, unreadable face, text, logo, watermark.
{A3_NEGATIVE}
""").strip()
