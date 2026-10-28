"""Command entry point for NLS-NetOS CLI."""

from __future__ import annotations

import argparse

from .status import render, valid_section


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nls", description="NLS-NetOS router management CLI")
    sub = parser.add_subparsers(dest="command")
    status = sub.add_parser("status", help="show router/platform status")
    status.add_argument("section", nargs="?", default="all", help="platform, hardware, cpu, memory, pci, drivers, interfaces")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "status":
        if not valid_section(args.section):
            print(f"nls: unknown status section: {args.section}")
            return 2
        print(render(args.section))
        return 0
    build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
