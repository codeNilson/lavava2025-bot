from typing import Optional
import math

import discord

from src.models.match_model import Match
from src.services.map_service import get_map
from src.models.player_model import Player


def build_player_confirmation_embed(
    players: list[Player],
    confirmed_players: Optional[list[Player]] = None,
    denied_players: Optional[list[Player]] = None,
) -> discord.Embed:
    """Create an embed listing all players with their confirmation status."""
    embed = discord.Embed(title="🏆 Partida Lavava 2025", color=discord.Color.red())
    embed.description = (
        "⚔️ **Uma nova partida está sendo formada!**\n\n"
        "Todos os jogadores listados abaixo estão **qualificados** para participar. "
        "Use os botões para **confirmar** se você irá jogar ou **recusar** se não puder participar desta vez.\n\n"
        "⏰ **Tempo limite:** 2 minutos para confirmação"
    )

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
        text=f"🎮 {confirmed_count} confirmados • 🚫 {denied_count} recusados • ⏳ {pending_count} aguardando • 👥 {total} total"
    )

    return embed


def build_captains_selected_embed(
    first_captain: Player,
    second_captain: Player,
) -> discord.Embed:
    """Create an embed showing the chosen captains."""
    embed = discord.Embed(
        title="⚔️ Capitães Escolhidos",
        description="Os capitães foram selecionados aleatoriamente para a próxima partida.",
        color=discord.Color.blue(),
    )

    embed.add_field(
        name="Capitão 1",
        value=f"🗡️ {first_captain.mention}",
        inline=True,
    )

    embed.add_field(
        name="",
        value="",
        inline=True,
    )

    embed.add_field(
        name="Capitão 2",
        value=f"🛡️ {second_captain.mention}",
        inline=True,
    )

    embed.set_footer(text="Hora de formar as equipes! Boa sorte aos capitães!")

    return embed


def build_team_selection_embed(
    first_team: list[Player],
    second_team: list[Player],
) -> discord.Embed:
    """Create an embed showing the players to choose."""
    embed = discord.Embed(
        title="⚔️ Escolha dos Jogadores",
        description="Os capitães devem escolher seus jogadores para a partida.",
        color=discord.Color.green(),
    )

    # Time Atacante - Tratar caso vazio
    attacking_value = (
        "\n".join(player.mention for player in first_team)
        if first_team
        else "⏳ *Aguardando seleção...*"
    )
    embed.add_field(
        name="🗡️ Time Atacante",
        value=attacking_value,
        inline=True,
    )

    # Campo vazio para espaçamento
    embed.add_field(name="\u200b", value="\u200b", inline=True)

    # Time Defensor - Tratar caso vazio
    defending_value = (
        "\n".join(player.mention for player in second_team)
        if second_team
        else "⏳ *Aguardando seleção...*"
    )
    embed.add_field(
        name="🛡️ Time Defensor",
        value=defending_value,
        inline=True,
    )

    embed.set_footer(text="💡 Lembrete: o segundo capitão escolhe o 6º e o 7º pick.")

    return embed


async def build_match_result_embed(match: Match) -> discord.Embed:
    """Create an embed showing the match details."""

    if match.selected_map is None:
        return discord.Embed(
            title="⚠️ Erro",
            description="Nenhum mapa foi escolhido para a partida.",
            color=discord.Color.red(),
        )

    try:
        map_data = await get_map(match.selected_map)
        map_name = map_data.get("name", match.selected_map)
        map_image = map_data.get("splashUrl")
    except Exception:
        map_name = match.selected_map
        map_image = None

    embed = discord.Embed(
        title=f"🏆 Partida Lavava 2025 - {map_name}",
        description="Partida formada! Boa sorte!",
        color=discord.Color.green(),
    )

    # Validar times não vazios
    attacking_value = (
        "\n".join(player.mention for player in match.attacking_team)
        if match.attacking_team
        else "*Nenhum jogador*"
    )
    defending_value = (
        "\n".join(player.mention for player in match.defending_team)
        if match.defending_team
        else "*Nenhum jogador*"
    )

    embed.add_field(
        name="🗡️ Time Atacante",
        value=attacking_value,
        inline=True,
    )

    # Campo vazio para espaçamento
    embed.add_field(name="\u200b", value="\u200b", inline=True)

    embed.add_field(
        name="🛡️ Time Defensor",
        value=defending_value,
        inline=True,
    )

    if map_image:
        embed.set_thumbnail(url=map_image)
        embed.set_image(url=map_image)

    embed.set_footer(text=f"🗺️ Mapa: {map_name} • Boa partida a todos!")

    return embed
