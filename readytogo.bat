@echo off
echo Waiting 30 minutes...
timeout /t 1800 /nobreak

cd /d D:\workspace\auto-image-create\develop
python chatgpt_batch_pyautogui.py

pause