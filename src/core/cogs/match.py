from typing import Optional
import logging
import discord
from discord import app_commands
from discord.ext import commands
from src.core.ui.embeds import list_players_embed
from src.core.ui.views import ConfirmParticipationView
from src.services.player_service import get_all_players

from src.models.player_model import Player

logger = logging.getLogger("lavava.cog.match")


class MatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.available_players: Optional[list[Player]] = None
        self.confirmed_players: list[Player] = []

    @app_commands.command(
        name="confirmar_participantes",
        description="Escolher capitães para a partida.",
    )
    async def confirm_players(
        self,
        interaction: discord.Interaction,
    ):

        self.confirmed_players.clear()

        players_loaded = await self._load_all_players(interaction)
        if not players_loaded:
            return

        await interaction.response.send_message(
            embed=list_players_embed(self.available_players),  # type: ignore
            view=ConfirmParticipationView(self.available_players, cog=self),  # type: ignore
        )

    async def _load_all_players(
        self,
        interaction: discord.Interaction,
    ):
        """Load all players from the database."""

        players_data = await get_all_players()

        if len(players_data) < 0 or not players_data:
            await interaction.response.send_message(
                "Não há jogadores suficientes para iniciar uma partida.",
                delete_after=10,
            )
            return False
        self.available_players = [Player(**player) for player in players_data]
        return True


async def setup(bot: commands.Bot):
    """Load the MatchCog."""
    await bot.add_cog(MatchCog(bot))
    logger.debug("MatchCog loaded successfully.")
