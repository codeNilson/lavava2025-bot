import asyncio
from api import fetch_api

PLAYERS_ENDPOINT = "players"


async def get_all_players():
    players_data = await fetch_api(
        PLAYERS_ENDPOINT,
    )
    return players_data


if __name__ == "__main__":
    response = asyncio.run(get_all_players())
    print(response)
