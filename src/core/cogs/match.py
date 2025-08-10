import logging
import random
import discord
from discord import app_commands
from discord.ext import commands

from src.core.ui.views.select_maps_view import SelectMapView
from src.models.match_model import Match
from src.models.player_model import Player
from src.core.ui.embeds import (
    captains_choose,
    choose_captains_embed,
    list_players_embed,
)
from src.core.ui.views import ConfirmParticipationView
from src.core.ui.views.players_buttons_view import PlayersButtonsView
from src.services.player_service import get_all_players

logger = logging.getLogger("lavava.cog.match")


class MatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_match = Match()

    @app_commands.command(
        name="confirmar-participantes",
        description="Confirmar jogadores para a partida.",
    )
    @app_commands.default_permissions(administrator=True)
    async def confirm_players(self, interaction: discord.Interaction) -> None:
        self.current_match.confirmed_players.clear()

        players_loaded: bool = await self._load_all_players(interaction)
        if not players_loaded:
            return

        confirmation_view = ConfirmParticipationView(
            self.current_match.available_players, cog=self
        )

        await interaction.response.send_message(
            embed=list_players_embed(self.current_match.available_players),
            view=confirmation_view,
        )

        message: discord.InteractionMessage = await interaction.original_response()
        confirmation_view.message = message

        timed_out = await confirmation_view.wait()
        if timed_out:
            return

        await interaction.followup.send(
            "A partida foi iniciada com os jogadores confirmados."
        )

    async def _load_all_players(self, interaction: discord.Interaction) -> bool:
        """Load all players from the database."""
        players_data = await get_all_players()

        if len(players_data) < 10:
            await interaction.response.send_message(
                "Não há jogadores suficientes para iniciar uma partida.",
                delete_after=10,
            )
            return False

        self.current_match.available_players = [
            Player(**player) for player in players_data
        ]
        return True

    match_making = app_commands.Group(
        name="escolher",
        description="Comandos para escolher capitães e jogadores.",
        guild_only=True,
        default_permissions=discord.Permissions(administrator=True),
    )

    @match_making.command(
        name="capitães",
        description="Sortear capitães para a partida.",
    )
    async def choose_captains(self, interaction: discord.Interaction):
        if len(self.current_match.confirmed_players) < 2:
            await interaction.response.send_message(
                "É necessário pelo menos 2 jogadores confirmados para sortear capitães.",
                ephemeral=True,
            )
            return

        (self.current_match.first_captain, self.current_match.second_captain) = (
            random.sample(self.current_match.confirmed_players, 2)
        )

        await interaction.response.send_message(
            embed=captains_choose(
                self.current_match.first_captain,
                self.current_match.second_captain,
            ),
        )

    @match_making.command(
        name="jogadores",
        description="iniciar a escolha de jogadores para a partida.",
    )
    async def choose_players(self, interaction: discord.Interaction) -> None:
        """List available players for the match."""
        self.current_match.setup_team_selection()

        if (
            not self.current_match.first_captain
            or not self.current_match.second_captain
        ):
            await interaction.response.send_message(
                "Nenhum capitão foi escolhido ainda.", ephemeral=True
            )
            return

        view = PlayersButtonsView(self)

        for player in self.current_match.available_players:
            await view.add_player_button(player)

        await interaction.response.send_message(
            embed=choose_captains_embed(
                self.current_match.first_captain_team,
                self.current_match.second_captain_team,
            ),
            view=view,
        )

        message: discord.InteractionMessage = await interaction.original_response()
        view.message = message

        timed_out: bool = await view.wait()
        if timed_out:
            await interaction.followup.send(
                "O tempo para escolher os jogadores acabou."
            )

        await interaction.followup.send(
            "As equipes foram formadas. Hora de escolherem o bans de mapa!",
        )

    @match_making.command(
        name="mapas",
        description="iniciar a escolha de jogadores para a partida.",
    )
    async def choose_maps(self, interaction: discord.Interaction) -> None:

        view = SelectMapView(self)

        await interaction.response.send_message(
            view=view,
        )

        view.message = await interaction.original_response()

        timed_out: bool = await view.wait()

        if timed_out:
            await interaction.followup.send("O tempo para escolher os mapas acabou.")
            return


async def setup(bot: commands.Bot):
    """Load the MatchCog."""
    await bot.add_cog(MatchCog(bot))
    logger.debug("MatchCog loaded successfully.")
