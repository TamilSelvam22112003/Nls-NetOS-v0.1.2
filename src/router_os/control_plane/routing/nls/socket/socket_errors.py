"""Socket subsystem exceptions."""
class NLSSocketError(Exception):
    """Base socket error."""

class SocketConfigurationError(NLSSocketError):
    pass

class SocketStateError(NLSSocketError):
    pass
