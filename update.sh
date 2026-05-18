#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_editable() {
  if command -v uv >/dev/null 2>&1; then
    uv tool install --force --editable "$ROOT_DIR"
  elif command -v pipx >/dev/null 2>&1; then
    pipx install --force --editable "$ROOT_DIR"
  else
    python3 -m pip install --user --upgrade --editable "$ROOT_DIR"
    echo "If math is not found, add your Python user scripts directory to PATH."
  fi
}

verify_install() {
  local math_cmd
  math_cmd="$(command -v math || true)"
  if [[ -z "$math_cmd" ]]; then
    echo "Error: math command was not found after update." >&2
    return 1
  fi

  local result_output
  result_output="$("$math_cmd" add 2 3)"
  if [[ "$result_output" != *"Result: 5"* ]]; then
    echo "Error: math add 2 3 did not return the expected result." >&2
    echo "$result_output" >&2
    return 1
  fi

  local error_output
  local error_code
  set +e
  error_output="$("$math_cmd" sub 1 2 2>&1)"
  error_code=$?
  set -e

  if [[ "$error_code" -ne 2 ]]; then
    echo "Error: math sub 1 2 returned exit code $error_code; expected 2." >&2
    echo "$error_output" >&2
    return 1
  fi

  if [[ "$error_output" == *"invalid choice"* || "$error_output" == *"choose from"* ]]; then
    echo "Error: unknown operation output still contains argparse's long choices list." >&2
    echo "$error_output" >&2
    return 1
  fi

  if [[ "$error_output" != *"Did you mean: subtract?"* ]]; then
    echo "Error: unknown operation output did not include the expected suggestion." >&2
    echo "$error_output" >&2
    return 1
  fi

  echo "Math CLI updated."
  echo "Command: $math_cmd"
  echo "Verified: math add 2 3"
  echo "Verified: concise unknown-operation error"
}

install_editable
verify_install
