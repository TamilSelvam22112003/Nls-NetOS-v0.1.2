from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from .config import InterfaceConfig, NetOSConfig, NlsConfig, RouterConfig
from .defaults import DEFAULT_CONFIG
from .validator import ConfigValidationError, validate_config


class ConfigLoadError(RuntimeError):
    """Raised when configuration cannot be loaded or validated."""


def load_config(path: str | Path) -> NetOSConfig:
    config_path = Path(path).expanduser().resolve()
    if not config_path.is_file():
        raise ConfigLoadError(f"configuration file not found: {config_path}")
    try:
        with config_path.open("r", encoding="utf-8") as handle:
            loaded: Any = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise ConfigLoadError(f"invalid YAML in {config_path}: {exc}") from exc
    except OSError as exc:
        raise ConfigLoadError(f"unable to read {config_path}: {exc}") from exc

    merged = deepcopy(DEFAULT_CONFIG)
    if loaded is not None:
        if not isinstance(loaded, dict):
            raise ConfigLoadError("configuration root must be a mapping")
        _deep_merge(merged, loaded)
    try:
        validate_config(merged)
    except ConfigValidationError as exc:
        raise ConfigLoadError(str(exc)) from exc

    return NetOSConfig(
        router=RouterConfig(**merged["router"]),
        nls=NlsConfig(**merged["nls"]),
        interfaces=tuple(InterfaceConfig(**item) for item in merged["interfaces"]),
    )


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
