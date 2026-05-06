"""TC-UI: UI + Integration happy path tests — 25% triage."""

import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage

BRAND_LINK = "a[href*='/brand_products/']"
LOGOUT_LINK = "a[href='/logout']"


@pytest.mark.smoke
@pytest.mark.happy_path
def test_ui_smoke_authenticated_flow(page: Page, ui_base_url: str, test_user: dict) -> None:
    """
    Smoke autenticado: login → buscar 'top' → buscar 'tshirt' → listar marcas → logout.
    El usuario se reutiliza entre runs desde user_data.txt.
    """
    # 1. Login
    login = LoginPage(page)
    login.load(ui_base_url)
    login.login(test_user["email"], test_user["password"])
    assert page.locator(LOGOUT_LINK).is_visible(), (
        f"Login fallido para {test_user['email']} — no aparece el link de Logout"
    )

    # 2. Buscar "top"
    home = HomePage(page)
    home.load(f"{ui_base_url}/products")
    home.search("top")
    top_count = home.get_search_results_count()
    assert top_count > 0, "La búsqueda 'top' no devolvió resultados"

    # 3. Buscar "tshirt"
    home.load(f"{ui_base_url}/products")
    home.search("tshirt")
    tshirt_count = home.get_search_results_count()
    assert tshirt_count > 0, "La búsqueda 'tshirt' no devolvió resultados"

    # 4. Listar marcas
    home.load(f"{ui_base_url}/products")
    page.locator(BRAND_LINK).first.wait_for()
    brand_count = page.locator(BRAND_LINK).count()
    assert brand_count > 0, "No se cargaron marcas en el sidebar"

    # 5. Logout
    page.locator(LOGOUT_LINK).click()
    page.wait_for_load_state("load")
    assert "login" in page.url, "El logout no redirigió a /login"


@pytest.mark.smoke
@pytest.mark.happy_path
def test_ui_04_catalog_loads_products(page: Page, ui_base_url: str) -> None:
    """TC-UI-04: Home page loads product cards from the API — count > 0, cards visible."""
    home = HomePage(page)
    home.load(ui_base_url)

    count = home.get_product_count()

    assert count > 0, f"Se esperaban productos en el catálogo, se encontraron {count}"


@pytest.mark.happy_path
def test_ui_05_search_returns_results(page: Page, ui_base_url: str) -> None:
    """TC-UI-05: Searching 'top' on the products page returns visible results."""
    home = HomePage(page)
    home.load(f"{ui_base_url}/products")
    home.search("top")

    count = home.get_search_results_count()

    assert count > 0, "La búsqueda de 'top' no devolvió resultados"


@pytest.mark.happy_path
def test_ui_03_login_failed_shows_error(page: Page, ui_base_url: str) -> None:
    """TC-UI-03: Login with wrong credentials shows error message without redirect."""
    login = LoginPage(page)
    login.load(ui_base_url)
    login.login("wrong@email.com", "WrongPassword123")

    error = login.get_error_message()

    assert error is not None, "No se mostró mensaje de error tras login inválido"
    assert "incorrect" in error.lower(), f"Mensaje inesperado: '{error}'"
