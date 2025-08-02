import os
from dotenv import load_dotenv


load_dotenv()


def get_variable(variable: str, fallback: str | None = None) -> str:
    response = os.environ.get(variable, fallback)
    if not response:
        raise RuntimeError(f"Variável {variable} não configurada no arquivo .env!")
    return response
