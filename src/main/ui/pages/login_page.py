from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.selectors import (
    LOGIN_BUTTON,
    LOGIN_ERROR_MESSAGE,
    LOGIN_PASSWORD_INPUT,
    LOGIN_USERNAME_INPUT,
)
from src.main.ui.pages.ui_element import UIElement


class LoginPage(BasePage):
    def url(self) -> str:
        return "/login.html"

    @property
    def username_input(self) -> UIElement:
        return UIElement(
            self.page.locator(LOGIN_USERNAME_INPUT).first,
            name="Username input"
        )

    @property
    def password_input(self) -> UIElement:
        return UIElement(
            self.page.locator(LOGIN_PASSWORD_INPUT).first,
            name="Password input"
        )

    @property
    def login_button(self) -> UIElement:
        return UIElement(
            self.page.locator(LOGIN_BUTTON).first,
            name="Login button"
        )

    @property
    def error_message(self) -> UIElement:
        return UIElement(
            self.page.locator(LOGIN_ERROR_MESSAGE).first,
            name="Error message"
        )

    def login(self, username: str, password: str):
        def _action():
            self.username_input.to_be_visible().fill(username)
            self.password_input.to_be_visible().fill(password)
            # Prefer Enter in password field, fallback to button click
            try:
                self.password_input.locator.press("Enter")
            except Exception:
                self.login_button.click()
            self.page.wait_for_load_state("domcontentloaded")
            if "login" in self.page.url.lower():
                error_locator = self.page.locator(LOGIN_ERROR_MESSAGE).first
                error_locator.wait_for(state="visible", timeout=3_000)
            return self

        return self._step(
            title=f"Login as {username}",
            action=_action
        )
