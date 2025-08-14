from dataclasses import dataclass, field
from typing import Optional, List, Any


@dataclass
class MapInfo:
    id: str
    name: str
    splashUrl: Optional[str] = None


@dataclass
class MatchResponse:
    id: str
    winner: Optional[Any] = None
    loser: Optional[Any] = None
    map: Optional[MapInfo] = None
    playerPerformances: List[Any] = field(default_factory=list)
    mvp: Optional[Any] = None
    ace: Optional[Any] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "MatchResponse":
        if data is None:
            raise ValueError("No data to build MatchResponse")

        map_data = data.get("map")
        map_info = MapInfo(**map_data) if map_data else None
        match_id = data.get("id")
        if match_id is None:
            raise ValueError("Match response missing 'id' field")

        return cls(
            id=str(match_id),
            winner=data.get("winner"),
            loser=data.get("loser"),
            map=map_info,
            playerPerformances=data.get("playerPerformances", []),
            mvp=data.get("mvp"),
            ace=data.get("ace"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
        )
