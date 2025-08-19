import logging

import discord
from discord import app_commands
from discord.ext import commands


from src.core.ui.embeds import build_ranking_embed
from src.services.ranking_service import LeaderboardResponse
from src.services.ranking_service import get_leaderboard

logger = logging.getLogger("lavava.cog.ranking")

RANKING_CHANNEL = discord.Object(1372683950144753767)


class RankingCog(commands.Cog):
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

            ranking_channel = self.bot.get_channel(RANKING_CHANNEL.id)

            if not ranking_channel or not isinstance(
                ranking_channel, discord.TextChannel
            ):
                await interaction.followup.send(
                    "Canal de ranking não encontrado ou não é um canal de texto.",
                    ephemeral=True,
                )
                return

            embed: discord.Embed = build_ranking_embed(leaderboard)

            await ranking_channel.send(
                embed=embed,
                content="@everyone **O ranking foi atualizado!** :trophy: :sparkles:\n"
                "Veja os resultados e lute para subir no pódio! :crossed_swords: :fire:\n\n",
            )

        except RuntimeError as e:
            logger.error("Failed to fetch leaderboard: %s", str(e))
            await interaction.followup.send(
                "Erro ao buscar o ranking. Tente novamente mais tarde.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RankingCog(bot))
    logger.debug("MatchCog loaded successfully.")
