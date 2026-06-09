@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue B Photographer Mode - Multi Select
echo Starting Fenjue B photographer mode...
echo Background selection supports: 1 2 3 / 1-3 / 1-3 7 10-12
python fenjue_prompt_mode_launcher.py B
pause
