from __future__ import annotations

import ipaddress
from collections.abc import Mapping


class ConfigValidationError(ValueError):
    """Raised when configuration violates the supported bootstrap schema."""


def validate_config(data: object) -> None:
    if not isinstance(data, Mapping):
        raise ConfigValidationError("configuration root must be a mapping")
    _require_keys(data, {"router", "nls", "interfaces"}, "configuration")

    router = data["router"]
    if not isinstance(router, Mapping):
        raise ConfigValidationError("router must be a mapping")
    _require_keys(router, {"hostname", "router_id"}, "router")
    if not isinstance(router["hostname"], str) or not router["hostname"].strip():
        raise ConfigValidationError("router.hostname must be a non-empty string")
    if not isinstance(router["router_id"], str):
        raise ConfigValidationError("router.router_id must be a string")
    try:
        ipaddress.IPv4Address(router["router_id"])
    except ipaddress.AddressValueError as exc:
        raise ConfigValidationError("router.router_id must be a valid IPv4 address") from exc

    nls = data["nls"]
    if not isinstance(nls, Mapping):
        raise ConfigValidationError("nls must be a mapping")
    _require_keys(nls, {"enabled"}, "nls")
    if not isinstance(nls["enabled"], bool):
        raise ConfigValidationError("nls.enabled must be a boolean")

    interfaces = data["interfaces"]
    if not isinstance(interfaces, list):
        raise ConfigValidationError("interfaces must be a list")
    seen: set[str] = set()
    valid_roles = {"lan", "wan"}
    for index, item in enumerate(interfaces):
        if not isinstance(item, Mapping):
            raise ConfigValidationError(f"interfaces[{index}] must be a mapping")
        _require_keys(item, {"name", "role"}, f"interfaces[{index}]")
        name, role = item["name"], item["role"]
        if not isinstance(name, str) or not name.strip():
            raise ConfigValidationError(f"interfaces[{index}].name must be a non-empty string")
        if name in seen:
            raise ConfigValidationError(f"duplicate interface name: {name}")
        seen.add(name)
        if role not in valid_roles:
            raise ConfigValidationError(f"interfaces[{index}].role must be one of: {', '.join(sorted(valid_roles))}")


def _require_keys(data: Mapping[str, object], allowed: set[str], scope: str) -> None:
    missing = allowed.difference(data.keys())
    unknown = set(data.keys()).difference(allowed)
    if missing:
        raise ConfigValidationError(f"{scope} missing required keys: {', '.join(sorted(missing))}")
    if unknown:
        raise ConfigValidationError(f"{scope} contains unsupported keys: {', '.join(sorted(unknown))}")
