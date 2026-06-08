@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Starting Fenjue prompt-mode launcher...
echo A = original stable compact style
echo B = photographer four-block style
python fenjue_prompt_mode_launcher.py
pause
