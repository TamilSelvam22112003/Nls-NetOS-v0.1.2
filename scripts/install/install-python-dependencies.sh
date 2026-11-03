#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10+ required"'
python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install --upgrade pip setuptools wheel
"$ROOT/.venv/bin/python" -m pip install -e "$ROOT[dev]"
echo "Python environment ready at $ROOT/.venv"
