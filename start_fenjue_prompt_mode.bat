@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue A-B-C Prompt Mode
echo Starting Fenjue prompt-mode launcher...
echo A = original stable compact style
echo B = photographer four-block style
echo B supports multi-select: 1 2 3 / 1-3 / 1-3 7 10-12
echo C = World Cup front-facing supporter poster

where python >nul 2>&1
if not errorlevel 1 (
    python fenjue_prompt_mode_launcher.py
    goto :done
)

set "LOCAL_PYTHON=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if exist "%LOCAL_PYTHON%" (
    "%LOCAL_PYTHON%" fenjue_prompt_mode_launcher.py
    goto :done
)

echo Python was not found. Expected either python on PATH or:
echo %LOCAL_PYTHON%

:done
pause
