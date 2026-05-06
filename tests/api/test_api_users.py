"""TC-USR: User CRUD happy path tests — 25% triage."""

import pytest
from services.api_client import ApiClient
from fixtures.user_factory import make_register_user

CREATE = "createAccount"
GET = "getUserDetailByEmail"
UPDATE = "updateAccount"
DELETE = "deleteAccount"


def _payload(user):
    return user.model_dump(mode="json", exclude_none=True)


def _cleanup(api_client: ApiClient, user) -> None:
    api_client.delete(DELETE, data={"email": str(user.email), "password": user.password})


class TestUserCRUD:
    """Happy path tests for User CRUD endpoints."""

    @pytest.mark.smoke
    @pytest.mark.happy_path
    def test_usr_01_register_valid_user(self, api_client: ApiClient) -> None:
        """TC-USR-01: POST /createAccount — responseCode 201, "User created!"."""
        user = make_register_user()

        response = api_client.post(CREATE, data=_payload(user))
        body = response.json()

        assert response.status_code == 200
        assert body["responseCode"] == 201
        assert body["message"] == "User created!"

        _cleanup(api_client, user)

    @pytest.mark.smoke
    @pytest.mark.happy_path
    def test_usr_05_get_existing_user(self, api_client: ApiClient) -> None:
        """TC-USR-05: GET /getUserDetailByEmail — responseCode 200, user data correct."""
        user = make_register_user()
        api_client.post(CREATE, data=_payload(user))

        response = api_client.get(GET, params={"email": str(user.email)})
        body = response.json()

        assert response.status_code == 200
        assert body["responseCode"] == 200
        assert body["user"]["email"] == str(user.email)

        _cleanup(api_client, user)

    @pytest.mark.smoke
    @pytest.mark.happy_path
    def test_usr_08_update_valid_user(self, api_client: ApiClient) -> None:
        """TC-USR-08: PUT /updateAccount — responseCode 200, "User updated!"."""
        user = make_register_user()
        api_client.post(CREATE, data=_payload(user))

        updated = make_register_user(email=str(user.email), name="Updated Test Name")
        response = api_client.put(UPDATE, data=_payload(updated))
        body = response.json()

        assert response.status_code == 200
        assert body["responseCode"] == 200
        assert body["message"] == "User updated!"

        _cleanup(api_client, user)

    @pytest.mark.smoke
    @pytest.mark.happy_path
    def test_usr_11_delete_valid_user(self, api_client: ApiClient) -> None:
        """TC-USR-11: DELETE /deleteAccount — responseCode 200, "Account deleted!"."""
        user = make_register_user()
        api_client.post(CREATE, data=_payload(user))

        response = api_client.delete(DELETE, data={"email": str(user.email), "password": user.password})
        body = response.json()

        assert response.status_code == 200
        assert body["responseCode"] == 200
        assert body["message"] == "Account deleted!"

    @pytest.mark.happy_path
    def test_usr_15_persistence_after_update(self, api_client: ApiClient) -> None:
        """TC-USR-15: GET after PUT — new data reflected correctly."""
        user = make_register_user()
        api_client.post(CREATE, data=_payload(user))

        new_name = "Persisted Name Check"
        updated = make_register_user(email=str(user.email), name=new_name)
        api_client.put(UPDATE, data=_payload(updated))

        response = api_client.get(GET, params={"email": str(user.email)})
        body = response.json()

        assert body["responseCode"] == 200
        assert body["user"]["name"] == new_name

        _cleanup(api_client, user)
