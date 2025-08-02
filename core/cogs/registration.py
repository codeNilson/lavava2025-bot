import logging
import discord
from discord.ext import commands
from discord.ext.commands import Bot

logger = logging.getLogger("lavava.cog.registration")


class RegistrationCog(commands.Cog):
    """Cog for handling user registration."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle new member registration."""
        logger.info("New member joined: %s (ID: %s)", member.name, member.id)
        await member.send("Welcome to the server! Please register by following the instructions.")


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(RegistrationCog(bot))
    logger.debug("AdminCog loaded successfully.")
