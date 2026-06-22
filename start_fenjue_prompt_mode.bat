@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue Prompt Mode Router

echo Fenjue prompt-mode router
echo A = original scene-character-outfit
echo B = photographer mode
echo C = master artist composition
echo D = target fixed prompt batch
echo E = photoset template mode
echo R = reset/recalibrate ChatGPT coordinates
echo U = clear upload cooldown counter

set "LAUNCH_ARGS=%*"
if "%~1"=="" (
    echo.
    set /p "CHOICE=Choose [A/B/C/D/E/R/U, default A]: "
    if "!CHOICE!"=="" set "CHOICE=A"
    if /I "!CHOICE!"=="R" (
        set "LAUNCH_ARGS=--calibrate"
    ) else if /I "!CHOICE!"=="RESET" (
        set "LAUNCH_ARGS=--calibrate"
    ) else if /I "!CHOICE!"=="U" (
        set "LAUNCH_ARGS=--clear-upload-counter"
    ) else if /I "!CHOICE!"=="UPLOAD_RESET" (
        set "LAUNCH_ARGS=--clear-upload-counter"
    ) else (
        set "LAUNCH_ARGS=!CHOICE!"
    )
)

where python >nul 2>&1
if not errorlevel 1 (
    python fenjue_prompt_mode_launcher.py !LAUNCH_ARGS!
    goto :done
)

set "LOCAL_PYTHON=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if exist "%LOCAL_PYTHON%" (
    "%LOCAL_PYTHON%" fenjue_prompt_mode_launcher.py !LAUNCH_ARGS!
    goto :done
)

echo Python was not found. Expected either python on PATH or:
echo %LOCAL_PYTHON%

:done
pause
