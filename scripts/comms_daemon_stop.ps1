# Stop comms inbox watcher(s) gracefully (Windows).
# Usage:
#   powershell -File scripts\comms_daemon_stop.ps1 -Party kimi   # stop only kimi's daemon
#   powershell -File scripts\comms_daemon_stop.ps1               # stop ALL daemons
# Waits up to -TimeoutSec for the process to exit, then cleans up the
# stop file and pid file so a later start works without residue.

param(
  [string]$Party = "",
  [int]$TimeoutSec = 45
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

if ($Party) {
  $Tag = "_$($Party.ToLower())"
  $StopFile = Join-Path $Root "comms\STOP_DAEMON_$($Party.ToUpper())"
  $Scope = $Party.ToLower()
} else {
  $Tag = ""
  $StopFile = Join-Path $Root "comms\STOP_DAEMON"   # global: stops every daemon
  $Scope = "all"
}
$PidFile = Join-Path $Root "comms\.daemon$Tag.pid"

New-Item $StopFile -ItemType File -Force | Out-Null
Write-Host "stop file created: $StopFile (scope=$Scope)"

# wait for the daemon's next tick to notice and exit
$pid_ = $null
if (Test-Path $PidFile) { $pid_ = Get-Content $PidFile -ErrorAction SilentlyContinue }
$deadline = (Get-Date).AddSeconds($TimeoutSec)
while ((Get-Date) -lt $deadline) {
  if (-not $pid_ -or -not (Get-Process -Id $pid_ -ErrorAction SilentlyContinue)) { break }
  Start-Sleep -Seconds 3
}

if ($pid_ -and (Get-Process -Id $pid_ -ErrorAction SilentlyContinue)) {
  Write-Host "daemon pid=$pid_ still alive after ${TimeoutSec}s - stop file left in place, it will exit on next tick"
  exit 1
}

# clean up so a fresh start has no residue
Remove-Item $StopFile -Force -ErrorAction SilentlyContinue
Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
Write-Host "comms-daemon ($Scope) stopped; stop+pid files cleaned"
