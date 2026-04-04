from services.api_client import ApiClient


def test_get_products_list(api_base_url):
    client = ApiClient(api_base_url)
    response = client.get("/productsList")

    payload = response.json()
    products = payload.get("products", [])

    print(f"Request URL: {response.url}")
    print(f"HTTP status: {response.status_code}")
    print(f"API responseCode: {payload.get('responseCode')}")
    print(f"Products returned: {len(products)}")

    assert response.status_code == 200
    assert payload["responseCode"] == 200
    assert isinstance(products, list)
    assert products
