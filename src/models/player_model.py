from typing import Optional


class Player:
    def __init__(
        self,
        username: str,
        *args,
        discordId: Optional[int] = None,
        **kwargs,
    ) -> None:
        self.username: str = username
        self.discord_id: Optional[int] = discordId

    def __str__(self) -> str:
        return f"{self.username}"

    def __repr__(self) -> str:
        return f"PlayerModel(username={self.username}, discord_id={self.discord_id})"
