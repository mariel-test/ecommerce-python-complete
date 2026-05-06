"""E2E-01 y E2E-04: Flujos de ciclo de vida completo — 25% triage."""

import pytest
from services.api_client import ApiClient
from fixtures.user_factory import make_register_user

CREATE = "createAccount"
VERIFY = "verifyLogin"
GET = "getUserDetailByEmail"
UPDATE = "updateAccount"
DELETE = "deleteAccount"


def _payload(user):
    return user.model_dump(mode="json", exclude_none=True)


class TestE2EFlows:

    @pytest.mark.smoke
    @pytest.mark.happy_path
    def test_e2e_01_full_user_lifecycle(self, api_client: ApiClient) -> None:
        """E2E-01: create → login → get → update → get (verify) → delete → login (404)."""
        user = make_register_user()

        # 1. Registro
        r = api_client.post(CREATE, data=_payload(user))
        assert r.json()["responseCode"] == 201, f"createAccount falló: {r.json()}"

        # 2. Login
        r = api_client.post(VERIFY, data={"email": str(user.email), "password": user.password})
        assert r.json()["responseCode"] == 200, f"verifyLogin falló: {r.json()}"
        assert r.json()["message"] == "User exists!"

        # 3. Obtener detalle
        r = api_client.get(GET, params={"email": str(user.email)})
        assert r.json()["responseCode"] == 200, f"getUserDetail falló: {r.json()}"
        assert r.json()["user"]["email"] == str(user.email)

        # 4. Actualizar
        updated = make_register_user(email=str(user.email), name="E2E Updated Name")
        r = api_client.put(UPDATE, data=_payload(updated))
        assert r.json()["responseCode"] == 200, f"updateAccount falló: {r.json()}"

        # 5. Verificar persistencia
        r = api_client.get(GET, params={"email": str(user.email)})
        assert r.json()["user"]["name"] == "E2E Updated Name", "El nombre actualizado no persiste"

        # 6. Eliminar
        r = api_client.delete(DELETE, data={"email": str(user.email), "password": user.password})
        assert r.json()["responseCode"] == 200, f"deleteAccount falló: {r.json()}"

        # 7. Login post-eliminación debe ser 404
        r = api_client.post(VERIFY, data={"email": str(user.email), "password": user.password})
        assert r.json()["responseCode"] == 404, "Usuario eliminado sigue siendo accesible"

    @pytest.mark.happy_path
    def test_e2e_04_access_after_deletion(self, api_client: ApiClient) -> None:
        """E2E-04: create → delete → verifyLogin, getUserDetail y updateAccount devuelven 404."""
        user = make_register_user()
        api_client.post(CREATE, data=_payload(user))
        api_client.delete(DELETE, data={"email": str(user.email), "password": user.password})

        r = api_client.post(VERIFY, data={"email": str(user.email), "password": user.password})
        assert r.json()["responseCode"] == 404, "verifyLogin: usuario eliminado no debe existir"

        r = api_client.get(GET, params={"email": str(user.email)})
        assert r.json()["responseCode"] == 404, "getUserDetail: usuario eliminado no debe existir"

        updated = make_register_user(email=str(user.email))
        r = api_client.put(UPDATE, data=_payload(updated))
        assert r.json()["responseCode"] == 404, "updateAccount: usuario eliminado no debe existir"
