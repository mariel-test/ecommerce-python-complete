from .base_page import BasePage


class HomePage(BasePage):
    SEARCH_INPUT = "#search_product"
    SEARCH_BUTTON = "#submit_search"
    PRODUCT_CARDS = ".features_items .product-image-wrapper"

    def get_title(self) -> str:
        return self.page.title()

    def search(self, term: str) -> None:
        self.page.fill(self.SEARCH_INPUT, term)
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("domcontentloaded")

    def get_product_count(self) -> int:
        return self.page.locator(self.PRODUCT_CARDS).count()

    def get_search_results_count(self) -> int:
        self.page.locator(self.PRODUCT_CARDS).first.wait_for()
        return self.page.locator(self.PRODUCT_CARDS).count()
