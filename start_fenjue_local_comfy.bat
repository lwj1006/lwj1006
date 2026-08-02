@echo off
setlocal EnableExtensions
title Fenjue Local ComfyUI

set "COMFY_ROOT=D:\AI\ComfyUI"
set "PROJECT_ROOT=D:\workspace\auto-image-create\develop"
set "COMFY_PY=%COMFY_ROOT%\.venv\Scripts\python.exe"
set "PROJECT_PY=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"

if not exist "%COMFY_PY%" (
    echo [ERROR] ComfyUI Python was not found: %COMFY_PY%
    pause
    exit /b 1
)
if not exist "%PROJECT_ROOT%\fenjue_local_comfy_launcher.py" (
    echo [ERROR] Fenjue local launcher was not found.
    pause
    exit /b 1
)
if not exist "%PROJECT_PY%" set "PROJECT_PY=python"

call :check_server
if errorlevel 1 (
    echo [INFO] Starting ComfyUI in a visible window...
    powershell.exe -NoProfile -Command "Start-Process -FilePath '%COMFY_PY%' -ArgumentList @('%COMFY_ROOT%\main.py','--listen','127.0.0.1','--port','8188','--lowvram','--enable-manager') -WorkingDirectory '%COMFY_ROOT%' -WindowStyle Normal"
    for /L %%I in (1,1,60) do (
        call :check_server
        if not errorlevel 1 goto :ready
        timeout.exe /t 2 /nobreak >nul
    )
    echo [ERROR] ComfyUI did not start within 120 seconds.
    pause
    exit /b 1
)

:ready
echo [INFO] ComfyUI is ready.
echo [INFO] Output: %COMFY_ROOT%\output\Fenjue
cd /d "%PROJECT_ROOT%"
"%PROJECT_PY%" fenjue_local_comfy_launcher.py E %*
if errorlevel 1 echo [ERROR] Local generation stopped. Shutdown is disabled.
pause
exit /b %errorlevel%

:check_server
powershell.exe -NoProfile -Command "try { $null = Invoke-RestMethod 'http://127.0.0.1:8188/system_stats' -TimeoutSec 2; exit 0 } catch { exit 1 }"
exit /b %errorlevel%
