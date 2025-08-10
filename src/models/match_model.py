from dataclasses import dataclass, field
from typing import Optional
from src.models.player_model import Player


@dataclass
class Match:
    available_players: list[Player] = field(default_factory=list)
    confirmed_players: list[Player] = field(default_factory=list)
    denied_players: list[Player] = field(default_factory=list)

    first_captain: Optional[Player] = None
    first_captain_team: list[Player] = field(default_factory=list)

    second_captain: Optional[Player] = None
    second_captain_team: list[Player] = field(default_factory=list)

    is_first_captain_turn: bool = True

    def setup_team_selection(self):
        """Prepare team selection by clearing teams and adding captains."""
        self.first_captain_team.clear()
        self.second_captain_team.clear()

        if self.first_captain and self.second_captain:
            self.first_captain_team.append(self.first_captain)
            self.second_captain_team.append(self.second_captain)

    def reset(self):
        """Reset all match data."""
        self.available_players.clear()
        self.confirmed_players.clear()
        self.denied_players.clear()
        self.first_captain = None
        self.first_captain_team.clear()
        self.second_captain = None
        self.second_captain_team.clear()
        self.is_first_captain_turn = True
