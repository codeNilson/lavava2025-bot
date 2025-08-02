import logging
import discord
from discord.ext import commands


logger = logging.getLogger("lavava.bot")


class LavavaBot(commands.Bot):
    def __init__(
        self,
        command_prefix = commands.when_mentioned_or("!"),
        intents: discord.Intents = discord.Intents.default(),
    ):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        if self.user is not None:
            logger.info(
                "Bot is ready. Logged in as %s (ID: %s)", self.user.name, self.user.id
            )
        else:
            logger.info("Bot is ready, but user information is not available.")

    async def setup_hook(self):
        await self.load_extension("core.cogs.admin")
        await self.tree.sync()
