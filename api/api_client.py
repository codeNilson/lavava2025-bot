from typing import Optional, Dict, Any, Literal
import aiohttp
from utils import get_variable

BASE_URL = get_variable("API_BASE_URL")
LOGIN = get_variable("LOGIN")
PASSWORD = get_variable("PASSWORD")


async def fetch_api(
    endpoint: str,
    *,
    method: Literal["GET", "POST", "PATCH", "DELETE"] = "GET",
    data: Optional[Dict[str, Any]] = None,
):

    url = BASE_URL + endpoint.replace("/", "")
    auth = aiohttp.BasicAuth(LOGIN, PASSWORD)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method, url=url, json=data, auth=auth
            ) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            raise RuntimeError("Recurso não encontrado") from e
        elif e.status == 401:
            raise RuntimeError("Credenciais inválidas") from e
        raise RuntimeError(f"Erro HTTP {e.status}") from e
    except aiohttp.ClientError as e:
        raise RuntimeError(f"Erro de conexão: {e}") from e
