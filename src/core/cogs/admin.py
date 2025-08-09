import logging
from typing import Optional, Union

import discord
from discord.ext import commands
from discord import app_commands

from src.services.player_service import register_new_player

logger = logging.getLogger(f"lavava.cog.{__name__}")


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ping", description="Comando de teste para administração"
    )
    @app_commands.default_permissions(administrator=True)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.command(
        name="registrar-jogador",
        description="Registrar novo jogador",
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(member="O membro a ser registrado")
    async def register(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ) -> None:
        """Register a new player."""

        await register_new_player(member)

        await interaction.response.send_message(
            f"✅ Jogador {member.name} registrado.", ephemeral=True
        )


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(AdminCog(bot))
    logger.debug("AdminCog loaded successfully.")
