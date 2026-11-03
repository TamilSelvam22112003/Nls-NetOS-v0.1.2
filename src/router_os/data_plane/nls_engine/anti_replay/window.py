"""Replay protection state for established NLS contexts."""

class ReplayWindow:
    """Small bounded receive window for monotonically increasing counters."""

    def __init__(self, size: int = 64) -> None:
        if size <= 0:
            raise ValueError("window size must be positive")
        self._size = size
        self._highest = -1
        self._seen: set[int] = set()

    def accept(self, counter: int) -> bool:
        if counter < 0:
            return False
        if counter in self._seen:
            return False
        if self._highest >= 0 and counter < self._highest - self._size + 1:
            return False
        self._seen.add(counter)
        if counter > self._highest:
            self._highest = counter
        cutoff = self._highest - self._size + 1
        self._seen = {value for value in self._seen if value >= cutoff}
        return True
