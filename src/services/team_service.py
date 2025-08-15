import logging
from typing import List

from src.models.player_model import Player
from src.api import fetch_api

TEAMS_ENDPOINT = "teams"

logger = logging.getLogger("lavava.services.team_service")


async def create_team(match_id: str, players: List[Player]):
    """Create a team for a specific match with the provided players."""
    
    logger.info("Creating team for match %s with %d players", match_id, len(players))
    
    # Extract player IDs and log them for debugging
    players_id_list = [player.id for player in players]
    logger.debug("Players being added to team: %s", players_id_list)

    try:
        response = await fetch_api(
            TEAMS_ENDPOINT,
            method="POST",
            data={
                "matchId": match_id,
                "playersIds": players_id_list,
            },
        )
        
        logger.info("Team created successfully for match %s", match_id)
        return response
        
    except Exception as e:
        logger.error("Failed to create team for match %s: %s", match_id, str(e))
        raise
