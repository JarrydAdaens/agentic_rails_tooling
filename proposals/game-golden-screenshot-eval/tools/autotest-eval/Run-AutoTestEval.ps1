<#
.SYNOPSIS
    Runs the Block Game 2 autotest eval: launches the game headless-style, replays a
    deterministic scripted scene, captures a screenshot, compares it against the golden
    set, and returns exit code 0 (pass) / 1 (fail).

.DESCRIPTION
    Central knowledge document: context/reports/2026-07-03-autotest-harness-revival.md

    Modes:
      Eval   (default) - runs EVALSmoke.script and verifies the Golden_vs_Current
                         screenshot assertion passed in the game's Test Results.log.
      Golden           - runs EVALGolden.script and stores the captured screenshot
                         into tools/autotest-eval/goldens/ as the new golden.

.EXAMPLE
    powershell -File tools\autotest-eval\Run-AutoTestEval.ps1
    powershell -File tools\autotest-eval\Run-AutoTestEval.ps1 -Mode Golden
#>
[CmdletBinding()]
param(
    [ValidateSet('Eval', 'Golden')]
    [string]$Mode = 'Eval',

    # Build output folder containing BlockWorld.exe
    [string]$ExeDir,

    # Seconds to wait for the game process before killing it and failing
    [int]$TimeoutSec = 240
)

$ErrorActionPreference = 'Stop'

$RepoRoot   = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
if (-not $ExeDir) {
    $ExeDir = Join-Path $RepoRoot 'source\Block Games\[STEAM] BlockWorld\bin\DESKTOP\Debug'
}
$Exe            = Join-Path $ExeDir 'BlockWorld.exe'
$ScriptsSource  = Join-Path $RepoRoot 'source\Block Games\Craft World\Source Content\Other\Scripts'
$ScriptsTarget  = Join-Path $ExeDir 'Source Content\Other\Scripts'
$TestFilesDir   = Join-Path $ExeDir 'blockgametests'
$GoldensDir     = Join-Path $PSScriptRoot 'goldens'
$LastRunDir     = Join-Path $PSScriptRoot 'last-run'
# Test rows land in the game's per-run 'Log Always' file (the legacy C:\Logs 'Test Results.log'
# writer is dead on desktop - neither UnloadContent nor OnExiting runs before Environment.Exit)
$GameLogsRoot   = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'My Games\BlockWorld\Logs'

$GoldenShot  = 'EVALGoldenShot.png'
$CurrentShot = 'EVALCurrentShot.png'
$TestName    = 'Golden_vs_Current'

function Fail([string]$Message) {
    Write-Host "EVAL FAIL: $Message" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath $Exe)) {
    Fail "BlockWorld.exe not found at '$Exe'. Build Craft World.sln (Debug|DESKTOP) first - see getting-started.md."
}

# --- Deploy scripts and goldens next to the exe -------------------------------------
# The build does not copy raw 'Source Content'; sync the Scripts tree so new/edited
# .script files are picked up (never deletes anything in the target).
robocopy $ScriptsSource $ScriptsTarget /E /NJH /NJS /NDL /NFL | Out-Null
if ($LASTEXITCODE -ge 8) { Fail "robocopy of scripts failed with code $LASTEXITCODE." }

# The BLOCKWORLD flavor ships no content maps, but the testingmode boot path loads
# content-map header 0 - deploy one deterministic test map. Quirk: the game checks
# 'Content\Other\Maps' for existence but reads .cosm files from 'Source Content\Other\Maps'.
$TestMapSource = Join-Path $RepoRoot 'source\Block Games\Craft World\Source Content\Survival Games\Other\Maps\Court.cosm'
$MapsCheckDir  = Join-Path $ExeDir 'Content\Other\Maps'
$MapsReadDir   = Join-Path $ExeDir 'Source Content\Other\Maps'
New-Item -ItemType Directory -Force -Path $MapsCheckDir | Out-Null
New-Item -ItemType Directory -Force -Path $MapsReadDir | Out-Null
Copy-Item -LiteralPath $TestMapSource -Destination (Join-Path $MapsReadDir 'EVALTestMap.cosm') -Force

New-Item -ItemType Directory -Force -Path $TestFilesDir | Out-Null
New-Item -ItemType Directory -Force $LastRunDir | Out-Null

# Remove stale artifacts so a leftover file can never fake a pass
Remove-Item -LiteralPath (Join-Path $TestFilesDir $CurrentShot) -Force -ErrorAction SilentlyContinue
if ($Mode -eq 'Golden') {
    Remove-Item -LiteralPath (Join-Path $TestFilesDir $GoldenShot) -Force -ErrorAction SilentlyContinue
} else {
    $GoldenSource = Join-Path $GoldensDir $GoldenShot
    if (-not (Test-Path -LiteralPath $GoldenSource)) {
        Fail "No golden at '$GoldenSource'. Run with -Mode Golden first, eyeball the PNG, then re-run the eval."
    }
    Copy-Item -LiteralPath $GoldenSource -Destination (Join-Path $TestFilesDir $GoldenShot) -Force
}

