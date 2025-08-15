import logging

from src.models.match_model import Match
from src.api import fetch_api
from src.models.match_response_model import MatchResponse

MATCH_ENDPOINT = "matches"

logger = logging.getLogger("lavava.services.match_service")


async def create_match(data: Match) -> MatchResponse:
    """Create a match in the API and return a typed MatchResponse."""

    logger.info("Creating match with map: %s", data.selected_map)

    if not data.selected_map:
        logger.error("Attempted to create match without selected map")
        raise ValueError("Selected map must be provided to create a match.")

    try:
        response = await fetch_api(
            MATCH_ENDPOINT,
            method="POST",
            data={
                "mapName": data.selected_map,
            },
        )

        match_info: MatchResponse = MatchResponse.from_dict(response)  # type: ignore
        logger.info("Match created successfully with ID: %s", match_info.id)
        return match_info

    except Exception as e:
        logger.error(
            "Failed to create match with map %s: %s", data.selected_map, str(e)
        )
        raise
