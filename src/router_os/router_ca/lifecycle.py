"""Certificate/key lifecycle decisions used by boot and runtime workers."""

from datetime import datetime, timezone


def is_expired(valid_to):
    if valid_to is None:
        return False
    return valid_to <= datetime.now(timezone.utc).replace(tzinfo=None)


def needs_refresh(valid_to, refresh_before_expiry_seconds):
    if valid_to is None:
        return True
    from datetime import timedelta
    return valid_to <= datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=refresh_before_expiry_seconds)
