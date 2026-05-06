"""TC-PROD: Products API happy path tests — 25% triage."""

import pytest
from services.api_client import ApiClient

PRODUCTS_ENDPOINT = "productsList"
SEARCH_ENDPOINT = "searchProduct"


@pytest.mark.smoke
@pytest.mark.happy_path
def test_prod_01_list_all_products(api_client: ApiClient) -> None:
    """TC-PROD-01: GET /productsList — responseCode 200, non-empty array with required fields."""
    response = api_client.get(PRODUCTS_ENDPOINT)
    body = response.json()
    products = body.get("products", [])

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert isinstance(products, list)
    assert len(products) > 0
    assert all("id" in p and "name" in p and "price" in p for p in products)


@pytest.mark.happy_path
def test_prod_04_search_term_top(api_client: ApiClient) -> None:
    """TC-PROD-04: POST /searchProduct 'top' — responseCode 200, relevant results returned."""
    response = api_client.post(SEARCH_ENDPOINT, data={"search_product": "top"})
    body = response.json()
    products = body.get("products", [])

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert isinstance(products, list)
    assert len(products) > 0


@pytest.mark.happy_path
def test_prod_05_search_term_tshirt(api_client: ApiClient) -> None:
    """TC-PROD-05: POST /searchProduct 'tshirt' — responseCode 200, tshirt products returned."""
    response = api_client.post(SEARCH_ENDPOINT, data={"search_product": "tshirt"})
    body = response.json()
    products = body.get("products", [])

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert isinstance(products, list)
    assert len(products) > 0
