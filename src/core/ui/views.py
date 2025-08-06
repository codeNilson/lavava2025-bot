from typing import Optional
import discord
from src.models.player_model import Player
from ..cogs.match import MatchCog


class ConfirmParticipationView(discord.ui.View):
    """View to confirm participation in a match."""

    def __init__(self, players: list[Player], cog: MatchCog) -> None:
        super().__init__(timeout=30)
        self.players: list[Player] = players
        self.cog: MatchCog = cog
        self.available_players: list[Player] = self.cog.available_players or []

    @discord.ui.button(label="Bora jogar!", style=discord.ButtonStyle.green, emoji="🔥")
    async def confirm_button(
        self, interaction: discord.Interaction, _: discord.ui.Button
    ) -> None:
        """Handle the confirmation button click."""

        user_exists: Optional[Player] = discord.utils.find(
            lambda p: p.discord_id == interaction.user.id,
            self.available_players,
        )

        if not user_exists:
            await interaction.response.send_message(
                "Você não está na lista de jogadores disponíveis.",
                ephemeral=True,
                delete_after=30,
            )
            return

        if any(p.discord_id == interaction.user.id for p in self.cog.confirmed_players):
            await interaction.response.send_message(
                "Você já confirmou sua participação.",
                ephemeral=True,
                delete_after=30,
            )
            return

        self.cog.confirmed_players.append(user_exists)

        await interaction.response.send_message(
            "Participação confirmada!",
            ephemeral=True,
            delete_after=30,
        )

        return

    @discord.ui.button(label="Dessa vez não", style=discord.ButtonStyle.red, emoji="😴")
    async def cancel_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        """Handle the confirmation button click."""
        user_confirmed: bool = discord.utils.find(
            lambda p: p.discord_id == interaction.user.id,
            self.cog.confirmed_players,
        )

        if user_confirmed:
            self.cog.confirmed_players.remove(user_confirmed)

            await interaction.response.send_message(
                "Participação cancelada.",
                ephemeral=True,
                delete_after=30,
            )
            return
        await interaction.response.send_message(
            "Você não confirmou sua participação.",
            ephemeral=True,
            delete_after=30,
        )

    @override
    async def on_timeout(self, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
