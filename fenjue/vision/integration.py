from __future__ import annotations

from pathlib import Path

from .controller import VisionAutomationController
from .opencv_inspector import OpenCVScreenInspector


VISION_FLAGS = {"--vision", "--opencv", "--automation=vision", "--automation=opencv"}
VISION_DRY_RUN_FLAGS = {"--vision-dry-run", "--opencv-dry-run"}


def visual_automation_requested(args: list[str]) -> bool:
    normalized = {argument.strip().lower() for argument in args}
    return bool(normalized & (VISION_FLAGS | VISION_DRY_RUN_FLAGS))


def visual_dry_run_requested(args: list[str]) -> bool:
    normalized = {argument.strip().lower() for argument in args}
    return bool(normalized & VISION_DRY_RUN_FLAGS)


def activate_visual_runtime(batch_module, args: list[str]) -> VisionAutomationController | None:
    if not visual_automation_requested(args):
        return None

    diagnostic_dir = Path(batch_module.SCREENSHOT_DIR) / "vision"
    inspector = OpenCVScreenInspector(diagnostic_dir=diagnostic_dir)
    controller = VisionAutomationController(batch_module, inspector)

    if visual_dry_run_requested(args):
        state = inspector.inspect()
        diagnostic = inspector.save_diagnostic("dry_run")
        print(f"Vision dry run state: {state}", flush=True)
        print(f"Vision dry run screenshot: {diagnostic}", flush=True)
        return controller

    batch_module.startup_refresh_before_button_work = controller.prepare_session
    batch_module.open_new_chat_and_send_prime_after_upload_cooldown = (
        controller.open_new_chat_and_send_prime_after_upload_cooldown
    )
    batch_module.upload_reference_images = controller.upload_reference_images
    batch_module.send_prompt = controller.send_prompt
    batch_module.wait_for_generation = controller.wait_for_generation
    batch_module.recover_after_generation_limit = controller.recover_after_generation_limit
    print(
        "OpenCV visual automation active. Legacy coordinate automation remains available by launching without --vision.",
        flush=True,
    )
    return controller
