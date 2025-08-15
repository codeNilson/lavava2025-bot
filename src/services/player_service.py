import logging
import discord

from src.error.api_errors import ResourceAlreadyExistsError
from src.api import fetch_api

PLAYERS_ENDPOINT = "players"

logger = logging.getLogger("lavava.services.player_service")


async def get_all_players():
    """Fetch all players from the API."""
    logger.info("Fetching all players from API")

    try:
        players_data = await fetch_api(PLAYERS_ENDPOINT)
        logger.info("Successfully retrieved %d players", len(players_data))  # type: ignore
        return players_data
    except Exception as e:
        logger.error("Failed to fetch players: %s", str(e))
        raise


async def register_new_player(player: discord.Member):
    """Register a new player in the system."""
    logger.info("Registering new player: %s (ID: %s)", player.name, player.id)

    # Get the Jogador role first
    jogador_role = discord.utils.get(player.guild.roles, name="Jogador")
    if jogador_role is None:
        logger.error('"Jogador" role not found in guild %s', player.guild.name)
        raise ValueError('"Jogador" role not found in this guild.')

    player_has_role = jogador_role in player.roles

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

        # Player not registered + doesn't have role = add role
        if not player_has_role:
            await player.add_roles(
                jogador_role,
                reason="Player registered via bot command",
            )
            logger.info("Player %s assigned 'Jogador' role successfully", player.name)

    except ResourceAlreadyExistsError:
        logger.warning(
            "Player %s (ID: %s) already exists in the system.",
            player.name,
            player.id,
        )

        # Player already registered but doesn't have role = add role
        if not player_has_role:
            await player.add_roles(
                jogador_role,
                reason="Player already exists, ensuring role is assigned",
            )
            logger.info("Existing player %s assigned 'Jogador' role", player.name)


async def deactivate_player(player: discord.Member, reason: str):
    """Deactivate a player from the system."""
    logger.info(
        "Deactivating player: %s (ID: %s) - Reason: %s", player.name, player.id, reason
    )

    try:
        await fetch_api(
            f"{PLAYERS_ENDPOINT}/username/{player.name}",
            method="DELETE",
        )

        logger.info("Player %s deactivated successfully", player.name)

    except Exception as e:
        logger.error("Failed to deactivate player %s: %s", player.name, str(e))
        raise
