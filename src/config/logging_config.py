import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from src.utils import get_variable


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        formatted = super().format(record)

        # Add color if outputting to terminal
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, "")
            if color:
                formatted = formatted.replace(
                    record.levelname, f"{color}{record.levelname}{self.RESET}"
                )

        return formatted


def get_log_level() -> str:
    log_level = get_variable("LOG_LEVEL", fallback="INFO").upper()
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid LOG_LEVEL: {log_level}")
    return log_level


def setup_root_logger():
    log_level = get_log_level()

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Root Logger
    logger = logging.getLogger()

    # Clear existing handlers to prevent duplicates
    if logger.handlers:
        logger.handlers.clear()

    # Formatters
    formatter = Formatter(
        "%(asctime)s %(levelname)-8s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    colored_formatter = ColoredFormatter(
        "%(asctime)s %(levelname)-8s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handlers
    file_handler = TimedRotatingFileHandler(
        "logs/lavava_logger.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="UTF-8",
    )

    console_handler = logging.StreamHandler()

    # Apply formatters
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(colored_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(log_level)

    # Configure external libraries
    logging.getLogger("discord.client").setLevel("INFO")
    logging.getLogger("discord.gateway").setLevel("INFO")
    logging.getLogger("aiohttp.access").setLevel("WARNING")
