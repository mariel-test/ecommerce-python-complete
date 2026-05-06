import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from services.api_client import ApiClient
from fixtures.user_factory import make_register_user

load_dotenv()

_API_URL = os.getenv("BASE_URL", "https://automationexercise.com/api")
_USER_FILE = Path(__file__).parent / "user_data.txt"

_CREATE = "createAccount"
_DELETE = "deleteAccount"
_VERIFY = "verifyLogin"


def _read_stored() -> dict | None:
    if not _USER_FILE.exists():
        return None
    data = {}
    for line in _USER_FILE.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data if {"email", "password"} <= data.keys() else None


def _save(email: str, password: str) -> None:
    _USER_FILE.write_text(f"email={email}\npassword={password}\n")


def _exists_in_api(client: ApiClient, email: str, password: str) -> bool:
    r = client.post(_VERIFY, data={"email": email, "password": password})
    return r.json().get("responseCode") == 200


@pytest.fixture(scope="session")
def test_user(api_client: ApiClient):
    """
    Usuario persistente para tests de UI.
    Lee credenciales de user_data.txt; si el usuario no existe en la API lo crea.
    Al finalizar la sesión elimina el usuario de la API (el TXT queda para el próximo run).
    """
    stored = _read_stored()

    if stored and _exists_in_api(api_client, stored["email"], stored["password"]):
        email, password = stored["email"], stored["password"]
        print(f"\n[test_user] Sesión activa — reutilizando usuario: {email}")
    else:
        overrides = {"email": stored["email"], "password": stored["password"]} if stored else {}
        user = make_register_user(**overrides)
        api_client.post(_CREATE, data=user.model_dump(mode="json", exclude_none=True))
        email, password = str(user.email), user.password
        _save(email, password)
        label = "Re-creado con credenciales del TXT" if stored else "Creado nuevo"
        print(f"\n[test_user] {label}: {email}")

    yield {"email": email, "password": password}

    api_client.delete(_DELETE, data={"email": email, "password": password})
    print(f"\n[test_user] Usuario eliminado de la API: {email} (TXT conservado)")
