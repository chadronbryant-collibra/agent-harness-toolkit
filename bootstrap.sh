#!/bin/sh
set -eu
toolkit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3.11+ is required. Open START-HERE.md in Claude for setup.' >&2
  exit 2
fi
exec python3 "$toolkit_dir/toolkit.py" "$@"
