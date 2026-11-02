#!/usr/bin/env python3
"""Repository-level development boot entry point.

Lifecycle implementation lives in router_os.application so installed execution
is independent of the repository working directory.
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from router_os.application import main

if __name__ == "__main__":
    raise SystemExit(main())
