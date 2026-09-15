# Start comms inbox watcher in the background (Windows).
# Usage:
#   powershell -File scripts\comms_daemon_start.ps1
#   powershell -File scripts\comms_daemon_start.ps1 -Interval 30
#   powershell -File scripts\comms_daemon_start.ps1 -Party kimi   # per-session: own inbox only
# Stop: New-Item STOP -ItemType File   OR   comms\STOP_DAEMON            (stops ALL daemons)
#       New-Item comms\STOP_DAEMON_KIMI -ItemType File                   (stops only kimi's)
#       then wait one interval; or Stop-Process -Id (Get-Content comms\.daemon[_<party>].pid)

param(
  [int]$Interval = 30,
  [string]$Party = ""
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Py = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) {
  # no project venv — daemons are stdlib-only, fall back to python on PATH
  $Py = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
}
$Script = Join-Path $Root "scripts\comms_daemon.py"
$Tag = if ($Party) { "_$($Party.ToLower())" } else { "" }
$PidFile = Join-Path $Root "comms\.daemon$Tag.pid"
$OutLog = Join-Path $Root "comms\daemon$Tag.stdout.log"
$ErrLog = Join-Path $Root "comms\daemon$Tag.stderr.log"
$Scope = if ($Party) { $Party.ToLower() } else { "all" }

if (-not $Py) {
  Write-Error "No python found (no .venv and python.exe not on PATH)"
  exit 1
}

if (Test-Path $PidFile) {
  $old = Get-Content $PidFile -ErrorAction SilentlyContinue
  if ($old -and (Get-Process -Id $old -ErrorAction SilentlyContinue)) {
    Write-Host "comms-daemon ($Scope) already running pid=$old"
    exit 0
  }
}

$argList = @($Script, "--loop", "--interval", "$Interval")
if ($Party) { $argList += @("--party", $Party.ToLower()) }
$p = Start-Process -FilePath $Py -ArgumentList $argList `
  -WorkingDirectory $Root -WindowStyle Hidden `
  -RedirectStandardOutput $OutLog -RedirectStandardError $ErrLog `
  -PassThru

Set-Content -Path $PidFile -Value $p.Id -Encoding ascii
Write-Host "comms-daemon started pid=$($p.Id) interval=${Interval}s scope=$Scope"
Write-Host "wake board: comms\PENDING$Tag.md"
if ($Party) {
  Write-Host "stop: New-Item $(Join-Path $Root "comms\STOP_DAEMON_$($Party.ToUpper())") -ItemType File -Force"
} else {
  Write-Host "stop: New-Item $(Join-Path $Root 'comms\STOP_DAEMON') -ItemType File -Force"
}
