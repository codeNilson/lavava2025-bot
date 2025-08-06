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

    try:
        await fetch_api(
            PLAYERS_ENDPOINT,
            method="POST",
            data={
                "username": player.name,
                "discordId": player.id,
            },
        )
    except ResourceAlreadyExistsError:
        logger.debug(
            "Player %s (ID: %s) already exists in the database.",
            player.name,
            player.id,
        )
        return


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
