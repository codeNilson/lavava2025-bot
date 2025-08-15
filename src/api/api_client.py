import logging
from typing import Optional, Dict, Any, Literal
import aiohttp
from src.error import ResourceNotFound, ResourceAlreadyExistsError
from src.utils import get_variable

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

    logger.debug("Making %s request to %s", method, endpoint)
    if data:
        logger.debug("Request payload: %s", data)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method, url=url, json=data, auth=auth
            ) as response:
                logger.info(
                    "API request successful: %s %s - Status: %d",
                    method,
                    endpoint,
                    response.status,
                )
                response.raise_for_status()

                if response.status == 204 or response.content_length == 0:
                    logger.debug("Response has no content (status %d)", response.status)
                    return

                # Check if response has JSON content
                content_type = response.headers.get("content-type", "")
                if "application/json" not in content_type:
                    logger.warning(
                        "Response is not JSON (content-type: %s)", content_type
                    )
                    return

                return await response.json()

    except aiohttp.ClientResponseError as e:
        logger.error(
            "API request failed: %s %s - Status: %d", method, endpoint, e.status
        )

        if e.status == 401:
            logger.error("Invalid credentials for API access")
            raise RuntimeError("Credenciais inválidas para acesso à API") from e
        elif e.status == 404:
            logger.error("Resource not found: %s", endpoint)
            raise ResourceNotFound("Recurso não encontrado") from e
        elif e.status == 409:
            logger.warning("Resource conflict: %s", endpoint)
            raise ResourceAlreadyExistsError("Conflito") from e
        else:
            logger.error(
                "HTTP error %d: %s",
                e.status,
                e.message if hasattr(e, "message") else "Unknown error",
            )
            raise RuntimeError(f"Erro HTTP {e.status}") from e

    except aiohttp.ClientError as e:
        logger.error("Connection error when accessing %s: %s", endpoint, str(e))
        raise RuntimeError(f"Erro de conexão: {e}") from e
    except Exception as e:
        logger.error("Unexpected error during API request to %s: %s", endpoint, str(e))
        raise
