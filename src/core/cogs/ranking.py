import logging

import discord
from discord.ext import commands

from src.core.ui.embeds import build_ranking_embed
from src.services.ranking_service import LeaderboardResponse
from src.services.ranking_service import get_leaderboard


class RankingCog(command.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ranking",
        description="Mostra o ranking dos jogadores.",
    )
    async def update_ranking(self, interaction: discord.Interaction) -> None:
        # Defer response since API call might take time
        await interaction.response.defer()

        try:
            leaderboard: LeaderboardResponse = await get_leaderboard()
            
            if not leaderboard or not leaderboard.content:
                await interaction.followup.send(
                    "Não foi possível obter o ranking no momento ou não há jogadores ranqueados.",
                    ephemeral=True,
                )
                return

            embed = build_ranking_embed(leaderboard)
            await interaction.followup.send(embed=embed)

        except RuntimeError as e:
            logger.error("Failed to fetch leaderboard: %s", str(e))
            await interaction.followup.send(
                "Erro ao buscar o ranking. Tente novamente mais tarde.",
                ephemeral=True,
            )