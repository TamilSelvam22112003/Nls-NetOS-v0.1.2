from __future__ import annotations

import json

from router_os.cli import main


def test_status_is_safe_and_explicit(capsys) -> None:
    assert main(["status"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["name"] == "NLS-NetOS"
    assert payload["version"] == "0.1.2"
    assert payload["status"] == "scaffold"
    assert payload["network_io"] is False
    assert payload["privileged_operations"] is False


def test_version_command(capsys) -> None:
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    assert "0.1.2" in capsys.readouterr().out
