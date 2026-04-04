import os
import pytest
from dotenv import load_dotenv
from services.api_client import ApiClient

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com/api")
UI_BASE_URL = os.getenv("UI_BASE_URL", "https://automationexercise.com")
EMAIL = os.getenv("EMAIL", "testuser@mail.com")
PASSWORD = os.getenv("PASSWORD", "Test@1234")

@pytest.fixture
def api_base_url() -> str:
    return BASE_URL

@pytest.fixture
def ui_base_url() -> str:
    return UI_BASE_URL

@pytest.fixture
def credentials() -> dict:
    return {"email": EMAIL, "password": PASSWORD}

@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    """API client fixture with session scope."""
    return ApiClient(BASE_URL)