from playwright.sync_api import Page

from src.main.api.generator.generate_data import GenerateData
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class AdminPage(BasePage):
    def url(self) -> str:
        return "/admin/users.html"

    @property
    def admin_panel_text(self) -> UIElement:
        return UIElement(
            self.page.locator('h1:has-text("Users"), .pageTitle, [class*="admin"]').first,
            name="Admin panel text"
        )

    @property
    def create_user_button(self) -> UIElement:
        return UIElement(
            self.page.locator('button:has-text("Create user"), a:has-text("Create user"), [title*="Create user" i]').first,
            name="Create user button"
        )

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
    def submit_button(self) -> UIElement:
        return UIElement(
            self.page.locator('button:has-text("Create"), button:has-text("Save"), button[type="submit"]').first,
            name="Submit button"
        )

    @property
    def users_list(self) -> UIElement:
        return UIElement(
            self.page.locator('.usersList, [class*="user"], table').first,
            name="Users list"
        )

    def create_user(self, username: str, password: str):
        """Создать нового пользователя"""
        def _action():
            self.create_user_button.to_be_visible().click()
            self.username_input.to_be_visible().fill(username)
            self.password_input.to_be_visible().fill(password)
            self.submit_button.click()
            return self

        return self._step(
            title=f"Create user: {username}",
            action=_action
        )
