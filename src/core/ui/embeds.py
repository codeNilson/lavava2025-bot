from typing import Optional
import math
import discord
from src.models.player_model import Player


def list_players_embed(
    players: list[Player],
    confirmed_players: Optional[list[Player]] = None,
    denied_players: Optional[list[Player]] = None,
) -> discord.Embed:
    """Create an embed listing all players with their confirmation status."""
    embed = discord.Embed(title="Confirmar participação", color=discord.Color.blue())
    embed.description = "🎮 **Confirmação de Participação**\n\nVerifique se seu nome está na lista. Os jogadores listados podem participar da próxima partida.\n\n✅ **Confirme sua participação** se deseja jogar!"

    # Listas para controle de status
    confirmed_players = confirmed_players or []
    denied_players = denied_players or []

    # IDs para comparação
    confirmed_ids = {player.discord_id for player in confirmed_players}
    denied_ids = {player.discord_id for player in denied_players}

    for i in range(math.ceil(len(players) / 5)):
        column = ""

        for player in players[i * 5 : (i + 1) * 5]:
            if player.discord_id in confirmed_ids:
                emoji = "✅"
            elif player.discord_id in denied_ids:
                emoji = "❌"
            else:
                emoji = "⏳"

            column += f"{emoji} {player.username}\n"

        embed.add_field(name="", value=column, inline=True)

    total = len(players)
    confirmed_count = len(confirmed_players)
    denied_count = len(denied_players)
    pending_count = total - confirmed_count - denied_count

    embed.set_footer(
        text=f"✅ {confirmed_count} | ❌ {denied_count} | ⏳ {pending_count} | Total: {total}"
    )

    return embed
