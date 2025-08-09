import logging
import asyncio
import discord

from ..api import fetch_api
from ..error.api_errors import ResourceAlreadyExistsError

PLAYERS_ENDPOINT = "players"

logger = logging.getLogger("lavava.services.player_service")


async def get_all_players():
    players_data = await fetch_api(
        PLAYERS_ENDPOINT,
    )
    return players_data


async def register_new_player(player: discord.Member):

    if "Jogador" in [role.name for role in player.roles]:
        raise ResourceAlreadyExistsError(f"Player {player.name} is already registered.")

    await fetch_api(
        PLAYERS_ENDPOINT,
        method="POST",
        data={
            "username": player.name,
            "discordId": player.id,
        },
    )

    jogador_role = discord.utils.get(player.guild.roles, name="Jogador")
    if jogador_role is None:
        logger.error('"Jogador" role not found in guild %s', player.guild.name)
        raise ValueError('"Jogador" role not found in this guild.')
    await player.add_roles(
        jogador_role,
        reason="Player registered via bot command",
    )


async def deactivate_player(player: discord.Member, reason: str):
    await fetch_api(
        f"{PLAYERS_ENDPOINT}/{player.id}/deactivate",
        method="DELETE",
        data={
            "reason": reason,
        },
    )


if __name__ == "__main__":
    response = asyncio.run(get_all_players())
    print(response)
