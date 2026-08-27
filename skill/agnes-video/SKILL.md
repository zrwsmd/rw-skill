---
name: agnes-video
summary: Generate long multi-shot Agnes videos, create Chinese SRT captions from the shot plan, merge clips, burn subtitles, and save all output under D:\agnes-generate\video.
---

# Agnes Video

Use for all video generation. For videos longer than one short clip, automatically plan multiple shots, generate them sequentially, merge them, make Chinese subtitles from the approved story plan, and burn captions into the final MP4.

## Requirements

- Windows PowerShell and `curl.exe`.
- `AGNES_API_KEY` must exist in the agent environment.
- `ffmpeg` must be in PATH; verify with `ffmpeg -version` before a production task.
- Never print or disclose `AGNES_API_KEY`.
- Always save results under `D:\agnes-generate\video`.

## API and limits

- Create: `POST https://apihub.agnes-ai.com/v1/videos`
- Poll: `GET https://apihub.agnes-ai.com/agnesapi?video_id=VIDEO_ID`
- Model: `agnes-video-v2.0`
- Generate 10–15 second shots by default: `361` frames at `24` fps.
- A single shot must not exceed `441` frames.
- Do not ask the model to render subtitles in frames. Generate clean video, then burn a UTF-8 SRT with FFmpeg.

## Planning rules

1. Determine total duration, aspect ratio, project name, story, and visual style.
2. For long videos, split into 10–15 second shots. Example: 60 seconds = four 15-second shots.
3. Create a continuity lock that is repeated in every shot: fixed protagonist appearance, clothing, props, environment, palette, lens/style, and negative constraints.
4. Each shot must begin from the prior shot's final state where practical.
5. Write one concise Chinese caption for each shot. These are planned story captions, not speech-to-text captions.
6. Project names must use lowercase letters, numbers, and hyphens only.

## Folder layout

For project `PROJECT-NAME`:

```text
D:\agnes-generate\video\PROJECT-NAME\shots\shot-01.mp4
D:\agnes-generate\video\PROJECT-NAME\subtitle\PROJECT-NAME.zh-CN.srt
D:\agnes-generate\video\PROJECT-NAME\final\PROJECT-NAME.no-subtitles.mp4
D:\agnes-generate\video\PROJECT-NAME\final\PROJECT-NAME.zh-CN.mp4
```

## Generate one shot

Run this function once. It creates an asynchronous Agnes task, polls it, downloads the MP4, and returns its local path.

```powershell
if (-not $env:AGNES_API_KEY) { throw "AGNES_API_KEY is not set." }

function New-AgnesVideoSegment {
  param(
    [Parameter(Mandatory=$true)][string]$Prompt,
    [Parameter(Mandatory=$true)][string]$OutputPath,
    [int]$Width=1152, [int]$Height=768,
    [int]$NumFrames=361, [int]$FrameRate=24
  )
  $payload = @{
    model="agnes-video-v2.0"; prompt=$Prompt; width=$Width; height=$Height
    num_frames=$NumFrames; frame_rate=$FrameRate
    negative_prompt="blurry, low quality, distorted, changing identity, extra limbs, text, subtitle, logo, watermark, camera shake"
  } | ConvertTo-Json -Depth 5 -Compress
  $requestFile = Join-Path $env:TEMP ("agnes-video-"+[guid]::NewGuid()+".json")
  [System.IO.File]::WriteAllText($requestFile,$payload,(New-Object System.Text.UTF8Encoding($false)))
  $create = curl.exe -sS -X POST "https://apihub.agnes-ai.com/v1/videos" -H "Authorization: Bearer $env:AGNES_API_KEY" -H "Content-Type: application/json; charset=utf-8" --data-binary "@$requestFile"
  $videoId = [regex]::Match($create,'"video_id"\s*:\s*"([^"]+)"').Groups[1].Value
  if (-not $videoId) { throw "Agnes task creation failed: $create" }
  $videoUrl=""
  for($i=1;$i -le 90;$i++) {
    Start-Sleep 10
    $raw = curl.exe -sS -H "Authorization: Bearer $env:AGNES_API_KEY" "https://apihub.agnes-ai.com/agnesapi?video_id=$videoId"
    $status=[regex]::Match($raw,'"status"\s*:\s*"([^"]+)"').Groups[1].Value
    $progress=[regex]::Match($raw,'"progress"\s*:\s*(\d+)').Groups[1].Value
    $videoUrl=[regex]::Match($raw,'"url"\s*:\s*"([^"]+)"').Groups[1].Value
    Write-Host "Task $videoId [$i/90] status: $status; progress: $progress%"
    if($status -eq "completed" -and $videoUrl){break}
    if($status -eq "failed"){throw "Agnes video failed: $raw"}
    if($i -eq 90){throw "Polling timed out. video_id: $videoId"}
  }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputPath)|Out-Null
  Invoke-WebRequest -Uri $videoUrl -OutFile $OutputPath
  if(-not(Test-Path $OutputPath)){throw "Video download failed: $OutputPath"}
  Write-Host "Saved shot: $OutputPath" -ForegroundColor Green
  return $OutputPath
}
```

## Make subtitles

Run once. `Captions` and `Durations` must have the same number of items as shots.

