import logging
from typing import List

from src.models.player_model import Player
from src.api import fetch_api

TEAMS_ENDPOINT = "teams"

logger = logging.getLogger("lavava.services.match_service")


async def create_team(match_id: str, players: List[Player]):

    players_id_list = [player.id for player in players]

    await fetch_api(
        TEAMS_ENDPOINT,
        method="POST",
        data={
            "matchId": match_id,
            "playersIds": players_id_list,
        },
    )
