from __future__ import annotations

import sys

from fenjue.modes.registry import activate_prompt_mode
from fenjue.modes.selection import choose_prompt_mode
from fenjue.runtime import batch

def _calibration_requested(argv: list[str]) -> bool:
    return any(argument.strip().lower() in {"--calibrate", "--reset-coords", "--reset-coordinates"} for argument in argv)


def _upload_counter_clear_requested(argv: list[str]) -> bool:
    return any(argument.strip().lower() in {"--clear-upload-counter", "--reset-upload-counter", "--clear-cooldown"} for argument in argv)


def main() -> None:
    args = sys.argv[1:]
    if _upload_counter_clear_requested(args):
        batch.clear_upload_counter_state("manual reset from launcher")
        print("Upload cooldown counter cleared.")
        return

    if _calibration_requested(args):
        batch.main()
        return

    selected_mode = choose_prompt_mode(args)
    activate_prompt_mode(selected_mode, batch, args=args)
    if selected_mode == "D":
        from fenjue.runtime import target_batch
        target_batch.main()
    else:
        batch.main()

if __name__ == "__main__":
    main()
