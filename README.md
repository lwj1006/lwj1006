# auto-image-create develop

ChatGPT desktop image batch automation project. Python code is organized as packages instead of root-level scripts.

## Entry point

- `start_fenjue_prompt_mode.bat`: common A/B/C/D/E launcher.
- `fenjue_prompt_mode_launcher.py`: thin Python entry point for the same router.

## Package layout

- `fenjue/runtime/`: desktop automation runtime and target-image batch runner.
- `fenjue/vision/`: optional OpenCV screen inspector and closed-loop visual automation layer.
- `fenjue/modes/original/`: mode A, scene + character + outfit.
- `fenjue/modes/photographer/`: mode B, photographer mode.
- `fenjue/modes/artist_composition/`: mode C, restored autoCreateV2 master artist composition pipeline.
- `fenjue/modes/target_batch/`: mode D, fixed prompt target-image batch.
- `fenjue/modes/photoset_template/`: mode E, markdown/reference-image photoset templates from `templatesE/`.
- `fenjue/modes/photoset_refined/`: mode E2, refined per-image prompts using the same E reference images without changing mode E.
- `fenjue/data/outfits/`: character outfit pools.
- `fenjue/legacy/`: older prompt prototype code kept for reference.
- `tools/`: reports and audit scripts.

## Recalibrate coordinates

```powershell
python .\fenjue_prompt_mode_launcher.py --calibrate
```

## Optional OpenCV visual automation

The existing calibrated-coordinate workflow is still the default. It is not
changed or patched unless an explicit visual flag is supplied.

Read-only live screen inspection:

```powershell
python .\fenjue_prompt_mode_launcher.py --mode=A --vision-dry-run
```

Run any prompt mode through the shared visual operation layer:

```powershell
python .\fenjue_prompt_mode_launcher.py --mode=E --vision
```

For the interactive BAT workflow, double-click
`start_fenjue_prompt_mode.bat`, choose `E`, then choose `V` (or press Enter)
for OpenCV visual automation. `V` is the visible test mode and never shuts the
computer down. Choose `L` to retain the legacy calibrated-coordinate workflow.
Choose `S` only for formal unattended operation: it adds
`--shutdown-on-error`, so after all bounded visual recovery attempts fail,
Windows schedules a forced shutdown with a 60-second cancellation window
(`shutdown /a`). `Ctrl+C` does not trigger it.

`--opencv` and `--automation=vision` are equivalent aliases. Visual mode uses
screenshots, OpenCV and normal PyAutoGUI input; it never reads browser DOM.
On a fresh chat it detects the centered composer, sends the one-time prime
message `给你提示词，你来画。`, waits for the active composer to move to the
bottom, and only then permits reference upload and formal prompt submission.
If the bottom composer already exists, priming is skipped.

Reference upload follows the image-mode sequence used by the current ChatGPT
UI: open the plus menu, select `创建图片`, open the image-model selector and
idempotently select `高`, reopen the plus menu, select `添加照片和文件`, and
then fill the Windows file picker.

All A/B/C/D/E/E2 modes share `fenjue.runtime.batch` for upload, prompt sending
and generation waiting. `fenjue.vision.integration.activate_visual_runtime()`
replaces only those three runtime hooks after the selected prompt mode is
activated. Future modes therefore get visual operation support automatically
when they use the common runtime; a different recognizer can implement the
`ScreenVision` protocol in `fenjue/vision/contracts.py` and be passed to the
same controller.
