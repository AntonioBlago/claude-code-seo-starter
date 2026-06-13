# setup.ps1 — create the claude_tools_venv and install the Python modules' deps.
# Run from the repo root:  .\claude_tools\setup.ps1
# Re-runnable: if the venv already exists it just refreshes the dependencies.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Root "claude_tools_venv"
$Py   = Join-Path $Venv "Scripts\python.exe"

# Prefer Python 3.12 via the launcher; fall back to whatever `python` resolves to.
function Get-Python {
    try { & py -3.12 --version *> $null; if ($?) { return @("py", "-3.12") } } catch {}
    return @("python")
}

if (-not (Test-Path $Py)) {
    $base = Get-Python
    Write-Host "Creating venv at $Venv ..."
    & $base[0] $base[1..($base.Count-1)] -m venv $Venv
}

Write-Host "Upgrading pip + installing requirements ..."
& $Py -m pip install --upgrade pip --quiet
& $Py -m pip install -r (Join-Path $PSScriptRoot "requirements.txt") --quiet

& $Py -c "import fpdf, pandas, openpyxl; print('claude_tools_venv ready -', 'fpdf2', fpdf.__version__, '| pandas', pandas.__version__)"
Write-Host "Run modules with:  .\claude_tools_venv\Scripts\python.exe -m claude_tools.<module>"
