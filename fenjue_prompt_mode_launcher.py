from __future__ import annotations

import sys
import subprocess
import traceback

from fenjue.modes.registry import activate_prompt_mode
from fenjue.modes.selection import choose_prompt_mode
from fenjue.runtime import batch
from fenjue.vision.integration import activate_visual_runtime, visual_dry_run_requested

def _calibration_requested(argv: list[str]) -> bool:
    return any(argument.strip().lower() in {"--calibrate", "--reset-coords", "--reset-coordinates"} for argument in argv)


def _upload_counter_clear_requested(argv: list[str]) -> bool:
    return any(argument.strip().lower() in {"--clear-upload-counter", "--reset-upload-counter", "--clear-cooldown"} for argument in argv)


def _shutdown_on_error_requested(argv: list[str]) -> bool:
    return any(argument.strip().lower() == "--shutdown-on-error" for argument in argv)


def _schedule_shutdown_after_error() -> None:
    print(
        "Unrecoverable automation error: Windows will shut down in 60 seconds. "
        "Run `shutdown /a` to cancel.",
        flush=True,
    )
    subprocess.run(
        [
            r"C:\Windows\System32\shutdown.exe",
            "/s",
            "/f",
            "/t",
            "60",
            "/c",
            "Fenjue OpenCV automation stopped after an unrecoverable error.",
        ],
        check=False,
    )


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
    activate_visual_runtime(batch, args=args)
    if visual_dry_run_requested(args):
        return
    if selected_mode == "D":
        from fenjue.runtime import target_batch
        target_batch.main()
    else:
        batch.main()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        if _shutdown_on_error_requested(sys.argv[1:]):
            _schedule_shutdown_after_error()
        raise
