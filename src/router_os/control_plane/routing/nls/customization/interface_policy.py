"""NLS-specific interface classification policy."""

from __future__ import annotations

from dataclasses import dataclass

from .config import NLSCustomization


@dataclass(frozen=True)
class InterfaceClassification:
    classification: str
    source: str
    reason: str


class NLSInterfacePolicy:
    """Applies NLS operator overrides before generic inference."""

    def __init__(self, customization: NLSCustomization | None = None) -> None:
        self.customization = customization or NLSCustomization()

    def classify(self, interface_name: str, *, loopback: bool = False, point_to_point: bool = False) -> InterfaceClassification:
        override = self.customization.classify_override(interface_name)
        if override:
            return InterfaceClassification(override, "CONFIGURED", "NLS interface override")
        if loopback:
            return InterfaceClassification("LOOPBACK", "DISCOVERED", "loopback interface")
        if point_to_point:
            return InterfaceClassification("POINT_TO_POINT", "DISCOVERED", "point-to-point link")
        if self.customization.allow_inferred_classification:
            return InterfaceClassification("UNKNOWN", "INFERRED", "no NLS classification override")
        return InterfaceClassification("UNKNOWN", "POLICY", "inference disabled")
