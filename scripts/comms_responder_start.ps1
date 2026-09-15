<#
.SYNOPSIS
    Starts the comms auto-responder daemon in a hidden background PowerShell process on Windows.

.EXAMPLE
    .\scripts\comms_responder_start.ps1 -Party kimi -Interval 15
#>

param (
    [string]$Party = "kimi",
    [int]$Interval = 15
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$DaemonScript = Join-Path $ScriptDir "comms_responder_daemon.py"

if (-not (Test-Path $PythonExe)) {
    # no project venv — daemon is stdlib-only, fall back to python on PATH
    $PythonExe = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
}
if (-not $PythonExe) {
    Write-Error "No python found (no .venv and python.exe not on PATH)"
    exit 1
}

$Arguments = "`"$DaemonScript`" --party $Party --loop --interval $Interval"

Write-Host "Starting comms responder daemon for $Party (interval ${Interval}s)..."
$Process = Start-Process -FilePath $PythonExe -ArgumentList $Arguments -WorkingDirectory $RepoRoot -WindowStyle Hidden -PassThru

Write-Host "Daemon process started with PID: $($Process.Id)"
