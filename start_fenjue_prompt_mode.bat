@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue A-B Prompt Mode
echo Starting Fenjue prompt-mode launcher...
echo A = original stable compact style
echo B = photographer four-block style
echo B supports multi-select: 1 2 3 / 1-3 / 1-3 7 10-12
python fenjue_prompt_mode_launcher.py
pause
