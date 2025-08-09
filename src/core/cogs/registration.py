import logging
from typing import Union
import discord
from discord.ext import commands
from discord.ext.commands import Bot

from ...services.player_service import register_new_player

logger = logging.getLogger(f"lavava.cog.{__name__}")


class RegistrationCog(commands.Cog):
    """Cog for handling user registration."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle new member registration."""
        logger.info("New member joined: %s (ID: %s)", member.name, member.id)
        await register_new_player(member)

    @commands.Cog.listener()
    async def on_member_ban(
        self, _: discord.Guild, member: Union[discord.Member, discord.User]
    ):
        """Handle member ban."""
        if isinstance(member, discord.Member):
            ban_entry = await member.guild.fetch_ban(member)
            ban_reason = ban_entry.reason if ban_entry.reason else "No reason provided"
            print(f"{member.name} was banned. Reason: {ban_reason}")


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(RegistrationCog(bot))
    logger.debug("AdminCog loaded successfully.")
