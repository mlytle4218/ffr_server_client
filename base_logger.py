import logging
import ffr_config



logger = logging

logger.basicConfig(
    filename=ffr_config.CLIENT_LOG_LOC,
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)