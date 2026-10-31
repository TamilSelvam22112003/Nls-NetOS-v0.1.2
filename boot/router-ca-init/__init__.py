"""Router-CA boot-time initialization package.

This package establishes the local trust-anchor inventory and starts the
Router-CA synchronization lifecycle. It does not define the future NLS
Router-CA packet format; that is intentionally a later protocol layer.
"""

from .config import RouterCAConfig
from .startup import RouterCAStartup

__all__ = ["RouterCAConfig", "RouterCAStartup"]
