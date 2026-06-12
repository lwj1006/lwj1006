@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue C World Cup Roadside Supporter Special
echo Starting Fenjue C World Cup roadside supporter special...
echo Every character has a stable assigned national-team supporter outfit.

where python >nul 2>&1
if not errorlevel 1 (
    python fenjue_prompt_mode_launcher.py --mode=C %*
    goto :done
)

set "LOCAL_PYTHON=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if exist "%LOCAL_PYTHON%" (
    "%LOCAL_PYTHON%" fenjue_prompt_mode_launcher.py --mode=C %*
    goto :done
)

echo Python was not found. Expected either python on PATH or:
echo %LOCAL_PYTHON%

:done
pause
