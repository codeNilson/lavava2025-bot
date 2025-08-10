import logging
from typing import Optional, TYPE_CHECKING
import discord
from discord.utils import find
from src.models.player_model import Player
from ..embeds import list_players_embed

if TYPE_CHECKING:
    from src.core.cogs.match import MatchCog


logger = logging.getLogger("lavava.ui.views.ConfirmParticipationView")


class ConfirmParticipationView(discord.ui.View):
    """View to confirm participation in a match."""

    def __init__(self, players: list[Player], cog: "MatchCog") -> None:
        super().__init__(timeout=120)  # 2 minutes timeout
        self.players: list[Player] = players
        self.cog: "MatchCog" = cog
        self.available_players: list[Player] = (
            self.cog.current_match.available_players or []
        )
        self.message: Optional[discord.Message] = None

    def _find_player_in_available(self, user_id: int) -> Optional[Player]:
        """Find a player in the available players list by user ID."""
        return find(lambda p: p.discord_id == user_id, self.available_players)

    def _user_has_confirmed(self, user_id: int) -> bool:
        """Check if a user has already confirmed participation."""
        return any(
            p.discord_id == user_id for p in self.cog.current_match.confirmed_players
        )

    @discord.ui.button(
        label="Bora jogar!",
        style=discord.ButtonStyle.success,
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
        self.cog.current_match.confirmed_players = [
            p
            for p in self.cog.current_match.confirmed_players
            if p.discord_id != user_id
        ]
        self.cog.current_match.denied_players = [
            p for p in self.cog.current_match.denied_players if p.discord_id != user_id
        ]

        # Adiciona à lista de confirmados
        self.cog.current_match.confirmed_players.append(user_player)

        updated_embed = list_players_embed(
            self.available_players,
            self.cog.current_match.confirmed_players,
            self.cog.current_match.denied_players,
        )

        await interaction.response.edit_message(embed=updated_embed, view=self)

    @discord.ui.button(
        label="Dessa vez não",
        style=discord.ButtonStyle.red,
        emoji="🏳️",
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
        self.cog.current_match.confirmed_players = [
            p
            for p in self.cog.current_match.confirmed_players
            if p.discord_id != user_id
        ]
        self.cog.current_match.denied_players = [
            p for p in self.cog.current_match.denied_players if p.discord_id != user_id
        ]

        # Adiciona à lista de negados
        self.cog.current_match.denied_players.append(user_player)

        updated_embed = list_players_embed(
            self.available_players,
            self.cog.current_match.confirmed_players,
            self.cog.current_match.denied_players,
        )

        await interaction.response.edit_message(embed=updated_embed, view=self)

    @discord.ui.button(
        label="⚡️ Iniciar Partida",
        style=discord.ButtonStyle.secondary,
    )
    async def start_button(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        """Handle the start match button click."""

        # Cast para Member
        member = interaction.user
        assert isinstance(member, discord.Member)

        if not member.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Somente um adm pode iniciar a partida.",
                ephemeral=True,
                delete_after=5,
            )
            return

        await interaction.response.send_message(
            "🚀 Partida iniciada! Preparando os times...",
            ephemeral=True,
        )

        self.stop()

    async def on_timeout(self) -> None:
        """Remove view when timeout occurs."""
        if not self.message:
            return

        timeout_embed = discord.Embed(
            title="⏰ Tempo Esgotado",
            description="O tempo para confirmar participação expirou.",
            color=discord.Color.orange(),
        )
        await self.message.edit(embed=timeout_embed, view=None)
