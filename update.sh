#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_editable() {
  if command -v uv >/dev/null 2>&1; then
    uv tool install --force --editable "$ROOT_DIR[all]"
  elif command -v pipx >/dev/null 2>&1; then
    pipx install --force --editable "$ROOT_DIR[all]"
  else
    local python_cmd
    python_cmd=""
    for candidate in python3.14 python3.13 python3.12 python3.11 python3; do
      if command -v "$candidate" >/dev/null 2>&1 \
          && "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 11))'; then
        python_cmd="$candidate"
        break
      fi
    done

    if [[ -z "$python_cmd" ]]; then
      echo "Error: Math CLI requires Python 3.11 or newer." >&2
      return 1
    fi

    "$python_cmd" -m pip install --user --upgrade --editable "$ROOT_DIR[all]"
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
