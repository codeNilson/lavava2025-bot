from dataclasses import dataclass
import logging
from typing import List, Dict, Any, Optional

from src.api import fetch_api

RANKING_ENDPOINT = "rankings"

logger = logging.getLogger("lavava.services.ranking_service")


@dataclass
class LeaderboardEntry:
    id: str
    playerId: str
    playerUsername: str
    totalPoints: int
    matchesWon: int
    matchesPlayed: int
    winRate: float
    season: str
    position: int
    lastUpdated: str
    createdAt: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LeaderboardEntry":
        return cls(
            id=data["id"],
            playerId=data["playerId"],
            playerUsername=data["playerUsername"],
            totalPoints=data["totalPoints"],
            matchesWon=data["matchesWon"],
            matchesPlayed=data["matchesPlayed"],
            winRate=data["winRate"],
            season=data["season"],
            position=data["position"],
            lastUpdated=data["lastUpdated"],
            createdAt=data["createdAt"],
        )


@dataclass
class LeaderboardResponse:
    content: List[LeaderboardEntry]
    totalElements: int
    totalPages: int
    size: int
    number: int
    first: bool
    last: bool
    numberOfElements: int
    empty: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LeaderboardResponse":
        entries = [LeaderboardEntry.from_dict(entry) for entry in data["content"]]
        return cls(
            content=entries,
            totalElements=data["totalElements"],
            totalPages=data["totalPages"],
            size=data["size"],
            number=data["number"],
            first=data["first"],
            last=data["last"],
            numberOfElements=data["numberOfElements"],
            empty=data["empty"],
        )


async def get_leaderboard(page: int = 0, size: int = 100) -> LeaderboardResponse:
    """Get leaderboard from API with proper typing."""

    logger.info("Fetching leaderboard (page=%d, size=%d)", page, size)

    response_data = await fetch_api(
        f"{RANKING_ENDPOINT}/leaderboard",
        method="GET",
        params={
            "sort": ["totalPoints"],
            "page": page,
            "size": size,
        },
    )

    if not response_data or "content" not in response_data:
        logger.warning("Received empty or invalid leaderboard data")
        return LeaderboardResponse(
            content=[],
            totalElements=0,
            totalPages=0,
            size=size,
            number=page,
            first=True,
            last=True,
            numberOfElements=0,
            empty=True,
        )

    logger.info(
        "Successfully retrieved %d leaderboard entries", len(response_data["content"])
    )

    return LeaderboardResponse.from_dict(response_data)
