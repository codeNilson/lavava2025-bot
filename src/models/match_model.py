from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID
from src.models.player_model import Player


@dataclass
class Match:

    available_players: list[Player] = field(default_factory=list)
    confirmed_players: list[Player] = field(default_factory=list)
    denied_players: list[Player] = field(default_factory=list)

    # Captains and teams
    attacking_captain: Optional[Player] = None
    attacking_team: list[Player] = field(default_factory=list)

    defending_captain: Optional[Player] = None
    defending_team: list[Player] = field(default_factory=list)

    # Turn state for drafting (custom order supported)
    is_attacking_captain_turn: bool = True

    # Map selected after bans
    selected_map: Optional[str] = None

    def initialize_teams(self) -> None:
        """Clear teams and add captains as initial team members."""
        self.attacking_team.clear()
        self.defending_team.clear()

        if self.attacking_captain and self.defending_captain:
            self.attacking_team.append(self.attacking_captain)
            self.defending_team.append(self.defending_captain)

    def reset_match(self) -> None:
        """Reset all match data to initial state."""
        self.match_id = None
        self.available_players.clear()
        self.confirmed_players.clear()
        self.denied_players.clear()
        self.attacking_captain = None
        self.attacking_team.clear()
        self.defending_captain = None
        self.defending_team.clear()
        self.is_attacking_captain_turn = True
        self.selected_map = None
