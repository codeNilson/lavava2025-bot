import logging
from typing import Optional, TYPE_CHECKING
import discord
from discord.utils import find
from src.models.player_model import Player

if TYPE_CHECKING:
    from src.core.cogs.match import MatchCog


logger = logging.getLogger("lavava.ui.views.ConfirmParticipationView")


class ConfirmParticipationView(discord.ui.View):
    """View to confirm participation in a match."""

    def __init__(self, players: list[Player], cog: "MatchCog") -> None:
        super().__init__(timeout=30)
        self.players: list[Player] = players
        self.cog: "MatchCog" = cog
        self.available_players: list[Player] = self.cog.available_players or []
        self.message: Optional[discord.Message] = None

    def _find_player_in_available(self, user_id: int) -> Optional[Player]:
        """Find a player in the available players list by user ID."""
        return find(lambda p: p.discord_id == user_id, self.available_players)

    def _user_has_confirmed(self, user_id: int) -> bool:
        """Check if a user has already confirmed participation."""
        return any(p.discord_id == user_id for p in self.cog.confirmed_players)

    @discord.ui.button(label="Bora jogar!", style=discord.ButtonStyle.green, emoji="🔥")
    async def confirm_button(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        """Handle the confirmation button click."""

        user_player: Optional[Player] = self._find_player_in_available(
            interaction.user.id
        )

        if user_player and user_player not in self.cog.confirmed_players:
            self.cog.confirmed_players.append(user_player)
            await interaction.response.send_message(
                "Participação confirmada!",
                ephemeral=True,
                delete_after=30,
            )
            logger.debug(
                "User %s (ID: %s) confirmed participation.",
                interaction.user.name,
                interaction.user.id,
            )
        elif user_player and user_player in self.cog.confirmed_players:
            await interaction.response.send_message(
                "Você já confirmou sua participação.",
                ephemeral=True,
                delete_after=5,
            )
        else:
            await interaction.response.send_message(
                "Você não está na lista de jogadores disponíveis.",
                ephemeral=True,
                delete_after=5,
            )

    @discord.ui.button(label="Dessa vez não", style=discord.ButtonStyle.red, emoji="😴")
    async def cancel_button(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        """Handle the confirmation button click."""

        if self._user_has_confirmed(interaction.user.id):
            self.cog.confirmed_players = [
                p
                for p in self.cog.confirmed_players
                if p.discord_id != interaction.user.id
            ]
            await interaction.response.send_message(
                "Participação cancelada.",
                ephemeral=True,
                delete_after=30,
            )
            logger.debug(
                "User %s (ID: %s) canceled participation.",
                interaction.user.name,
                interaction.user.id,
            )

        else:
            await interaction.response.send_message(
                "Você não confirmou sua participação.",
                ephemeral=True,
                delete_after=5,
            )

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True  # type: ignore

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        user_player: Optional[Player] = self._find_player_in_available(
            interaction.user.id
        )

        if not user_player:
            await interaction.response.send_message(
                "Você não está na lista de jogadores disponíveis.",
                ephemeral=True,
                delete_after=5,
            )
            return False

        return True
