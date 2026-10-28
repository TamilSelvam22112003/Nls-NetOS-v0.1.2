"""Safe, non-privileged command-line entry point."""
from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from router_os.version import VERSION


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nls-netos",
        description="NLS-NetOS experimental scaffold (no network configuration performed).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        "command",
        nargs="?",
        choices=("status",),
        default="status",
        help="show scaffold status",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "status":
        print(json.dumps({
            "name": "NLS-NetOS",
            "version": VERSION,
            "status": "scaffold",
            "network_io": False,
            "privileged_operations": False,
        }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
