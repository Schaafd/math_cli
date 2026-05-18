#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v uv >/dev/null 2>&1; then
  uv tool install --force --editable "$ROOT_DIR"
elif command -v pipx >/dev/null 2>&1; then
  pipx install --force --editable "$ROOT_DIR"
else
  python3 -m pip install --user --upgrade --editable "$ROOT_DIR"
  echo "If math is not found, add your Python user scripts directory to PATH."
fi

echo "Math CLI installed."
echo "Try: math add 2 3"
