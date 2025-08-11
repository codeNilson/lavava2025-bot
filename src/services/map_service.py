from src.api.api_client import fetch_api


async def get_map(name: str) -> dict:
    """Fetch map details by name."""
    map_data = await fetch_api(f"/maps/{name}")
    return map_data
