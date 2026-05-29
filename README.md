# auto-image-create

ChatGPT desktop image batch automation project.

## Files

- `chatgpt_batch_pyautogui.py`: main automation script.
- `chatgpt_batch_playwright.py`: browser automation executor. It controls an isolated browser context instead of the real mouse and keyboard.
- `prompt_templates.py`: prompt templates. Add new templates here and register them in `PROMPT_TEMPLATE_FUNCTIONS`.
- `prompt_options.py`: random pools for clothing themes, scenes, poses, lighting, and moods.
- `backups/chatgpt_batch_pyautogui.monolith.py`: copy of the previous single-file script.

## Playwright Browser Executor

This is the preferred branch direction for running batches while the real mouse
and keyboard remain free for other work or games.

Install once:

```powershell
python -m pip install -r .\requirements-playwright.txt
python -m playwright install chromium
```

First run:

```powershell
python .\chatgpt_batch_playwright.py --once
```

The first visible browser window may ask you to log in to ChatGPT. The login
state is saved in `playwright-profile/`, which is ignored by Git.

Batch run:

```powershell
python .\chatgpt_batch_playwright.py --runs 30
```

Useful options:

```powershell
python .\chatgpt_batch_playwright.py --runs 30 --generation-wait 150
python .\chatgpt_batch_playwright.py --once --dry-run
python .\chatgpt_batch_playwright.py --runs 30 --headless
```

Keep `chatgpt_batch_pyautogui.py` as the fallback executor until the browser
selectors are verified against the current ChatGPT UI.

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
