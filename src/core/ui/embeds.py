import math
import discord
from src.models.player_model import Player


def list_players_embed(players: list[Player]) -> discord.Embed:
    """Create an embed listing all players."""
    embed = discord.Embed(title="Confirmar participação", color=discord.Color.blue())
    embed.description = "🎮 **Confirmação de Participação**\n\nVerifique se seu nome está na lista. Os jogadores listados podem participar da próxima partida.\n\n✅ **Confirme sua participação** se deseja jogar!"

    for i in range(math.ceil(len(players) / 5)):
        column = ""

        for player in players[i * 5 : (i + 1) * 5]:
            column += f"• {player.username}\n"
        embed.add_field(name="", value=column, inline=True)
    return embed
