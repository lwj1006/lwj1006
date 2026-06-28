from __future__ import annotations


# Shot titles are deliberately about composition and action only. Character hair,
# face, age, and body shape always come from the selected character references.
EXTENDED_SHOT_TITLES: dict[str, tuple[str, ...]] = {
    "062": (
        "Standing beside the fountain with the skirt lightly gathered",
        "Flower-in-hand side-profile close portrait",
        "Wide seated portrait on the stone fountain rim",
        "Forward lean beside the sparkling fountain spray",
        "Full-length walking portrait along the fountain edge",
        "Seated portrait with one hand raised into the sunlight",
        "Standing hand gesture near the fountain basin",
    ),
    "063": (
        "Table-level beauty close-up with cheek resting on forearm",
        "Floor-seated full portrait with dress spread around the body",
        "Front beauty close-up holding two cut figs",
        "Upright kneeling portrait with hand beneath chin",
        "Sideways reclining tabletop portrait with figs",
        "Clean face close-up with fingertips near chin",
        "Three-quarter tabletop pose with folded forearms",
        "Waist-up portrait presenting a plate of figs",
        "Standing three-quarter portrait holding a plate and whole fig",
    ),
    "064": (
        "Over-shoulder three-quarter portrait",
        "Front close portrait with fingertip beside cheek",
        "Waist-up folded-arm portrait with one hand beneath chin",
        "Tight beauty portrait with sleeve-covered hand near lips",
        "Three-quarter standing portrait with lowered gaze",
        "Over-shoulder smiling close portrait",
        "Direct smiling head-and-shoulders portrait",
    ),
    "065": (
        "Floor-seated curled pose beside white roses",
        "Standing side portrait holding a white rose",
        "Centered chair-seated full portrait",
        "Floor-seated reaching pose beside the flower bundle",
        "Reverse chair pose with one knee raised",
        "Standing portrait cradling white roses",
        "Side-seated chair portrait in warm window light",
        "Tight flower-and-face beauty portrait",
        "Standing doorway portrait framed by ivy",
    ),
    "066": (
        "Floor-seated full portrait within pooled lavender tulle",
        "Lavender flower beside the cheek close-up",
        "Upper-body portrait gathering tulle at the chest",
        "Symmetrical floor-seated portrait with hands beneath chin",
        "Reclining beauty close-up against lavender tulle",
        "Upright full portrait with gown spread across the floor",
        "Direct close-up holding one lavender flower",
        "Three-quarter seated portrait holding flowers",
        "Waist-up portrait with flowers at neckline and hand",
        "Soft-focus face portrait framed by lavender flowers",
    ),
    "067": (
        "Cross-legged sofa portrait wrapped in white faux fur",
        "Low-gaze seated portrait with crossed legs",
        "Waist-up lace bodice and faux-fur editorial",
        "Wide black-leather sofa portrait with turned gaze",
        "Relaxed close seated portrait with hand on thigh",
        "Dark reclining portrait with one hand raised",
        "Direct close seated portrait framed by faux fur",
    ),
    "068": (
        "Flower-bouquet close portrait in backlit garden",
        "Side-standing portrait beside flower-covered easel",
        "Full portrait holding a violin",
        "Seated flower-table portrait holding a butterfly prop",
        "Downward-gaze portrait among hydrangeas",
        "Backlit profile lifting a butterfly toward the light",
        "Full standing portrait beside the floral easel",
        "Centered seated full portrait holding the tulle skirt",
        "Seated three-quarter portrait framed by flowers",
    ),
    "069": (
        "Horizontal profile portrait leaning against the wall",
        "Horizontal over-shoulder portrait beside stacked books",
        "Floor-seated vertical portrait among books",
        "Tabletop reclining reading portrait",
        "Sideways bed-level portrait beside an open book",
        "Knee-hugging seated portrait beside books",
        "Seated portrait with both hands raised into the hair",
        "Overhead bed portrait among open books",
    ),
    "070": (
        "Full window-seat reading portrait",
        "Chair-back waist-up portrait with glasses",
        "Standing doorway profile with turned shoulders",
        "Chair-seated portrait with one hand in the hair",
        "Two-panel window-side hair gesture study",
        "Standing window portrait with folded arms",
        "Full window-seat portrait holding an open book",
    ),
    "071": (
        "Chair-seated close portrait holding a measuring tape",
        "Wide chair portrait beside desk and fireplace",
        "Forward-leaning tabletop fashion pose",
        "Close seated portrait holding a closed book",
        "Full desk-edge seated portrait in window light",
        "Chair-seated portrait gathering the striped shirt",
        "Forward tabletop portrait beside fruit and camera",
    ),
    "072": (
        "Table-level beauty portrait with one finger near lips",
        "Tight beauty portrait with both hands framing the face",
        "Elbows-down close portrait with hands clasped above",
        "Horizontal full-body reclining studio pose",
        "Table-level portrait with hand beneath chin",
        "Vertical beauty close-up with hands beside cheek",
    ),
    "073": (
        "Sofa reclining full portrait reading a red book",
        "Bright window-ledge standing profile",
        "Soft sofa reclining close portrait",
        "Front sofa portrait resting on a red book",
        "Low sofa reading portrait with open red book",
        "Kneeling floor portrait looking back toward camera",
    ),
    "074": (
        "Soft smiling window-side close portrait",
        "Dark-backdrop profile with hand at neck",
        "Direct warm smiling head-and-shoulders portrait",
        "Three-quarter backlit standing portrait with raised hand",
        "Backlit profile close portrait",
        "Eyes-closed smiling portrait with hand near chin",
        "Three-quarter close portrait shading the eyes",
        "Centered direct portrait with gentle smile",
    ),
    "075": (
        "Bouquet-held chair beauty portrait",
        "Chair-seated three-quarter bridal portrait",
        "Standing full portrait holding the skirt and bouquet",
        "Wide chair-seated full gown composition",
        "Floor-seated reading portrait with gown spread wide",
        "Chair portrait beside fruiting branches",
        "Apple-branch close portrait",
        "Bouquet and face bridal close-up",
        "Wide chair portrait beside the fruit arrangement",
    ),
    "076": (
        "Floor-seated full studio pose",
        "Front standing mid-length fashion portrait",
        "Reclining curved-chair full portrait",
        "Full standing side-turn portrait",
        "Centered front standing full portrait",
        "Low prone studio pose with hands extended",
        "Compact crouching side portrait",
        "Front mid-length folded-arm portrait",
        "Side reclining floor portrait with head on hand",
        "Standing rear three-quarter portrait looking back",
    ),
    "077": (
        "Cheerful close portrait in red layered top",
        "Warm snapshot portrait with peace sign in red layered top",
        "Pastel close portrait in mint draped top",
        "Backstage snapshot in mint draped top",
        "Cute surprised close portrait in mint draped top",
        "Seated three-quarter portrait in mint draped top",
        "Playful raised-hands portrait in mint draped top",
        "Soft smiling close portrait in mint draped top",
    ),
    "078": (
        "Dark over-shoulder cafe portrait",
        "Window-lit face close-up",
        "Wide seated portrait behind a wooden chair",
        "Front portrait raising one hand into the hair",
        "Standing side portrait leaning over the wooden counter",
        "Upward-gaze seated profile in dim interior",
        "Table-level forward-reaching portrait",
    ),
    "079": (
        "Sofa-seated full portrait beside oversized cat plush",
        "Kneeling sofa portrait with playful hand gestures",
        "Cross-legged sofa portrait holding a small cat plush",
        "Relaxed sofa portrait hugging a cat plush",
        "Front sofa portrait with both hands beneath chin",
        "Cross-legged sofa portrait hugging a cat plush",
        "Kneeling floor portrait with one hand raised",
    ),
    "080": (
        "Window-side over-shoulder portrait in pink ribbon camisole",
        "Window-lit face and shoulder close-up in pink",
        "Sofa-level smiling close portrait in pink",
        "Green-window profile with blue flower cheek detail",
        "Vintage floral-sofa portrait in pink ribbon camisole",
        "Direct floral-sofa close portrait in pink",
        "Plant-room beauty portrait holding blue flowers",
        "Seated plant-room portrait in pink ribbon camisole",
        "Grapefruit eye-framing portrait in teal camisole",
        "Grapefruit and cherry close portrait in teal camisole",
    ),
    "081": (
        "Striped-sofa over-shoulder seated portrait",
        "Direct shoulder-line close portrait",
        "Floor-seated side portrait against textured wall",
        "Window-chair profile with sheer curtains",
        "Kneeling table-side portrait looking back",
        "Window-wall seated portrait with turned gaze",
    ),
    "082": (
        "Garden close portrait with hand near temple",
        "Lime and glass-bowl close composition",
        "Full rear three-quarter standing garden portrait",
        "Forward-leaning portrait holding a lime",
        "Side reclining portrait beside glass water bowl",
        "Standing garden portrait lifting one lime",
        "Ground-seated portrait beside glass water bowl",
        "Overhead reclining portrait holding a lime",
        "Overhead full-body portrait on woven mat",
    ),
    "083": (
        "Kneeling floor portrait holding a lime",
        "Side kneeling portrait among hydrangeas and limes",
        "Wide floor-seated portrait beside hydrangeas",
        "Reclining flower-room portrait holding a lime",
        "Tight shoulder-and-lime beauty portrait",
    ),
    "084": (
        "Red-backdrop seated portrait with crossed legs",
        "Red-backdrop seated portrait with hand in hair",
        "Full standing red-and-black fashion portrait",
        "Glasses beauty close-up against crimson red",
        "Gray-studio crouching portrait with lace eye mask",
        "Gray-studio lace eye-mask close-up",
    ),
}


