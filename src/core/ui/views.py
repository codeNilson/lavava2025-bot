import discord
from discord.ext import commands
from src.models.player_model import Player
from ..cogs.match import MatchCog


class ConfirmParticipationView(discord.ui.View):
    """View to confirm participation in a match."""

    def __init__(self, players: list[Player], cog: MatchCog):
        super().__init__(timeout=30)
        self.players = players
        self.cog = cog

    @discord.ui.button(label="Bora jogar!", style=discord.ButtonStyle.green, emoji="🔥")
    async def confirm_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Handle the confirmation button click."""

        available_players = self.cog.available_players or []

        user_exists = discord.utils.find(
            lambda p: p.discord_id == interaction.user.id, available_players
        )

        if not user_exists:
            await interaction.response.send_message(
                "Você não está na lista de jogadores disponíveis.",
                ephemeral=True,
            )
            return

        self.cog.confirmed_players.append(user_exists)

        return

    @discord.ui.button(label="Dessa vez não", style=discord.ButtonStyle.red, emoji="😴")
    async def cancel_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Handle the confirmation button click."""
        print("Não confirmado!!")
        return
