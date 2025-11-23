import logging

from src.config import settings

def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        datefmt=settings.LOG_DATE_FORMAT,
    )
    return logging.getLogger(__name__)
