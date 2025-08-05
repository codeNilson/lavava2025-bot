import discord
from src.models.player_model import Player


class ConfirmParticipationView(discord.ui.View):
    """View to confirm participation in a match."""

    def __init__(self, players: list[Player]):
        super().__init__(timeout=30)
        self.players = players

    @discord.ui.button(label="Bora jogar!", style=discord.ButtonStyle.green, emoji="🔥")
    async def confirm_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Handle the confirmation button click."""
        print("Confirmado!!")
        return

    @discord.ui.button(label="Dessa vez não", style=discord.ButtonStyle.red, emoji="😴")
    async def cancel_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Handle the confirmation button click."""
        print("Não confirmado!!")
        return