# 083/4 is an accidental duplicate from template 082 and must not enter the run.
EXTENDED_IMAGE_INDICES: dict[str, tuple[int, ...]] = {
    template_id: tuple(range(1, len(titles) + 1))
    for template_id, titles in EXTENDED_SHOT_TITLES.items()
}
EXTENDED_IMAGE_INDICES["083"] = (1, 2, 3, 5, 6)


SHOT_OUTFIT_OVERRIDES: dict[tuple[str, int], str] = {
    ("077", 1): "Cream short-sleeve tee under a cherry-red camisole with small bow details and a dotted translucent neck scarf.",
    ("077", 2): "Cream short-sleeve tee under a cherry-red camisole with small bow details and a dotted translucent neck scarf.",
    **{
        ("077", index): "White tank top under a pale mint wide-neck draped long-sleeve top; keep the layered neckline and sleeves secure and clearly constructed."
        for index in range(3, 9)
    },
    **{
        ("080", index): "Pale pink camisole with prominent tied ribbon bows at both shoulder straps and cream high-waisted bottoms."
        for index in range(1, 9)
    },
    ("080", 9): "Teal-green lace-trim camisole with a securely fitted neckline; grapefruit is the main prop.",
    ("080", 10): "Teal-green lace-trim camisole with a securely fitted neckline; grapefruit slices and cherries are the main props.",
}


STANDARD_NEGATIVE_PROMPT = (
    "wrong character, template-model hairstyle, template-model face, template-model body type, "
    "photorealistic skin, live-action person, 3D render, missing black line art, malformed anatomy, "
    "extra fingers, fused hands, duplicated limbs, broken joints, impossible pose, garment fusion, "
    "unsewn fabric, accidental transparency, missing opaque lining, unsafe exposure, wardrobe malfunction, "
    "incorrect prop, incorrect room, incorrect palette, flat lighting, clipped highlights, muddy shadows, "
    "oversaturation, watermark, logo, text, compression artifacts"
)
