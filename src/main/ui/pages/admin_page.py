from playwright.sync_api import Page

from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class AdminPage(BasePage):
    def url(self) -> str:
        return "/admin/users.html"

    @property
    def admin_panel_text(self) -> UIElement:
        return UIElement(
            self.page.locator('h1').first,
            name="Admin panel text"
        )

    @property
    def create_user_button(self) -> UIElement:
        return UIElement(
            self.page.locator(
                'a[href*="createUser"], '
                'button:has-text("Create user"), '
                'a:has-text("Create user")'
            ).first,
            name="Create user button"
        )

    @property
    def username_input(self) -> UIElement:
        return UIElement(
            self.page.locator(
                'input[name="username"], '
                'input#username, '
                'input[name="username1"], '
                'input#input_teamcityUsername, '
                'input[name="userName"], '
                'input#userName'
            ).first,
            name="Username input"
        )

    @property
    def password_input(self) -> UIElement:
        return UIElement(
            self.page.locator(
                'input[name="password"], '
                'input#password, '
                'input[name="password1"], '
                'input#password1, '
                'input[type="password"]'
            ).first,
            name="Password input"
        )

    @property
    def confirm_password_input(self) -> UIElement:
        return UIElement(
            self.page.locator(
                'input[name="retypedPassword"], '
                'input#retypedPassword'
            ).first,
            name="Confirm password input"
        )

    @property
    def submit_button(self) -> UIElement:
        return UIElement(
            self.page.locator(
                'button[type="submit"], '
                'input[type="submit"], '
                'input[name="submitCreateUser"], '
                'button:has-text("Create"), '
                'button:has-text("Save"), '
                'input[value="Create User"]'
            ).first,
            name="Submit button"
        )

    @property
    def users_list(self) -> UIElement:
        return UIElement(
            self.page.locator('table').first,
            name="Users list"
        )

    def create_user(self, username: str, password: str):
        def _action():
            try:
                btn = self.create_user_button.locator
                btn.wait_for(state="visible", timeout=10_000)
                btn.scroll_into_view_if_needed()
                btn.click()
            except Exception:
                self.page.goto(
                    f"{self.ui_base_url}/admin/createUser.html",
                    wait_until="domcontentloaded",
                )

            username_input = self.username_input.locator
            username_input.wait_for(state="visible", timeout=10_000)
            username_input.scroll_into_view_if_needed()
            username_input.fill(username)

            password_input = self.password_input.locator
            password_input.wait_for(state="visible", timeout=10_000)
            password_input.scroll_into_view_if_needed()
            password_input.fill(password)

            confirm_password_input = self.confirm_password_input.locator
            confirm_password_input.wait_for(state="visible", timeout=10_000)
            confirm_password_input.scroll_into_view_if_needed()
            confirm_password_input.fill(password)

            submit_btn = self.submit_button.locator
            submit_btn.wait_for(state="visible", timeout=10_000)
            submit_btn.scroll_into_view_if_needed()
            submit_btn.click()

            self.page.wait_for_load_state("networkidle", timeout=10_000)
            return self

        return self._step(
            title=f"Create user: {username}",
            action=_action
        )
