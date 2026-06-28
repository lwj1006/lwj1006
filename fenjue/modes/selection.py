from __future__ import annotations

import re

from fenjue.modes.registry import available_mode_codes, prompt_mode_lines

SUPPORTED_MODES = available_mode_codes()

def normalize_mode_argument(argument: str) -> str | None:
    normalized = argument.strip().upper()
    if normalized in {"A", "--MODE=A", "--PROMPT-MODE=A"}:
        return "A"
    if normalized in {"B", "--MODE=B", "--PROMPT-MODE=B"}:
        return "B"
    if normalized in {"C", "--MODE=C", "--PROMPT-MODE=C", "--ARTIST-COMPOSITION"}:
        return "C"
    if normalized in {"D", "--MODE=D", "--PROMPT-MODE=D", "--TARGET"}:
        return "D"
    if normalized in {"E", "--MODE=E", "--PROMPT-MODE=E", "--PHOTOSET", "--TEMPLATE-MODE"}:
        return "E"
    if normalized in {"E2", "--MODE=E2", "--PROMPT-MODE=E2", "--PHOTOSET-REFINED", "--TEMPLATE-REFINED"}:
        return "E2"
    return None

def choose_prompt_mode(argv: list[str]) -> str:
    for argument in argv:
        mode = normalize_mode_argument(argument)
        if mode:
            return mode
    while True:
        print("")
        print("Choose prompt mode:")
        for line in prompt_mode_lines():
            print(line)
        choice = input("Prompt mode [A/B/C/D/E/E2, default A]: ").strip().upper() or "A"
        if choice in SUPPORTED_MODES:
            return choice
        print("Please enter A, B, C, D, E, or E2.")

def parse_index_selection(raw_choice: str, item_count: int) -> list[int] | None:
    normalized = raw_choice.strip().upper()
    if normalized in {"", "0", "ALL", "RANDOM"}:
        return None
    indexes = []
    for token in re.split("[\\s,\\u3001\\uff0c+]+", normalized):
        if not token:
            continue
        if "-" in token:
            parts = token.split("-", 1)
            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                raise ValueError(f"Invalid range: {token}")
            start, end = (int(part) for part in parts)
            if start > end:
                start, end = end, start
            indexes.extend(range(start, end + 1))
        elif token.isdigit():
            indexes.append(int(token))
        else:
            raise ValueError(f"Invalid selection token: {token}")
    invalid = [index for index in indexes if index < 1 or index > item_count]
    if invalid:
        raise ValueError(f"Scene indexes out of range: {invalid}")
    return list(dict.fromkeys(indexes))
