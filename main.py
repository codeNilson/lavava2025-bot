import os
from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv

from core.bot import LavavaBot
from settings.logging_config import setup_root_logger


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


def main() -> None:
    setup_root_logger()
    token = get_token()
    intents = Intents.default()
    intents.message_content = True
    bot = LavavaBot(intents=intents)
    bot.run(token)


if __name__ == "__main__":
    main()
