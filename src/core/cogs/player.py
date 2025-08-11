import logging
from typing import Union

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from ...services.player_service import register_new_player

logger = logging.getLogger(f"lavava.cog.{__name__}")


class PlayerCog(commands.Cog):
    """Cog for handling user registration."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle new member registration."""
        logger.info("New member joined: %s (ID: %s)", member.name, member.id)
        await register_new_player(member)

    @commands.Cog.listener()
    async def on_member_ban(
        self, _: discord.Guild, member: Union[discord.Member, discord.User]
    ):
        """Handle member ban."""
        if isinstance(member, discord.Member):
            ban_entry = await member.guild.fetch_ban(member)
            ban_reason = ban_entry.reason if ban_entry.reason else "No reason provided"
            print(f"{member.name} was banned. Reason: {ban_reason}")

    @app_commands.command(
        name="registrar",
        description="Registrar novo jogador",
    )
    async def register(self, interaction: discord.Interaction) -> None:
        """Register a new player."""

        member: Union[discord.User, discord.Member] = interaction.user
        assert isinstance(member, discord.Member)

        await register_new_player(member)

        await interaction.response.send_message(
            f"✅ Registro concluído com sucesso! Seja bem-vindo, {member.name}!",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(PlayerCog(bot))
    logger.debug("AdminCog loaded successfully.")
