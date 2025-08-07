from typing import Optional

class Player:
    def __init__(
        self,
        username: str,
        *args,
        discordId: Optional[int] = None,
        **kwargs,
    ) -> None:
        self.username = username
        self.discord_id = discordId

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"PlayerModel(username={self.username}, discord_id={self.discord_id})"
