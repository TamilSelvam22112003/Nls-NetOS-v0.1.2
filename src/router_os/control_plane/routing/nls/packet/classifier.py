"""Packet classification before protocol parsing."""
def classify(payload: bytes) -> str:
    if not payload:
        return "empty"
    return "nls"
