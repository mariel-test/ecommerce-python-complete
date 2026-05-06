"""TC-BRAND: Brands API happy path tests — 25% triage."""

import pytest
from services.api_client import ApiClient

BRANDS_ENDPOINT = "brandsList"


@pytest.mark.smoke
@pytest.mark.happy_path
def test_brand_01_list_all_brands(api_client: ApiClient) -> None:
    """TC-BRAND-01: GET /brandsList — responseCode 200, non-empty array with id and brand."""
    response = api_client.get(BRANDS_ENDPOINT)
    body = response.json()
    brands = body.get("brands", [])

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert isinstance(brands, list)
    assert len(brands) > 0
    assert all("id" in b and "brand" in b for b in brands)
