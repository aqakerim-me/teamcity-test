from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class LoginPage(BasePage):
    def url(self) -> str:
        return "/login.html"

    @property
    def username_input(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="username"], input[id="username"], input[placeholder*="Username" i]').first,
            name="Username input"
        )

    @property
    def password_input(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="password"], input[id="password"], input[type="password"]').first,
            name="Password input"
        )

    @property
    def login_button(self) -> UIElement:
        return UIElement(
            self.page.locator('button:has-text("Log in"), button[type="submit"], input[type="submit"]').first,
            name="Login button"
        )

    @property
    def error_message(self) -> UIElement:
        return UIElement(
            self.page.locator('.errorMessage, .error, [class*="error"]').first,
            name="Error message"
        )

    def login(self, username: str, password: str):
        """Выполнить логин"""
        def _action():
            self.username_input.to_be_visible().fill(username)
            self.password_input.to_be_visible().fill(password)
            self.login_button.click()
            return self

        return self._step(
            title=f"Login as {username}",
            action=_action
        )
