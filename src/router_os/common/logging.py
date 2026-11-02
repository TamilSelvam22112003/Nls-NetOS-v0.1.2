from __future__ import annotations

import logging

LOGGER_NAME = "nls-netos"


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    return logger


def get_logger(component: str | None = None) -> logging.Logger:
    logger = configure_logging()
    return logger.getChild(component) if component else logger
