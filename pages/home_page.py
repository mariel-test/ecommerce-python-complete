from .base_page import BasePage


class HomePage(BasePage):
    def get_title(self) -> str:
        return self.page.title()

    def search(self, term: str) -> None:
        self.page.fill("input[name='search']", term)
        self.page.press("input[name='search']", "Enter")
