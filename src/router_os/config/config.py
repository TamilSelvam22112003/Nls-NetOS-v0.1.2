from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class InterfaceConfig:
    name: str
    role: str


@dataclass(frozen=True, slots=True)
class RouterConfig:
    hostname: str
    router_id: str


@dataclass(frozen=True, slots=True)
class NlsConfig:
    enabled: bool


@dataclass(frozen=True, slots=True)
class NetOSConfig:
    router: RouterConfig
    nls: NlsConfig
    interfaces: tuple[InterfaceConfig, ...]

    def as_mapping(self) -> Mapping[str, object]:
        return MappingProxyType({
            "router": {"hostname": self.router.hostname, "router_id": self.router.router_id},
            "nls": {"enabled": self.nls.enabled},
            "interfaces": [{"name": item.name, "role": item.role} for item in self.interfaces],
        })
