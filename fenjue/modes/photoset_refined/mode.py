from __future__ import annotations

from fenjue.modes.photoset_template import mode as base_mode
from fenjue.modes.photoset_template.refined import prompt_for_refined_shot


LABEL = "refined photoset template mode"


def activate(batch, args=None) -> None:
    base_mode.activate(batch, args=args)

    def prompt_for_refined_photoset(
        character_name,
        art_plan=None,
        action_style=None,
        recent_tags=None,
        visual_design=None,
        outfit_direction=None,
        shot_scale=None,
        composition_plan=None,
    ):
        template = base_mode._active_template()
        shot = base_mode._active_shot()
        prompt = prompt_for_refined_shot(character_name, template, shot)
        base_mode._current_shot_index += 1
        return prompt

    batch.prompt_for_art_direction = prompt_for_refined_photoset
    batch.prompt_template_name = lambda template_index=0: f"photoset_refined_{base_mode._active_template().template_id}"
    print(
        "Prompt mode E2 active: refined photoset prompts. "
        "Original E templates and prompts remain unchanged; reference images are shared.",
        flush=True,
    )
