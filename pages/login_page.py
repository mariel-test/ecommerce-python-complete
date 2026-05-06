from .base_page import BasePage


class LoginPage(BasePage):
    LOGIN_EMAIL = "input[data-qa='login-email']"
    LOGIN_PASSWORD = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGIN_ERROR = "p:has-text('Your email or password is incorrect!')"

    def load(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/login", wait_until="load")

    def login(self, email: str, password: str) -> None:
        self.page.fill(self.LOGIN_EMAIL, email)
        self.page.fill(self.LOGIN_PASSWORD, password)
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_load_state("domcontentloaded")

    def get_error_message(self) -> str | None:
        locator = self.page.locator(self.LOGIN_ERROR)
        return locator.text_content() if locator.is_visible() else None
