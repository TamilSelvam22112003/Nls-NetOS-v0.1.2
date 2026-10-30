"""Identity-key rotation must be explicit because it changes router identity."""


def rotate_identity() -> None:
    raise RuntimeError("Asymmetric identity rotation requires explicit provisioning/policy")
