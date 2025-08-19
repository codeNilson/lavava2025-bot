import logging
import random
import discord
from discord import app_commands
from discord.ext import commands

from src.services.ranking_service import LeaderboardResponse
from src.models.match_response_model import MatchResponse
from src.models.match_model import Match
from src.models.player_model import Player
from src.services.ranking_service import get_leaderboard
from src.services.team_service import create_team
from src.services.match_service import create_match
from src.services.player_service import get_all_players
from src.core.ui.views.select_maps_view import SelectMapView
from src.core.ui.embeds import (
    build_captains_selected_embed,
    build_team_selection_embed,
    build_player_confirmation_embed,
    build_match_result_embed,
    build_ranking_embed,
)
from src.core.ui.views import ConfirmParticipationView
from src.core.ui.views.players_buttons_view import PlayersButtonsView

logger = logging.getLogger("lavava.cog.match")


class MatchCog(commands.Cog):
    """
    Fluxo:
    /arena check-in → /arena capitães → /arena draft → /arena mapas
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_match = Match()

    # Create a group of commands for the match cog
    match_making = app_commands.Group(
        name="arena",
        description="Comandos para preparação da partida.",
        guild_only=True,
        default_permissions=discord.Permissions(administrator=True),
    )

    @match_making.command(
        name="check-in",
        description="Confirma jogadores que desejam participar da partida.",
    )
    @app_commands.default_permissions(administrator=True)
    async def confirm_players(self, interaction: discord.Interaction) -> None:
        """List all registred players and start the confirmation process"""

        # Clear current match data
        self.current_match.reset_match()

        # Call function to load all players from the database
        players_loaded: bool = await self._load_all_players(interaction)
        if not players_loaded:
            return

        # Create the view for confirmation
        confirmation_view = ConfirmParticipationView(
            self.current_match.available_players, cog=self
        )

        # Respond the interaction with the confirmation embed and the view
        await interaction.response.send_message(
            embed=build_player_confirmation_embed(self.current_match.available_players),
            view=confirmation_view,
        )

        # Get the message that was sent to the user and set it to the view
        # so it can be edited later
        message: discord.InteractionMessage = await interaction.original_response()
        confirmation_view.message = message

        # Wait the interaction to be confirmed or timed out
        timed_out = await confirmation_view.wait()
        if timed_out:
            self.current_match.reset_match()  # reseta estado
            await interaction.followup.send(
                "Tempo para confirmação encerrado. Operação cancelada.",
                ephemeral=True,
            )
            return

        # Send a message to the user with the confirmed players
        await interaction.followup.send(
            "Etapa de confirmação encerrada. Hora de sortear os capitães!"
        )

    async def _load_all_players(self, interaction: discord.Interaction) -> bool:
        """Load all players from the database."""

        # fetch players from backend
        players_data = await get_all_players()

        # check if there are enough players to start a match
        # if not, send a message to the user and return False
        if not players_data or len(players_data) < 10:
            await interaction.response.send_message(
                "Não há jogadores suficientes para iniciar uma partida.",
                ephemeral=True,
                delete_after=10,
            )
            return False

        # set the available players to the players loaded from the database
        self.current_match.available_players = [
            Player(**player) for player in players_data
        ]
        return True

    @match_making.command(
        name="capitães",
        description="Sortea capitães para a partida.",
    )
    async def choose_captains(self, interaction: discord.Interaction):
        if len(self.current_match.confirmed_players) < 2:
            await interaction.response.send_message(
                "É necessário pelo menos 2 jogadores confirmados para sortear capitães.",
                ephemeral=True,
            )
            return

        (
            self.current_match.attacking_captain,
            self.current_match.defending_captain,
        ) = random.sample(self.current_match.confirmed_players, 2)

        await interaction.response.send_message(
            embed=build_captains_selected_embed(
                self.current_match.attacking_captain,
                self.current_match.defending_captain,
            ),
        )

    @match_making.command(
        name="draft",
        description="inicia a escolha de jogadores para a partida.",
    )
    async def choose_players(self, interaction: discord.Interaction) -> None:
        """List available players for the match."""
        self.current_match.initialize_teams()

        if (
            not self.current_match.attacking_captain
            or not self.current_match.defending_captain
        ):
            await interaction.response.send_message(
                "Nenhum capitão foi escolhido ainda.", ephemeral=True
            )
            return

        view = PlayersButtonsView(self)

        for player in self.current_match.available_players:
            await view.add_player_button(player)

        await interaction.response.send_message(
            embed=build_team_selection_embed(
                self.current_match.attacking_team,
                self.current_match.defending_team,
            ),
            view=view,
        )

        message: discord.InteractionMessage = await interaction.original_response()
        view.message = message

        timed_out: bool = await view.wait()
        if timed_out:
            return

        await interaction.followup.send(
            "As equipes foram formadas! Capitães, hora de escolherem os **bans** de mapa!",
        )

    @match_making.command(
        name="mapas",
        description="Inicia o banimento de mapas para a partida.",
    )
    async def choose_maps(self, interaction: discord.Interaction) -> None:

        view = SelectMapView(self)

        await interaction.response.send_message(
            view=view,
        )

        message = await interaction.original_response()

        view.message = message

        timed_out: bool = await view.wait()

        if timed_out:
            return

        await message.edit(
            embed=await build_match_result_embed(self.current_match),
            view=None,
        )

    @match_making.command(
        name="start",
        description="Inicia a partida com as equipes e mapas selecionados.",
    )
    async def start_match(self, interaction: discord.Interaction) -> None:

        if self._teams_not_full() or not self.current_match.selected_map:
            await interaction.response.send_message(
                "As equipes não estão completas ou o mapa não foi selecionado.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(thinking=True)

        match_info: MatchResponse = await create_match(self.current_match)

        await create_team(
            match_info.id,
            self.current_match.attacking_team,
        )

        logger.info("Attacking team created for match %s", match_info.id)

        await create_team(
            match_info.id,
            self.current_match.defending_team,
        )

        logger.info("Defending team created for match %s", match_info.id)

        await interaction.followup.send(
            "Partida iniciada com sucesso! Boa sorte a todos os jogadores!",
        )

    def _teams_not_full(self) -> bool:
        return (
            len(self.current_match.attacking_team) < 5
            or len(self.current_match.defending_team) < 5
        )

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


async def setup(bot: commands.Bot):
    """Load the MatchCog."""
    await bot.add_cog(MatchCog(bot))
    logger.debug("MatchCog loaded successfully.")
