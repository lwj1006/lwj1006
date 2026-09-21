"""User-selected expression preference, applied only to final E prompts."""
import re

EXPRESSION_POLICY = (
    "Use a relaxed natural mouth or a subtle closed-mouth smile, with relaxed cheeks and jaw. "
    "Do not show teeth, stretch the mouth into a broad grin, purse or protrude the lips, or perform a kissing expression. "
    "This mouth-expression preference overrides the reference image and any character or shot expression notes. "
    "Keep the shot's gaze, head angle, body pose and hand placement."
)

# Replace expression phrases, not whole sentences: nearby gaze, contacts and
# camera instructions must survive. Negative clauses retain their prohibitions.
_REPLACEMENTS = (
    (r"\b(?:blow(?:s|ing)?|send(?:s|ing)?)\s+(?:a\s+)?kiss(?:es)?\b", "give a subtle closed-mouth smile"),
    (r"\b(?:pucker(?:s|ed|ing)?|purse[sd]?|pursing)\s+(?:(?:her|the|your)\s+)?lips\b", "keep the lips relaxed and gently closed"),
    (r"\b(?:lips|mouth)\s+(?:are\s+|is\s+)?(?:puckered|pursed)\b", "lips are relaxed and gently closed"),
    (r"\b(?:(?:broad|wide|big|open|bright|small|direct)\s+)*(?:toothy|tooth-revealing|teeth-revealing|tooth-baring|teeth-baring|broad|wide|big|open-mouth|open-mouthed)\s+(?:smile|smiling|grin)\b", "subtle closed-mouth smile"),
    (r"\bsmil(?:e|es|ing)\s+with\s+(?:an?\s+)?open\s+mouth\b", "smile subtly with lips gently closed"),
    (r"\b(?:show(?:s|ing)?|reveal(?:s|ing)?|bar(?:e|es|ing))\s+(?:(?:her|the|white|upper|front)\s+)*teeth\b", "keep the lips gently closed"),
    (r"\b(?:gentle|slightly|small|soft|restrained|playful|cute|closed-mouth)[ -]+(?:(?:slightly|small|soft|closed-mouth)[ -]+)*(?:pout(?:y|ing)?|kiss(?:ing)?(?:-like)?)(?:\s+(?:expression|mouth|lips|face))?\b", "relaxed mouth"),
    (r"\b(?:pout(?:s|y|ing)?|pucker(?:ed|ing)?|kiss(?:ing)?(?:-like)?)(?:\s+(?:expression|mouth|lips|face))?\b", "relaxed mouth"),
    (r"\bgrin(?:s|ning)?\b", "subtle closed-mouth smile"),
)


def apply_e_expression_preference(prompt: str) -> str:
    parts = re.split(r"([.;\n])", prompt)
    in_negative = False
    for i, part in enumerate(parts):
        if part.strip().startswith("["):
            in_negative = "NEGATIVE" in part.upper()
        if in_negative:
            continue
        for pattern, replacement in _REPLACEMENTS:
            def replace_positive(match):
                prefix = part[:match.start()]
                clause = re.split(r"[,;:]|\b(?:but|and)\b", prefix, flags=re.I)[-1]
                if re.search(r"\b(?:no|not|never|avoid|without)\b", clause, re.I):
                    return match.group(0)
                return replacement
            part = re.sub(pattern, replace_positive, part, flags=re.I)
        parts[i] = part
    body = "".join(parts)
    first, separator, rest = body.partition("\n")
    return first + "\n\n[EXPRESSION PREFERENCE]\n" + EXPRESSION_POLICY + separator + rest
