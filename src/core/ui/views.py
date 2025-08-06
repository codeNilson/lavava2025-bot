import logging
from typing import Optional, TYPE_CHECKING
import discord
from discord.utils import find
from src.models.player_model import Player
from .embeds import list_players_embed

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

    @discord.ui.button(
        label="Bora jogar!",
        style=discord.ButtonStyle.green,
        emoji="🔥",
    )
    async def confirm_button(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        """Handle the confirmation button click."""

        user_id = interaction.user.id

        # Encontra o jogador na lista disponível
        user_player = self._find_player_in_available(user_id)
        if not user_player:
            await interaction.response.send_message(
                "❌ Você não está na lista de jogadores disponíveis.",
                ephemeral=True,
            )
            return

        # Remove das listas se já estava em alguma
        self.cog.confirmed_players = [
            p for p in self.cog.confirmed_players if p.discord_id != user_id
        ]
        self.cog.denied_players = [
            p for p in self.cog.denied_players if p.discord_id != user_id
        ]

        # Adiciona à lista de confirmados
        self.cog.confirmed_players.append(user_player)

        # Atualiza o embed
        from .embeds import list_players_embed

        updated_embed = list_players_embed(
            self.available_players, self.cog.confirmed_players, self.cog.denied_players
        )

        await interaction.response.edit_message(embed=updated_embed, view=self)

    @discord.ui.button(
        label="Dessa vez não",
        style=discord.ButtonStyle.secondary,
        emoji="❌",
    )
    async def deny_button(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        """Handle the deny button click."""

        user_id = interaction.user.id

        # Encontra o jogador na lista disponível
        user_player = self._find_player_in_available(user_id)
        if not user_player:
            await interaction.response.send_message(
                "❌ Você não está na lista de jogadores disponíveis.",
                ephemeral=True,
            )
            return

        # Remove das listas se já estava em alguma
        self.cog.confirmed_players = [
            p for p in self.cog.confirmed_players if p.discord_id != user_id
        ]
        self.cog.denied_players = [
            p for p in self.cog.denied_players if p.discord_id != user_id
        ]

        # Adiciona à lista de negados
        self.cog.denied_players.append(user_player)

        updated_embed = list_players_embed(
            self.available_players, self.cog.confirmed_players, self.cog.denied_players
        )

        await interaction.response.edit_message(embed=updated_embed, view=self)

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
