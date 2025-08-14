import logging

from src.services.team_service import create_team
from src.models.match_model import Match
from src.api import fetch_api
from src.models.match_response_model import MatchResponse

MATCH_ENDPOINT = "matches"

logger = logging.getLogger("lavava.services.match_service")


async def create_match(data: Match) -> MatchResponse:
    """Create a match in the API and return a typed MatchResponse."""

    if not data.selected_map:
        raise ValueError("Selected map must be provided to create a match.")

    response = await fetch_api(
        MATCH_ENDPOINT,
        method="POST",
        data={
            "mapName": data.selected_map,
        },
    )

    logger.info("Match created with response: %s", response)

    match_info: MatchResponse = MatchResponse.from_dict(response)
    return match_info
