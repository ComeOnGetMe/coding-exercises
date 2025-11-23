import logging

from src.config import logging_settings

def setup_logging():
    logging.basicConfig(
        level=logging_settings.LEVEL,
        format=logging_settings.FORMAT,
        datefmt=logging_settings.DATE_FORMAT,
    )
    return logging.getLogger(__name__)
