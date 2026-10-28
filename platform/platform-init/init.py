"""Platform initialization entry point for NLS-NetOS."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Dict, Optional

from .capabilities import detect_capabilities
from .discovery import discover_platform


@dataclass
class PlatformContext:
    """Runtime snapshot shared by platform services."""

    discovery: Dict[str, Any] = field(default_factory=dict)
    capabilities: Dict[str, Any] = field(default_factory=dict)
    initialized: bool = False
    shutting_down: bool = False


class PlatformManager:
    """Coordinate platform discovery, capability detection and shutdown."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._context = PlatformContext()

    @property
    def context(self) -> PlatformContext:
        with self._lock:
            return self._context

    def initialize(self) -> PlatformContext:
        with self._lock:
            if self._context.initialized:
                return self._context
            self._context.shutting_down = False
            self._context.discovery = discover_platform()
            self._context.capabilities = detect_capabilities(self._context.discovery)
            self._context.initialized = True
            return self._context

    def shutdown(self) -> None:
        with self._lock:
            self._context.shutting_down = True
            self._context.initialized = False


_manager: Optional[PlatformManager] = None


def initialize() -> PlatformContext:
    """Initialize the process-wide platform manager."""
    global _manager
    if _manager is None:
        _manager = PlatformManager()
    return _manager.initialize()


def shutdown() -> None:
    """Shutdown the process-wide platform manager."""
    if _manager is not None:
        _manager.shutdown()


__all__ = ["PlatformContext", "PlatformManager", "initialize", "shutdown"]
