@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue Prompt Mode Router
if not defined FENJUE_LOG_LEVEL set "FENJUE_LOG_LEVEL=INFO"

set "RUNTIME_UPLOAD_DIR=%~d0\_fu"
if not exist "%RUNTIME_UPLOAD_DIR%" mkdir "%RUNTIME_UPLOAD_DIR%"
echo Clearing temporary upload files: %RUNTIME_UPLOAD_DIR%
del /f /q /a "%RUNTIME_UPLOAD_DIR%\*" >nul 2>&1
for /d %%D in ("%RUNTIME_UPLOAD_DIR%\*") do rd /s /q "%%~fD"

echo ================================================================
echo   FENJUE IMAGE AUTOMATION
echo ================================================================
echo   IMAGE MODES
echo   [A] Original    [B] Photographer    [C] Composition
echo   [D] Fixed batch [E] Photoset         [E2] Refined photoset
echo   [F] Local ComfyUI photoset ^(prompt + character ref + template ref^)
echo.
echo   TOOLS
echo   [R] Recalibrate coordinates          [U] Clear upload cooldown
echo   [L] Continue last E/E2 progress ^(progress is saved automatically^)
echo   Log level: %FENJUE_LOG_LEVEL% ^(set FENJUE_LOG_LEVEL=DEBUG for details^)

set "LAUNCH_ARGS=%*"
if "%~1"=="" (
    echo.
    set /p "CHOICE=Choose [A/B/C/D/E/E2/F/L/R/U, default A]: "
    if "!CHOICE!"=="" set "CHOICE=A"
    if /I "!CHOICE!"=="R" (
        set "LAUNCH_ARGS=--calibrate"
    ) else if /I "!CHOICE!"=="RESET" (
        set "LAUNCH_ARGS=--calibrate"
    ) else if /I "!CHOICE!"=="U" (
        set "LAUNCH_ARGS=--clear-upload-counter"
    ) else if /I "!CHOICE!"=="UPLOAD_RESET" (
        set "LAUNCH_ARGS=--clear-upload-counter"
    ) else if /I "!CHOICE!"=="F" (
        call "%~dp0start_fenjue_local_comfy.bat"
        goto :done
    ) else (
        echo.
        echo Automation control
        echo   [V] OpenCV test ^(recommended^)  [S] OpenCV unattended + shutdown
        echo   [L] Legacy calibrated coordinates
        set /p "AUTOMATION_CHOICE=Choose [V/S/L, default V]: "
        if "!AUTOMATION_CHOICE!"=="" set "AUTOMATION_CHOICE=V"
        set "LAUNCH_ARGS=!CHOICE!"
        if /I "!AUTOMATION_CHOICE!"=="V" set "LAUNCH_ARGS=!LAUNCH_ARGS! --vision"
        if /I "!AUTOMATION_CHOICE!"=="OPENCV" set "LAUNCH_ARGS=!LAUNCH_ARGS! --vision"
        if /I "!AUTOMATION_CHOICE!"=="S" set "LAUNCH_ARGS=!LAUNCH_ARGS! --vision --shutdown-on-error"
        if /I "!AUTOMATION_CHOICE!"=="FORMAL" set "LAUNCH_ARGS=!LAUNCH_ARGS! --vision --shutdown-on-error"
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
