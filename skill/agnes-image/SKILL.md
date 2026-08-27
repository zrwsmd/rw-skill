---
name: agnes-image
summary: Generate images with Agnes Image 2.1 Flash and save every result under D:\agnes-generate\image.
---

# Agnes Image

Use for image generation, posters, covers, product visuals, illustrations, or still-image editing.

## Requirements

- Windows PowerShell and `curl.exe`.
- `AGNES_API_KEY` must exist in the agent environment.
- Never print or disclose `AGNES_API_KEY`.
- Always save results to `D:\agnes-generate\image`.

## API

- Endpoint: `POST https://apihub.agnes-ai.com/v1/images/generations`
- Model: `agnes-image-2.1-flash`
- Default size: `2K`
- Default ratio: `1:1`; use `16:9` for landscape and `9:16` for vertical.

## Rules

1. Turn the request into a precise visual prompt with subject, composition, lighting, style, and required text.
2. Use a UTF-8 JSON file. Never put Chinese prompt text directly into a CMD `curl -d` argument.
3. Return both the cloud URL and the local path only after the downloaded file exists.

## PowerShell template

```powershell
if (-not $env:AGNES_API_KEY) { throw "AGNES_API_KEY is not set." }

$payload = @{
  model = "agnes-image-2.1-flash"
  prompt = "REPLACE_WITH_USER_IMAGE_PROMPT"
  size = "2K"
  ratio = "1:1"
  extra_body = @{ response_format = "url" }
} | ConvertTo-Json -Depth 5 -Compress

$requestFile = Join-Path $env:TEMP "agnes-image-request.json"
[System.IO.File]::WriteAllText($requestFile, $payload, (New-Object System.Text.UTF8Encoding($false)))

$response = curl.exe -sS -X POST "https://apihub.agnes-ai.com/v1/images/generations" `
  -H "Authorization: Bearer $env:AGNES_API_KEY" `
  -H "Content-Type: application/json; charset=utf-8" `
  --data-binary "@$requestFile"

$imageUrl = [regex]::Match($response, '"url"\s*:\s*"([^"]+)"').Groups[1].Value
if (-not $imageUrl) {
  Write-Host "Agnes image request failed:" -ForegroundColor Red
  Write-Host $response
  exit 1
}

$outputDir = "D:\agnes-generate\image"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
$localPath = Join-Path $outputDir ("agnes-image-{0}.png" -f (Get-Date -Format "yyyyMMdd-HHmmss"))
Invoke-WebRequest -Uri $imageUrl -OutFile $localPath
if (-not (Test-Path $localPath)) { throw "Image download failed: $localPath" }

Write-Host "Image cloud URL: $imageUrl" -ForegroundColor Green
Write-Host "Image local path: $localPath" -ForegroundColor Green
```

For image-to-image work, use only documented reference-image fields with public HTTPS URLs or Data URIs. Do not claim a local path is remotely accessible.
