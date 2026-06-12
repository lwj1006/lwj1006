@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fenjue C World Cup Roadside Supporter Special
echo Starting Fenjue C World Cup roadside supporter special...
echo Every character has a stable assigned national-team supporter outfit.
python fenjue_prompt_mode_launcher.py --mode=C %*
pause
