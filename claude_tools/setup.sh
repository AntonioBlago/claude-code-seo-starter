#!/usr/bin/env bash
# setup.sh — create the claude_tools_venv and install the Python modules' deps.
# Run from the repo root:  bash claude_tools/setup.sh
# Re-runnable: if the venv already exists it just refreshes the dependencies.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
VENV="$ROOT/claude_tools_venv"

# Windows venvs put python in Scripts/, POSIX in bin/.
if [ -x "$VENV/Scripts/python.exe" ]; then PY="$VENV/Scripts/python.exe"
else PY="$VENV/bin/python"; fi

# Prefer Python 3.12, fall back to python3 / python.
pick_python() {
  if command -v py >/dev/null 2>&1 && py -3.12 --version >/dev/null 2>&1; then echo "py -3.12"
  elif command -v python3.12 >/dev/null 2>&1; then echo "python3.12"
  elif command -v python3 >/dev/null 2>&1; then echo "python3"
  else echo "python"; fi
}

if [ ! -x "$PY" ]; then
  echo "Creating venv at $VENV ..."
  $(pick_python) -m venv "$VENV"
  if [ -x "$VENV/Scripts/python.exe" ]; then PY="$VENV/Scripts/python.exe"; else PY="$VENV/bin/python"; fi
fi

echo "Upgrading pip + installing requirements ..."
"$PY" -m pip install --upgrade pip --quiet
"$PY" -m pip install -r "$SCRIPT_DIR/requirements.txt" --quiet

"$PY" -c "import fpdf, pandas, openpyxl; print('claude_tools_venv ready -', 'fpdf2', fpdf.__version__, '| pandas', pandas.__version__)"
echo "Run modules with:  ./claude_tools_venv/Scripts/python -m claude_tools.<module>"
