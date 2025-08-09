import logging
import random
import discord
from discord import app_commands
from discord.ext import commands
from src.core.cogs import admin
from src.core.ui.embeds import captains_choose, list_players_embed
from src.core.ui.views import ConfirmParticipationView
from src.services.player_service import get_all_players

from src.models.player_model import Player

logger = logging.getLogger("lavava.cog.match")


class MatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.available_players: list[Player] = []
        self.confirmed_players: list[Player] = []
        self.denied_players: list[Player] = []

        self.first_captain: Player | None = None
        self.second_captain: Player | None = None

    @app_commands.command(
        name="confirmar_participantes",
        description="Escolher capitães para a partida.",
    )
    async def confirm_players(
        self,
        interaction: discord.Interaction,
    ) -> None:

        self.confirmed_players.clear()

        players_loaded: bool = await self._load_all_players(interaction)
        if not players_loaded or not self.available_players:
            return

        confirmation_view = ConfirmParticipationView(self.available_players, cog=self)

        await interaction.response.send_message(
            embed=list_players_embed(self.available_players),  # type: ignore
            view=confirmation_view,  # type: ignore
        )

        message = await interaction.original_response()

        confirmation_view.message = message

        timed_out = await confirmation_view.wait()

        if timed_out:
            return

        await interaction.followup.send(
            "A partida foi iniciada com os jogadores confirmados."
        )

    async def _load_all_players(
        self,
        interaction: discord.Interaction,
    ) -> bool:
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

    @app_commands.command(
        name="sortear-capitães",
        description="Sortear capitães para a partida.",
    )
    @app_commands.default_permissions(administrator=True)
    async def choose_captains(self, interaction: discord.Interaction):
        if len(self.available_players) < 2:
            await interaction.response.send_message(
                "É necessário pelo menos 2 jogadores confirmados para sortear capitães.",
                ephemeral=True,
            )
            return
        self.first_captain, self.second_captain = random.sample(
            self.available_players, 2
        )

        await interaction.response.send_message(
            embed=captains_choose(
                self.first_captain,
                self.second_captain,
            ),
        )


async def setup(bot: commands.Bot):
    """Load the MatchCog."""
    await bot.add_cog(MatchCog(bot))
    logger.debug("MatchCog loaded successfully.")