# --- Snapshot existing game logs so we can find this run's new 'Log Always' file ----
$PreLogs = @{}
if (Test-Path -LiteralPath $GameLogsRoot) {
    Get-ChildItem $GameLogsRoot -Recurse -Filter 'Log Always*.txt' -ErrorAction SilentlyContinue | ForEach-Object {
        $PreLogs[$_.FullName] = $true
    }
}

# --- Launch the game -----------------------------------------------------------------
$ScriptName = if ($Mode -eq 'Golden') { 'EVALGolden' } else { 'EVALSmoke' }
$GameArgs = @('autotest', 'testingmode', 'fixedtimestep', 'script', $ScriptName)
Write-Host "Launching: BlockWorld.exe $($GameArgs -join ' ')  (timeout ${TimeoutSec}s)"

# Raw ProcessStartInfo: PowerShell's Start-Process wildcard-expands the [STEAM] path segment
$StartInfo = New-Object System.Diagnostics.ProcessStartInfo
$StartInfo.FileName = $Exe
$StartInfo.Arguments = $GameArgs -join ' '
$StartInfo.WorkingDirectory = $ExeDir
$StartInfo.UseShellExecute = $false
$Proc = [System.Diagnostics.Process]::Start($StartInfo)
if (-not $Proc.WaitForExit($TimeoutSec * 1000)) {
    $Proc.Kill()
    Fail "Game did not exit within ${TimeoutSec}s - killed. The script may have stalled before its 'exit' command; check $TestFilesDir and $GameLogsRoot."
}
Write-Host "Game exited after $([int]($Proc.ExitTime - $Proc.StartTime).TotalSeconds)s."

# --- Collect this run's 'Log Always' file ---------------------------------------------
$Delta = ''
if (Test-Path -LiteralPath $GameLogsRoot) {
    $NewLogs = Get-ChildItem $GameLogsRoot -Recurse -Filter 'Log Always*.txt' -ErrorAction SilentlyContinue |
        Where-Object { -not $PreLogs.ContainsKey($_.FullName) }
    foreach ($LogFile in $NewLogs) {
        $Delta += [System.IO.File]::ReadAllText($LogFile.FullName)
    }
}
if ($Delta) {
    $Delta | Set-Content (Join-Path $LastRunDir 'game-log-always.txt')
    $TestRows = $Delta -split "`r?`n" | Where-Object { $_ -match '║.*(True|False)║' }
    if ($TestRows) { Write-Host '--- Test result rows ---'; $TestRows | ForEach-Object { Write-Host $_ } }
} else {
    Write-Host "Warning: no new 'Log Always' file found under $GameLogsRoot for this run."
}

# Copy screenshots for inspection
foreach ($Shot in @($GoldenShot, $CurrentShot)) {
    $ShotPath = Join-Path $TestFilesDir $Shot
    if (Test-Path -LiteralPath $ShotPath) { Copy-Item -LiteralPath $ShotPath -Destination $LastRunDir -Force }
}

if ($Delta -match 'GAME HAS HANGED') {
    Fail 'The in-game hang watchdog fired (GAME HAS HANGED in results log).'
}

# --- Verdict --------------------------------------------------------------------------
if ($Mode -eq 'Golden') {
    $Captured = Join-Path $TestFilesDir $GoldenShot
    if (-not (Test-Path -LiteralPath $Captured)) {
        Fail "Golden run finished but '$Captured' was not produced. The boot or script likely failed early; see $LastRunDir."
    }
    New-Item -ItemType Directory -Force $GoldensDir | Out-Null
    Copy-Item -LiteralPath $Captured -Destination (Join-Path $GoldensDir $GoldenShot) -Force
    Copy-Item -LiteralPath $Captured -Destination $LastRunDir -Force
    Write-Host "EVAL GOLDEN CAPTURED: $(Join-Path $GoldensDir $GoldenShot)" -ForegroundColor Green
    Write-Host 'Eyeball the PNG (grid of blocks viewed from above), then run the eval without -Mode Golden.'
    exit 0
}

# Eval mode: the named assertion row must exist AND read True. Unknown commands and
# in-command exceptions are silently skipped by the game, so absence = failure.
$ResultLines = $Delta -split "`r?`n" | Where-Object { $_ -match [regex]::Escape($TestName) }
if (-not $ResultLines) {
    Fail "Assertion '$TestName' never reported a result. The script died early (boot failure, missing golden in blockgametests, or a stale command name); see $LastRunDir."
}
$FailedLines = $ResultLines | Where-Object { $_ -match 'False' }
if ($FailedLines) {
    Fail "Screenshot diverged from the golden set:`n$($FailedLines -join "`n")`nCompare $CurrentShot vs $GoldenShot in $LastRunDir."
}

Write-Host "EVAL PASS: $TestName reported True." -ForegroundColor Green
exit 0
