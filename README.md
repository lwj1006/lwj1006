# auto-image-create develop

ChatGPT desktop image batch automation project. Python code is organized as packages instead of root-level scripts.

## Entry point

- `start_fenjue_prompt_mode.bat`: common A/B/C/D/E launcher.
- `fenjue_prompt_mode_launcher.py`: thin Python entry point for the same router.

## Package layout

- `fenjue/runtime/`: desktop automation runtime and target-image batch runner.
- `fenjue/modes/original/`: mode A, scene + character + outfit.
- `fenjue/modes/photographer/`: mode B, photographer mode.
- `fenjue/modes/artist_composition/`: mode C, restored autoCreateV2 master artist composition pipeline.
- `fenjue/modes/target_batch/`: mode D, fixed prompt target-image batch.
- `fenjue/data/outfits/`: character outfit pools.
- `fenjue/legacy/`: older prompt prototype code kept for reference.
- `tools/`: reports and audit scripts.

## Recalibrate coordinates

```powershell
python .\fenjue_prompt_mode_launcher.py --calibrate
```
