import logging
import discord
from discord.ext import commands
from discord.ext.commands import Bot

logger = logging.getLogger("lavava.cog.funny")


class FunnyCog(commands.Cog):
    """Cog for funny commands."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.reactions = {
            "natan": "🐂",
            "nathan": "🐂",
            "eric": "💩",
            "leo": "🥇",
            "leozin": "🥇",
            "catherine": "👩🏻‍🦯",
            "cath": "👩🏻‍🦯",
            "cat": "👩🏻‍🦯",
            "pain": "🥈",
            "douglas": "🥈",
            "shaqueda": "🥉",
            "klaus": "🥈",
            "klauz": "🥈",
            "klauzemberg": "🥈",
        }

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        content_lower = message.content.lower()
        for keyword, reaction in self.reactions.items():
            if keyword in content_lower:
                await message.add_reaction(reaction)
                break


async def setup(bot: commands.Bot):
    """Load the FunnyCog."""
    await bot.add_cog(FunnyCog(bot))
    logger.debug("FunnyCog loaded successfully.")
