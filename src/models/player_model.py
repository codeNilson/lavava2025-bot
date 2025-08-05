class Player:
    def __init__(self, username: str, discordId: str, *args, **kwargs):
        self.username = username
        self.discord_id = discordId

    def __repr__(self):
        return f"PlayerModel(username={self.username}, discord_id={self.discord_id})"
