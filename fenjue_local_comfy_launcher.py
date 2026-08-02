from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from fenjue.modes.registry import activate_prompt_mode
from fenjue.runtime import batch
from fenjue.local.comfyui_client import ComfyUIClient


def _safe_component(value: str) -> str:
    cleaned = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE).strip("._")
    return cleaned or "image"


def _local_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--comfy-server", default="http://127.0.0.1:8188")
    parser.add_argument("--comfy-steps", type=int, default=28)
    parser.add_argument("--comfy-denoise", type=float, default=0.65)
    parser.add_argument("--comfy-identity-weight", type=float, default=0.55)
    parser.add_argument("--comfy-identity-reference", type=int, default=2)
    parser.add_argument("--comfy-retries", type=int, default=3)
    return parser.parse_known_args(argv)[0]


def main() -> None:
    argv = sys.argv[1:]
    mode = next((item.upper() for item in argv if item.upper() in {"E", "E2"}), "E")
    options = _local_arguments(argv)
    activate_prompt_mode(mode, batch, args=argv)
    client = ComfyUIClient(server=options.comfy_server)
    client.ensure_ready()
    total = batch.TOTAL_RUNS
    print(f"Local ComfyUI backend ready: mode={mode}, jobs={total}, steps={options.comfy_steps}", flush=True)
    for run_number in range(1, total + 1):
        character = batch.resolve_run_character("", run_number)
        references = batch.reference_files_for_character(character)
        if len(references) < 2:
            raise RuntimeError(f"{character} has no template reference for local generation")
        character_references = references[:-1]
        template_reference = references[-1]
        prompt = batch.prompt_for_art_direction(character)
        template_id = Path(template_reference).parent.name
        shot_id = Path(template_reference).stem
        prefix = f"Fenjue/{_safe_component(character)}/{template_id}_{shot_id}"
        print(f"[{run_number}/{total}] start: {character}, template={template_id}, image={shot_id}", flush=True)
        last_error: Exception | None = None
        for attempt in range(1, options.comfy_retries + 1):
            try:
                result = client.generate(
                    prompt,
                    character_references,
                    template_reference,
                    prefix,
                    steps=options.comfy_steps,
                    denoise=options.comfy_denoise,
                    identity_weight=options.comfy_identity_weight,
                    identity_reference_index=options.comfy_identity_reference,
                )
                break
            except Exception as exc:
                last_error = exc
                print(f"[{run_number}/{total}] attempt {attempt}/{options.comfy_retries} failed: {exc}", flush=True)
                if attempt < options.comfy_retries:
                    time.sleep(10 * attempt)
        else:
            raise RuntimeError(f"Local generation failed after {options.comfy_retries} attempts") from last_error
        batch.record_completed_run(character, run_number)
        print(f"[{run_number}/{total}] done in {result.elapsed_seconds:.1f}s: {result.output_files[0]}", flush=True)
    print("All local ComfyUI jobs completed.", flush=True)


if __name__ == "__main__":
    main()
