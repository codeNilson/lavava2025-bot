import logging
from typing import override
import discord
from discord.ext import commands


logger = logging.getLogger("lavava.bot")


class LavavaBot(commands.Bot):
    def __init__(
        self,
        intents: discord.Intents = discord.Intents.default(),
    ):
        super().__init__(command_prefix="!", intents=intents)
        super().tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: Exception
    ):
        if isinstance(error, commands.CommandNotFound):
            await interaction.response.send_message(
                "Esse comando não existe. Cê é burrão hein?", ephemeral=True
            )
            logger.debug("User tried to use a non-existent command: %s", interaction.command.name)  # type: ignore
        else:
            await interaction.response.send_message(
                "Um erro desconhecido ocorreu. Tente novamente mais ou contate um admin.",
                ephemeral=True,
            )
            logger.exception("Unexpected error in command: %s", error)


    async def on_ready(self):
        if self.user is not None:
            logger.info(
                "Bot is ready. Logged in as %s (ID: %s)", self.user.name, self.user.id
            )
        else:
            logger.info("Bot is ready, but user information is not available.")

    @override
    async def setup_hook(self):
        await self.load_extension("core.cogs.admin")
        await self.load_extension("core.cogs.funny")
        await self.tree.sync()
