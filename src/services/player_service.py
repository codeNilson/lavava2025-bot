import logging
import discord

from src.error.api_errors import ResourceAlreadyExistsError
from src.api import fetch_api

PLAYERS_ENDPOINT = "players"

logger = logging.getLogger("lavava.services.player_service")


# === Utility Functions ===

def _get_jogador_role(guild: discord.Guild) -> discord.Role:
    """Get the 'Jogador' role from the guild."""
    jogador_role = discord.utils.get(guild.roles, name="Jogador")
    if jogador_role is None:
        logger.error('"Jogador" role not found in guild %s', guild.name)
        raise ValueError('"Jogador" role not found in this guild.')
    return jogador_role


async def _ensure_player_has_role(player: discord.Member, reason: str) -> None:
    """Ensure player has the 'Jogador' role."""
    jogador_role = _get_jogador_role(player.guild)
    
    if jogador_role not in player.roles:
        await player.add_roles(jogador_role, reason=reason)
        logger.info("Player %s assigned 'Jogador' role", player.name)
    else:
        logger.debug("Player %s already has 'Jogador' role", player.name)


async def _remove_player_role(player: discord.Member, reason: str) -> None:
    """Remove the 'Jogador' role from player."""
    jogador_role = _get_jogador_role(player.guild)
    
    if jogador_role in player.roles:
        await player.remove_roles(jogador_role, reason=reason)
        logger.info("Player %s 'Jogador' role removed", player.name)
    else:
        logger.debug("Player %s doesn't have 'Jogador' role", player.name)


# === API Functions ===

async def _register_player_api(player: discord.Member) -> None:
    """Register player in the API."""
    await fetch_api(
        PLAYERS_ENDPOINT,
        method="POST",
        data={
            "username": player.name,
            "discordId": player.id,
        },
    )


async def _deactivate_player_api(username: str) -> None:
    """Deactivate player in the API."""
    await fetch_api(
        f"{PLAYERS_ENDPOINT}/username/{username}",
        method="DELETE",
    )


async def _activate_player_api(username: str) -> None:
    """Activate player in the API."""
    await fetch_api(
        f"{PLAYERS_ENDPOINT}/username/{username}/activate",
        method="PATCH",
    )


# === Public Functions ===

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

    try:
        # Try to register player in API
        await _register_player_api(player)
        logger.info("Player %s registered successfully in API", player.name)
        
        # Ensure player has the role
        await _ensure_player_has_role(
            player, 
            "Player registered via bot command"
        )

    except ResourceAlreadyExistsError:
        logger.warning(
            "Player %s (ID: %s) already exists in the system.",
            player.name,
            player.id,
        )
        
        # Player already exists - try to reactivate in case they're deactivated
        try:
            await _activate_player_api(player.name)
            logger.info("Player %s was deactivated and has been reactivated", player.name)
            
            # Ensure player has the role after reactivation
            await _ensure_player_has_role(
                player,
                "Player reactivated via registration attempt"
            )
            
        except (ResourceAlreadyExistsError, RuntimeError) as reactivate_error:
            logger.debug(
                "Could not reactivate player %s (they might be already active): %s",
                player.name,
                str(reactivate_error)
            )
            
            # Even if reactivation fails, ensure they have the role
            await _ensure_player_has_role(
                player,
                "Player already exists, ensuring role is assigned"
            )
        
        # Always raise the original error for upstream handling
        raise


async def deactivate_player(player: discord.Member, reason: str):
    """Deactivate a player from the system."""
    logger.info(
        "Deactivating player: %s (ID: %s) - Reason: %s", 
        player.name, player.id, reason
    )

    try:
        # Remove role first
        await _remove_player_role(player, "Player deactivated via bot command")
        
        # Then deactivate in API
        await _deactivate_player_api(player.name)
        logger.info("Player %s deactivated successfully", player.name)

    except Exception as e:
        logger.error("Failed to deactivate player %s: %s", player.name, str(e))
        raise


async def active_player(player: discord.Member):
    """Activate a player in the system."""
    logger.info("Activating player: %s (ID: %s)", player.name, player.id)

    try:
        # Activate in API first
        await _activate_player_api(player.name)
        logger.info("Player %s activated successfully in API", player.name)
        
        # Then ensure they have the role
        await _ensure_player_has_role(
            player,
            "Player activated via bot command"
        )

    except Exception as e:
        logger.error("Failed to activate player %s: %s", player.name, str(e))
        raise
