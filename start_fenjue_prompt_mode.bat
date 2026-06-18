@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue Prompt Mode Router
echo Starting Fenjue prompt-mode router...
echo A = original scene-character-outfit
echo B = photographer mode
echo C = master artist composition
echo D = target fixed prompt batch
echo E = photoset template mode

where python >nul 2>&1
if not errorlevel 1 (
    python fenjue_prompt_mode_launcher.py %*
    goto :done
)

set "LOCAL_PYTHON=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if exist "%LOCAL_PYTHON%" (
    "%LOCAL_PYTHON%" fenjue_prompt_mode_launcher.py %*
    goto :done
)

echo Python was not found. Expected either python on PATH or:
echo %LOCAL_PYTHON%

:done
pause
