import logging
import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(f"lavava.cog.{__name__}")


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Comando de teste para administração",
    )
    @app_commands.default_permissions(administrator=True)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(AdminCog(bot))
    logger.debug("AdminCog loaded successfully.")
