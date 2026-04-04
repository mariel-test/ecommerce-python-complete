from pages.home_page import HomePage


def test_home_page_title(page, ui_base_url):
    home = HomePage(page)
    home.load(ui_base_url)
    assert "Automation Exercise" in home.get_title()
