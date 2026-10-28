# Morning reminder: fills prompts/09-codex-generate.md with today's folder,
# saves it as codex-prompt.txt, copies it to the clipboard and opens it in Notepad.

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$today = Get-Date -Format 'yyyy-MM-dd'
$folder = Get-ChildItem carousels -Directory -Filter "$today-*" | Select-Object -First 1

if (-not $folder) {
    $msg = "LoopFound: no carousel folder for $today. Check automations\logs for last night's run."
    $file = Join-Path $root 'automations\logs\no-folder.txt'
    New-Item -ItemType Directory -Force (Split-Path $file) | Out-Null
    $msg | Set-Content $file
    Start-Process notepad.exe $file
    exit 0
}

$rel = "carousels/$($folder.Name)"
$prompt = ((Get-Content prompts\09-codex-generate.md -Raw) -split '\r?\n---\r?\n')[1]
$prompt = $prompt.Replace('[FOLDER]', $rel).Trim()

$out = Join-Path $folder.FullName 'codex-prompt.txt'
@"
GOOD MORNING. Today's carousel: $($folder.Name)

STEP 1  Read research.md and copy.md in the folder. Open two links.
STEP 2  Approve: in brief.md change the Status line to "Status: approved".
STEP 3  In the terminal:
          cd $root
          codex
STEP 4  Paste everything below the line (it is already on your clipboard).
STEP 5  Check final\ has 18 files, then ask Claude for the six-point check.

------------------------------------------------------------------------
$prompt
"@ | Set-Content $out -Encoding utf8

Set-Clipboard -Value $prompt
Start-Process notepad.exe $out
