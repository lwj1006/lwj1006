param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Runtime.WindowsRuntime

function Await-WinRt {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Operation,
        [Parameter(Mandatory = $true)]
        [type]$ResultType
    )

    $method = [System.WindowsRuntimeSystemExtensions].GetMethods() |
        Where-Object {
            $_.Name -eq "AsTask" -and
            $_.IsGenericMethod -and
            $_.GetParameters().Count -eq 1
        } |
        Select-Object -First 1
    $task = $method.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.Wait()
    return $task.Result
}

$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.FileAccessMode, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrResult, Windows.Foundation, ContentType = WindowsRuntime]

$file = Await-WinRt (
    [Windows.Storage.StorageFile]::GetFileFromPathAsync($Path)
) ([Windows.Storage.StorageFile])
$stream = Await-WinRt (
    $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
) ([Windows.Storage.Streams.IRandomAccessStream])
$decoder = Await-WinRt (
    [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
) ([Windows.Graphics.Imaging.BitmapDecoder])
$bitmap = Await-WinRt (
    $decoder.GetSoftwareBitmapAsync()
) ([Windows.Graphics.Imaging.SoftwareBitmap])
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($null -eq $engine) {
    throw "Windows OCR engine is unavailable for the current user profile languages."
}
$result = Await-WinRt (
    $engine.RecognizeAsync($bitmap)
) ([Windows.Media.Ocr.OcrResult])

$payload = [ordered]@{
    text = $result.Text
    lines = @(
        foreach ($line in $result.Lines) {
            $words = @($line.Words)
            if ($words.Count -eq 0) {
                continue
            }
            $left = ($words | ForEach-Object { $_.BoundingRect.X } | Measure-Object -Minimum).Minimum
            $top = ($words | ForEach-Object { $_.BoundingRect.Y } | Measure-Object -Minimum).Minimum
            $right = ($words | ForEach-Object {
                $_.BoundingRect.X + $_.BoundingRect.Width
            } | Measure-Object -Maximum).Maximum
            $bottom = ($words | ForEach-Object {
                $_.BoundingRect.Y + $_.BoundingRect.Height
            } | Measure-Object -Maximum).Maximum
            [ordered]@{
                text = $line.Text
                x = [int]$left
                y = [int]$top
                width = [int]($right - $left)
                height = [int]($bottom - $top)
            }
        }
    )
}
$payload | ConvertTo-Json -Depth 4 -Compress
