@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Starting Fenjue V3 pyautogui batch...
echo Workspace: %cd%
python chatgpt_batch_pyautogui.py
pause
