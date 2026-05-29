$ErrorActionPreference = "Stop"

$projectDir = "D:\workspace\auto-image-create"
$logDir = Join-Path $projectDir "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$stdout = Join-Path $logDir "hidden_once_$timestamp.out.log"
$stderr = Join-Path $logDir "hidden_once_$timestamp.err.log"

$env:PYTHONIOENCODING = "utf-8"

Start-Process `
    -FilePath "python" `
    -ArgumentList ".\chatgpt_batch_pyautogui.py --once --review-url" `
    -WorkingDirectory $projectDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdout `
    -RedirectStandardError $stderr

Write-Host "Started hidden ChatGPT batch run."
Write-Host "stdout: $stdout"
Write-Host "stderr: $stderr"
