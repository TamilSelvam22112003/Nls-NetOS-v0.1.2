from __future__ import annotations

from abc import ABC, abstractmethod


class Subsystem(ABC):
    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...
