from typing import Optional
import logging
import discord
from discord import app_commands
from discord.ext import commands
from src.services.player_service import get_all_players

from src.models.player_model import Player

logger = logging.getLogger("lavava.cog.match")


class MatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players: Optional[list[Player]] = None

    @app_commands.command(
        name="load_players",
        description="Load all players from the database.",
    )
    async def load_all_players(self, interaction: discord.Interaction):
        """Load all players from the database."""

        players_data = await get_all_players()
        self.players = [Player(**player) for player in players_data]
        logger.info("Loaded %d players from the database.", len(self.players))
        for player in self.players:
            print(player)


async def setup(bot: commands.Bot):
    """Load the MatchCog."""
    await bot.add_cog(MatchCog(bot))
    logger.debug("MatchCog loaded successfully.")
