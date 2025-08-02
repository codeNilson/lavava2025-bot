import os
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv

logger = logging.getLogger("discord.client")


def get_token() -> str:
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN não encontrado no .env")
    return token


def get_bot() -> Bot:
    intents = Intents.default()
    intents.message_content = True
    return Bot(command_prefix="!", intents=intents)


def setup_logger():

    handler = TimedRotatingFileHandler(
        "logs/lavava_logger.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="UTF-8",
    )

    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    handler.setFormatter(formatter)


def main() -> None:
    setup_logger()
    token = get_token()
    bot = get_bot()
    logger.info("Iniciando o bot...")
    bot.run(token)


if __name__ == "__main__":
    main()
