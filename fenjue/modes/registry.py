from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

LAUNCHER_VERSION = "package-router-20260617"

@dataclass(frozen=True)
class PromptMode:
    code: str
    label: str
    module: str
    ready: bool = True

PROMPT_MODES = {
    "A": PromptMode("A", "original scene-character-outfit", "fenjue.modes.original.mode"),
    "B": PromptMode("B", "photographer mode", "fenjue.modes.photographer.mode"),
    "C": PromptMode("C", "master artist composition", "fenjue.modes.artist_composition.mode"),
    "D": PromptMode("D", "target fixed prompt batch", "fenjue.modes.target_batch.mode"),
    "E": PromptMode("E", "reserved photoset template mode", "fenjue.modes.reserved.mode_e", ready=False),
}

def available_mode_codes() -> tuple[str, ...]:
    return tuple(PROMPT_MODES)

def prompt_mode_lines() -> list[str]:
    lines = []
    for mode in PROMPT_MODES.values():
        suffix = "" if mode.ready else " (not implemented yet)"
        lines.append(f"  {mode.code} = {mode.label}{suffix}")
    return lines

def activate_prompt_mode(mode: str, batch, args=None) -> None:
    normalized = mode.strip().upper()
    try:
        prompt_mode = PROMPT_MODES[normalized]
    except KeyError as exc:
        known = ", ".join(available_mode_codes())
        raise ValueError(f"Unknown prompt mode {mode!r}. Available modes: {known}.") from exc
    if not prompt_mode.ready:
        raise NotImplementedError(f"Prompt mode {normalized} is registered, but its implementation has not been added yet.")
    print(f"Fenjue prompt launcher version: {LAUNCHER_VERSION}", flush=True)
    mode_module = import_module(prompt_mode.module)
    mode_module.activate(batch, args=args)
