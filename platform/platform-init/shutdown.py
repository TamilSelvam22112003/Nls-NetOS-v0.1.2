"""Platform shutdown hooks.

Shutdown is intentionally idempotent. Higher-level router services should stop
before calling this module so that platform resources remain available until
control-plane and data-plane workers have drained.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable


class ShutdownCoordinator:
    """Run registered shutdown callbacks in reverse registration order."""

    def __init__(self) -> None:
        self._callbacks: list[Callable[[], Any]] = []
        self._stopped = False

    def register(self, callback: Callable[[], Any]) -> None:
        if self._stopped:
            raise RuntimeError("shutdown coordinator is already stopped")
        self._callbacks.append(callback)

    def shutdown(self) -> None:
        if self._stopped:
            return
        errors: list[BaseException] = []
        for callback in reversed(self._callbacks):
            try:
                callback()
            except BaseException as exc:  # preserve every failure for the caller
                errors.append(exc)
        self._stopped = True
        self._callbacks.clear()
        if errors:
            raise RuntimeError(f"{len(errors)} shutdown callback(s) failed") from errors[0]


__all__ = ["ShutdownCoordinator"]
