import logging
from logging.handlers import RotatingFileHandler
import ffr_config

logger = logging

logger.basicConfig(
        handlers=[
            RotatingFileHandler(
                ffr_config.CLIENT_LOG_LOC,
                maxBytes=10240000,
                backupCount=5
            )
        ],
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s PID_%(process)d %(message)s'
    )

