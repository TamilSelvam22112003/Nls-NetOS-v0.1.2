from __future__ import annotations

import argparse
import os
from enum import Enum, auto
from pathlib import Path

from .common.logging import get_logger
from .config import NetOSConfig, load_config
from .control_plane import ControlPlaneSubsystem
from .crypto import CryptoSubsystem
from .data_plane import DataPlaneSubsystem
from .platform import PlatformSubsystem

LOG = get_logger("boot")


class BootPhase(Enum):
    OFF = auto()
    STARTING = auto()
    PLATFORM_INITIALIZED = auto()
    CONFIGURATION_LOADED = auto()
    CRYPTO_INITIALIZED = auto()
    ROUTER_IDENTITY_LOADED = auto()
    CONTROL_PLANE_RUNNING = auto()
    DATA_PLANE_RUNNING = auto()
    READY = auto()
    FAILED = auto()


class BootError(RuntimeError):
    """Raised when the bootstrap sequence cannot reach READY."""


class RouterApplication:
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path
        self.phase = BootPhase.OFF
        self.config: NetOSConfig | None = None
        self.platform = PlatformSubsystem()
        self.crypto = CryptoSubsystem()
        self.control_plane: ControlPlaneSubsystem | None = None
        self.data_plane: DataPlaneSubsystem | None = None

    def boot(self) -> None:
        self.phase = BootPhase.STARTING
        LOG.info("NLS-NetOS starting...")
        try:
            self.platform.initialize()
            self.platform.start()
            self.phase = BootPhase.PLATFORM_INITIALIZED
            LOG.info("Platform initialized")

            self.config = load_config(self.config_path)
            self.phase = BootPhase.CONFIGURATION_LOADED
            LOG.info("Configuration loaded")

            self.crypto.initialize()
            self.crypto.start()
            self.phase = BootPhase.CRYPTO_INITIALIZED
            LOG.info("Crypto subsystem initialized")

            self.phase = BootPhase.ROUTER_IDENTITY_LOADED
            LOG.info("Router identity loaded")

            self.control_plane = ControlPlaneSubsystem(self.config)
            self.control_plane.initialize()
            self.control_plane.start()
            self.phase = BootPhase.CONTROL_PLANE_RUNNING
            LOG.info("Control plane starting")

            self.data_plane = DataPlaneSubsystem(self.config)
            self.data_plane.initialize()
            self.data_plane.start()
            self.phase = BootPhase.DATA_PLANE_RUNNING
            LOG.info("Data plane starting")

            self.phase = BootPhase.READY
            LOG.info("NLS-NetOS ready")
        except Exception as exc:
            self.phase = BootPhase.FAILED
            LOG.error("NLS-NetOS startup aborted: %s", exc)
            self.stop()
            raise BootError(str(exc)) from exc

    def stop(self) -> None:
        if self.data_plane is not None:
            self.data_plane.stop()
        if self.control_plane is not None:
            self.control_plane.stop()
        self.crypto.stop()
        self.platform.stop()
        if self.phase is not BootPhase.FAILED:
            self.phase = BootPhase.OFF


def default_config_path() -> Path:
    override = os.environ.get("NLS_NETOS_CONFIG")
    return Path(override).expanduser() if override else Path.cwd() / "config" / "router.yaml"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the NLS-NetOS prototype runtime")
    parser.add_argument("--config", type=Path, default=default_config_path(), help="path to router YAML configuration")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    app = RouterApplication(args.config)
    try:
        app.boot()
    except BootError:
        return 1
    return 0
