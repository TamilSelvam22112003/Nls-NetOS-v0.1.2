"""Generic platform-driver lifecycle with resource ownership."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class PlatformDriver:
    name: str
    resources: dict[str, Any] = field(default_factory=dict)
    started: bool = False
    _cleanup: list[Callable[[], None]] = field(default_factory=list, repr=False)

    def register_resource(self, name: str, resource: Any) -> Any:
        if not name:
            raise ValueError("resource name must not be empty")
        if self.started:
            raise RuntimeError("cannot register resources after driver start")
        self.resources[name] = resource
        return resource

    def on_cleanup(self, callback: Callable[[], None]) -> None:
        if not callable(callback):
            raise TypeError("cleanup callback must be callable")
        self._cleanup.append(callback)

    def start(self) -> None:
        if self.started:
            return
        self.started = True

    def stop(self) -> None:
        if not self.started:
            return
        errors: list[Exception] = []
        for callback in reversed(self._cleanup):
            try:
                callback()
            except Exception as exc:  # noqa: BLE001 - preserve all cleanup errors
                errors.append(exc)
        self.started = False
        if errors:
            raise RuntimeError(f"{len(errors)} platform-driver cleanup operation(s) failed") from errors[0]
