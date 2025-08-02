import logging
import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(f"lavava.cog.{__name__}")


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @app_commands.command(name="teste", description="Comando de teste básico")
    async def teste(self, interaction: discord.Interaction):
        """Comando slash básico para teste."""
        await interaction.response.send_message("🎉 Slash command funcionando!")

    @commands.command(name="shutdown")
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx: commands.Context):
        """Comando para desligar o bot."""
        await ctx.send("Lavava Bot será desligado.")
        await self.bot.close()


async def setup(bot: commands.Bot):
    """Load the AdminCog."""
    await bot.add_cog(AdminCog(bot))
    logger.info("AdminCog loaded successfully.")
