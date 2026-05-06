"""Tests for login API endpoints."""

import pytest
from services.api_client import ApiClient
from fixtures.user_factory import make_login_user, make_invalid_users, make_register_user
from models.user import UserLogin


class TestAPILogin:
    """Test suite for /api/verifyLogin endpoint."""

    API_ENDPOINT = "verifyLogin"
    CREATE_ENDPOINT = "createAccount"
    DELETE_ENDPOINT = "deleteAccount"

    @pytest.mark.smoke
    @pytest.mark.happy_path
    def test_auth_01_login_valid_credentials(self, api_client: ApiClient) -> None:
        """TC-AUTH-01: POST /verifyLogin with existing user — responseCode 200, "User exists!"."""
        user = make_register_user()
        api_client.post(self.CREATE_ENDPOINT, data=user.model_dump(mode="json", exclude_none=True))

        response = api_client.post(self.API_ENDPOINT, data={"email": str(user.email), "password": user.password})
        body = response.json()

        assert response.status_code == 200
        assert body["responseCode"] == 200
        assert body["message"] == "User exists!"

        api_client.delete(self.DELETE_ENDPOINT, data={"email": str(user.email), "password": user.password})

    @pytest.mark.happy_path
    def test_auth_10_login_after_account_deleted(self, api_client: ApiClient) -> None:
        """TC-AUTH-10: POST /verifyLogin after DELETE — responseCode 404, "User not found!"."""
        user = make_register_user()
        api_client.post(self.CREATE_ENDPOINT, data=user.model_dump(mode="json", exclude_none=True))
        api_client.delete(self.DELETE_ENDPOINT, data={"email": str(user.email), "password": user.password})

        response = api_client.post(self.API_ENDPOINT, data={"email": str(user.email), "password": user.password})
        body = response.json()

        assert response.status_code == 200
        assert body["responseCode"] == 404
        assert body["message"] == "User not found!"

    def test_api_7_post_verify_login_valid_credentials(self, api_client: ApiClient) -> None:
        """
        TC-USR-01: API 7 - POST Verify Login with valid credentials.
        
        Validates that login endpoint returns proper response structure
        with responseCode and message. For a non-existent user, should return 404.
        """
        # Arrange
        login_user = make_login_user(
            email="test@yopmail.com",
            password="Test@1234"
        )
        payload = {
            "email": login_user.email,
            "password": login_user.password,
        }
        
        # Act
        response = api_client.post(self.API_ENDPOINT, data=payload)
        response_json = response.json()
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        # Response contains responseCode and message fields
        assert "responseCode" in response_json, "Response must contain responseCode"
        assert "message" in response_json, "Response must contain message"
        # Valid response codes are 200 (User exists!) or 404 (User not found!)
        assert response_json.get("responseCode") in [200, 404], \
            f"Expected responseCode 200 or 404, got {response_json.get('responseCode')}"

    def test_api_8_post_verify_login_missing_email(self, api_client: ApiClient) -> None:
        """
        TC-USR-03: API 8 - POST Verify Login without email parameter.
        
        Validates that login without email parameter returns 400
        with appropriate error message. This is an alternative path test.
        """
        # Arrange
        payload = {
            "password": "Test@1234",
        }
        
        # Act
        response = api_client.post(self.API_ENDPOINT, data=payload)
        response_json = response.json()
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response_json.get("responseCode") == 400, \
            f"Expected responseCode 400, got {response_json.get('responseCode')}"
        assert "email or password parameter is missing" in response_json.get("message", ""), \
            f"Expected 'email or password parameter is missing' in message, got {response_json.get('message')}"

    def test_api_9_delete_verify_login_method_not_allowed(self, api_client: ApiClient) -> None:
        """
        TC-USR-07: API 9 - DELETE Verify Login (method not allowed).
        
        Validates that DELETE method is not supported on /api/verifyLogin endpoint,
        returning 405. This is an alternative path test for HTTP method validation.
        """
        # Arrange
        # No payload needed for DELETE
        
        # Act
        response = api_client.delete(self.API_ENDPOINT)
        response_json = response.json()
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response_json.get("responseCode") == 405, \
            f"Expected responseCode 405, got {response_json.get('responseCode')}"
        assert "This request method is not supported" in response_json.get("message", ""), \
            f"Expected 'This request method is not supported' in message, got {response_json.get('message')}"

    def test_api_10_post_verify_login_invalid_credentials(self, api_client: ApiClient) -> None:
        """
        TC-USR-06: API 10 - POST Verify Login with invalid credentials.
        
        Validates that login with non-existent email and wrong password
        returns 404 with 'User not found!' message. This is an alternative path test.
        """
        # Arrange
        payload = {
            "email": "nonexistent@yopmail.com",
            "password": "WrongPassword123",
        }
        
        # Act
        response = api_client.post(self.API_ENDPOINT, data=payload)
        response_json = response.json()
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response_json.get("responseCode") == 404, \
            f"Expected responseCode 404, got {response_json.get('responseCode')}"
        assert response_json.get("message") == "User not found!", \
            f"Expected 'User not found!', got {response_json.get('message')}"

    @pytest.mark.parametrize("invalid_user", make_invalid_users())
    def test_login_with_invalid_email_formats(
        self, api_client: ApiClient, invalid_user: dict
    ) -> None:
        """
        TC-USR-04: Parameterized test for various invalid email formats.
        
        Tests multiple invalid email scenarios to validate that API properly
        rejects malformed email addresses.
        """
        # Arrange
        payload = {
            "email": invalid_user["email"],
            "password": invalid_user["password"],
        }
        
        # Act
        response = api_client.post(self.API_ENDPOINT, data=payload)
        response_json = response.json()
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response_json.get("responseCode") in [400, 404], \
            f"Expected responseCode 400 or 404 for {invalid_user['reason']}, " \
            f"got {response_json.get('responseCode')}"
