import logging

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


from src.core.ui.embeds import build_ranking_embed
from src.services.ranking_service import LeaderboardResponse
from src.services.ranking_service import get_leaderboard
from src.utils import get_variable

load_dotenv()

logger = logging.getLogger("lavava.cog.ranking")

RANKING_CHANNEL = discord.Object(get_variable("RANKING_CHANNEL_ID"))

if not RANKING_CHANNEL:
    logger.error("RANKING_CHANNEL_ID not found in environment variables.")
    raise ValueError("RANKING_CHANNEL_ID must be set in the environment variables.")


class RankingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ranking",
        description="Mostra o ranking dos jogadores.",
    )
    async def update_ranking(self, interaction: discord.Interaction) -> None:
        # Defer response since API call might take time
        # await interaction.response.defer(thinking=True)

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

            await interaction.response.send_message(
                "Ranking atualizado com sucesso! Confira o canal de ranking.",
                ephemeral=True,
                delete_after=10,
            )

        except RuntimeError as e:
            logger.error("Failed to fetch leaderboard: %s", str(e))
            await interaction.followup.send(
                "Erro ao buscar o ranking. Tente novamente mais tarde.",
                ephemeral=True,
            )

    # listener
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        channel = message.channel

        if (
            not isinstance(channel, discord.TextChannel)
            or channel.id != RANKING_CHANNEL.id
            or message.is_system()
        ):
            return

        await channel.purge(
            limit=100, check=lambda m: m != message and not m.is_system()
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RankingCog(bot))
    logger.debug("MatchCog loaded successfully.")
