import logging
from src.api.api_client import fetch_api

logger = logging.getLogger("lavava.services.map_service")


async def get_map(name: str) -> dict:
    """Fetch map details by name."""
    logger.info("Fetching map details for: %s", name)
    
    try:
        map_data = await fetch_api(f"/maps/{name}")
        logger.info("Successfully retrieved map data for %s", name)
        return map_data
    except Exception as e:
        logger.error("Failed to fetch map %s: %s", name, str(e))
        raise