```powershell
function ConvertTo-SrtTimestamp {
  param([double]$Seconds)
  $t=[TimeSpan]::FromSeconds($Seconds)
  "{0:D2}:{1:D2}:{2:D2},{3:D3}" -f $t.Hours,$t.Minutes,$t.Seconds,$t.Milliseconds
}
function Write-AgnesSrt {
  param([string[]]$Captions,[double[]]$Durations,[string]$OutputPath)
  if($Captions.Count -ne $Durations.Count){throw "Caption count must equal duration count."}
  $lines=New-Object System.Collections.Generic.List[string]; $cursor=0.0
  for($i=0;$i -lt $Captions.Count;$i++){
    $start=ConvertTo-SrtTimestamp $cursor; $cursor += $Durations[$i]; $end=ConvertTo-SrtTimestamp $cursor
    $lines.Add([string]($i+1)); $lines.Add("$start --> $end"); $lines.Add($Captions[$i]); $lines.Add("")
  }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputPath)|Out-Null
  [System.IO.File]::WriteAllLines($OutputPath,[string[]]$lines,(New-Object System.Text.UTF8Encoding($false)))
  return $OutputPath
}
```

## Long-video workflow example

For a 60-second project, create four 15-second prompts with the same `$lock`, then run shots sequentially. Adapt the prompt/captions to the user's actual request.

```powershell
$project="moon-cat-journey"
$root=Join-Path "D:\agnes-generate\video" $project
$shotsDir=Join-Path $root "shots"; $subtitleDir=Join-Path $root "subtitle"; $finalDir=Join-Path $root "final"
New-Item -ItemType Directory -Force -Path $shotsDir,$subtitleDir,$finalDir|Out-Null
$lock=@"
Same protagonist: orange tabby cat, green eyes, white astronaut suit, blue patch on right shoulder.
Same world: lunar research base at night, Earth visible in a deep blue-black sky.
Cinematic photorealism, 35mm lens look, teal moonlight, warm rim lighting. No text in video frames.
"@

$shot01=New-AgnesVideoSegment -OutputPath (Join-Path $shotsDir "shot-01.mp4") -Prompt "$lock`nShot 1 of 4. Wide establishing shot. The cat exits the lunar base and walks to a silver rover. Slow forward dolly. End behind the cat approaching the rover."
$shot02=New-AgnesVideoSegment -OutputPath (Join-Path $shotsDir "shot-02.mp4") -Prompt "$lock`nShot 2 of 4. Begin behind the cat approaching the rover. The cat boards and activates its lights. Side tracking camera. End as the rover starts moving left to right."
$shot03=New-AgnesVideoSegment -OutputPath (Join-Path $shotsDir "shot-03.mp4") -Prompt "$lock`nShot 3 of 4. Begin with the rover moving left to right. It crosses lunar dust toward a ridge. Low tracking camera. End at the ridge crest."
$shot04=New-AgnesVideoSegment -OutputPath (Join-Path $shotsDir "shot-04.mp4") -Prompt "$lock`nShot 4 of 4. Begin at the ridge crest. The cat stands beside the rover looking at Earth. Rise to a wide aerial ending."

$captions=@("月球科研基地，深夜。","橘猫宇航员踏上了新的探索旅程。","月球车驶过寂静而辽阔的月面。","山脊尽头，地球静静悬在星空中。")
$durations=[double[]](15,15,15,15)
$srtPath=Write-AgnesSrt -Captions $captions -Durations $durations -OutputPath (Join-Path $subtitleDir "$project.zh-CN.srt")
```

## Merge and burn subtitles

Run after all shots are downloaded. Keep the no-subtitle master and create a separate subtitled final MP4.

```powershell
$project="moon-cat-journey"
$root=Join-Path "D:\agnes-generate\video" $project
$shotsDir=Join-Path $root "shots"; $subtitleDir=Join-Path $root "subtitle"; $finalDir=Join-Path $root "final"
$manifest=Join-Path $root "concat.txt"
$master=Join-Path $finalDir "$project.no-subtitles.mp4"
$srt=Join-Path $subtitleDir "$project.zh-CN.srt"
$final=Join-Path $finalDir "$project.zh-CN.mp4"
$clips=Get-ChildItem $shotsDir -Filter "shot-*.mp4" | Sort-Object Name
if($clips.Count -lt 2){throw "At least two shots are required."}
if(-not(Test-Path $srt)){throw "Subtitle file missing: $srt"}
$lines=$clips|ForEach-Object{"file '"+$_.FullName.Replace("'","'\''")+"'"}
[System.IO.File]::WriteAllLines($manifest,[string[]]$lines,(New-Object System.Text.UTF8Encoding($false)))
ffmpeg -y -f concat -safe 0 -i $manifest -c copy $master
if(-not(Test-Path $master)){ffmpeg -y -f concat -safe 0 -i $manifest -c:v libx264 -pix_fmt yuv420p -c:a aac $master}
if(-not(Test-Path $master)){throw "Could not create master video."}
$filterPath=$srt.Replace("\","/").Replace(":","\:")
$vf="subtitles='$filterPath':charenc=UTF-8:force_style='FontName=Microsoft YaHei,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=42'"
ffmpeg -y -i $master -vf $vf -c:v libx264 -crf 18 -preset medium -c:a copy $final
if(-not(Test-Path $final)){throw "Could not create subtitled video."}
Write-Host "Subtitle file: $srt" -ForegroundColor Green
Write-Host "Master video: $master" -ForegroundColor Green
Write-Host "Final video: $final" -ForegroundColor Green
```

## Output rules

Report every shot path, subtitle path, no-subtitle master path, and final subtitled MP4 path. Do not claim speech-synchronized captions; these are timed captions from the shot plan.
