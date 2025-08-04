from discord import Intents
from discord.ext.commands import Bot

from src.core.bot import LavavaBot
from src.config.logging_config import setup_root_logger
from src.utils import get_variable


def get_token() -> str:
    token = get_variable("DISCORD_TOKEN")
    return token


def get_bot() -> Bot:
    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    return LavavaBot(intents=intents)


def main() -> None:
    setup_root_logger()
    token = get_token()
    bot = get_bot()
    bot.run(token)


if __name__ == "__main__":
    main()
