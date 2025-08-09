import discord
from src.models.player import Player


class PlayersButtonsView(discord.ui.View):
    """View for player buttons in the match context."""

    def __init__(self, available_players: list[Player], timeout=180):
        super().__init__(timeout=timeout)
        self.available_players = available_players
        self.first_captain: Player | None = None
        self.second_captain: Player | None = None
