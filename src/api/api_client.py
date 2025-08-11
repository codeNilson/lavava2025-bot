import logging
from typing import Optional, Dict, Any, Literal
import aiohttp
from ..error import ResourceAlreadyExistsError
from ..utils import get_variable

BASE_URL = get_variable("API_BASE_URL")
LOGIN = get_variable("LOGIN")
PASSWORD = get_variable("PASSWORD")

logger = logging.getLogger("lavava.client")


async def fetch_api(
    endpoint: str,
    *,
    method: Literal["GET", "POST", "PATCH", "DELETE"] = "GET",
    data: Optional[Dict[str, Any]] = None,
):

    url = BASE_URL + endpoint
    url = url.replace("//", "/").replace(":/", "://")
    auth = aiohttp.BasicAuth(LOGIN, PASSWORD)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method, url=url, json=data, auth=auth
            ) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            logger.error(
                "Invalid credentials for API access. Status code: %s. Endpoint: %s",
                e.status,
                url,
            )
        if e.status == 404:
            logger.error(
                "Error while trying to reach API. Status code: %s. Endpoint: %s",
                e.status,
                url,
            )
            raise RuntimeError("Recurso não encontrado") from e
        if e.status == 409:
            raise ResourceAlreadyExistsError("Conflito") from e

        raise RuntimeError(f"Erro HTTP {e.status}") from e
    except aiohttp.ClientError as e:
        logger.error("Connection error: %s", e)
        raise RuntimeError(f"Erro de conexão: {e}") from e
