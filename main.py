import os
import logging
from logging.handlers import TimedRotatingFileHandler
from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv


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

    logger = logging.getLogger()
    logger.addHandler(handler)


def main() -> None:
    setup_logger()
    token = get_token()
    bot = get_bot()

    bot.run(token)


if __name__ == "__main__":
    main()
