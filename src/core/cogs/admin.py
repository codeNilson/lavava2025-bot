import logging

import discord
from discord.ext import commands
from discord import app_commands

from src.services.player_service import register_new_player

logger: logging.Logger = logging.getLogger(f"lavava.cog.{__name__}")


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ping", description="Comando de teste para administração"
    )
    @app_commands.default_permissions(administrator=True)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Pong!",
            ephemeral=True,
            delete_after=5,
        )

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

    group_clean = app_commands.Group(
        name="limpar",
        description="Comandos para limpar mensagens ou membros.",
        default_permissions=discord.Permissions(administrator=True),
    )

    @group_clean.command(name="mensagens", description="Limpa mensagens de um canal.")
    async def clean_messages(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        """Clear messages from the channel"""

        await interaction.response.send_message(
            f"Ok, limpando mensagens do canal {channel}.",
            ephemeral=True,
            delete_after=30,
        )
        await channel.purge(limit=None, bulk=True)
        await interaction.followup.send("✅ Mensagens removidas com sucesso.")

    @group_clean.command(name="cargos", description="Limpa os membros de um cargo.")
    async def clean_roles(
        self, interaction: discord.Interaction, role: discord.Role
    ) -> None:
        """Clear roles from members"""
        if not role:
            await interaction.response.send_message(
                "⚠️ Nenhum cargo fornecido. Por favor, forneça um ou mais cargos."
            )
            return

        await self.reset_role(role)
        await interaction.response.send_message("Cargos removidos com sucesso.")

    async def reset_role(self, role: discord.Role) -> None:

        for member in role.members:
            await member.remove_roles(role)

        logger.info(
            "Todos os membros com o cargo %s foram removidos com sucesso.", role.name
        )


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(AdminCog(bot))
    logger.debug("AdminCog loaded successfully.")
