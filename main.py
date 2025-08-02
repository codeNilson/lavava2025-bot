from discord import Intents
from discord.ext.commands import Bot

from core.bot import LavavaBot
from config.logging_config import setup_root_logger
from utils import get_variable


def get_token() -> str:
    token = get_variable("DISCORD_TOKEN")
    return token


def get_bot() -> Bot:
    intents = Intents.default()
    intents.message_content = True
    return Bot(command_prefix="!", intents=intents)


def main() -> None:
    setup_root_logger()
    token = get_token()
    intents = Intents.default()
    intents.message_content = True
    bot = LavavaBot(intents=intents)
    bot.run(token)


if __name__ == "__main__":
    main()
