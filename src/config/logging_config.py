import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from src.utils import get_variable


def get_log_level() -> str:
    log_level = get_variable("LOG_LEVEL", fallback="LOG_INFO").upper()
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid LOG_LEVEL: {log_level}")
    return log_level


def setup_root_logger():

    log_level = get_log_level()

    # Root Logger
    logger = logging.getLogger()

    # Discord.py style formatter: YYYY-MM-DD HH:MM:SS LEVEL    logger_name Message
    formatter = Formatter(
        "%(asctime)s %(levelname)-8s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = TimedRotatingFileHandler(
        "logs/lavava_logger.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="UTF-8",
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(log_level)
