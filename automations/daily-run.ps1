# Evening run: prepares tomorrow's carousel folder with Claude (prompts/04-daily-run.md).
# Prepare only. It never generates images, posts, schedules or messages anyone.
# Images are made by hand in ChatGPT from the folder's chatgpt-prompts.md.

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

$today    = Get-Date -Format 'yyyy-MM-dd'
$tomorrow = (Get-Date).AddDays(1).ToString('yyyy-MM-dd')
$logDir   = Join-Path $root 'automations\logs'
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir "$today.log"

if (Get-ChildItem carousels -Directory -Filter "$tomorrow-*" -ErrorAction SilentlyContinue) {
    "Folder for $tomorrow already exists. Nothing to do." | Tee-Object $log -Append
    exit 0
}

# Topics from the last 14 days, so the run does not repeat them
$cutoff = (Get-Date).AddDays(-14).ToString('yyyy-MM-dd')
$recent = Get-ChildItem carousels -Directory |
    Where-Object { $_.Name.Substring(0, 10) -ge $cutoff } |
    ForEach-Object { "- $($_.Name)" }
if (-not $recent) { $recent = '- (none)' }

$prompt = ((Get-Content prompts\04-daily-run.md -Raw) -split '\r?\n---\r?\n')[1]
$prompt = $prompt.Replace('[DATE]', $today).Replace('[LIST OF DATED FOLDER NAMES]', ($recent -join "`n"))
$prompt += @"

Extra steps for this automated run:
- Read CLAUDE.md and style/style-dna.md from the repo yourself (they are not attached).
- Use folder carousels/$tomorrow-<short-topic>/. Write brief.md with "Status: waiting for approval".
- Also write chatgpt-prompts.md in that folder: for each of the six slides, a heading
  "## 0N-name", then one fenced text block ready to paste into ChatGPT:
  "Generate exactly one image, 3:4 portrait (1080x1440). Use the prompt below word
  for word. Do not rewrite, shorten, or improve it." followed by "PROMPT:" and that
  slide's full prompt from prompts.md, style block included. Below each block, one line:
  "Save as: final/0N-name.png".
- No one is here to answer questions. Do not wait for approval; finish with the summary.
"@

"=== $(Get-Date -Format s) starting run for $tomorrow" | Out-File $log -Append
$prompt | claude -p --allowedTools 'WebSearch' 'WebFetch' 'Read' 'Glob' 'Grep' 'Write' 'Edit' 2>&1 |
    Out-File $log -Append
"=== $(Get-Date -Format s) finished (exit $LASTEXITCODE)" | Out-File $log -Append
