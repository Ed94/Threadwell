# Bulk, incremental backup of vault assets/threads/* to the configured remote.
#
# Reads [backup].root from secrets/credentials.toml. The remote path is never
# echoed or logged — handle it like any other secret.
#
# Behaviour: robocopy /E mirror (add or refresh, never delete). Re-runs only
# push deltas. assets/WIP/ is deliberately excluded — it is local-only.
#
# Robocopy exit codes we accept as success: 0 (no change), 1 (files pushed),
# 2 / 3 (extras on destination, kept). 4-7 are transient / partial — re-run
# after the warning. 8+ are hard fails.

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

# Resolve paths relative to this script.
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Vault       = (Resolve-Path (Join-Path $ScriptDir '..')).Path
$Source      = Join-Path $Vault 'assets'
$ConfigFile  = Join-Path $Vault 'secrets\config.toml'

if (-not (Test-Path -LiteralPath $Source)) {
    Write-Error "source not found: $Source"
    exit 2
}
if (-not (Test-Path -LiteralPath $ConfigFile)) {
    Write-Error "config file not found: $ConfigFile"
    exit 2
}

# Parse [backup].root from config.toml. Handles both TOML basic strings
# ("...", backslashes escaped) and literal strings ('...', backslashes literal).
$lines   = Get-Content -LiteralPath $ConfigFile
$inBackup = $false
$rawValue = $null
foreach ($line in $lines) {
    $trimmed = $line.Trim()
    if ($trimmed -match '^\[(.+)\]$') {
        $inBackup = ($Matches[1] -eq 'backup')
        continue
    }
    if ($inBackup -and $trimmed -match '^root\s*=\s*(.*)$') {
        $rawValue = $Matches[1].Trim()
        break
    }
}
if (-not $rawValue) {
    Write-Error "[backup].root missing in $CredFile"
    exit 2
}

$remote = $null
if ($rawValue.StartsWith("'") -and $rawValue.EndsWith("'") -and $rawValue.Length -ge 2) {
    $remote = $rawValue.Substring(1, $rawValue.Length - 2)
} elseif ($rawValue.StartsWith('"') -and $rawValue.EndsWith('"') -and $rawValue.Length -ge 2) {
    $inner = $rawValue.Substring(1, $rawValue.Length - 2)
    try {
        $remote = [System.Text.RegExp.Regex]::Unescape($inner)
    } catch {
        Write-Error "[backup].root has unparseable escapes"
        exit 2
    }
} else {
    Write-Error "[backup].root must be a quoted TOML string"
    exit 2
}
if (-not $remote) {
    Write-Error "[backup].root is empty"
    exit 2
}

# Reachability check — do not echo the path on failure.
if (-not (Test-Path -LiteralPath $remote)) {
    Write-Error "destination unreachable (check [backup].root in credentials.toml)"
    exit 3
}

# /E   copy subdirs incl. empty
# /XD WIP  exclude the local-only WIP directory
# /R:3 /W:5 retries with backoff
# /MT:4 multithread (conservative for UNC)
# /NP /NDL /NFL keep the log short — no progress, no directory list, no per-file list
#
# Robocopy's banner prints the destination path. Suppress ALL its output
# to keep the secret off stdout/stderr. Exit code is preserved.
robocopy $Source $remote /E /XD WIP /R:3 /W:5 /MT:4 /NP /NDL /NFL *>&1 | Out-Null
$rc = $LASTEXITCODE

switch ($rc) {
    0 { Write-Host "backup ok (no change)" }
    1 { Write-Host "backup ok (files pushed)" }
    2 { Write-Host "backup ok (extras on destination, kept)" }
    3 { Write-Host "backup ok (files pushed, extras on destination, kept)" }
    { 4 -le $_ -and $_ -le 7 } {
        Write-Warning "backup partial (code $rc) — re-run to retry"
        exit 0
    }
    default {
        Write-Error "backup failed (code $rc)"
        exit $rc
    }
}
