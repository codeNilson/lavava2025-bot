import logging
from typing import Union, Optional
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from src.error.api_errors import ResourceNotFound
from src.services.player_service import (
    active_player,
    deactivate_player,
    get_player_profile,
    register_new_player,
)
from src.models.player_model import Player

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
        if not isinstance(member, discord.Member):
            return
        ban_entry = await member.guild.fetch_ban(member)
        ban_reason = ban_entry.reason if ban_entry.reason else "No reason provided"

        try:
            await deactivate_player(member, ban_reason)
        except ResourceNotFound:
            logger.warning(
                "Player %s (ID: %s) not found in the system. Skipping deactivation.",
                member.name,
                member.id,
            )
            return

        logger.info(
            "Member %s (ID: %s) banned. Deactivated player with reason: %s",
            member.name,
            member.id,
            ban_reason,
        )

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

    @app_commands.command(
        name="desativar",
        description="Desativar jogador",
    )
    @app_commands.describe(
        member="Membro do servidor para desativar",
        reason="Motivo da desativação",
    )
    async def deactivate(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "Nenhum motivo fornecido",
    ) -> None:
        """Deactivate a player."""

        await deactivate_player(member, reason)

        await interaction.response.send_message(
            f"✅ Jogador {member.name} desativado com sucesso!",
            ephemeral=True,
        )

    @app_commands.command(
        name="reativar",
        description="Reativar jogador",
    )
    @app_commands.describe(member="Membro do servidor para reativar")
    async def reactivate(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        """Reactivate a player."""

        await active_player(member)
        await interaction.response.send_message(
            f"✅ Jogador {member.name} reativado com sucesso!",
            ephemeral=True,
        )

    # @app_commands.command(
    #     name="perfil",
    #     description="Exibir perfil do jogador",
    # )
    # @app_commands.describe(member="Membro do servidor para exibir o perfil")
    # async def profile(
    #     self,
    #     interaction: discord.Interaction,
    #     member: Optional[discord.Member | discord.User] = None,
    # ) -> None:
    #     """Display player profile."""
    #     if member is None:
    #         member = interaction.user

    #     if not isinstance(member, discord.Member):
    #         await interaction.response.send_message(
    #             "❌ Membro não encontrado ou não é um membro do servidor.",
    #             ephemeral=True,
    #         )
    #         return

    #     player_data = await get_player_profile(member.name)
    #     assert player_data is not None

    #     # Assumimos que player_data tem todos os campos necessários
    #     dt = datetime.fromisoformat(player_data['lastUpdated'])
    #     formatted_date = dt.strftime('%d/%m/%Y %H:%M')

    #     winrate = float(player_data['winRate'])
    #     if winrate <= 1:
    #         winrate *= 100

    #     # Título com o username — mantemos a identificação única aqui
    #     embed = discord.Embed(
    #         title=f"{player_data['playerUsername']} — Perfil",
    #         color=discord.Color.blurple(),
    #     )

    #     # Miniatura do avatar
    #     embed.set_thumbnail(url=member.display_avatar.url)

    #     # Discord mention exibido uma única vez em campo próprio (sem repetir no título/author)
    #     embed.add_field(name="Discord", value=member.mention, inline=True)

    #     # Estatísticas principais
    #     embed.add_field(name="🏅 Posição", value=f"#{player_data['position']}", inline=True)
    #     embed.add_field(name="⭐ Pontos", value=str(player_data['totalPoints']), inline=True)
    #     embed.add_field(name="📈 Winrate", value=f"{winrate:.2f}%", inline=True)
    #     embed.add_field(name="🎮 Partidas", value=str(player_data['matchesPlayed']), inline=True)

    #     embed.set_footer(text=f"Atualizado em: {formatted_date}")

    #     await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(PlayerCog(bot))
    logger.debug("AdminCog loaded successfully.")
