import logging
from typing import Optional, TYPE_CHECKING
import discord
from discord.utils import find
from src.core.ui.embeds import build_player_confirmation_embed
from src.models.player_model import Player

if TYPE_CHECKING:
    from src.core.cogs.match import MatchCog


logger = logging.getLogger("lavava.ui.views.ConfirmParticipationView")


class ConfirmParticipationView(discord.ui.View):
    """View to confirm participation in a match."""

    def __init__(self, cog: "MatchCog") -> None:
        super().__init__(timeout=30)
        self.cog: "MatchCog" = cog
        self.message: Optional[discord.Message] = None

    @property
    def confirmed_players(self) -> list[discord.Member]:
        """Get the list of confirmed players from the current match."""
        return self.cog.current_match.confirmed_players

    @property
    def denied_players(self) -> list[discord.Member]:
        """Get the list of confirmed players from the current match."""
        return self.cog.current_match.denied_players

    def _find_player_in_confirmed(self, user_id: int) -> Optional[discord.Member]:
        """Find a player in the confirmed players list by user ID."""
        return find(lambda p: p.id == user_id, self.confirmed_players)

    def _find_player_in_denied(self, user_id: int) -> Optional[discord.Member]:
        """Find a player in the denied players list by user ID."""
        return find(lambda p: p.id == user_id, self.denied_players)

    @discord.ui.button(
        label="Bora jogar!",
        style=discord.ButtonStyle.success,
        emoji="🔥",
    )
    async def confirm_button(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        """Handle the confirmation button click."""

        member: discord.User | discord.Member = interaction.user
        assert isinstance(member, discord.Member)

        # Previne confirmações duplicadas
        player_already_confirmed = self._find_player_in_confirmed(member.id)
        if player_already_confirmed:
            await interaction.response.send_message(
                "❌ Você já confirmou sua participação!",
                ephemeral=True,
            )
            return

        # Remove o jogador da lista de negados, se presente
        denied_players = self.denied_players
        for p in denied_players:
            if p.id == member.id:
                denied_players.remove(p)
                break

        # Adiciona à lista de confirmados
        self.cog.current_match.confirmed_players.append(member)

        updated_embed: discord.Embed = build_player_confirmation_embed(
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

        member: discord.User | discord.Member = interaction.user
        assert isinstance(member, discord.Member)

        # Encontra o jogador na lista disponível
        player_already_denied = self._find_player_in_denied(member.id)
        if player_already_denied:
            await interaction.response.send_message(
                "❌ Você já recusou sua participação!",
                ephemeral=True,
            )
            return

        # Remove o jogador da lista de confirmados, se presente
        confirmed_players = self.confirmed_players
        for p in confirmed_players:
            if p.id == member.id:
                confirmed_players.remove(p)
                break

        # Adiciona à lista de negados
        self.cog.current_match.denied_players.append(member)

        updated_embed = build_player_confirmation_embed(
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
        member: discord.User | discord.Member = interaction.user
        assert isinstance(member, discord.Member)

        if not member.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Somente um adm pode iniciar a partida.",
                ephemeral=True,
                delete_after=5,
            )
            return

        # TODO: Alterar o requisito para 10 jogadores confirmados
        if len(self.cog.current_match.confirmed_players) < 2:
            await interaction.response.send_message(
                "É necessário pelo menos 2 jogadores confirmados para iniciar a partida.",
                ephemeral=True,
                delete_after=5,
            )
            return

        for button in self.children:
            if isinstance(button, discord.ui.Button):
                button.disabled = True

        # Edit the message that contains this view to persist disabled state
        await interaction.response.edit_message(view=self)

        # Stop the view to prevent further interactions
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
