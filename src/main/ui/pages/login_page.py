from playwright.sync_api import Page

from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class LoginPage(BasePage):
    def url(self) -> str:
        return "/login.html"

    @property
    def username_input(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="username"]').first,
            name="Username input"
        )

    @property
    def password_input(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="password"], input[type="password"]').first,
            name="Password input"
        )

    @property
    def login_button(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="submitLogin"], input[type="submit"], button:has-text("Log in")').first,
            name="Login button"
        )

    @property
    def error_message(self) -> UIElement:
        return UIElement(
            self.page.locator('#errorMessage, [role="alert"], .tcMessage').first,
            name="Error message"
        )

    def login(self, username: str, password: str):
        def _action():
            self.username_input.to_be_visible().fill(username)
            self.password_input.to_be_visible().fill(password)
            # Нажимаем Enter в поле пароля вместо клика по кнопке — универсальный способ
            try:
                self.password_input.locator.press("Enter")
            except Exception:
                # fallback: клик по кнопке, если Enter не работает
                self.login_button.click()
            self.page.wait_for_load_state("networkidle")
            return self

        return self._step(
            title=f"Login as {username}",
            action=_action
        )
