"""Network interface inspection."""
from pathlib import Path

NET = Path("/sys/class/net")


def list_interfaces():
    return [p.name for p in sorted(NET.iterdir())] if NET.exists() else []


def interface_attribute(name, attribute):
    path = NET / name / attribute
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None
