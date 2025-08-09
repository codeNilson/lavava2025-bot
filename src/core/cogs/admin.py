import logging
from typing import Optional, Union

import discord
from discord.ext import commands
from discord import app_commands

from src.services.player_service import register_new_player
from src.utils import get_variable

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
        name="registrar",
        description="Registrar novo jogador",
    )
    @app_commands.default_permissions()
    async def register(self, interaction: discord.Interaction) -> None:
        """Register a new player."""

        member: Union[discord.User, discord.Member] = interaction.user
        assert isinstance(member, discord.Member)

        await register_new_player(member)

        guild: discord.Guild = member.guild

        player_role: Optional[discord.Role] = discord.utils.get(
            guild.roles, name="Jogador"
        )
        if player_role:
            await member.add_roles(player_role)
            await interaction.response.send_message(
                "✅ Jogador registrado e cargo adicionado com sucesso!", ephemeral=True
            )

    async def cog_load(self) -> None:
        guild: Optional[discord.Guild] = self.bot.get_guild(
            int(get_variable("GUILD_ID"))
        )
        if not guild:
            return

        player_role: discord.Role | None = discord.utils.get(
            guild.roles, name="Jogador"
        )

        if not player_role:
            logger.warning("Role 'Jogador' not found in the guild.")
            return

        for cmd in await self.bot.tree.fetch_commands(guild=guild):
            if cmd.name in ["registrar"]:
                permissions = {
                    "id": player_role.id,
                    "type": 1,  # 1 = ROLE
                    "permission": False,
                }

                await self.bot.http.edit_application_command_permissions(
                    self.bot.user.id,  # type: ignore
                    guild.id,
                    cmd.id,
                    permissions,
                )
                break


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(AdminCog(bot))
    logger.debug("AdminCog loaded successfully.")
