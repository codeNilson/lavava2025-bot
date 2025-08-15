import logging
import discord

from src.api import fetch_api

PLAYERS_ENDPOINT = "players"

logger = logging.getLogger("lavava.services.player_service")


async def get_all_players():
    """Fetch all players from the API."""
    logger.info("Fetching all players from API")

    try:
        players_data = await fetch_api(PLAYERS_ENDPOINT)
        logger.info("Successfully retrieved %d players", len(players_data))
        return players_data
    except Exception as e:
        logger.error("Failed to fetch players: %s", str(e))
        raise


async def register_new_player(player: discord.Member):
    """Register a new player in the system."""
    logger.info("Registering new player: %s (ID: %s)", player.name, player.id)

    try:
        await fetch_api(
            PLAYERS_ENDPOINT,
            method="POST",
            data={
                "username": player.name,
                "discordId": player.id,
            },
        )

        logger.info("Player %s registered successfully in API", player.name)

        jogador_role = discord.utils.get(player.guild.roles, name="Jogador")
        if jogador_role is None:
            logger.error('"Jogador" role not found in guild %s', player.guild.name)
            raise ValueError('"Jogador" role not found in this guild.')

        await player.add_roles(
            jogador_role,
            reason="Player registered via bot command",
        )

        logger.info("Player %s assigned 'Jogador' role successfully", player.name)

    except Exception as e:
        logger.error("Failed to register player %s: %s", player.name, str(e))
        raise


async def deactivate_player(player: discord.Member, reason: str):
    """Deactivate a player from the system."""
    logger.info(
        "Deactivating player: %s (ID: %s) - Reason: %s", player.name, player.id, reason
    )

    try:
        await fetch_api(
            f"{PLAYERS_ENDPOINT}/{player.id}/deactivate",
            method="DELETE",
            data={
                "reason": reason,
            },
        )

        logger.info("Player %s deactivated successfully", player.name)

    except Exception as e:
        logger.error("Failed to deactivate player %s: %s", player.name, str(e))
        raise
