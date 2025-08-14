import logging
from typing import List

from src.models.player_model import Player
from src.api import fetch_api

TEAMS_ENDPOINT = "teams"

logger = logging.getLogger("lavava.services.match_service")


async def create_team(match_id: str, players_ids: List[Player]):
    # Filter out players without a discord_id and log them for debugging
    players_with_ids = [p for p in players_ids if getattr(p, "discord_id", None) is not None]
    missing = [p for p in players_ids if getattr(p, "discord_id", None) is None]

    if missing:
        logger.warning(
            "Some players are missing discord_id for match %s: %s",
            match_id,
            [str(p) for p in missing],
        )

    players_id_list = [player.discord_id for player in players_with_ids]

    await fetch_api(
        TEAMS_ENDPOINT,
        method="POST",
        data={
            "matchId": match_id,
            "playersId": players_id_list,
        },
    )
