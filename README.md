# auto-image-create

ChatGPT desktop image batch automation project.

## Files

- `chatgpt_batch_pyautogui.py`: main automation script.
- `prompt_templates.py`: prompt templates. Add new templates here and register them in `PROMPT_TEMPLATE_FUNCTIONS`.
- `prompt_options.py`: random pools for clothing themes, scenes, poses, lighting, and moods.
- `backups/chatgpt_batch_pyautogui.monolith.py`: copy of the previous single-file script.

## Prompt Rotation

The main script rotates templates by run number:

```python
template_index = run_number - 1
prompt = prompt_for_theme(..., template_index=template_index)
```

With two templates, runs alternate template 1, template 2, template 1, template 2...

## Recalibrate Coordinates

```powershell
python .\chatgpt_batch_pyautogui.py --calibrate
```
